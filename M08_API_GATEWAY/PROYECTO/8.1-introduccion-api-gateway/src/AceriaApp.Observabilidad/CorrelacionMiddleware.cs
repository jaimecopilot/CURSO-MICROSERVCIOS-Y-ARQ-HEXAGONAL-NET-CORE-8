using System.Diagnostics;
using Microsoft.AspNetCore.Http;
using Serilog.Context;
namespace AceriaApp.Observabilidad;
public static class ContextoCorrelacion
{
    public const string Cabecera = "X-Correlation-ID";
    private static readonly object Clave = new();
    public static string Obtener(HttpContext context) =>
        context.Items.TryGetValue(Clave, out var value) ? (string)value! : "";
    internal static void Guardar(HttpContext context, string id) => context.Items[Clave] = id;
    internal static bool Valido(string value) => value.Length is > 0 and <= 64 &&
        value.All(c => char.IsAsciiLetterOrDigit(c) || c is '-' or '_');
}
public sealed class CorrelacionMiddleware(RequestDelegate next)
{
    public async Task InvokeAsync(HttpContext context)
    {
        var entrada = context.Request.Headers[ContextoCorrelacion.Cabecera].ToString();
        var id = ContextoCorrelacion.Valido(entrada) ? entrada : Guid.NewGuid().ToString("N");
        ContextoCorrelacion.Guardar(context, id);
        context.Response.Headers[ContextoCorrelacion.Cabecera] = id;
        context.Response.OnStarting(() =>
        {
            context.Response.Headers[ContextoCorrelacion.Cabecera] = id;
            return Task.CompletedTask;
        });
        using (LogContext.PushProperty("CorrelationId", id))
        using (LogContext.PushProperty("TraceId", Activity.Current?.TraceId.ToString() ?? context.TraceIdentifier))
            await next(context);
    }
}
