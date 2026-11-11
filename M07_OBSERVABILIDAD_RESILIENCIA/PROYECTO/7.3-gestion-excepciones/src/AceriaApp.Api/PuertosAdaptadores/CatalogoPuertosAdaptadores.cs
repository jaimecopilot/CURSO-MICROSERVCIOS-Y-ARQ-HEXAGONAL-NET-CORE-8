namespace AceriaApp.Api.PuertosAdaptadores;

public class CatalogoPuertosAdaptadores
{
    public static List<Puerto> PuertosPorDefecto()
    {
        return new List<Puerto>
        {
            new() { Nombre = "IOrdenServicio", Tipo = "Entrada", Capa = "Aplicacion" },
            new() { Nombre = "IInventarioServicio", Tipo = "Entrada", Capa = "Aplicacion" },
            new() { Nombre = "IOrdenRepositorio", Tipo = "Salida", Capa = "Aplicacion" },
            new() { Nombre = "IInventarioRepositorio", Tipo = "Salida", Capa = "Aplicacion" },
            new() { Nombre = "IPublicadorEventos", Tipo = "Salida", Capa = "Aplicacion" }
        };
    }

    public static List<Adaptador> AdaptadoresPorDefecto()
    {
        return new List<Adaptador>
        {
            new() { Nombre = "EndpointsMinimalApi", Tipo = "Entrada", PuertoImplementado = "IOrdenServicio", Capa = "Presentacion" },
            new() { Nombre = "OrdenRepositorioSqlServer", Tipo = "Salida", PuertoImplementado = "IOrdenRepositorio", Capa = "Infraestructura" },
            new() { Nombre = "PublicadorEventosRabbitMq", Tipo = "Salida", PuertoImplementado = "IPublicadorEventos", Capa = "Infraestructura" }
        };
    }
}
