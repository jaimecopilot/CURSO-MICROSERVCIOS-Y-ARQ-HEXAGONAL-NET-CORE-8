namespace AceriaApp.Api.InyeccionDependencias;

public class RegistroInyeccion
{
    public string Interfaz { get; init; } = string.Empty;
    public string Implementacion { get; init; } = string.Empty;
    public string Ciclo { get; init; } = string.Empty;
    public bool RegistradoPorConstructor { get; init; }
    public bool ResuelveManualmente { get; init; }
    public bool CapturaContenedor { get; init; }
}
