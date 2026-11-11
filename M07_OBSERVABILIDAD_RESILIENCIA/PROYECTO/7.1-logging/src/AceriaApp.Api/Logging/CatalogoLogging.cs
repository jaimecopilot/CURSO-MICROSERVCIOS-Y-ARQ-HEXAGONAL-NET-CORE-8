using System.Collections.Generic;

namespace AceriaApp.Api.Logging;

public class CatalogoLogging
{
    public static List<ConfiguracionLogging> ConfiguracionesPorDefecto()
    {
        return new List<ConfiguracionLogging>
        {
            new()
            {
                NivelMinimo = "Debug",
                UsaLoggingEstructurado = true,
                TieneCorrelacion = true,
                EvitaDatosSensibles = true,
                ConfiguradoPorEntorno = true
            },
            new()
            {
                NivelMinimo = "Information",
                UsaLoggingEstructurado = true,
                TieneCorrelacion = true,
                EvitaDatosSensibles = true,
                ConfiguradoPorEntorno = true
            },
            new()
            {
                NivelMinimo = "Warning",
                UsaLoggingEstructurado = true,
                TieneCorrelacion = true,
                EvitaDatosSensibles = true,
                ConfiguradoPorEntorno = true
            }
        };
    }
}
