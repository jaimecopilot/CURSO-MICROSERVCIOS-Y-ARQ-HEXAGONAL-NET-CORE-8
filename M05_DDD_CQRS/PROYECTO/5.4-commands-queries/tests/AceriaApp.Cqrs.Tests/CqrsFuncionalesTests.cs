using System.Net;
using System.Net.Http.Json;
using AceriaApp.Produccion.Dominio;
using AceriaApp.Produccion.Aplicacion;
using AceriaApp.Produccion.Infraestructura;
using AceriaApp.PruebasProduccion;
using MediatR;
using AceriaApp.PruebasSqlServer;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Diagnostics;
using Microsoft.Extensions.DependencyInjection;
using Xunit;
namespace AceriaApp.Cqrs.Tests;
public sealed class CqrsFuncionalesTests
{
    [Fact]
    public async Task Mediador_resuelve_el_command_y_confirma_una_orden_real()
    {
        using var factory = new ProduccionApiFactory();
        using var scope = factory.Services.CreateScope();
        var sender = scope.ServiceProvider.GetRequiredService<ISender>();
        var resultado = await sender.Send(new CrearOrdenProduccionCommand(" Axia ", " Acero ", 40));
        Assert.True(resultado.EsExito);
        await using var db = factory.NuevoContexto();
        var orden = await db.Ordenes.Include(o => o.Lineas).SingleAsync();
        Assert.Equal(resultado.Valor, orden.Id);
        Assert.Equal("Axia", orden.Cliente);
        Assert.Equal(40, orden.CantidadTotal);
    }
    [Fact]
    public async Task Queries_proyectan_sin_tracking_ni_commit_y_los_DTO_no_mutan_el_dominio()
    {
        await using var store = BaseSqlServer.Crear();
        var opciones = new DbContextOptionsBuilder<ProduccionDbContext>().UseSqlServer(store.ConnectionString).Options;
        Guid id;
        await using (var escritura = new ProduccionDbContext(opciones))
        {
            await escritura.Database.EnsureCreatedAsync();
            var orden = new OrdenProduccion("Axia", "Acero", 200);
            orden.AgregarLinea("Inoxidable", 100);
            id = orden.Id;
            escritura.Ordenes.Add(orden);
            await escritura.SaveChangesAsync();
        }
        var soloLectura = new DbContextOptionsBuilder<ProduccionDbContext>().UseSqlServer(store.ConnectionString)
            .AddInterceptors(new ProhibirGuardado()).Options;
        await using var db = new ProduccionDbContext(soloLectura);
        Assert.Equal("Microsoft.EntityFrameworkCore.SqlServer", db.Database.ProviderName);
        var puerto = new OrdenProduccionLecturas(db);
        var detalle = await new ObtenerOrdenProduccionHandler(puerto).Handle(new(id), default);
        var lista = await new ListarOrdenesProduccionHandler(puerto).Handle(new(), default);
        Assert.Equal(300, detalle.Valor.CantidadTotal);
        Assert.Equal(2, detalle.Valor.Lineas.Count);
        Assert.Equal(id, Assert.Single(lista).Id);
        Assert.Empty(db.ChangeTracker.Entries());
        var copia = detalle.Valor with { Cliente = "Modificado fuera del dominio" };
        Assert.NotEqual(copia.Cliente, (await puerto.ObtenerAsync(id))!.Cliente);
        await using var comprobacion = new ProduccionDbContext(opciones);
        Assert.Equal(EstadoOrdenProduccion.Borrador, (await comprobacion.Ordenes.SingleAsync()).Estado);
    }
    [Fact]
    public async Task Query_inexistente_devuelve_error_tipado_y_la_lista_vacia_es_valida()
    {
        using var factory = new ProduccionApiFactory();
        using var scope = factory.Services.CreateScope();
        var sender = scope.ServiceProvider.GetRequiredService<ISender>();
        var resultado = await sender.Send(new ObtenerOrdenProduccionQuery(Guid.NewGuid()));
        Assert.False(resultado.EsExito);
        Assert.Equal(TipoErrorProduccion.NoEncontrado, resultado.Error.Tipo);
        Assert.Empty(await sender.Send(new ListarOrdenesProduccionQuery()));
    }
    [Fact]
    public async Task Command_invalido_no_elude_las_invariantes_del_agregado()
    {
        using var factory = new ProduccionApiFactory();
        using var scope = factory.Services.CreateScope();
        var sender = scope.ServiceProvider.GetRequiredService<ISender>();
        var resultado = await sender.Send(new CrearOrdenProduccionCommand("Axia", "Acero", 501));
        Assert.Equal(TipoErrorProduccion.Validacion, resultado.Error.Tipo);
        await using var db = factory.NuevoContexto();
        Assert.Equal(0, await db.Ordenes.CountAsync());
    }
    [Fact]
    public async Task Commands_de_estado_usados_por_el_mediador_respetan_la_secuencia()
    {
        using var factory = new ProduccionApiFactory();
        using var scope = factory.Services.CreateScope();
        var sender = scope.ServiceProvider.GetRequiredService<ISender>();
        var id = (await sender.Send(new CrearOrdenProduccionCommand("Axia", "Acero", 20))).Valor;
        Assert.Equal(TipoErrorProduccion.Conflicto, (await sender.Send(new FinalizarOrdenProduccionCommand(id))).Error.Tipo);
        Assert.True((await sender.Send(new PlanificarOrdenProduccionCommand(id))).EsExito);
        Assert.True((await sender.Send(new FinalizarOrdenProduccionCommand(id))).EsExito);
        Assert.Equal(TipoErrorProduccion.Conflicto, (await sender.Send(new FinalizarOrdenProduccionCommand(id))).Error.Tipo);
        await using var db = factory.NuevoContexto();
        Assert.Equal(EstadoOrdenProduccion.Finalizada, (await db.Ordenes.SingleAsync()).Estado);
    }
    [Fact]
    public async Task Http_lista_proyecciones_de_las_ordenes_creadas()
    {
        using var factory = new ProduccionApiFactory(); using var client = factory.CreateClient();
        await client.PostAsJsonAsync("/api/v1/produccion/ordenes", new { Cliente = "Axia", Material = "Acero", Cantidad = 25 });
        var respuesta = await client.GetAsync("/api/v1/produccion/ordenes");
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        var lista = await respuesta.Content.ReadFromJsonAsync<OrdenProduccionDto[]>();
        Assert.Equal(25, Assert.Single(lista!).CantidadTotal);
        Assert.Equal("Acero", Assert.Single(lista![0].Lineas).Material);
    }
    private sealed class ProhibirGuardado : SaveChangesInterceptor
    {
        public override InterceptionResult<int> SavingChanges(DbContextEventData data, InterceptionResult<int> result) =>
            throw new InvalidOperationException("Una query no debe guardar cambios.");
        public override ValueTask<InterceptionResult<int>> SavingChangesAsync(DbContextEventData data,
            InterceptionResult<int> result, CancellationToken ct = default) =>
            throw new InvalidOperationException("Una query no debe guardar cambios.");
    }
}
