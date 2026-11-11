using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using AceriaApp.Comunicacion.Aplicacion;
using AceriaApp.Comunicacion.Contratos;
using AceriaApp.Comunicacion.Infraestructura;
using AceriaApp.Inventario.Api;
using AceriaApp.Produccion.Dominio;
using AceriaApp.Produccion.Infraestructura;
using AceriaApp.PruebasRabbitMq;
using AceriaApp.PruebasSqlServer;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Xunit;
namespace AceriaApp.ComunicacionAsincrona.Tests;
public class RabbitMqTests
{
    [Fact]
    public async Task Broker_real_conserva_mensaje_sin_consumidor_y_lo_entrega()
    {
        await using var entorno=await RabbitPruebas.CrearAsync();
        var e=new OrdenPlanificadaV1(Guid.NewGuid(),Guid.NewGuid(),DateTimeOffset.UtcNow,new[]{new LineaPlanificadaV1("Acero",10)});
        await entorno.Bus.PublicarAsync(JsonSerializer.Serialize(e),default);
        string? contenido=null;
        Assert.True(await entorno.Bus.ConsumirUnoAsync((json,ct)=>{contenido=json;return Task.CompletedTask;},default));
        Assert.Equal(e.EventoId,JsonSerializer.Deserialize<OrdenPlanificadaV1>(contenido!)!.EventoId);
        Assert.False(await entorno.Bus.ConsumirUnoAsync((_,_)=>Task.CompletedTask,default));
    }
    [Fact]
    public async Task Fallo_tecnico_reencola_para_otro_intento()
    {
        await using var entorno=await RabbitPruebas.CrearAsync();await entorno.Bus.PublicarAsync("{}",default);
        await Assert.ThrowsAsync<IOException>(()=>entorno.Bus.ConsumirUnoAsync((_,_)=>throw new IOException("SQL temporalmente no disponible"),default));
        Assert.True(await entorno.Bus.ConsumirUnoAsync((_,_)=>Task.CompletedTask,default));
    }
    [Fact]
    public async Task Mensaje_incompatible_va_a_cola_de_errores()
    {
        await using var entorno=await RabbitPruebas.CrearAsync();await entorno.Bus.PublicarAsync("incompatible",default);
        Assert.True(await entorno.Bus.ConsumirUnoAsync((_,_)=>throw new InvalidDataException("Version incompatible"),default));
        Assert.False(await entorno.Bus.ConsumirUnoAsync((_,_)=>Task.CompletedTask,default));
        Assert.Equal(1u,await entorno.Bus.ContarErroresAsync(default));
    }

