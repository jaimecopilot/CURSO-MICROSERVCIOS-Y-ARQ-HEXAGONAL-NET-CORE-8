using System.Text.Json;
using AceriaApp.Produccion.Aplicacion;
using AceriaApp.Comunicacion.Aplicacion;
using AceriaApp.Comunicacion.Contratos;
using AceriaApp.Comunicacion.Infraestructura;
using AceriaApp.Inventario.Api;
using AceriaApp.Produccion.Dominio;
using AceriaApp.Produccion.Infraestructura;
using AceriaApp.PruebasSqlServer;
using Microsoft.EntityFrameworkCore;
using Xunit;
namespace AceriaApp.ComunicacionAsincrona.Tests;
public class OutboxInboxTests
{
    private static ProduccionDbContext Produccion(BaseSqlServer bd) => new(new DbContextOptionsBuilder<ProduccionDbContext>().UseSqlServer(bd.ConnectionString).Options);
    private static InventarioDbContext Inventario(BaseSqlServer bd) => new(new DbContextOptionsBuilder<InventarioDbContext>().UseSqlServer(bd.ConnectionString).Options);
    private static OrdenPlanificadaV1 Evento() => new(Guid.NewGuid(),Guid.NewGuid(),DateTimeOffset.UtcNow,new[]{new LineaPlanificadaV1("Acero",20)});
    [Fact]
    public async Task Planificar_guarda_estado_y_outbox_en_SQLServer()
    {
        await using var bd=BaseSqlServer.Crear(); await using var db=Produccion(bd); await db.Database.EnsureCreatedAsync();
        var o=new OrdenProduccion("Axia","Acero",20);db.Ordenes.Add(o);await db.SaveChangesAsync();
        var r=await new PlanificadorIntegrado(db).PlanificarAsync(o.Id,default);Assert.Equal(EstadoPlanificacion.Aceptada,r);
        await using var leer=Produccion(bd);Assert.Equal(EstadoOrdenProduccion.Planificada,(await leer.Ordenes.SingleAsync()).Estado);
        Assert.Single(await leer.MensajesSalida.ToListAsync());Assert.Equal("Microsoft.EntityFrameworkCore.SqlServer",leer.Database.ProviderName);
    }
    [Fact]
    public async Task Segunda_planificacion_no_crea_otro_evento()
    {
        await using var bd=BaseSqlServer.Crear();await using var db=Produccion(bd);await db.Database.EnsureCreatedAsync();
        var o=new OrdenProduccion("Axia","Acero",20);db.Ordenes.Add(o);await db.SaveChangesAsync();var p=new PlanificadorIntegrado(db);
        await p.PlanificarAsync(o.Id,default);Assert.Equal(EstadoPlanificacion.Conflicto,await p.PlanificarAsync(o.Id,default));Assert.Equal(1,await db.MensajesSalida.CountAsync());
    }
    [Fact]
    public async Task Fallo_insertar_outbox_revierte_estado_de_orden()
    {
        await using var bd=BaseSqlServer.Crear();await using var db=Produccion(bd);await db.Database.EnsureCreatedAsync();
        var o=new OrdenProduccion("Axia","Acero",20);db.Ordenes.Add(o);await db.SaveChangesAsync();
        await db.Database.ExecuteSqlRawAsync("CREATE TRIGGER BloquearSalida ON MensajesSalida AFTER INSERT AS THROW 51001, 'Fallo inducido de outbox', 1;");
        await Assert.ThrowsAsync<DbUpdateException>(()=>new PlanificadorIntegrado(db).PlanificarAsync(o.Id,default));
        await using var leer=Produccion(bd);Assert.Equal(EstadoOrdenProduccion.Borrador,(await leer.Ordenes.SingleAsync()).Estado);Assert.Equal(0,await leer.MensajesSalida.CountAsync());
    }
    [Fact]
    public async Task Inbox_duplicado_conserva_un_unico_registro_persistido()
    {
        await using var bd=BaseSqlServer.Crear();await using var db=Inventario(bd);await db.Database.EnsureCreatedAsync();var e=Evento();
        Assert.True(await new ReceptorPlanificacion(db).ProcesarAsync(e,default));
        await using var otro=Inventario(bd);Assert.False(await new ReceptorPlanificacion(otro).ProcesarAsync(e,default));
        Assert.Equal(1,await otro.Planificaciones.CountAsync());Assert.Equal(20,(await otro.Planificaciones.SingleAsync()).CantidadTotal);
    }
    [Fact]
    public async Task Misma_identidad_con_contenido_distinto_se_rechaza()
    {
        await using var bd=BaseSqlServer.Crear();await using var db=Inventario(bd);await db.Database.EnsureCreatedAsync();var e=Evento();
        await new ReceptorPlanificacion(db).ProcesarAsync(e,default);
        await Assert.ThrowsAsync<InvalidDataException>(()=>new ReceptorPlanificacion(db).ProcesarAsync(e with { Lineas=new[]{new LineaPlanificadaV1("Acero",21)} },default));
        Assert.Equal(20,(await db.Planificaciones.SingleAsync()).CantidadTotal);
    }
    [Fact]
    public async Task Consumidores_concurrentes_guardan_un_solo_efecto()
    {
        await using var bd=BaseSqlServer.Crear();await using var a=Inventario(bd);await a.Database.EnsureCreatedAsync();await using var b=Inventario(bd);var e=Evento();
        var resultados=await Task.WhenAll(new ReceptorPlanificacion(a).ProcesarAsync(e,default),new ReceptorPlanificacion(b).ProcesarAsync(e,default));
        Assert.Single(resultados, x=>x);await using var leer=Inventario(bd);Assert.Equal(1,await leer.Planificaciones.CountAsync());
    }

