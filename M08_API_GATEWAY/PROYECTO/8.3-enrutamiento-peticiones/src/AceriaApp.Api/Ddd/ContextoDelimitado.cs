namespace AceriaApp.Api.Ddd;

public class ContextoDelimitado
{
    public string Nombre { get; init; } = string.Empty;
    public string TipoDeSubdominio { get; init; } = string.Empty;
    public string LenguajeUbicuo { get; init; } = string.Empty;
    public bool TieneModeloPropio { get; init; }
    public bool ComparteModeloConOtro { get; init; }
}
