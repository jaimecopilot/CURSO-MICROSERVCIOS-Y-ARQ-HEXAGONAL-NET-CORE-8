namespace AceriaApp.Api.Enrutamiento;

public class ReglaEnrutamiento
{
    public string Patron { get; init; } = string.Empty;
    public string MetodoHttp { get; init; } = string.Empty;
    public int Orden { get; init; }
    public bool TieneTransformacionDeRuta { get; init; }
    public bool TieneTransformacionDeCabecera { get; init; }
    public bool TieneTransformacionDeConsulta { get; init; }
}
