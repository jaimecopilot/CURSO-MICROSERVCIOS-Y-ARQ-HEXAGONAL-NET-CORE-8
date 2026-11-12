using System.Net;
using System.Net.Http.Json;
using AceriaApp.Produccion.Dominio;
using AceriaApp.Produccion.Aplicacion;
using AceriaApp.Produccion.Infraestructura;
using AceriaApp.PruebasProduccion;
using Microsoft.EntityFrameworkCore;
using Xunit;
namespace AceriaApp.CasosDeUso.Tests;
public sealed class CasosDeUsoFuncionalesTests
{
    private static OrdenesProduccionCasosUso Casos(ProduccionDbContext db) =>
        new(new OrdenProduccionRepositorio(db), new ProduccionUnitOfWork(db));

    [Fact]
    public async Task Repositorio_no_guarda_hasta_el_commit_y_rehidrata_el_agregado()
    {
        using var factory = new ProduccionApiFactory();
        await using var escritura = factory.NuevoContexto();
        var orden = new OrdenProduccion("Axia", "Acero", 20);
        await new OrdenProduccionRepositorio(escritura).AgregarAsync(orden);
        await using (var antes = factory.NuevoContexto())
            Assert.Equal(0, await antes.Ordenes.CountAsync());
        await new ProduccionUnitOfWork(escritura).CommitAsync();
        await using var despues = factory.NuevoContexto();
        var leida = await new OrdenProduccionRepositorio(despues).ObtenerAsync(orden.Id);
        Assert.Equal(orden, leida);
        Assert.NotSame(orden, leida);
        Assert.Equal(orden.Lineas[0].Id, Assert.Single(leida!.Lineas).Id);
        Assert.Equal(new NombreMaterial("Acero"), leida.Lineas[0].Material);
        Assert.Equal(20, leida.CantidadTotal);
    }
    [Fact]
    public async Task Casos_de_uso_confirman_cada_transicion_en_otra_unidad_de_trabajo()
    {
        using var factory = new ProduccionApiFactory();
        Guid id;
        await using (var db = factory.NuevoContexto())
            id = (await Casos(db).CrearAsync(" Axia ", " Acero ", 25)).Valor;
        await using (var db = factory.NuevoContexto())
            Assert.Equal("Planificada", (await Casos(db).PlanificarAsync(id)).Valor.Estado);
        await using (var db = factory.NuevoContexto())
            Assert.Equal("Finalizada", (await Casos(db).FinalizarAsync(id)).Valor.Estado);
        await using var lectura = factory.NuevoContexto();
        var dto = (await Casos(lectura).ObtenerAsync(id)).Valor;
        Assert.Equal("Axia", dto.Cliente);
        Assert.Equal("Finalizada", dto.Estado);
        Assert.Equal(25, dto.CantidadTotal);
    }
    [Fact]
    public async Task Errores_esperados_son_resultados_tipados_sin_escrituras_parciales()
    {
        using var factory = new ProduccionApiFactory();
        await using var db = factory.NuevoContexto();
        var caso = Casos(db);
        var invalida = await caso.CrearAsync("Axia", "Acero", 501);
        Assert.False(invalida.EsExito);
        Assert.Equal(TipoErrorProduccion.Validacion, invalida.Error.Tipo);
        Assert.Equal("cantidad.invalida", invalida.Error.Codigo);
        Assert.Equal(TipoErrorProduccion.NoEncontrado, (await caso.ObtenerAsync(Guid.NewGuid())).Error.Tipo);
        Assert.Equal(TipoErrorProduccion.NoEncontrado, (await caso.PlanificarAsync(Guid.NewGuid())).Error.Tipo);
        Assert.Empty(db.ChangeTracker.Entries());
        Assert.Equal(0, await db.Ordenes.CountAsync());
    }
    [Fact]
    public void Resultado_impide_observar_la_rama_incorrecta()
    {
        var ok = ResultadoProduccion<int>.Exito(5);
        var fallo = ResultadoProduccion<int>.Fallo(new("x", "Inválida", TipoErrorProduccion.Validacion));
        Assert.Equal(5, ok.Valor);
        Assert.Throws<InvalidOperationException>(() => ok.Error);
        Assert.Throws<InvalidOperationException>(() => fallo.Valor);
        Assert.Throws<ArgumentNullException>(() => ResultadoProduccion<string>.Exito(null!));
        Assert.Throws<ArgumentNullException>(() => ResultadoProduccion<int>.Fallo(null!));
    }
    [Fact]
    public async Task Http_crea_201_y_location_apunta_al_recurso_persistido()
    {
        using var factory = new ProduccionApiFactory(); using var client = factory.CreateClient();
        var respuesta = await client.PostAsJsonAsync("/api/v1/produccion/ordenes", new { Cliente = " Axia ", Material = " Acero ", Cantidad = 20 });
        Assert.Equal(HttpStatusCode.Created, respuesta.StatusCode);
        Assert.NotNull(respuesta.Headers.Location);
        var dto = await client.GetFromJsonAsync<OrdenProduccionDto>(respuesta.Headers.Location);
        Assert.Equal("Axia", dto!.Cliente);
        Assert.Equal("Acero", Assert.Single(dto.Lineas).Material);
        await using var lectura = factory.NuevoContexto();
        Assert.Equal(dto.Id, (await lectura.Ordenes.SingleAsync()).Id);
    }
    [Fact]
    public async Task Http_rechaza_datos_invalidos_con_400_antes_de_persistir()
    {
        using var factory = new ProduccionApiFactory(); using var client = factory.CreateClient();
        var casos = new[] { (" ", "Acero", 20), ("Axia", " ", 20), ("Axia", "Acero", 0),
            ("Axia", "Acero", 501), (new string('C', 101), "Acero", 1), ("Axia", new string('M', 101), 1), ("Axia", (string)null!, 1) };
        foreach (var (cliente, material, cantidad) in casos)
        {
            var respuesta = await client.PostAsJsonAsync("/api/v1/produccion/ordenes", new { Cliente = cliente, Material = material, Cantidad = cantidad });
            Assert.Equal(HttpStatusCode.BadRequest, respuesta.StatusCode);
        }
        await using var lectura = factory.NuevoContexto();
        Assert.Equal(0, await lectura.Ordenes.CountAsync());
    }
    [Fact]
    public async Task Http_distingue_404_y_409_sin_alterar_el_estado()
    {
        using var factory = new ProduccionApiFactory(); using var client = factory.CreateClient();
        var ausente = $"/api/v1/produccion/ordenes/{Guid.NewGuid()}";
        Assert.Equal(HttpStatusCode.NotFound, (await client.GetAsync(ausente)).StatusCode);
        Assert.Equal(HttpStatusCode.NotFound, (await client.PostAsync(ausente + "/finalizar", null)).StatusCode);
        var creada = await client.PostAsJsonAsync("/api/v1/produccion/ordenes", new { Cliente = "Axia", Material = "Acero", Cantidad = 20 });
        var conflicto = await client.PostAsync(creada.Headers.Location + "/finalizar", null);
        Assert.Equal(HttpStatusCode.Conflict, conflicto.StatusCode);
        Assert.Contains("estado.invalido", await conflicto.Content.ReadAsStringAsync());
        await using var lectura = factory.NuevoContexto();
        Assert.Equal(EstadoOrdenProduccion.Borrador, (await lectura.Ordenes.SingleAsync()).Estado);
    }
}
