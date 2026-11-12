namespace AceriaApp.Api.HealthChecks;

public class HealthCheck
{
    public string Nombre { get; init; } = string.Empty;
    public string Tipo { get; init; } = string.Empty;
    public string Recurso { get; init; } = string.Empty;
    public bool ConsultaDependenciaExterna { get; init; }
    public bool TieneTimeout { get; init; }
    public bool ExponeInformacionSensible { get; init; }
}
