using System.Diagnostics;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;
using Microsoft.Extensions.Logging;
namespace AceriaApp.Observabilidad;
public sealed class ResumenPeticionMiddleware(RequestDelegate next, ILogger<ResumenPeticionMiddleware> logger)
{
    public async Task InvokeAsync(HttpContext context)
    {
        var inicio = Stopwatch.GetTimestamp();
        var ruta = (context.GetEndpoint() as RouteEndpoint)?.RoutePattern.RawText ?? "[sin-ruta]";
        var fallo = false;
        try { await next(context); }
        catch { fallo = true; throw; }
        finally
        {
            if (!context.Request.Path.StartsWithSegments("/health"))
            {
                var estado = context.RequestAborted.IsCancellationRequested ? 499 : fallo ? 500 : context.Response.StatusCode;
                var nivel = estado >= 500 ? LogLevel.Error : estado >= 400 && estado != 499 ? LogLevel.Warning : LogLevel.Information;
                logger.Log(nivel, "Peticion {Metodo} {Ruta} respondio {Estado} en {Milisegundos} ms",
                    context.Request.Method, ruta, estado, Stopwatch.GetElapsedTime(inicio).TotalMilliseconds);
            }
        }
    }
}
