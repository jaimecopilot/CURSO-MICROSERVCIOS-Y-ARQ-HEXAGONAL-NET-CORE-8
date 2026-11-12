using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.ModeloDominio;

public class ValidadorModeloDominio
{
    private static readonly string[] TiposPermitidos = { "Entidad", "ValueObject" };

    public ResultadoModelo Validar(IEnumerable<ElementoModelo> elementos)
    {
        var errores = new List<string>();
        var lista = elementos.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay elementos declarados.");
        }

        foreach (var elemento in lista)
        {
            if (string.IsNullOrWhiteSpace(elemento.Nombre))
            {
                errores.Add("Un elemento no declara el nombre.");
            }

            if (!TiposPermitidos.Contains(elemento.Tipo))
            {
                errores.Add($"Tipo no permitido en '{elemento.Nombre}': '{elemento.Tipo}'.");
            }

            if (elemento.Tipo == "Entidad" && !elemento.TieneIdentidad)
            {
                errores.Add($"La entidad '{elemento.Nombre}' no tiene identidad.");
            }

            if (elemento.Tipo == "ValueObject" && elemento.TieneIdentidad)
            {
                errores.Add($"El value object '{elemento.Nombre}' no debería tener identidad.");
            }

            if (elemento.Tipo == "ValueObject" && !elemento.EsInmutable)
            {
                errores.Add($"El value object '{elemento.Nombre}' no es inmutable.");
            }

            if (!elemento.ValidaInvariantes)
            {
                errores.Add($"El elemento '{elemento.Nombre}' no valida invariantes.");
            }
        }

        return new ResultadoModelo(errores.Count == 0, errores);
    }
}

public record ResultadoModelo(bool EsValido, IReadOnlyList<string> Errores);
