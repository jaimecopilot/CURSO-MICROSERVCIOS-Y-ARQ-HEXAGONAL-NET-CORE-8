namespace AceriaApp.Monolito.Api.Metricas;

// PASO 1.2.7: datos de una capacidad del monolito.
public class MetricasServicio
{
    public string Nombre { get; init; } = string.Empty;
    public int NumeroDeEndpoints { get; init; }
    public int NumeroDeTablas { get; init; }
    public int NumeroDeDependenciasExternas { get; init; }

    public double IndiceDeComplejidad() =>
        NumeroDeEndpoints + NumeroDeTablas + NumeroDeDependenciasExternas;

    public bool EsCandidatoAExtraccion() =>
        NumeroDeDependenciasExternas <= 1 && NumeroDeTablas <= 3;
}
