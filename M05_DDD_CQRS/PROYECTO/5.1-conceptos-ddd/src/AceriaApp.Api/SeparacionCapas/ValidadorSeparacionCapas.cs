namespace AceriaApp.Api.SeparacionCapas;

public class ValidadorSeparacionCapas
{
    private static readonly Dictionary<string, string[]> ReferenciasPermitidas = new()
    {
        { "Dominio", Array.Empty<string>() },
        { "Aplicacion", new[] { "Dominio" } },
        { "Infraestructura", new[] { "Aplicacion", "Dominio" } },
        { "Api", new[] { "Aplicacion", "Infraestructura" } }
    };

    public ResultadoSeparacion Validar(IEnumerable<Proyecto> proyectos)
    {
        var errores = new List<string>();

        foreach (var proyecto in proyectos)
        {
            if (!ReferenciasPermitidas.ContainsKey(proyecto.Capa))
            {
                errores.Add($"Capa desconocida: '{proyecto.Capa}'.");
                continue;
            }

            var permitidas = ReferenciasPermitidas[proyecto.Capa];
            foreach (var referencia in proyecto.Referencias)
            {
                if (!permitidas.Contains(referencia))
                {
                    errores.Add($"El proyecto '{proyecto.Nombre}' de la capa '{proyecto.Capa}' no puede referenciar '{referencia}'.");
                }
            }
        }

        return new ResultadoSeparacion(errores.Count == 0, errores);
    }
}

public record ResultadoSeparacion(bool EsValida, IReadOnlyList<string> Errores);
