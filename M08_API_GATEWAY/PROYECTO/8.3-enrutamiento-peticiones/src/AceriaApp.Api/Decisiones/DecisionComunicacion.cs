namespace AceriaApp.Api.Decisiones;

public class DecisionComunicacion
{
    public string Interaccion { get; init; } = string.Empty;
    public string Enfoque { get; init; } = string.Empty;
    public bool RequiereRespuestaInmediata { get; init; }
    public bool ToleraConsistenciaEventual { get; init; }
    public bool TienePatronHibrido { get; init; }
}
