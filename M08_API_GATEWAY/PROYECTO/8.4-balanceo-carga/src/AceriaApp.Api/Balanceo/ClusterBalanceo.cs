namespace AceriaApp.Api.Balanceo;

public class ClusterBalanceo
{
    public string Identificador { get; init; } = string.Empty;
    public string Politica { get; init; } = string.Empty;
    public int NumeroDeDestinos { get; init; }
    public bool TienePesos { get; init; }
    public bool CombinadoConHealthChecks { get; init; }
}
