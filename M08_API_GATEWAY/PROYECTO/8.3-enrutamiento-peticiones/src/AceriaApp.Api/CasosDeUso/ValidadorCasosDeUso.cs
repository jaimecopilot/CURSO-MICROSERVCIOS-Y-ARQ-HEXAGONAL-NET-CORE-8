using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.CasosDeUso;

public class ValidadorCasosDeUso
{
    private static readonly string[] TiposPermitidos = { "Escritura", "Lectura" };

    public ResultadoCasosDeUso Validar(IEnumerable<CasoDeUso> casos)
    {
        var errores = new List<string>();
        var lista = casos.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay casos de uso declarados.");
        }

        foreach (var caso in lista)
        {
            if (string.IsNullOrWhiteSpace(caso.Nombre))
            {
                errores.Add("Un caso de uso no declara el nombre.");
            }

            if (!TiposPermitidos.Contains(caso.Tipo))
            {
                errores.Add($"Tipo no permitido en '{caso.Nombre}': '{caso.Tipo}'.");
            }

            if (!caso.TieneManejador)
            {
                errores.Add($"El caso de uso '{caso.Nombre}' no tiene manejador.");
            }

            if (!caso.DevuelveResult)
            {
                errores.Add($"El caso de uso '{caso.Nombre}' no devuelve Result.");
            }

            if (caso.Tipo == "Escritura" && !caso.CoordinaUnidadDeTrabajo)
            {
                errores.Add($"El caso de uso de escritura '{caso.Nombre}' no coordina la unidad de trabajo.");
            }

            if (caso.ContieneReglasDeNegocio)
            {
                errores.Add($"El caso de uso '{caso.Nombre}' contiene reglas de negocio.");
            }
        }

        return new ResultadoCasosDeUso(errores.Count == 0, errores);
    }
}

public record ResultadoCasosDeUso(bool EsValido, IReadOnlyList<string> Errores);
