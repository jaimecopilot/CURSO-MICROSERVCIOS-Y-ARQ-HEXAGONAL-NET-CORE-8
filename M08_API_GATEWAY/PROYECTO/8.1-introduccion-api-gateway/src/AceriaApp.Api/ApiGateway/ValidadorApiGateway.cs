using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.ApiGateway;

public class ValidadorApiGateway
{
    public ResultadoApiGateway Validar(IEnumerable<RutaGateway> rutas)
    {
        var errores = new List<string>();
        var lista = rutas.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay rutas declaradas.");
        }

        foreach (var ruta in lista)
        {
            if (string.IsNullOrWhiteSpace(ruta.RutaExterna))
            {
                errores.Add("Una ruta no declara la ruta externa.");
            }

            if (string.IsNullOrWhiteSpace(ruta.ServicioDestino))
            {
                errores.Add($"La ruta '{ruta.RutaExterna}' no declara el servicio destino.");
            }

            if (string.IsNullOrWhiteSpace(ruta.RutaInterna))
            {
                errores.Add($"La ruta '{ruta.RutaExterna}' no declara la ruta interna.");
            }

            if (!ruta.AplicaAutenticacion)
            {
                errores.Add($"La ruta '{ruta.RutaExterna}' no aplica autenticación.");
            }

            if (!ruta.AplicaRateLimit)
            {
                errores.Add($"La ruta '{ruta.RutaExterna}' no aplica limitación de tasa.");
            }

            if (!ruta.AplicaCorrelacion)
            {
                errores.Add($"La ruta '{ruta.RutaExterna}' no aplica correlación.");
            }
        }

        return new ResultadoApiGateway(errores.Count == 0, errores);
    }
}

public record ResultadoApiGateway(bool EsValida, IReadOnlyList<string> Errores);
