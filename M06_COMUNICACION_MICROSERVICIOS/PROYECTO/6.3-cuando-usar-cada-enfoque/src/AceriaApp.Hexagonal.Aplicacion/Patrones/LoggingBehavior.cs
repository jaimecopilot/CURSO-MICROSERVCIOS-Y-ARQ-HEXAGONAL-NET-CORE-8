using MediatR;
using Microsoft.Extensions.Logging;
namespace AceriaApp.Hexagonal.Aplicacion.Patrones;

/// <summary>Observa el flujo sin registrar payloads ni alterar tipos de respuesta.</summary>
public sealed class LoggingBehavior<TRequest, TResponse>(ILogger<LoggingBehavior<TRequest, TResponse>> logger)
    : IPipelineBehavior<TRequest, TResponse> where TRequest : notnull
{
    public async Task<TResponse> Handle(TRequest request, RequestHandlerDelegate<TResponse> next, CancellationToken ct)
    {
        ct.ThrowIfCancellationRequested();
        logger.LogInformation("Inicio {Solicitud}", typeof(TRequest).Name);
        var response = await next();
        logger.LogInformation("Fin {Solicitud}", typeof(TRequest).Name);
        return response;
    }
}
