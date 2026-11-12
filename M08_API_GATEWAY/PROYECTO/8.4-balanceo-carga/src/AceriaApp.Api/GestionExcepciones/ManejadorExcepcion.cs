namespace AceriaApp.Api.GestionExcepciones;

public class ManejadorExcepcion
{
    public string TipoExcepcion { get; init; } = string.Empty;
    public int CodigoHttp { get; init; }
    public string Titulo { get; init; } = string.Empty;
    public bool UsaProblemDetails { get; init; }
    public bool RegistraError { get; init; }
}
