using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.Mediator;

public class ValidadorMensajes
{
    private static readonly string[] TiposPermitidos = { "Comando", "Consulta", "Notificacion" };

    public ResultadoMensajes Validar(IEnumerable<Mensaje> mensajes)
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
                errores.Add($"Tipo de mensaje no permitido en '{mensaje.Nombre}': '{mensaje.Tipo}'.");
            }

            if (!mensaje.TieneManejador)
            {
                errores.Add($"El mensaje '{mensaje.Nombre}' no tiene manejador registrado.");
            }

            if (mensaje.Tipo == "Notificacion" && mensaje.DevuelveResultado)
            {
                errores.Add($"La notificación '{mensaje.Nombre}' no puede devolver resultado.");
            }
        }

        return new ResultadoMensajes(errores.Count == 0, errores);
    }
}

public record ResultadoMensajes(bool EsValido, IReadOnlyList<string> Errores);
