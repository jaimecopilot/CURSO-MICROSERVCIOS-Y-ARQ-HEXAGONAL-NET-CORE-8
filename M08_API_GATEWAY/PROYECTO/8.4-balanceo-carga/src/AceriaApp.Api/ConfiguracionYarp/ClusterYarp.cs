namespace AceriaApp.Api.ConfiguracionYarp;

public class ClusterYarp
{
    public string Identificador { get; init; } = string.Empty;
    public IReadOnlyList<string> Destinos { get; init; } = Array.Empty<string>();
    public bool TieneDireccionValida { get; init; }
    public bool TieneConfiguracionPorEntorno { get; init; }
}
