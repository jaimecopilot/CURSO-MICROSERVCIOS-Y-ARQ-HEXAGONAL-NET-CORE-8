using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.Enrutamiento;

public class ValidadorEnrutamiento
{
    private static readonly string[] MetodosPermitidos = { "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS" };

    public ResultadoEnrutamiento Validar(IEnumerable<ReglaEnrutamiento> reglas)
    {
        var errores = new List<string>();
        var lista = reglas.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay reglas declaradas.");
        }

        foreach (var regla in lista)
        {
            if (string.IsNullOrWhiteSpace(regla.Patron))
            {
                errores.Add("Una regla no declara el patrón.");
            }

            if (!MetodosPermitidos.Contains(regla.MetodoHttp))
            {
                errores.Add($"Método HTTP no permitido en '{regla.Patron}': '{regla.MetodoHttp}'.");
            }

            if (regla.Orden < 0)
            {
                errores.Add($"El orden de la regla '{regla.Patron}' es negativo: '{regla.Orden}'.");
            }

            if (!regla.TieneTransformacionDeRuta &&
                !regla.TieneTransformacionDeCabecera &&
                !regla.TieneTransformacionDeConsulta)
            {
                errores.Add($"La regla '{regla.Patron}' no declara ninguna transformación.");
            }
        }

        return new ResultadoEnrutamiento(errores.Count == 0, errores);
    }
}

public record ResultadoEnrutamiento(bool EsValida, IReadOnlyList<string> Errores);