    private sealed class TransportePrueba(bool falla) : ITransporteEventos
    {
        public int Publicados;
        public Task PublicarAsync(string contenido,CancellationToken ct)
        { if(falla)throw new IOException("Broker no disponible");Publicados++;return Task.CompletedTask; }
    }
    [Fact]
    public async Task Fallo_del_broker_conserva_outbox_pendiente()
    {
        await using var bd=BaseSqlServer.Crear();await using var db=Produccion(bd);await db.Database.EnsureCreatedAsync();
        var o=new OrdenProduccion("Axia","Acero",20);db.Ordenes.Add(o);await db.SaveChangesAsync();await new PlanificadorIntegrado(db).PlanificarAsync(o.Id,default);
        await Assert.ThrowsAsync<IOException>(()=>new DespachadorOutbox(db,new TransportePrueba(true)).DespacharAsync(default));
        await using var leer=Produccion(bd);Assert.Null((await leer.MensajesSalida.SingleAsync()).EnviadoEnUtc);Assert.Equal(EstadoOrdenProduccion.Planificada,(await leer.Ordenes.SingleAsync()).Estado);
    }
    [Fact]
    public async Task Confirmacion_del_broker_marca_envio_y_no_repite_pendiente()
    {
        await using var bd=BaseSqlServer.Crear();await using var db=Produccion(bd);await db.Database.EnsureCreatedAsync();
        var o=new OrdenProduccion("Axia","Acero",20);db.Ordenes.Add(o);await db.SaveChangesAsync();await new PlanificadorIntegrado(db).PlanificarAsync(o.Id,default);var transporte=new TransportePrueba(false);
        Assert.Equal(1,await new DespachadorOutbox(db,transporte).DespacharAsync(default));Assert.Equal(0,await new DespachadorOutbox(db,transporte).DespacharAsync(default));
        await using var leer=Produccion(bd);Assert.NotNull((await leer.MensajesSalida.SingleAsync()).EnviadoEnUtc);Assert.Equal(1,transporte.Publicados);
    }
    [Fact]
    public async Task Dos_contextos_con_lectura_antigua_no_planifican_dos_veces()
    {
        await using var bd=BaseSqlServer.Crear();await using var a=Produccion(bd);await a.Database.EnsureCreatedAsync();
        var o=new OrdenProduccion("Axia","Acero",20);a.Ordenes.Add(o);await a.SaveChangesAsync();await using var b=Produccion(bd);
        await b.Ordenes.Include(x=>x.Lineas).SingleAsync();Assert.Equal(EstadoPlanificacion.Aceptada,await new PlanificadorIntegrado(a).PlanificarAsync(o.Id,default));
        Assert.Equal(EstadoPlanificacion.Conflicto,await new PlanificadorIntegrado(b).PlanificarAsync(o.Id,default));await using var leer=Produccion(bd);Assert.Equal(1,await leer.MensajesSalida.CountAsync());
    }

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public async Task Anadir_linea_y_planificar_comparten_version_del_agregado(bool planificarPrimero)
    {
        await using var bd = BaseSqlServer.Crear();
        await using var a = Produccion(bd); await a.Database.EnsureCreatedAsync();
        var orden = new OrdenProduccion("Axia", "Acero", 20);
        a.Ordenes.Add(orden); await a.SaveChangesAsync();
        await using var b = Produccion(bd);
        await b.Ordenes.Include(x => x.Lineas).SingleAsync();
        var casos = new OrdenesProduccionCasosUso(new OrdenProduccionRepositorio(a), new ProduccionUnitOfWork(a));
        if (planificarPrimero)
        {
            Assert.Equal(EstadoPlanificacion.Aceptada, await new PlanificadorIntegrado(b).PlanificarAsync(orden.Id, default));
            var resultado = await casos.AgregarLineaAsync(orden.Id, "Acero", 10);
            Assert.Equal(TipoErrorProduccion.Conflicto, resultado.Error!.Tipo);
        }
        else
        {
            var resultado = await casos.AgregarLineaAsync(orden.Id, "Acero", 10);
            Assert.True(resultado.EsExito);
            Assert.Equal(EstadoPlanificacion.Conflicto, await new PlanificadorIntegrado(b).PlanificarAsync(orden.Id, default));
            await using var reintento = Produccion(bd);
            Assert.Equal(EstadoPlanificacion.Aceptada, await new PlanificadorIntegrado(reintento).PlanificarAsync(orden.Id, default));
        }
        await using var leer = Produccion(bd);
        var persistida = await leer.Ordenes.Include(x => x.Lineas).SingleAsync();
        var evento = JsonSerializer.Deserialize<OrdenPlanificadaV1>((await leer.MensajesSalida.SingleAsync()).Contenido)!;
        Assert.Equal(EstadoOrdenProduccion.Planificada, persistida.Estado);
        Assert.Equal(planificarPrimero ? 20 : 30, persistida.CantidadTotal);
        Assert.Equal(persistida.CantidadTotal, evento.Lineas.Sum(x => x.Cantidad));
    }
}
