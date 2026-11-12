using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using AceriaApp.Gateway;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Hosting.Server;
using Microsoft.AspNetCore.Hosting.Server.Features;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace AceriaApp.Pruebas.Gateway;

// Servidores HTTP reales de contrato. No sustituyen las pruebas SQL/RabbitMQ de integración.
public sealed class GatewayPruebas : IAsyncDisposable
{
    public BackendPruebas Produccion { get; private set; } = null!;
    public BackendPruebas Inventario1 { get; private set; } = null!;
    public BackendPruebas? Inventario2 { get; private set; }
    public WebApplication Proxy { get; private set; } = null!;
    public HttpClient Cliente { get; private set; } = null!;

    public static async Task<GatewayPruebas> CrearAsync(bool segundaInstancia = false, Action<WebApplicationBuilder>? configurar = null)
    {
        var prueba = new GatewayPruebas();
        try
        {
            prueba.Produccion = await BackendPruebas.CrearAsync("produccion");
            prueba.Inventario1 = await BackendPruebas.CrearAsync("inventario-1");
            if (segundaInstancia) prueba.Inventario2 = await BackendPruebas.CrearAsync("inventario-2");
            prueba.Proxy = GatewayProgram.CreateApp([], builder =>
            {
                builder.Configuration.Sources.Clear();
                builder.Configuration.AddJsonFile(Path.Combine(AppContext.BaseDirectory, "gateway.appsettings.json"), false, false);
                builder.Configuration.AddInMemoryCollection(new Dictionary<string, string?>
                {
                    ["Urls"] = "http://127.0.0.1:0",
                    ["Observabilidad:NivelMinimo"] = "Fatal",
                    ["ReverseProxy:Clusters:produccion-cluster:Destinations:produccion:Address"] = prueba.Produccion.Direccion,
                    ["ReverseProxy:Clusters:inventario-cluster:Destinations:inventario-1:Address"] = prueba.Inventario1.Direccion
                });
                if (prueba.Inventario2 is not null || builder.Configuration["ReverseProxy:Clusters:inventario-cluster:Destinations:inventario-2:Address"] is not null)
                    builder.Configuration.AddInMemoryCollection(new Dictionary<string, string?>
                    {
                        ["ReverseProxy:Clusters:inventario-cluster:Destinations:inventario-2:Address"] = prueba.Inventario2?.Direccion ?? prueba.Inventario1.Direccion
                    });
                builder.Logging.ClearProviders();
                configurar?.Invoke(builder);
            });
            await prueba.Proxy.StartAsync();
            prueba.Cliente = new HttpClient(new HttpClientHandler { AllowAutoRedirect = false })
            {
                BaseAddress = new Uri(DireccionDe(prueba.Proxy)), Timeout = TimeSpan.FromSeconds(10)
            };
            return prueba;
        }
        catch { await prueba.DisposeAsync(); throw; }
    }

    public async Task ReiniciarInventario2Async()
    {
        var direccion = Inventario2!.Direccion;
        await Inventario2.DisposeAsync();
        Inventario2 = await BackendPruebas.CrearAsync("inventario-2", direccion);
    }

    public static string DireccionDe(WebApplication app) => app.Services.GetRequiredService<IServer>()
        .Features.Get<IServerAddressesFeature>()!.Addresses.Single();

    public static async Task EsperarAsync(Func<Task<bool>> condicion, string motivo)
    {
        using var plazo = new CancellationTokenSource(TimeSpan.FromSeconds(20));
        while (!plazo.IsCancellationRequested)
        {
            if (await condicion()) return;
            try { await Task.Delay(100, plazo.Token); }
            catch (OperationCanceledException) { break; }
        }
        throw new TimeoutException(motivo);
    }

    public async ValueTask DisposeAsync()
    {
        Cliente?.Dispose();
        if (Proxy is not null) { await Proxy.StopAsync(); await Proxy.DisposeAsync(); }
        if (Produccion is not null) await Produccion.DisposeAsync();
        if (Inventario1 is not null) await Inventario1.DisposeAsync();
        if (Inventario2 is not null) await Inventario2.DisposeAsync();
    }
}

public sealed record EcoPeticion(string Instancia, string Metodo, string Ruta, string Query,
    string Cuerpo, string Correlacion, string Canal, string RutaSeleccionada);

public sealed class BackendPruebas : IAsyncDisposable
{
    private readonly WebApplication app;
    private int peticiones;
    private int escrituras;
    private int sondeos;
    private bool detenido;
    public string Direccion { get; }
    public int Peticiones => Volatile.Read(ref peticiones);
    public int Escrituras => Volatile.Read(ref escrituras);
    public int Sondeos => Volatile.Read(ref sondeos);
    public bool Listo { get; set; } = true;

    private BackendPruebas(WebApplication app)
    {
        this.app = app;
        Direccion = GatewayPruebas.DireccionDe(app);
    }

    public static async Task<BackendPruebas> CrearAsync(string instancia, string? direccion = null)
    {
        var builder = WebApplication.CreateBuilder();
        builder.WebHost.UseUrls(direccion ?? "http://127.0.0.1:0");
        builder.Logging.ClearProviders();
        var app = builder.Build();
        BackendPruebas? backend = null;
        app.MapGet("/health/ready", () =>
        {
            Interlocked.Increment(ref backend!.sondeos);
            return Results.StatusCode(backend.Listo ? 200 : 503);
        });
        app.Map("/{**ruta}", async (HttpContext contexto) =>
        {
            Interlocked.Increment(ref backend!.peticiones);
            if (contexto.Request.Method is not ("GET" or "HEAD")) Interlocked.Increment(ref backend.escrituras);
            contexto.Response.Headers["X-Instancia"] = instancia;
            if (contexto.Request.Query.ContainsKey("abortar")) { contexto.Abort(); return; }
            var estado = int.TryParse(contexto.Request.Query["estado"], out var numero) ? numero : 200;
            contexto.Response.StatusCode = estado;
            if (estado is 400 or 404 or 409 or 422)
            {
                contexto.Response.ContentType = "application/problem+json";
                await contexto.Response.WriteAsync($"{{\"type\":\"https://aceria.test/problemas/regla\",\"title\":\"Regla del servicio\",\"status\":{estado},\"detail\":\"Respuesta original\",\"codigo\":\"ACERIA-001\"}}");
                return;
            }
            if (estado == 201) contexto.Response.Headers.Location =
                $"{contexto.Request.Scheme}://{contexto.Request.Host}/api/v1/ordenes/creada?version=1";
            using var lector = new StreamReader(contexto.Request.Body);
            var cuerpo = await lector.ReadToEndAsync();
            await contexto.Response.WriteAsJsonAsync(new EcoPeticion(instancia, contexto.Request.Method,
                contexto.Request.Path, contexto.Request.QueryString.Value ?? "", cuerpo,
                contexto.Request.Headers["X-Correlation-ID"].ToString(),
                contexto.Request.Headers["X-Canal"].ToString(),
                contexto.Request.Headers["X-Ruta"].ToString()));
        });
        await app.StartAsync();
        backend = new BackendPruebas(app);
        return backend;
    }

    public async Task DetenerAsync()
    {
        if (detenido) return;
        detenido = true;
        await app.StopAsync();
    }

    public async ValueTask DisposeAsync() { await DetenerAsync(); await app.DisposeAsync(); }
}
