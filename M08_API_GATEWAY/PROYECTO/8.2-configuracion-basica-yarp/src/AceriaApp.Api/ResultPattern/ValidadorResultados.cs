using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.ResultPattern;

public class ValidadorResultados
{
    public ResultadoResultados Validar(IEnumerable<ResultadoOperacion> operaciones)
    {
        var errores = new List<string>();
        var lista = operaciones.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay operaciones declaradas.");
        }

        foreach (var operacion in lista)
        {
            if (string.IsNullOrWhiteSpace(operacion.Nombre))
            {
                errores.Add("Una operación no declara el nombre.");
            }

            if (!operacion.UsaResult && operacion.NumeroDeErroresEsperados > 0)
            {
                errores.Add($"La operación '{operacion.Nombre}' tiene errores esperados pero no usa el patrón Result.");
            }

            if (operacion.UsaExcepcionesParaErroresEsperados)
            {
                errores.Add($"La operación '{operacion.Nombre}' usa excepciones para errores esperados.");
            }
        }

        return new ResultadoResultados(errores.Count == 0, errores);
    }
}

public record ResultadoResultados(bool EsValido, IReadOnlyList<string> Errores);
