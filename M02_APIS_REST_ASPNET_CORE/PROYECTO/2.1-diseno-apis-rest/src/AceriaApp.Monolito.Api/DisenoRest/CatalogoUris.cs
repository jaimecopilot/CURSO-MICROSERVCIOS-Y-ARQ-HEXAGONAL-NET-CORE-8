namespace AceriaApp.Monolito.Api.DisenoRest;
public class CatalogoUris
{
    private readonly IReadOnlyList<string> _uris;
    public CatalogoUris(IEnumerable<string> uris) => _uris = uris.ToArray();
    public IEnumerable<string> UrisValidas(ValidadorUriRest validador) =>
        _uris.Where(u => validador.Validar(u).EsValida);
    public IEnumerable<string> UrisInvalidas(ValidadorUriRest validador) =>
        _uris.Where(u => !validador.Validar(u).EsValida);
    // RETO 2.1: agregar Resumen y ResumenUris según la guía de prácticas.
}
