namespace AceriaApp.Api.Logging;

public class ConfiguracionLogging
{
    public string NivelMinimo { get; init; } = string.Empty;
    public bool UsaLoggingEstructurado { get; init; }
    public bool TieneCorrelacion { get; init; }
    public bool EvitaDatosSensibles { get; init; }
    public bool ConfiguradoPorEntorno { get; init; }
}
