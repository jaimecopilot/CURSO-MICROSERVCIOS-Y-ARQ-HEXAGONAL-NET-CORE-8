using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Diagnostics.HealthChecks;
namespace AceriaApp.Observabilidad;
public static class RegistroSalud
{
    public static IServiceCollection AddSaludAceria(this IServiceCollection services, IConfiguration config, bool inventario)
    {
        var health = services.AddHealthChecks();
        var bases = inventario ? new[] { "AceriaInventario" } : new[] { "AceriaApp", "AceriaHexagonal", "AceriaProduccion" };
        foreach (var nombre in bases)
            health.AddCheck("sql-" + nombre, new SqlServicioHealthCheck(config.GetConnectionString(nombre) ?? ""),
                tags: new[] { "ready" }, timeout: TimeSpan.FromSeconds(3));
        if (config.GetValue<bool>("Comunicacion:WorkersActivos"))
            health.AddCheck("rabbitmq", new RabbitServicioHealthCheck(config["Comunicacion:RabbitMqUri"] ?? ""),
                tags: new[] { "ready" }, timeout: TimeSpan.FromSeconds(3));
        return services;
    }
    public static IEndpointRouteBuilder MapSaludAceria(this IEndpointRouteBuilder endpoints)
    {
        endpoints.MapHealthChecks("/health/live", Opciones(_ => false));
        endpoints.MapHealthChecks("/health/ready", Opciones(r => r.Tags.Contains("ready")));
        return endpoints;
    }
    private static HealthCheckOptions Opciones(Func<HealthCheckRegistration, bool> filtro) => new()
    {
        Predicate = filtro,
        ResultStatusCodes = { [HealthStatus.Healthy] = 200, [HealthStatus.Degraded] = 503, [HealthStatus.Unhealthy] = 503 },
        ResponseWriter = (context, report) => context.Response.WriteAsJsonAsync(new
        {
            estado = report.Status.ToString(),
            componentes = report.Entries.Select(e => new
            { nombre = e.Key, estado = e.Value.Status.ToString(), milisegundos = e.Value.Duration.TotalMilliseconds })
        }, cancellationToken: context.RequestAborted)
    };
}
