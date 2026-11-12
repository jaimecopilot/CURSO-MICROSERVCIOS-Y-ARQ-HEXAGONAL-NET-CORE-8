using System.Collections.Generic;
using System.Linq;

namespace AceriaApp.Api.Logging;

public class ValidadorLogging
{
    private static readonly string[] NivelesPermitidos = { "Trace", "Debug", "Information", "Warning", "Error", "Critical" };

    public ResultadoLogging Validar(IEnumerable<ConfiguracionLogging> configuraciones)
    {
        var errores = new List<string>();
        var lista = configuraciones.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay configuraciones de logging declaradas.");
        }

        foreach (var configuracion in lista)
        {
            if (!NivelesPermitidos.Contains(configuracion.NivelMinimo))
            {
                errores.Add($"Nivel mínimo no permitido: '{configuracion.NivelMinimo}'.");
            }

            if (!configuracion.UsaLoggingEstructurado)
            {
                errores.Add($"La configuración con nivel '{configuracion.NivelMinimo}' no usa logging estructurado.");
            }

            if (!configuracion.TieneCorrelacion)
            {
                errores.Add($"La configuración con nivel '{configuracion.NivelMinimo}' no tiene correlación.");
            }

            if (!configuracion.EvitaDatosSensibles)
            {
                errores.Add($"La configuración con nivel '{configuracion.NivelMinimo}' no evita datos sensibles.");
            }

            if (!configuracion.ConfiguradoPorEntorno)
            {
                errores.Add($"La configuración con nivel '{configuracion.NivelMinimo}' no está configurada por entorno.");
            }
        }

        return new ResultadoLogging(errores.Count == 0, errores);
    }
}

public record ResultadoLogging(bool EsValida, IReadOnlyList<string> Errores);
