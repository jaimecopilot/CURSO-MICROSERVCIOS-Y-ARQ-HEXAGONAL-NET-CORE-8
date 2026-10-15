using System.Linq;
namespace AceriaApp.Monolito.Api.Diseno;

// PASO 1.3.9: catalogar y filtrar los límites de servicio.
public class CatalogoLimites
{
    private readonly List<LimiteServicio> _limites;
    public CatalogoLimites(List<LimiteServicio> limites) { _limites = limites; }
    public IEnumerable<LimiteServicio> LimitesValidos(ValidadorLimiteServicio validador) =>
        _limites.Where(l => validador.Validar(l).EsValido);
    public IEnumerable<LimiteServicio> LimitesInvalidos(ValidadorLimiteServicio validador) =>
        _limites.Where(l => !validador.Validar(l).EsValido);

    // RETO 1.3: descomentar el record ResumenLimites (debajo) y el método.
    // public ResumenLimites Resumen(ValidadorLimiteServicio validador)
    // {
    //     var validos = _limites.Count(l => validador.Validar(l).EsValido);
    //     var invalidos = _limites.Count - validos;
    //     var total = _limites.Count;
    //     var porcentaje = total == 0 ? 0 : (double)validos / total * 100;
    //     return new ResumenLimites(validos, invalidos, porcentaje);
    // }
}
// public record ResumenLimites(int Validos, int Invalidos, double PorcentajeValidez);
