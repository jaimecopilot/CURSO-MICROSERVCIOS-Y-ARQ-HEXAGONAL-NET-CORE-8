using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.DominioAceria;

public class ValidadorDominioAceria
{
    private static readonly string[] ContextosPermitidos = { "Produccion", "Aprovisionamiento", "Clientes", "Facturacion" };
    private static readonly string[] TiposPermitidos = { "Entidad", "ValueObject", "Agregado" };

    public ResultadoDominioAceria Validar(IEnumerable<ElementoAceria> elementos)
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

            if (!ContextosPermitidos.Contains(elemento.Contexto))
            {
                errores.Add($"Contexto no permitido en '{elemento.Nombre}': '{elemento.Contexto}'.");
            }

            if (!TiposPermitidos.Contains(elemento.Tipo))
            {
                errores.Add($"Tipo no permitido en '{elemento.Nombre}': '{elemento.Tipo}'.");
            }

            if (!elemento.TieneInvariantes)
            {
                errores.Add($"El elemento '{elemento.Nombre}' no tiene invariantes.");
            }
        }

        return new ResultadoDominioAceria(errores.Count == 0, errores);
    }
}

public record ResultadoDominioAceria(bool EsValido, IReadOnlyList<string> Errores);
