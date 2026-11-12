using System.Collections.Generic;
namespace AceriaApp.Api.Mediator;

public class CatalogoMensajes
{
    public static List<Mensaje> MensajesPorDefecto()
    {
        return new List<Mensaje>
        {
            new() { Nombre = "CrearOrdenCommand", Tipo = "Comando", TieneManejador = true, DevuelveResultado = true },
            new() { Nombre = "CancelarOrdenCommand", Tipo = "Comando", TieneManejador = true, DevuelveResultado = false },
            new() { Nombre = "ObtenerOrdenQuery", Tipo = "Consulta", TieneManejador = true, DevuelveResultado = true },
            new() { Nombre = "ListarOrdenesQuery", Tipo = "Consulta", TieneManejador = true, DevuelveResultado = true },
            new() { Nombre = "OrdenCreadaNotification", Tipo = "Notificacion", TieneManejador = true, DevuelveResultado = false }
        };
    }
}
