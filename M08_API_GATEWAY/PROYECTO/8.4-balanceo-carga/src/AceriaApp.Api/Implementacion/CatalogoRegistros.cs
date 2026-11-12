namespace AceriaApp.Api.Implementacion;

public class CatalogoRegistros
{
    public static List<RegistroServicio> RegistrosPorDefecto()
    {
        return new List<RegistroServicio>
        {
            new() { Puerto = "IOrdenRepositorio", Implementacion = "OrdenRepositorioSqlServer", Ciclo = "Scoped", EsAdaptadorDeSalida = true },
            new() { Puerto = "IInventarioRepositorio", Implementacion = "InventarioRepositorioSqlServer", Ciclo = "Scoped", EsAdaptadorDeSalida = true },
            new() { Puerto = "IPublicadorEventos", Implementacion = "PublicadorEventosRabbitMq", Ciclo = "Singleton", EsAdaptadorDeSalida = true },
            new() { Puerto = "IOrdenServicio", Implementacion = "OrdenServicio", Ciclo = "Scoped", EsAdaptadorDeSalida = false },
            new() { Puerto = "IInventarioServicio", Implementacion = "InventarioServicio", Ciclo = "Scoped", EsAdaptadorDeSalida = false }
        };
    }
}
