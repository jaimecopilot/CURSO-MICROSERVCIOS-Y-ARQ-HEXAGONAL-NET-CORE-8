namespace AceriaApp.Api.Mediator;

public class Mensaje
{
    public string Nombre { get; init; } = string.Empty;
    public string Tipo { get; init; } = string.Empty;
    public bool TieneManejador { get; init; }
    public bool DevuelveResultado { get; init; }
}
