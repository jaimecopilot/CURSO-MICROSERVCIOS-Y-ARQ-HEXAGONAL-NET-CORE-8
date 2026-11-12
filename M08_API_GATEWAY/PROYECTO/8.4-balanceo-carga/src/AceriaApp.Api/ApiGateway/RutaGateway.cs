namespace AceriaApp.Api.ApiGateway;

public class RutaGateway
{
    public string RutaExterna { get; init; } = string.Empty;
    public string ServicioDestino { get; init; } = string.Empty;
    public string RutaInterna { get; init; } = string.Empty;
    public bool AplicaAutenticacion { get; init; }
    public bool AplicaRateLimit { get; init; }
    public bool AplicaCorrelacion { get; init; }
}
