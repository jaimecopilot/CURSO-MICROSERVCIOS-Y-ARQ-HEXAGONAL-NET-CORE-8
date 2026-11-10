using AceriaApp.Hexagonal.Aplicacion.CasosUso;
using AceriaApp.Hexagonal.Aplicacion.Puertos;
using AceriaApp.Hexagonal.Infraestructura.Adaptadores;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace AceriaApp.Hexagonal.Infraestructura;

public static class ServiciosHexagonales
{
    public static IServiceCollection AddServiciosHexagonales(this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<HexagonalDbContext>(options =>
            options.UseSqlServer(configuration.GetConnectionString("AceriaHexagonal")));
        services.AddScoped<IOrdenRepositorio, OrdenRepositorioSqlServer>();
        services.AddScoped<OrdenesCasoUso>();
        return services;
    }
}
