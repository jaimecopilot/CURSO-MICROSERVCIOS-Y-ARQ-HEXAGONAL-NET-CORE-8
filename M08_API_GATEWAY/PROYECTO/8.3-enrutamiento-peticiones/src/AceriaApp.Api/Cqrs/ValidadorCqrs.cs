using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.Cqrs;

public class ValidadorCqrs
{
    private static readonly string[] TiposPermitidos = { "Command", "Query" };

    public ResultadoCqrs Validar(IEnumerable<MensajeCqrs> mensajes)
    {
        var errores = new List<string>();
        var lista = mensajes.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay mensajes declarados.");
        }

        foreach (var mensaje in lista)
        {
            if (string.IsNullOrWhiteSpace(mensaje.Nombre))
            {
                errores.Add("Un mensaje no declara el nombre.");
            }

            if (!TiposPermitidos.Contains(mensaje.Tipo))
            {
                errores.Add($"Tipo no permitido en '{mensaje.Nombre}': '{mensaje.Tipo}'.");
            }

            if (!mensaje.TieneManejador)
            {
                errores.Add($"El mensaje '{mensaje.Nombre}' no tiene manejador.");
            }

            if (!mensaje.DevuelveResult)
            {
                errores.Add($"El mensaje '{mensaje.Nombre}' no devuelve Result.");
            }

            if (mensaje.Tipo == "Command" && !mensaje.UsaEscritura)
            {
                errores.Add($"El command '{mensaje.Nombre}' no usa escritura.");
            }

            if (mensaje.Tipo == "Query" && !mensaje.UsaSoloLectura)
            {
                errores.Add($"La query '{mensaje.Nombre}' no es de solo lectura.");
            }

            if (mensaje.Tipo == "Query" && mensaje.UsaEscritura)
            {
                errores.Add($"La query '{mensaje.Nombre}' usa escritura.");
            }
        }

        return new ResultadoCqrs(errores.Count == 0, errores);
    }
}

public record ResultadoCqrs(bool EsValido, IReadOnlyList<string> Errores);
