namespace AceriaApp.Api.ComunicacionSincrona;

public class LlamadaSincrona
{
    public string ServicioOrigen { get; init; } = string.Empty;
    public string ServicioDestino { get; init; } = string.Empty;
    public string Metodo { get; init; } = string.Empty;
    public bool TieneTimeout { get; init; }
    public bool TieneReintentos { get; init; }
    public bool TieneCircuitBreaker { get; init; }
    public bool TieneClaveIdempotencia { get; init; }
}
