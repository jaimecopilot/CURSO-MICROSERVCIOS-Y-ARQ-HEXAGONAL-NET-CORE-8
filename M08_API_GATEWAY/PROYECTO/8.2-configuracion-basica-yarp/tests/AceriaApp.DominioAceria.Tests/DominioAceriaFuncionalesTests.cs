using System.Net;
using System.Net.Http.Json;
using AceriaApp.Produccion.Dominio;
using AceriaApp.Produccion.Aplicacion;
using AceriaApp.Produccion.Infraestructura;
using AceriaApp.PruebasProduccion;
using Microsoft.EntityFrameworkCore;
using Xunit;
namespace AceriaApp.DominioAceria.Tests;
public sealed class DominioAceriaFuncionalesTests
{
    private const string Ruta = "/api/v1/produccion/ordenes";
    private static async Task<string> Crear(HttpClient client, int cantidad = 200)
    {
        var response = await client.PostAsJsonAsync(Ruta, new { Cliente = "Axia", Material = "Acero", Cantidad = cantidad });
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        return response.Headers.Location!.ToString();
    }
    [Fact]
    public async Task Flujo_de_aceria_crea_lineas_planifica_finaliza_y_consulta_el_agregado()
    {
        using var factory = new ProduccionApiFactory(); using var client = factory.CreateClient();
        var ruta = await Crear(client);
        var agregado = await client.PostAsJsonAsync(ruta + "/lineas", new { Material = "Acero inoxidable", Cantidad = 100 });
        Assert.Equal(HttpStatusCode.OK, agregado.StatusCode);
        var antes = (await agregado.Content.ReadFromJsonAsync<OrdenProduccionDto>())!;
        Assert.Equal(300, antes.CantidadTotal);
        Assert.Equal(2, antes.Lineas.Count);
        Assert.Equal(HttpStatusCode.OK, (await client.PostAsync(ruta + "/planificar", null)).StatusCode);
        Assert.Equal(HttpStatusCode.OK, (await client.PostAsync(ruta + "/finalizar", null)).StatusCode);
        var dto = (await client.GetFromJsonAsync<OrdenProduccionDto>(ruta))!;
        Assert.Equal("Finalizada", dto.Estado);
        Assert.Equal(300, dto.CantidadTotal);
        Assert.Equal(antes.Lineas.Select(x => x.Id).OrderBy(x => x), dto.Lineas.Select(x => x.Id).OrderBy(x => x));
        await using var db = factory.NuevoContexto();
        var persistida = await db.Ordenes.Include(o => o.Lineas).SingleAsync();
        Assert.Equal(EstadoOrdenProduccion.Finalizada, persistida.Estado);
        Assert.Equal(2, persistida.Lineas.Count);
        Assert.Equal(300, persistida.CantidadTotal);
    }
    [Fact]
    public async Task Total_excesivo_devuelve_400_y_un_intento_valido_posterior_sigue_funcionando()
    {
        using var factory = new ProduccionApiFactory(); using var client = factory.CreateClient();
        var ruta = await Crear(client, 300);
        var rechazo = await client.PostAsJsonAsync(ruta + "/lineas", new { Material = "Inoxidable", Cantidad = 201 });
        Assert.Equal(HttpStatusCode.BadRequest, rechazo.StatusCode);
        Assert.Contains("capacidad.excedida", await rechazo.Content.ReadAsStringAsync());
        await using (var control = factory.NuevoContexto())
        {
            var orden = await control.Ordenes.Include(o => o.Lineas).SingleAsync();
            Assert.Single(orden.Lineas);
            Assert.Equal(300, orden.CantidadTotal);
        }
        Assert.Equal(HttpStatusCode.OK, (await client.PostAsJsonAsync(ruta + "/lineas", new { Material = "Inoxidable", Cantidad = 200 })).StatusCode);
        Assert.Equal(500, (await client.GetFromJsonAsync<OrdenProduccionDto>(ruta))!.CantidadTotal);
    }
    [Fact]
    public async Task Lineas_invalidas_no_llegan_a_la_base_de_datos()
    {
        using var factory = new ProduccionApiFactory(); using var client = factory.CreateClient();
        var ruta = await Crear(client, 20);
        var casos = new[] { (" ", 1), (new string('M', 101), 1), ((string)null!, 1), ("Acero", 0), ("Acero", 501) };
        foreach (var (material, cantidad) in casos)
        {
            var respuesta = await client.PostAsJsonAsync(ruta + "/lineas", new { Material = material, Cantidad = cantidad });
            Assert.Equal(HttpStatusCode.BadRequest, respuesta.StatusCode);
        }
        await using var db = factory.NuevoContexto();
        var orden = await db.Ordenes.Include(o => o.Lineas).SingleAsync();
        Assert.Single(orden.Lineas);
        Assert.Equal(20, orden.CantidadTotal);
    }
    [Fact]
    public async Task Planificar_cierra_la_edicion_y_finalizar_no_vuelve_a_abrirla()
    {
        using var factory = new ProduccionApiFactory(); using var client = factory.CreateClient();
        var ruta = await Crear(client, 20);
        Assert.Equal(HttpStatusCode.OK, (await client.PostAsync(ruta + "/planificar", null)).StatusCode);
        foreach (var finalizar in new[] { false, true })
        {
            if (finalizar) Assert.Equal(HttpStatusCode.OK, (await client.PostAsync(ruta + "/finalizar", null)).StatusCode);
            var rechazo = await client.PostAsJsonAsync(ruta + "/lineas", new { Material = "Inoxidable", Cantidad = 1 });
            Assert.Equal(HttpStatusCode.Conflict, rechazo.StatusCode);
            Assert.Contains("estado.invalido", await rechazo.Content.ReadAsStringAsync());
        }
        await using var db = factory.NuevoContexto();
        var orden = await db.Ordenes.Include(o => o.Lineas).SingleAsync();
        Assert.Equal(EstadoOrdenProduccion.Finalizada, orden.Estado);
        Assert.Single(orden.Lineas);
    }
    [Fact]
    public async Task Agregar_linea_a_orden_ausente_devuelve_404_sin_crear_otra_orden()
    {
        using var factory = new ProduccionApiFactory(); using var client = factory.CreateClient();
        var respuesta = await client.PostAsJsonAsync($"{Ruta}/{Guid.NewGuid()}/lineas", new { Material = "Acero", Cantidad = 1 });
        Assert.Equal(HttpStatusCode.NotFound, respuesta.StatusCode);
        Assert.Contains("orden.ausente", await respuesta.Content.ReadAsStringAsync());
        await using var db = factory.NuevoContexto();
        Assert.Equal(0, await db.Ordenes.CountAsync());
    }
    [Fact]
    public async Task Cada_orden_es_un_limite_de_capacidad_independiente()
    {
        using var factory = new ProduccionApiFactory(); using var client = factory.CreateClient();
        var uno = await Crear(client, 300);
        var dos = await Crear(client, 300);
        foreach (var ruta in new[] { uno, dos })
            Assert.Equal(HttpStatusCode.OK, (await client.PostAsJsonAsync(ruta + "/lineas", new { Material = "Inoxidable", Cantidad = 200 })).StatusCode);
        var lista = (await client.GetFromJsonAsync<OrdenProduccionDto[]>(Ruta))!;
        Assert.Equal(2, lista.Length);
        Assert.All(lista, o => Assert.Equal(500, o.CantidadTotal));
        await using var db = factory.NuevoContexto();
        Assert.Equal(2, await db.Ordenes.CountAsync());
    }
    [Fact]
    public async Task Bordes_validos_se_normalizan_y_conservan_en_el_contrato_http()
    {
        using var factory = new ProduccionApiFactory(); using var client = factory.CreateClient();
        var cliente = new string('C', 100);
        var material = new string('M', 100);
        var creada = await client.PostAsJsonAsync(Ruta, new { Cliente = " " + cliente + " ", Material = " Acero ", Cantidad = 1 });
        Assert.Equal(HttpStatusCode.Created, creada.StatusCode);
        var linea = await client.PostAsJsonAsync(creada.Headers.Location + "/lineas", new { Material = " " + material + " ", Cantidad = 499 });
        Assert.Equal(HttpStatusCode.OK, linea.StatusCode);
        var dto = (await client.GetFromJsonAsync<OrdenProduccionDto>(creada.Headers.Location))!;
        Assert.Equal(cliente, dto.Cliente);
        Assert.Contains(dto.Lineas, l => l.Material == material && l.Cantidad == 499);
        Assert.Equal(500, dto.CantidadTotal);
    }
    [Fact]
    public async Task Cancelacion_de_la_escritura_se_propaga_sin_tratarla_como_regla_de_negocio()
    {
        using var factory = new ProduccionApiFactory();
        Guid id;
        await using (var preparacion = factory.NuevoContexto())
        {
            var orden = new OrdenProduccion("Axia", "Acero", 20);
            id = orden.Id;
            preparacion.Ordenes.Add(orden);
            await preparacion.SaveChangesAsync();
        }
        await using var db = factory.NuevoContexto();
        var casos = new OrdenesProduccionCasosUso(new OrdenProduccionRepositorio(db), new ProduccionUnitOfWork(db));
        using var cancelacion = new CancellationTokenSource();
        cancelacion.Cancel();
        await Assert.ThrowsAnyAsync<OperationCanceledException>(() => casos.AgregarLineaAsync(id, "Inoxidable", 10, cancelacion.Token));
        await using var control = factory.NuevoContexto();
        Assert.Single((await control.Ordenes.Include(o => o.Lineas).SingleAsync()).Lineas);
    }
}