    [Fact]
    public async Task Corte_tras_publish_confirmado_republica_mismo_evento_y_SQL_aplica_un_solo_efecto()
    {
        await using var entorno = await RabbitPruebas.CrearAsync();
        await using var baseProduccion = BaseSqlServer.Crear();
        await using var baseInventario = BaseSqlServer.Crear();
        await using (var inventario = InventarioDelTest(baseInventario))
            await inventario.Database.EnsureCreatedAsync();

        Guid ordenId;
        Guid eventoId;
        string contenidoOriginal;
        await using (var preparar = ProduccionDelTest(baseProduccion))
        {
            await preparar.Database.EnsureCreatedAsync();
            var orden = new OrdenProduccion("Axia", "Acero", 20);
            preparar.Ordenes.Add(orden);
            await preparar.SaveChangesAsync();
            ordenId = orden.Id;
            Assert.Equal(EstadoPlanificacion.Aceptada,
                await new PlanificadorIntegrado(preparar).PlanificarAsync(ordenId, default));
            var salida = await preparar.MensajesSalida.AsNoTracking().SingleAsync();
            eventoId = salida.Id;
            contenidoOriginal = salida.Contenido;
            Assert.Null(salida.EnviadoEnUtc);
            await preparar.Database.ExecuteSqlRawAsync("""
                CREATE TRIGGER dbo.RechazarMarcaDeEnvio ON dbo.MensajesSalida AFTER UPDATE AS
                BEGIN
                    SET NOCOUNT ON;
                    IF UPDATE(EnviadoEnUtc)
                        THROW 51002, 'Fallo inducido despues del publish confirmado', 1;
                END;
                """);
        }

        await using (var primerIntento = ProduccionDelTest(baseProduccion))
        {
            var fallo = await Assert.ThrowsAsync<DbUpdateException>(() =>
                new DespachadorOutbox(primerIntento, entorno.Bus).DespacharAsync(default));
            Assert.Equal(51002, Assert.IsType<SqlException>(fallo.InnerException).Number);
        }
        await using (var pendiente = ProduccionDelTest(baseProduccion))
        {
            var salida = await pendiente.MensajesSalida.AsNoTracking().SingleAsync();
            Assert.Equal(eventoId, salida.Id);
            Assert.Equal(contenidoOriginal, salida.Contenido);
            Assert.Null(salida.EnviadoEnUtc);
            Assert.Equal(EstadoOrdenProduccion.Planificada,
                (await pendiente.Ordenes.AsNoTracking().SingleAsync()).Estado);
            await pendiente.Database.ExecuteSqlRawAsync("DROP TRIGGER dbo.RechazarMarcaDeEnvio;");
        }

        await using (var segundoIntento = ProduccionDelTest(baseProduccion))
            Assert.Equal(1, await new DespachadorOutbox(segundoIntento, entorno.Bus).DespacharAsync(default));
        await using (var enviado = ProduccionDelTest(baseProduccion))
        {
            var salida = await enviado.MensajesSalida.AsNoTracking().SingleAsync();
            Assert.Equal(eventoId, salida.Id);
            Assert.Equal(contenidoOriginal, salida.Contenido);
            Assert.NotNull(salida.EnviadoEnUtc);
            Assert.Equal(0, await new DespachadorOutbox(enviado, entorno.Bus).DespacharAsync(default));
        }

        var entregas = new List<OrdenPlanificadaV1>();
        var efectos = new List<bool>();
        async Task ProcesarEntrega(string contenido, CancellationToken ct)
        {
            Assert.Equal(contenidoOriginal, contenido);
            var evento = JsonSerializer.Deserialize<OrdenPlanificadaV1>(contenido)!;
            await using var inventario = InventarioDelTest(baseInventario);
            efectos.Add(await new ReceptorPlanificacion(inventario).ProcesarAsync(evento, ct));
            entregas.Add(evento);
        }
        await ConsumirEntregaAsync(entorno.Bus, ProcesarEntrega);
        await ConsumirEntregaAsync(entorno.Bus, ProcesarEntrega);
        Assert.Equal(2, entregas.Count);
        Assert.All(entregas, evento =>
        {
            Assert.Equal(eventoId, evento.EventoId);
            Assert.Equal(ordenId, evento.OrdenId);
            Assert.Equal(20, evento.Lineas.Sum(linea => linea.Cantidad));
        });
        Assert.Equal(new[] { true, false }, efectos);
        Assert.False(await entorno.Bus.ConsumirUnoAsync(ProcesarEntrega, default));
        Assert.Equal(0u, await entorno.Bus.ContarErroresAsync(default));

        await using var comprobar = InventarioDelTest(baseInventario);
        var efecto = Assert.Single(await comprobar.Planificaciones.AsNoTracking().ToListAsync());
        Assert.Equal(eventoId, efecto.EventoId);
        Assert.Equal(ordenId, efecto.OrdenId);
        Assert.Equal(20, efecto.CantidadTotal);
        var huellaEsperada = Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(contenidoOriginal)));
        Assert.Equal(huellaEsperada, efecto.HuellaContenido);
        Assert.Equal("Microsoft.EntityFrameworkCore.SqlServer", comprobar.Database.ProviderName);
    }

    private static ProduccionDbContext ProduccionDelTest(BaseSqlServer bd) => new(
        new DbContextOptionsBuilder<ProduccionDbContext>().UseSqlServer(bd.ConnectionString)
            .ReplaceService<IModelCustomizer, ModeloConDisparador>().Options);

    private static InventarioDbContext InventarioDelTest(BaseSqlServer bd) => new(
        new DbContextOptionsBuilder<InventarioDbContext>().UseSqlServer(bd.ConnectionString).Options);

    private sealed class ModeloConDisparador(ModelCustomizerDependencies dependencias)
        : ModelCustomizer(dependencias)
    {
        public override void Customize(ModelBuilder modelo, DbContext contexto)
        {
            base.Customize(modelo, contexto);
            // Permite que el trigger ejecute THROW; evita el error previo de OUTPUT con triggers.
            modelo.Entity<MensajeSalida>().ToTable("MensajesSalida", tabla => tabla.UseSqlOutputClause(false));
        }
    }

    private static async Task ConsumirEntregaAsync(RabbitMqTransporte bus,
        Func<string, CancellationToken, Task> procesar)
    {
        using var plazo = new CancellationTokenSource(TimeSpan.FromSeconds(15));
        using var sondeo = new PeriodicTimer(TimeSpan.FromMilliseconds(50));
        while (!await bus.ConsumirUnoAsync(procesar, plazo.Token))
            await sondeo.WaitForNextTickAsync(plazo.Token);
    }
}
