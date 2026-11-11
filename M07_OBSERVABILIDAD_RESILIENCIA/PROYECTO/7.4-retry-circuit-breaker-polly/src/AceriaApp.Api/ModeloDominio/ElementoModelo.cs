namespace AceriaApp.Api.ModeloDominio;

public class ElementoModelo
{
    public string Nombre { get; init; } = string.Empty;
    public string Tipo { get; init; } = string.Empty;
    public bool TieneIdentidad { get; init; }
    public bool EsInmutable { get; init; }
    public bool ValidaInvariantes { get; init; }
}
