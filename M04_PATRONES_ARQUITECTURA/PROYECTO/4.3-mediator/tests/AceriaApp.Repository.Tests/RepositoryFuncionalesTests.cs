using AceriaApp.Hexagonal.Aplicacion.CasosUso;
using AceriaApp.Hexagonal.Aplicacion.Puertos;
using AceriaApp.Hexagonal.Dominio;
using AceriaApp.Hexagonal.Infraestructura.Adaptadores;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Xunit;

namespace AceriaApp.Repository.Tests;

public sealed class RepositoryFuncionalesTests
{
    [Fact]
    public async Task Caso_de_uso_funciona_con_un_doble_del_puerto_sin_EF()
    {
        var puerto = new RepositorioEnMemoria();
        var caso = new OrdenesCasoUso(puerto);
        var orden = await caso.CrearAsync("  Axia  ", "Acero", 20);
        var recuperada = await caso.ObtenerAsync(orden.Id);
        Assert.Equal("Axia", recuperada!.Cliente);
        Assert.Equal(20, recuperada.Cantidad);
    }

    [Fact]
    public async Task Caso_de_uso_no_persiste_lotes_que_superan_la_capacidad()
    {
        var puerto = new RepositorioEnMemoria();
        var caso = new OrdenesCasoUso(puerto);
        await Assert.ThrowsAsync<ArgumentOutOfRangeException>(() => caso.CrearAsync("Axia", "Acero", 501));
        Assert.Empty(await caso.ListarAsync());
    }

    [Fact]
    public async Task Adaptador_relacional_cumple_contrato_crear_y_recuperar_en_otro_contexto()
    {
        await using var cn = new SqliteConnection("Data Source=:memory:");
        await cn.OpenAsync();
        var options = new DbContextOptionsBuilder<HexagonalDbContext>().UseSqlite(cn).Options;
        var orden = new OrdenHexagonal("Axia", "Acero", 20);
        await using (var db = new HexagonalDbContext(options))
        {
            await db.Database.EnsureCreatedAsync();
            await new OrdenRepositorioSqlServer(db).AgregarAsync(orden);
        }
        await using var lectura = new HexagonalDbContext(options);
        var puerto = new OrdenRepositorioSqlServer(lectura);
        var recuperada = await puerto.ObtenerAsync(orden.Id);
        Assert.Equal("Axia", recuperada!.Cliente);
        Assert.Equal(20, recuperada.Cantidad);
        Assert.Null(await puerto.ObtenerAsync(Guid.NewGuid()));
    }

    [Fact]
    public async Task Adaptador_persiste_la_transicion_de_dominio()
    {
        await using var cn = new SqliteConnection("Data Source=:memory:");
        await cn.OpenAsync();
        var options = new DbContextOptionsBuilder<HexagonalDbContext>().UseSqlite(cn).Options;
        Guid id;
        await using (var db = new HexagonalDbContext(options))
        {
            await db.Database.EnsureCreatedAsync();
            var caso = new OrdenesCasoUso(new OrdenRepositorioSqlServer(db));
            id = (await caso.CrearAsync("Axia", "Acero", 20)).Id;
            await caso.FinalizarAsync(id);
        }
        await using var lectura = new HexagonalDbContext(options);
        Assert.Equal("Finalizada", (await new OrdenRepositorioSqlServer(lectura).ObtenerAsync(id))!.Estado);
    }

    private sealed class RepositorioEnMemoria : IOrdenRepositorio
    {
        private readonly Dictionary<Guid, OrdenHexagonal> ordenes = new();
        public Task<IReadOnlyList<OrdenHexagonal>> ListarAsync(CancellationToken ct = default) =>
            Task.FromResult<IReadOnlyList<OrdenHexagonal>>(ordenes.Values.ToList());
        public Task<OrdenHexagonal?> ObtenerAsync(Guid id, CancellationToken ct = default) =>
            Task.FromResult(ordenes.GetValueOrDefault(id));
        public Task AgregarAsync(OrdenHexagonal orden, CancellationToken ct = default)
        { ordenes.Add(orden.Id, orden); return Task.CompletedTask; }
        public Task GuardarAsync(OrdenHexagonal orden, CancellationToken ct = default)
        { ordenes[orden.Id] = orden; return Task.CompletedTask; }
    }
}
