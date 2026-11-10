namespace AceriaApp.Api.Capas;

public class CatalogoCapas
{
    public static Dictionary<string, IReadOnlyList<string>> ReglasPorDefecto()
    {
        return new Dictionary<string, IReadOnlyList<string>>
        {
            { "Presentacion", new[] { "Aplicacion" } },
            { "Aplicacion", new[] { "Dominio" } },
            { "Infraestructura", new[] { "Aplicacion", "Dominio" } },
            { "Dominio", Array.Empty<string>() }
        };
    }
}
