namespace AceriaApp.Api.DominioAceria;

public class ElementoAceria
{
    public string Nombre { get; init; } = string.Empty;
    public string Contexto { get; init; } = string.Empty;
    public string Tipo { get; init; } = string.Empty;
    public bool TieneInvariantes { get; init; }
    public bool EsRaizDeAgregado { get; init; }
}
