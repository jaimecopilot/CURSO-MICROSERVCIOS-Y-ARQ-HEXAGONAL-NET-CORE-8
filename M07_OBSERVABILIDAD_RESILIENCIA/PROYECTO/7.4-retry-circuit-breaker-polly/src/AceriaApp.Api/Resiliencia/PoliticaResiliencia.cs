namespace AceriaApp.Api.Resiliencia;

public class PoliticaResiliencia
{
    public string Nombre { get; init; } = string.Empty;
    public string Tipo { get; init; } = string.Empty;
    public int NumeroDeReintentos { get; init; }
    public int MinimoDeMuestras { get; init; }
    public double ProporcionDeFallos { get; init; } = 0.5;
    public int VentanaMuestreoSegundos { get; init; } = 10;
    public int DuracionAperturaSegundos { get; init; } = 5;
    public bool OperacionIdempotente { get; init; }
    public bool TieneTimeout { get; init; }
    public bool RegistraEventos { get; init; }
}
