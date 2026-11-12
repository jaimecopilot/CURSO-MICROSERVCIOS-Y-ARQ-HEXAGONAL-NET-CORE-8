using System.Diagnostics;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
namespace AceriaApp.Observabilidad;
public static class RegistroErrores
{
    public static IServiceCollection AddErroresAceria(this IServiceCollection services)
    {
        services.AddProblemDetails(options => options.CustomizeProblemDetails = c => Correlacionar(c.HttpContext, c.ProblemDetails));
        services.AddExceptionHandler<ManejadorExcepciones>();
        return services;
    }
    internal static void Correlacionar(HttpContext context, ProblemDetails problem)
    {
        problem.Extensions["traceId"] = Activity.Current?.Id ?? context.TraceIdentifier;
        problem.Extensions["correlationId"] = ContextoCorrelacion.Obtener(context);
    }
    public static IApplicationBuilder UseErroresAceria(this IApplicationBuilder app) => app.UseExceptionHandler();
    public static WebApplication MapDiagnosticoAceria(this WebApplication app)
    {
        if (app.Environment.IsDevelopment() && app.Configuration.GetValue<bool>("Observabilidad:DiagnosticoActivo"))
            app.MapGet("/api/diagnostico/fallo", IResult () => throw new InvalidOperationException("Detalle interno del fallo controlado."));
        return app;
    }
}
