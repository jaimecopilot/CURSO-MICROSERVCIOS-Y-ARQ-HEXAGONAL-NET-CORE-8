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
        return services;
    }
}
