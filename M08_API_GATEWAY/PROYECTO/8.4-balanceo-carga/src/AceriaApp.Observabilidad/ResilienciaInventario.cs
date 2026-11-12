using System.Net;
using AceriaApp.Comunicacion.Aplicacion;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Microsoft.Extensions.Http.Resilience;
using Microsoft.Extensions.Logging;
using Polly;
using Polly.Timeout;
namespace AceriaApp.Observabilidad;

public static class ResilienciaInventario
{
    public static IServiceCollection AddResilienciaInventario(this IServiceCollection services, IConfiguration config)
    {
        // Sustituye el puerto registrado en M6; su dominio y sus contratos no cambian.
        services.RemoveAll<IClienteInventario>();
        services.AddHttpClient<IClienteInventario, ClienteInventarioResiliente>("inventario-resiliente", http =>
        {
            http.BaseAddress = new Uri(config["Comunicacion:InventarioUrl"] ?? "http://localhost:5106/");
            http.Timeout = Timeout.InfiniteTimeSpan; // Polly gobierna un único presupuesto.
        }).AddPoliticaResilienciaInventario();
        return services;
    }

    public static IHttpClientBuilder AddPoliticaResilienciaInventario(this IHttpClientBuilder cliente)
    {
        cliente.Services.TryAddSingleton(TimeProvider.System);
        cliente.AddResilienceHandler("lectura-inventario", (pipeline, contexto) =>
        {
            var reloj = contexto.ServiceProvider.GetRequiredService<TimeProvider>();
            var log = contexto.ServiceProvider.GetRequiredService<ILoggerFactory>().CreateLogger("AceriaApp.Resiliencia");
            pipeline.TimeProvider = reloj;
            pipeline
                .AddTimeout(TimeSpan.FromSeconds(6))
                .AddRetry(new HttpRetryStrategyOptions
                {
                    MaxRetryAttempts = 2,
                    Delay = TimeSpan.FromMilliseconds(200),
                    BackoffType = DelayBackoffType.Exponential,
                    UseJitter = true,
                    ShouldHandle = args => ValueTask.FromResult(
                        EsLectura(args.Context.GetRequestMessage()?.Method) &&
                        EsTransitorio(args.Outcome, args.Context.CancellationToken)),
                    OnRetry = args =>
                    {
                        log.LogWarning(new EventId(7401, "ReintentoInventario"),
                            "Reintento de inventario {Intento} tras {DemoraMs} ms; estado HTTP {EstadoHttp}",
                            args.AttemptNumber + 1, args.RetryDelay.TotalMilliseconds, (int?)args.Outcome.Result?.StatusCode);
                        return default;
                    },
                    // Se usa el mismo reloj para Retry-After en fecha y para las estrategias.
                    // El timeout exterior cancela incluso una espera Retry-After de varios minutos.
                    DelayGenerator = args =>
                    {
                        var cabecera = args.Outcome.Result?.Headers.RetryAfter;
                        TimeSpan? espera = cabecera?.Delta;
                        if (espera is null && cabecera?.Date is { } fecha)
                            espera = fecha - reloj.GetUtcNow();
                        return ValueTask.FromResult(espera is { } valor && valor >= TimeSpan.Zero ? espera : null);
                    }
                })
                .AddCircuitBreaker(new HttpCircuitBreakerStrategyOptions
                {
                    MinimumThroughput = 4,
                    FailureRatio = 0.5,
                    SamplingDuration = TimeSpan.FromSeconds(10),
                    BreakDuration = TimeSpan.FromSeconds(5),
                    ShouldHandle = args => ValueTask.FromResult(
                        EsTransitorio(args.Outcome, args.Context.CancellationToken)),
                    OnOpened = _ =>
                    {
                        log.LogWarning(new EventId(7402, "CircuitoInventarioAbierto"), "Circuito de inventario {Estado}", "abierto");
                        return default;
                    },
                    OnClosed = _ =>
                    {
                        log.LogInformation(new EventId(7403, "CircuitoInventarioCerrado"), "Circuito de inventario {Estado}", "cerrado");
                        return default;
                    }
                })
                .AddTimeout(TimeSpan.FromSeconds(1));
        }).SelectPipelineByAuthority();
        cliente.AddHttpMessageHandler(() => new LeerRespuestaCompletaHandler());
        // IHttpClientFactory conserva la política por nombre y autoridad entre clientes/peticiones.
        return cliente;
    }

    private sealed class LeerRespuestaCompletaHandler : DelegatingHandler
    {
        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken ct)
        {
            var respuesta = await base.SendAsync(request, ct);
            try
            {
                // HttpClient normalmente almacena el cuerpo después de abandonar sus handlers.
                // Aquí la lectura queda dentro del timeout de intento y del presupuesto total.
                await respuesta.Content.ReadAsByteArrayAsync(ct);
                return respuesta;
            }
            catch { respuesta.Dispose(); throw; }
        }
    }

    private static bool EsLectura(HttpMethod? metodo) =>
        metodo == HttpMethod.Get || metodo == HttpMethod.Head || metodo == HttpMethod.Options;

    private static bool EsTransitorio(Outcome<HttpResponseMessage> resultado, CancellationToken ct)
    {
        if (ct.IsCancellationRequested) return false;
        if (resultado.Exception is HttpRequestException or TimeoutRejectedException) return true;
        return resultado.Result?.StatusCode is HttpStatusCode.RequestTimeout or HttpStatusCode.TooManyRequests ||
            resultado.Result is { } respuesta && (int)respuesta.StatusCode is >= 500 and <= 599;
    }
}
