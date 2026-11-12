using System.Collections.Generic;
namespace AceriaApp.Api.Cqrs;

public class CatalogoCqrs
{
    public static List<MensajeCqrs> MensajesPorDefecto()
    {
        return new List<MensajeCqrs>
        {
            new() { Nombre = "CrearOrdenCommand", Tipo = "Command", TieneManejador = true, UsaEscritura = true, UsaSoloLectura = false, DevuelveResult = true },
            new() { Nombre = "CancelarOrdenCommand", Tipo = "Command", TieneManejador = true, UsaEscritura = true, UsaSoloLectura = false, DevuelveResult = true },
            new() { Nombre = "ObtenerOrdenQuery", Tipo = "Query", TieneManejador = true, UsaEscritura = false, UsaSoloLectura = true, DevuelveResult = true },
            new() { Nombre = "ListarOrdenesQuery", Tipo = "Query", TieneManejador = true, UsaEscritura = false, UsaSoloLectura = true, DevuelveResult = true }
        };
    }
}
