using System.Text.Json;
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
namespace AceriaApp.Observabilidad;
public sealed class ManejadorExcepciones(IProblemDetailsService detalles, ILogger<ManejadorExcepciones> logger) : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(HttpContext context, Exception exception, CancellationToken ct)
    {
        if (context.Response.HasStarted) return false;
        if (exception is OperationCanceledException && context.RequestAborted.IsCancellationRequested)
        {
            context.Response.StatusCode = 499;
            return true;
        }
        logger.LogError(new EventId(7301, "ExcepcionInesperada"), "Fallo inesperado de tipo {TipoExcepcion}", exception.GetType().Name);
        var problem = new ProblemDetails { Status = 500, Title = "Se ha producido un error interno.", Type = "about:blank" };
        RegistroErrores.Correlacionar(context, problem);
        context.Response.StatusCode = 500;
        if (!await detalles.TryWriteAsync(new ProblemDetailsContext { HttpContext = context, ProblemDetails = problem }))
            await context.Response.WriteAsJsonAsync(problem, (JsonSerializerOptions?)null, "application/problem+json", ct);
        return true;
    }
}
