namespace AceriaApp.Api.Capas;

public class Capa
{
    public string Nombre { get; init; } = string.Empty;
    public IReadOnlyList<string> DependenciasPermitidas { get; init; } = Array.Empty<string>();
}
