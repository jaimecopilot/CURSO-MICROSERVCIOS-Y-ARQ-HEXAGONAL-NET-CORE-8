namespace AceriaApp.Api.ResultPattern;

public class ResultadoOperacion
{
    public string Nombre { get; init; } = string.Empty;
    public bool UsaResult { get; init; }
    public bool UsaExcepcionesParaErroresEsperados { get; init; }
    public int NumeroDeErroresEsperados { get; init; }
}
