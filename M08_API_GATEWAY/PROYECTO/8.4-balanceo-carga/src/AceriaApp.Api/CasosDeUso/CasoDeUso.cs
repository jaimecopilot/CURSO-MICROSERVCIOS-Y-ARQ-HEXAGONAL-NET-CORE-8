namespace AceriaApp.Api.CasosDeUso;

public class CasoDeUso
{
    public string Nombre { get; init; } = string.Empty;
    public string Tipo { get; init; } = string.Empty;
    public bool TieneManejador { get; init; }
    public bool DevuelveResult { get; init; }
    public bool CoordinaUnidadDeTrabajo { get; init; }
    public bool ContieneReglasDeNegocio { get; init; }
}
