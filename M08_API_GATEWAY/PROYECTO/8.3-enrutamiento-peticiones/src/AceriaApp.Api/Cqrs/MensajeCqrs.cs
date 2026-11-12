namespace AceriaApp.Api.Cqrs;

public class MensajeCqrs
{
    public string Nombre { get; init; } = string.Empty;
    public string Tipo { get; init; } = string.Empty;
    public bool TieneManejador { get; init; }
    public bool UsaSoloLectura { get; init; }
    public bool UsaEscritura { get; init; }
    public bool DevuelveResult { get; init; }
}
