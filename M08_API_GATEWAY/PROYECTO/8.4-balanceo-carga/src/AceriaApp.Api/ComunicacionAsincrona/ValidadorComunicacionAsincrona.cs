using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.ComunicacionAsincrona;

public class ValidadorComunicacionAsincrona
{
    private static readonly string[] TiposPermitidos = { "Dominio", "Integracion" };

    public ResultadoComunicacionAsincrona Validar(IEnumerable<Evento> eventos)
    {
        var errores = new List<string>();
        var lista = eventos.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay eventos declarados.");
        }

        foreach (var evento in lista)
        {
            if (string.IsNullOrWhiteSpace(evento.Nombre))
            {
                errores.Add("Un evento no declara el nombre.");
            }

            if (!TiposPermitidos.Contains(evento.Tipo))
            {
                errores.Add($"Tipo no permitido en '{evento.Nombre}': '{evento.Tipo}'.");
            }

            if (string.IsNullOrWhiteSpace(evento.Publicador))
            {
                errores.Add($"El evento '{evento.Nombre}' no declara el publicador.");
            }

            if (evento.NumeroDeConsumidores < 0 || (evento.Tipo == "Integracion" && evento.NumeroDeConsumidores == 0))
            {
                errores.Add($"El evento '{evento.Nombre}' no tiene consumidores válidos para la política de este catálogo.");
            }

            if (evento.Tipo == "Integracion" && !evento.TieneIdempotencia)
            {
                errores.Add($"El evento '{evento.Nombre}' no declara idempotencia.");
            }

            if (evento.Tipo == "Integracion" && !evento.TieneReintentos)
            {
                errores.Add($"El evento '{evento.Nombre}' no declara reintentos.");
            }
        }

        return new ResultadoComunicacionAsincrona(errores.Count == 0, errores);
    }
}

public record ResultadoComunicacionAsincrona(bool EsValida, IReadOnlyList<string> Errores);
