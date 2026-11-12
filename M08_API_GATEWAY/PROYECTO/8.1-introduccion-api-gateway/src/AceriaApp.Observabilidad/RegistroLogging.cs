using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using Serilog;
using Serilog.Core;
using Serilog.Events;
using Serilog.Formatting.Json;
namespace AceriaApp.Observabilidad;
public static class RegistroLogging
{
    public static IServiceCollection AddLoggingAceria(this IServiceCollection services, string servicio, IConfiguration? config = null)
    {
        var nivel = config?.GetValue("Observabilidad:NivelMinimo", LogEventLevel.Information) ?? LogEventLevel.Information;
        services.AddLogging();
        services.AddHttpContextAccessor();
        services.AddTransient<PropagarCorrelacionHandler>();
        services.AddSerilog((provider, log) => log.MinimumLevel.Is(nivel)
            .MinimumLevel.Override("Microsoft.AspNetCore", LogEventLevel.Warning)
            .MinimumLevel.Override("Microsoft.AspNetCore.Diagnostics.ExceptionHandlerMiddleware", LogEventLevel.Fatal)
            .MinimumLevel.Override("Microsoft.EntityFrameworkCore", LogEventLevel.Warning)
            .MinimumLevel.Override("System.Net.Http.HttpClient", LogEventLevel.Warning)
            .MinimumLevel.Override("Polly", LogEventLevel.Fatal)
            .Enrich.FromLogContext().Enrich.With(new CamposHttpSeguros()).Enrich.WithProperty("Servicio", servicio)
            .ReadFrom.Services(provider).WriteTo.Console(new JsonFormatter()));
        return services;
    }
    private sealed class CamposHttpSeguros : ILogEventEnricher
    {
        public void Enrich(LogEvent logEvent, ILogEventPropertyFactory factory) =>
            logEvent.RemovePropertyIfPresent("RequestPath");
    }
    public static IApplicationBuilder UseLoggingAceria(this IApplicationBuilder app) =>
        app.UseMiddleware<CorrelacionMiddleware>().UseMiddleware<ResumenPeticionMiddleware>();
}
