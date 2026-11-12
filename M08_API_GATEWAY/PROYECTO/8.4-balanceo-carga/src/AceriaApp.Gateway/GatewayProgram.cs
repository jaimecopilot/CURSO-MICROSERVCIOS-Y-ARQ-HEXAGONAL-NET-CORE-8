using AceriaApp.Observabilidad;
using Yarp.ReverseProxy.Transforms;

namespace AceriaApp.Gateway;

public sealed class GatewayProgram
{
    public static Task Main(string[] args) => CreateApp(args).RunAsync();

    public static WebApplication CreateApp(string[] args, Action<WebApplicationBuilder>? configurar = null)
    {
        var builder = WebApplication.CreateBuilder(args);
        configurar?.Invoke(builder);
        builder.Services.AddLoggingAceria("Gateway", builder.Configuration);
        builder.Services.AddErroresAceria();
        builder.Services.AddReverseProxy()
            .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"))
            .AddTransforms(ruta =>
            {
                ruta.AddRequestTransform(contexto =>
                {
                    // La cabecera entrante puede ser inválida: se usa el valor ya validado en el borde.
                    contexto.ProxyRequest.Headers.Remove(ContextoCorrelacion.Cabecera);
                    contexto.ProxyRequest.Headers.TryAddWithoutValidation(ContextoCorrelacion.Cabecera,
                        ContextoCorrelacion.Obtener(contexto.HttpContext));
                    return ValueTask.CompletedTask;
                });
                ruta.AddResponseTransform(contexto =>
                {
                    var location = contexto.ProxyResponse?.Headers.Location;
                    var destino = contexto.ProxyResponse?.RequestMessage?.RequestUri;
                    if (location is { IsAbsoluteUri: true } && destino is not null &&
                        string.Equals(location.Scheme, destino.Scheme, StringComparison.OrdinalIgnoreCase) &&
                        string.Equals(location.Authority, destino.Authority, StringComparison.OrdinalIgnoreCase))
                    {
                        // Los recursos publicados conservan su path: Location sigue siendo público.
                        contexto.HttpContext.Response.Headers.Location = location.PathAndQuery + location.Fragment;
                    }
                    return ValueTask.CompletedTask;
                });
            });
        var app = builder.Build();
        app.UseLoggingAceria();
        app.UseErroresAceria();
        // Liveness acredita este proceso, no la disponibilidad de SQL, RabbitMQ o los destinos.
        app.MapGet("/health/live", () => Results.Ok(new { servicio = "Gateway", estado = "vivo" }));
        // La sobrecarga predeterminada incluye selección de destinos y middleware de balanceo.
        app.MapReverseProxy();
        return app;
    }
}
