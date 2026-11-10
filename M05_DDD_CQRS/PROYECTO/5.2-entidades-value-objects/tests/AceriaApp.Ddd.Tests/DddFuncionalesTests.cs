using AceriaApp.Produccion.Dominio;
using Xunit;
namespace AceriaApp.Ddd.Tests;
public sealed class DddFuncionalesTests
{
    [Fact]
    public void Crear_una_orden_asigna_identidad_y_normaliza_el_lenguaje_del_negocio()
    {
        var orden = new OrdenProduccion("  Axia  ", " Acero ", 20);
        Assert.NotEqual(Guid.Empty, orden.Id);
        Assert.Equal("Axia", orden.Cliente);
        Assert.Equal("Acero", orden.Material);
        Assert.Equal(20, orden.Cantidad);
        Assert.Equal(EstadoOrdenProduccion.Borrador, orden.Estado);
        Assert.NotEqual(orden, new OrdenProduccion("Axia", "Acero", 20));
    }
    [Fact]
    public void No_se_crean_ordenes_sin_cliente_o_material()
    {
        Assert.Throws<ReglaProduccionException>(() => new OrdenProduccion(" ", "Acero", 20));
        Assert.Throws<ReglaProduccionException>(() => new OrdenProduccion("Axia", " ", 20));
        Assert.Throws<ReglaProduccionException>(() => new OrdenProduccion(new string('C', 101), "Acero", 20));
        Assert.Throws<ReglaProduccionException>(() => new OrdenProduccion("Axia", new string('M', 101), 20));
        var limite = new OrdenProduccion(new string('C', 100), new string('M', 100), 20);
        Assert.Equal(100, limite.Cliente.Length);
        Assert.Equal(100, limite.Material.Length);
    }
    [Fact]
    public void Cantidad_respeta_los_limites_de_la_capacidad_didactica()
    {
        Assert.Throws<ReglaProduccionException>(() => new OrdenProduccion("Axia", "Acero", 0));
        Assert.Throws<ReglaProduccionException>(() => new OrdenProduccion("Axia", "Acero", 501));
        Assert.Equal(500, new OrdenProduccion("Axia", "Acero", 500).Cantidad);
    }
    [Fact]
    public void Planificar_y_finalizar_conserva_la_identidad()
    {
        var orden = new OrdenProduccion("Axia", "Acero", 20);
        var id = orden.Id;
        orden.Planificar();
        Assert.Equal(EstadoOrdenProduccion.Planificada, orden.Estado);
        orden.Finalizar();
        Assert.Equal(EstadoOrdenProduccion.Finalizada, orden.Estado);
        Assert.Equal(id, orden.Id);
        Assert.Throws<ReglaProduccionException>(orden.Planificar);
        Assert.Throws<ReglaProduccionException>(orden.Finalizar);
    }
    [Fact]
    public void Finalizar_sin_planificar_rechaza_la_transicion_sin_mutar()
    {
        var orden = new OrdenProduccion("Axia", "Acero", 20);
        var error = Assert.Throws<ReglaProduccionException>(orden.Finalizar);
        Assert.Equal("estado.invalido", error.Codigo);
        Assert.Equal(EstadoOrdenProduccion.Borrador, orden.Estado);
    }
}
