namespace AceriaApp.Api.SeparacionCapas;

public class CatalogoProyectos
{
    public static List<Proyecto> ProyectosPorDefecto()
    {
        return new List<Proyecto>
        {
            new()
            {
                Nombre = "AceriaApp.Hexagonal.Dominio",
                Capa = "Dominio",
                Referencias = Array.Empty<string>()
            },
            new()
            {
                Nombre = "AceriaApp.Hexagonal.Aplicacion",
                Capa = "Aplicacion",
                Referencias = new[] { "Dominio" }
            },
            new()
            {
                Nombre = "AceriaApp.Hexagonal.Infraestructura",
                Capa = "Infraestructura",
                Referencias = new[] { "Aplicacion", "Dominio" }
            },
            new()
            {
                Nombre = "AceriaApp.Api",
                Capa = "Api",
                Referencias = new[] { "Aplicacion", "Infraestructura" }
            }
        };
    }
}
