namespace AceriaApp.Api.ComunicacionAsincrona;

public class Evento
{
    public string Nombre { get; init; } = string.Empty;
    public string Tipo { get; init; } = string.Empty;
    public string Publicador { get; init; } = string.Empty;
    public int NumeroDeConsumidores { get; init; }
    public bool TieneIdempotencia { get; init; }
    public bool TieneReintentos { get; init; }
}
