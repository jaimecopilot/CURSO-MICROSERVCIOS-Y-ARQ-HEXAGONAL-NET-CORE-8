using AceriaApp.Comunicacion.Aplicacion;
using AceriaApp.Comunicacion.Contratos;
using Xunit;
namespace AceriaApp.Decisiones.Tests;
public class FlujoHibridoTests
{
    private sealed class Planificador : IPlanificadorIntegrado
    {
        public IReadOnlyList<LineaPlanificadaV1>? Lineas = new[]{new LineaPlanificadaV1("Acero",20)};
        public int Escrituras;
        public Task<IReadOnlyList<LineaPlanificadaV1>?> ObtenerLineasAsync(Guid id,CancellationToken ct)=>Task.FromResult(Lineas);
        public Task<EstadoPlanificacion> PlanificarAsync(Guid id,CancellationToken ct) { Escrituras++; return Task.FromResult(EstadoPlanificacion.Aceptada); }
    }
    private sealed class Inventario(MaterialDto? valor,bool fallo=false) : IClienteInventario
    { public Task<MaterialDto?> ObtenerAsync(string material,CancellationToken ct)=>fallo?throw new InventarioNoDisponibleException("No responde"):Task.FromResult(valor); }
    [Fact, Trait("Tipo","Unidad")]
    public async Task Disponibilidad_suficiente_delega_planificacion()
    {var p=new Planificador();Assert.Equal(EstadoPlanificacion.Aceptada,await new FlujoPlanificacion(p,new Inventario(new("Acero",100))).EjecutarAsync(Guid.NewGuid(),default));Assert.Equal(1,p.Escrituras);}
    [Fact, Trait("Tipo","Unidad")]
    public async Task Stock_insuficiente_no_escribe_outbox()
    {var p=new Planificador();Assert.Equal(EstadoPlanificacion.SinDisponibilidad,await new FlujoPlanificacion(p,new Inventario(new("Acero",10))).EjecutarAsync(Guid.NewGuid(),default));Assert.Equal(0,p.Escrituras);}
    [Fact, Trait("Tipo","Unidad")]
    public async Task Material_ausente_no_escribe_outbox()
    {var p=new Planificador();Assert.Equal(EstadoPlanificacion.SinDisponibilidad,await new FlujoPlanificacion(p,new Inventario(null)).EjecutarAsync(Guid.NewGuid(),default));Assert.Equal(0,p.Escrituras);}
    [Fact, Trait("Tipo","Unidad")]
    public async Task Fallo_remoto_se_propaga_sin_escribir()
    {var p=new Planificador();await Assert.ThrowsAsync<InventarioNoDisponibleException>(()=>new FlujoPlanificacion(p,new Inventario(null,true)).EjecutarAsync(Guid.NewGuid(),default));Assert.Equal(0,p.Escrituras);}
    [Fact, Trait("Tipo","Unidad")]
    public async Task Orden_inexistente_no_consulta_servicio_remoto()
    {var p=new Planificador{Lineas=null};Assert.Equal(EstadoPlanificacion.NoExiste,await new FlujoPlanificacion(p,new Inventario(null,true)).EjecutarAsync(Guid.NewGuid(),default));Assert.Equal(0,p.Escrituras);}
    [Fact, Trait("Tipo","Unidad")]
    public async Task Agrupa_lineas_del_mismo_material_antes_de_comparar_stock()
    {var p=new Planificador{Lineas=new[]{new LineaPlanificadaV1("Acero",50),new LineaPlanificadaV1("ACERO",50)}};Assert.Equal(EstadoPlanificacion.SinDisponibilidad,await new FlujoPlanificacion(p,new Inventario(new("Acero",80))).EjecutarAsync(Guid.NewGuid(),default));Assert.Equal(0,p.Escrituras);}
    [Fact, Trait("Tipo","Unidad")]
    public async Task Cancelacion_no_produce_planificacion()
    {var p=new Planificador();using var ct=new CancellationTokenSource();ct.Cancel();await Assert.ThrowsAnyAsync<OperationCanceledException>(()=>new FlujoPlanificacion(p,new Inventario(new("Acero",100))).EjecutarAsync(Guid.NewGuid(),ct.Token));Assert.Equal(0,p.Escrituras);}
}
