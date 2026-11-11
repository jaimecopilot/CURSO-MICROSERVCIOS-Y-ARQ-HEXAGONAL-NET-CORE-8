using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.Ddd;

public class ValidadorContextos
{
    private static readonly string[] TiposPermitidos = { "Nucleo", "Soporte", "Generico" };

    public ResultadoContextos Validar(IEnumerable<ContextoDelimitado> contextos)
    {
        var errores = new List<string>();
        var lista = contextos.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay contextos declarados.");
        }

        foreach (var contexto in lista)
        {
            if (string.IsNullOrWhiteSpace(contexto.Nombre))
            {
                errores.Add("Un contexto no declara el nombre.");
            }

            if (!TiposPermitidos.Contains(contexto.TipoDeSubdominio))
            {
                errores.Add($"Tipo de subdominio no permitido en '{contexto.Nombre}': '{contexto.TipoDeSubdominio}'.");
            }

            if (string.IsNullOrWhiteSpace(contexto.LenguajeUbicuo))
            {
                errores.Add($"El contexto '{contexto.Nombre}' no declara lenguaje ubicuo.");
            }

            if (!contexto.TieneModeloPropio)
            {
                errores.Add($"El contexto '{contexto.Nombre}' no tiene modelo propio.");
            }

            if (contexto.ComparteModeloConOtro)
            {
                errores.Add($"El contexto '{contexto.Nombre}' comparte modelo con otro contexto.");
            }
        }

        return new ResultadoContextos(errores.Count == 0, errores);
    }
}

public record ResultadoContextos(bool EsValido, IReadOnlyList<string> Errores);
