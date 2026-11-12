using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.ComunicacionSincrona;

public class ValidadorComunicacionSincrona
{
    private static readonly string[] MetodosPermitidos = { "GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH", "DELETE" };

    public ResultadoComunicacionSincrona Validar(IEnumerable<LlamadaSincrona> llamadas)
    {
        var errores = new List<string>();
        var lista = llamadas.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay llamadas declaradas.");
        }

        foreach (var llamada in lista)
        {
            if (string.IsNullOrWhiteSpace(llamada.ServicioOrigen))
            {
                errores.Add("Una llamada no declara el servicio origen.");
            }

            if (string.IsNullOrWhiteSpace(llamada.ServicioDestino))
            {
                errores.Add($"La llamada desde '{llamada.ServicioOrigen}' no declara el servicio destino.");
            }

            if (llamada.ServicioOrigen == llamada.ServicioDestino)
            {
                errores.Add($"La llamada de '{llamada.ServicioOrigen}' apunta al mismo servicio.");
            }

            if (!MetodosPermitidos.Contains(llamada.Metodo))
            {
                errores.Add($"Método no permitido en '{llamada.ServicioOrigen}': '{llamada.Metodo}'.");
            }

            if (!llamada.TieneTimeout)
            {
                errores.Add($"La llamada desde '{llamada.ServicioOrigen}' no tiene timeout.");
            }

            if (llamada.TieneReintentos && (llamada.Metodo is "POST" or "PATCH")
                && !llamada.TieneClaveIdempotencia)
            {
                errores.Add($"La llamada desde '{llamada.ServicioOrigen}' declara reintentos no seguros sin clave de idempotencia.");
            }
        }

        return new ResultadoComunicacionSincrona(errores.Count == 0, errores);
    }
}

public record ResultadoComunicacionSincrona(bool EsValida, IReadOnlyList<string> Errores);
