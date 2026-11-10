using AceriaApp.Hexagonal.Aplicacion.Patrones;
using Microsoft.Extensions.DependencyInjection;
namespace AceriaApp.Hexagonal.Infraestructura.Patrones;

public static class ServiciosPatrones
{
    /// <summary>Requiere HexagonalDbContext registrado; cada petición comparte contexto, repositorio y UoW.</summary>
    public static IServiceCollection AddPatronesOrdenes(this IServiceCollection services)
    {
        services.AddLogging();
        services.AddScoped<IOrdenTrabajoRepositorio, OrdenTrabajoRepositorio>();
        services.AddScoped<IUnitOfWork, EfUnitOfWork>();
        services.AddScoped<OrdenesTransaccionales>();
        services.AddScoped<OrdenesConResultado>();
        services.AddMediatR(cfg =>
        {
            cfg.RegisterServicesFromAssemblyContaining<CrearOrdenCommand>();
            cfg.Lifetime = ServiceLifetime.Scoped;
            cfg.AddOpenBehavior(typeof(LoggingBehavior<,>));
        });
        return services;
    }
}
