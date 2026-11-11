using System.Net;
using System.Net.Http.Json;
using AceriaApp.Api.Hexagonal;
using AceriaApp.Hexagonal.Aplicacion.Patrones;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using AceriaApp.PruebasSqlServer;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Xunit;
namespace AceriaApp.ResultPattern.Tests;

public sealed class ResultFuncionalesTests
{
    [Fact]
    public void Factories_impiden_resultados_o_errores_incompletos()
    {
        Assert.Throws<ArgumentNullException>(() => Result<string>.Exito(null!));
        Assert.Throws<ArgumentNullException>(() => Result<string>.Fallo(null!));
        Assert.Throws<ArgumentException>(() => new Error(" ", "Detalle", TipoError.Validacion));
        Assert.Throws<ArgumentException>(() => new Error("codigo", " ", TipoError.Validacion));
        Assert.Throws<ArgumentOutOfRangeException>(() => new Error("codigo", "Detalle", (TipoError)99));
    }

    [Fact]
    public void Un_resultado_no_expone_la_rama_que_no_le_corresponde()
    {
        var exito = Result<int>.Exito(5);
        var fallo = Result<int>.Fallo(new Error("orden.ausente", "No existe.", TipoError.NoEncontrado));
        Assert.True(exito.EsExito); Assert.Equal(5, exito.Valor);
        Assert.False(fallo.EsExito); Assert.Equal(TipoError.NoEncontrado, fallo.Error.Tipo);
        Assert.Throws<InvalidOperationException>(() => exito.Error);
        Assert.Throws<InvalidOperationException>(() => fallo.Valor);
    }

    [Fact]
    public async Task Crear_devuelve_201_location_y_lectura_del_recurso_persistido()
    {
        using var factory = new PatronesFactory(); using var client = factory.CreateClient();
        var response = await client.PostAsJsonAsync("/api/v1/patrones/ordenes", new { Cliente = "Axia", Material = "Acero", Cantidad = 20 });
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
        Assert.NotNull(response.Headers.Location);
        var lectura = await client.GetAsync(response.Headers.Location);
        Assert.Equal(HttpStatusCode.OK, lectura.StatusCode);
        var dto = await lectura.Content.ReadFromJsonAsync<OrdenHexagonalDto>();
        Assert.Equal("Axia", dto!.Cliente); Assert.Equal(20, dto.Cantidad);
    }

    [Fact]
    public async Task Datos_invalidos_devuelven_400_sin_crear_ordenes()
    {
        using var factory = new PatronesFactory(); using var client = factory.CreateClient();
        var casos = new[] { (" ", 20), ("Axia", 0), ("Axia", 501), (new string('A', 101), 20) };
        foreach (var (cliente, cantidad) in casos)
        {
            var response = await client.PostAsJsonAsync("/api/v1/patrones/ordenes", new { Cliente = cliente, Material = "Acero", Cantidad = cantidad });
            Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
            Assert.Contains("orden.validacion", await response.Content.ReadAsStringAsync());
        }
        using var scope = factory.Services.CreateScope();
        Assert.Equal(0, await scope.ServiceProvider.GetRequiredService<HexagonalDbContext>().Ordenes.CountAsync());
    }

    [Fact]
    public async Task Consultar_una_orden_ausente_devuelve_404()
    {
        using var factory = new PatronesFactory(); using var client = factory.CreateClient();
        var response = await client.GetAsync($"/api/v1/patrones/ordenes/{Guid.NewGuid()}");
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
        Assert.Contains("orden.ausente", await response.Content.ReadAsStringAsync());
    }

    [Fact]
    public async Task Finalizar_una_orden_ausente_devuelve_404()
    {
        using var factory = new PatronesFactory(); using var client = factory.CreateClient();
        var response = await client.PostAsync($"/api/v1/patrones/ordenes/{Guid.NewGuid()}/finalizar", null);
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }

    [Fact]
    public async Task Finalizar_dos_veces_devuelve_409_y_conserva_la_primera_transicion()
    {
        using var factory = new PatronesFactory(); using var client = factory.CreateClient();
        var creada = await client.PostAsJsonAsync("/api/v1/patrones/ordenes", new { Cliente = "Axia", Material = "Acero", Cantidad = 20 });
        var ruta = creada.Headers.Location + "/finalizar";
        Assert.Equal(HttpStatusCode.OK, (await client.PostAsync(ruta, null)).StatusCode);
        var repetida = await client.PostAsync(ruta, null);
        Assert.Equal(HttpStatusCode.Conflict, repetida.StatusCode);
        Assert.Contains("orden.finalizada", await repetida.Content.ReadAsStringAsync());
        var dto = await client.GetFromJsonAsync<OrdenHexagonalDto>(creada.Headers.Location);
        Assert.Equal("Finalizada", dto!.Estado);
    }

    private sealed class PatronesFactory : WebApplicationFactory<Program>
    {
        private readonly BaseSqlServer store = BaseSqlServer.Crear();
        public PatronesFactory()
        {
            try
            {
                using var db = new HexagonalDbContext(new DbContextOptionsBuilder<HexagonalDbContext>().UseSqlServer(store.ConnectionString).Options);
                Assert.Equal("Microsoft.EntityFrameworkCore.SqlServer", db.Database.ProviderName);
                db.Database.EnsureCreated();
            }
            catch { store.Dispose(); throw; }
        }
        protected override void ConfigureWebHost(IWebHostBuilder builder)
        {
            builder.UseEnvironment("Development"); builder.UseSetting("SkipDatabaseInitialization", "true");
            builder.ConfigureTestServices(services => {
                services.RemoveAll<DbContextOptions<HexagonalDbContext>>();
                services.AddDbContext<HexagonalDbContext>(o => o.UseSqlServer(store.ConnectionString));
            });
        }
        protected override void Dispose(bool disposing)
        { base.Dispose(disposing); if (disposing) store.Dispose(); }
    }
}
