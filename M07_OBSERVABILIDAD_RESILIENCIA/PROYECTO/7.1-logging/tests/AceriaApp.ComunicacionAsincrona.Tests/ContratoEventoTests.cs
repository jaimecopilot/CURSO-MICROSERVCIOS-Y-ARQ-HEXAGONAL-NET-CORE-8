using AceriaApp.Comunicacion.Contratos;
using Xunit;
namespace AceriaApp.ComunicacionAsincrona.Tests;
public class ContratoEventoTests
{
    private static OrdenPlanificadaV1 Valido() => new(Guid.NewGuid(), Guid.NewGuid(), DateTimeOffset.UtcNow, new[] { new LineaPlanificadaV1("Acero", 20) });
    [Fact, Trait("Tipo","Unidad")]
    public void Evento_valido_preserva_identidad_y_datos() { var e=Valido(); e.Validar(); Assert.Equal(20,e.Lineas.Sum(x=>x.Cantidad)); }
    [Fact, Trait("Tipo","Unidad")]
    public void Version_desconocida_se_rechaza() { Assert.Throws<InvalidDataException>(()=>(Valido() with { Version=2 }).Validar()); }
    [Fact, Trait("Tipo","Unidad")]
    public void Identificadores_vacios_se_rechazan() { Assert.Throws<InvalidDataException>(()=>(Valido() with { EventoId=Guid.Empty }).Validar()); Assert.Throws<InvalidDataException>(()=>(Valido() with { OrdenId=Guid.Empty }).Validar()); }
    [Fact, Trait("Tipo","Unidad")]
    public void Cantidades_y_lineas_invalidas_se_rechazan() { Assert.Throws<InvalidDataException>(()=>(Valido() with { Lineas=Array.Empty<LineaPlanificadaV1>() }).Validar()); Assert.Throws<InvalidDataException>(()=>(Valido() with { Lineas=new[]{new LineaPlanificadaV1("Acero",501)} }).Validar()); }
}
