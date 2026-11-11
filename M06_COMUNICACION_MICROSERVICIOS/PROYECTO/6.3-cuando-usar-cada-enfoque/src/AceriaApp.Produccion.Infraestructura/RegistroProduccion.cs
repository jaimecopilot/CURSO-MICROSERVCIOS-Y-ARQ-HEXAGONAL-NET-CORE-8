using AceriaApp.Produccion.Aplicacion;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
namespace AceriaApp.Produccion.Infraestructura;
public static class RegistroProduccion
{
    public static IServiceCollection AddProduccion(this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<ProduccionDbContext>(o => o.UseSqlServer(configuration.GetConnectionString("AceriaProduccion")));
        services.AddScoped<IOrdenProduccionRepositorio, OrdenProduccionRepositorio>();
        services.AddScoped<IProduccionUnitOfWork, ProduccionUnitOfWork>();
        services.AddScoped<OrdenesProduccionCasosUso>();
        services.AddScoped<IOrdenProduccionLecturas, OrdenProduccionLecturas>();
        services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(CrearOrdenProduccionCommand).Assembly));
        return services;
    }
}
