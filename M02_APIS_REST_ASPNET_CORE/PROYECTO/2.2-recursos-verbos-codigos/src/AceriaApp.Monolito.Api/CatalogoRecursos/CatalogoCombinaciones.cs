namespace AceriaApp.Monolito.Api.CatalogoRecursos;
public class CatalogoCombinaciones
{
    private readonly IReadOnlyList<CombinacionVerboCodigo> _combinaciones;
    public CatalogoCombinaciones(IEnumerable<CombinacionVerboCodigo> combinaciones) =>
        _combinaciones=combinaciones.ToArray();
    public IEnumerable<CombinacionVerboCodigo> CombinacionesValidas(ValidadorCombinacionVerboCodigo v) =>
        _combinaciones.Where(c=>v.Validar(c).EsValida);
    public IEnumerable<CombinacionVerboCodigo> CombinacionesInvalidas(ValidadorCombinacionVerboCodigo v) =>
        _combinaciones.Where(c=>!v.Validar(c).EsValida);
    // RETO 2.2: agregar Resumen y record ResumenCombinaciones.
}
