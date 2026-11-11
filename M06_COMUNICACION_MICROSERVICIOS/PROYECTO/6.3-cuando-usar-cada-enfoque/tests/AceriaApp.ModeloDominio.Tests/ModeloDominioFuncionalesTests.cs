using AceriaApp.Produccion.Dominio;
using Xunit;
namespace AceriaApp.ModeloDominio.Tests;
public sealed class ModeloDominioFuncionalesTests
{
    [Fact]
    public void Value_objects_tienen_igualdad_por_valor_normalizado()
    {
        var uno = new NombreMaterial(" Acero ");
        var otro = new NombreMaterial("Acero");
        Assert.Equal(uno, otro);
        Assert.Equal(uno.GetHashCode(), otro.GetHashCode());
        Assert.Single(new HashSet<NombreMaterial> { uno, otro });
        Assert.Equal(new CantidadProduccion(25), new CantidadProduccion(25));
        Assert.NotEqual(new CantidadProduccion(25), new CantidadProduccion(26));
    }
    [Fact]
    public void Value_objects_no_permiten_valores_invalidos()
    {
        Assert.Throws<ReglaProduccionException>(() => new NombreMaterial(null!));
        Assert.Throws<ReglaProduccionException>(() => new NombreMaterial(new string('A', 101)));
        Assert.Throws<ReglaProduccionException>(() => new CantidadProduccion(0));
        Assert.Throws<ReglaProduccionException>(() => new CantidadProduccion(501));
        Assert.Equal(100, new NombreMaterial(new string('A', 100)).Valor.Length);
    }
    [Fact]
    public void Lineas_con_igual_material_y_cantidad_conservan_identidades_distintas()
    {
        var orden = new OrdenProduccion("Axia", "Acero", 20);
        orden.AgregarLinea("Acero", 20);
        Assert.Equal(2, orden.Lineas.Count);
        Assert.NotEqual(orden.Lineas[0].Id, orden.Lineas[1].Id);
        Assert.NotEqual(orden.Lineas[0], orden.Lineas[1]);
        Assert.Equal(orden.Lineas[0].Material, orden.Lineas[1].Material);
    }
    [Fact]
    public void Capacidad_se_evalua_sobre_todo_el_agregado_sin_cambios_parciales()
    {
        var orden = new OrdenProduccion("Axia", "Acero", 300);
        orden.AgregarLinea("Acero inoxidable", 200);
        var error = Assert.Throws<ReglaProduccionException>(() => orden.AgregarLinea("Acero", 1));
        Assert.Equal("capacidad.excedida", error.Codigo);
        Assert.Equal(500, orden.CantidadTotal);
        Assert.Equal(2, orden.Lineas.Count);
    }
    [Fact]
    public void Coleccion_publica_no_permite_saltar_las_reglas_de_la_raiz()
    {
        var orden = new OrdenProduccion("Axia", "Acero", 20);
        var vista = Assert.IsAssignableFrom<ICollection<LineaDeOrden>>(orden.Lineas);
        Assert.True(vista.IsReadOnly);
        Assert.Throws<NotSupportedException>(vista.Clear);
        Assert.Single(orden.Lineas);
    }
    [Fact]
    public void Cambiar_cantidad_preserva_identidad_y_rechaza_total_excesivo()
    {
        var orden = new OrdenProduccion("Axia", "Acero", 200);
        orden.AgregarLinea("Acero inoxidable", 200);
        var idLinea = orden.Lineas[0].Id;
        orden.CambiarCantidadLinea(idLinea, 300);
        Assert.Equal(idLinea, orden.Lineas[0].Id);
        Assert.Equal(500, orden.CantidadTotal);
        Assert.Throws<ReglaProduccionException>(() => orden.CambiarCantidadLinea(idLinea, 301));
        Assert.Equal(300, orden.Lineas[0].Cantidad.Valor);
        Assert.Throws<ReglaProduccionException>(() => orden.CambiarCantidadLinea(Guid.NewGuid(), 1));
        Assert.Equal(500, orden.CantidadTotal);
    }
    [Fact]
    public void Una_orden_planificada_cierra_la_edicion_de_sus_lineas()
    {
        var orden = new OrdenProduccion("Axia", "Acero", 20);
        orden.Planificar();
        Assert.Throws<ReglaProduccionException>(() => orden.AgregarLinea("Acero", 10));
        Assert.Throws<ReglaProduccionException>(() => orden.CambiarCantidadLinea(orden.Lineas[0].Id, 30));
        orden.Finalizar();
        Assert.Throws<ReglaProduccionException>(() => orden.AgregarLinea("Acero", 10));
        Assert.Equal(20, orden.CantidadTotal);
    }
}
