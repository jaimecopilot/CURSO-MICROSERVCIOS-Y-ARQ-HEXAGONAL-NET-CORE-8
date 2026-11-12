using System.Collections.Generic;
namespace AceriaApp.Api.InyeccionDependencias;

public class CatalogoInyeccion
{
    public static List<RegistroInyeccion> RegistrosPorDefecto()
    {
        return new List<RegistroInyeccion>
        {
            new() { Interfaz = "IOrdenRepositorio", Implementacion = "OrdenRepositorioSqlServer", Ciclo = "Scoped", RegistradoPorConstructor = true },
            new() { Interfaz = "IInventarioRepositorio", Implementacion = "InventarioRepositorioSqlServer", Ciclo = "Scoped", RegistradoPorConstructor = true },
            new() { Interfaz = "IOrdenServicio", Implementacion = "OrdenServicio", Ciclo = "Scoped", RegistradoPorConstructor = true },
            new() { Interfaz = "IPublicadorEventos", Implementacion = "PublicadorEventosRabbitMq", Ciclo = "Singleton", RegistradoPorConstructor = true },
            new() { Interfaz = "IUnitOfWork", Implementacion = "UnitOfWorkEfCore", Ciclo = "Scoped", RegistradoPorConstructor = true }
        };
    }
}
