using AceriaApp.Comunicacion.Aplicacion;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
namespace AceriaApp.Comunicacion.Infraestructura;
public static class RegistroComunicacion
{
    public static IServiceCollection AddComunicacion(this IServiceCollection services, IConfiguration config)
    {
        services.AddHttpClient<IClienteInventario, ClienteInventarioHttp>(http =>
        {
            http.BaseAddress = new Uri(config["Comunicacion:InventarioUrl"] ?? "http://localhost:5106/");
            http.Timeout = TimeSpan.FromSeconds(3);
        });
        services.AddScoped<FlujoPlanificacion>();
        services.AddScoped<IPlanificadorIntegrado, PlanificadorIntegrado>();
        services.AddScoped<DespachadorOutbox>();
        services.AddSingleton(new RabbitMqOpciones(config["Comunicacion:RabbitMqUri"] ?? "amqp://curso:curso-local@localhost:5672/",
            config["Comunicacion:Prefijo"] ?? "aceria"));
        services.AddSingleton<RabbitMqTransporte>();
        services.AddSingleton<ITransporteEventos>(sp => sp.GetRequiredService<RabbitMqTransporte>());
        if (config.GetValue<bool>("Comunicacion:WorkersActivos")) services.AddHostedService<PublicadorOutboxWorker>();
        return services;
    }
}
