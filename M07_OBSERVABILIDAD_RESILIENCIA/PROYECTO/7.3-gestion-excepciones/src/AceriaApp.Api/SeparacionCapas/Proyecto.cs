namespace AceriaApp.Api.SeparacionCapas;

public class Proyecto
{
    public string Nombre { get; init; } = string.Empty;
    public string Capa { get; init; } = string.Empty;
    public IReadOnlyList<string> Referencias { get; init; } = Array.Empty<string>();
}
