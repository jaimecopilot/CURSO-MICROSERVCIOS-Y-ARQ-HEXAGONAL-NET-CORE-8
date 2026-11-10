using System.Data.Common;
using Microsoft.EntityFrameworkCore.Diagnostics;
using AceriaApp.Hexagonal.Aplicacion.Patrones;
using AceriaApp.Hexagonal.Dominio;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using AceriaApp.Hexagonal.Infraestructura.Patrones;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Xunit;
namespace AceriaApp.UnitOfWork.Tests;

public sealed class UnitOfWorkFuncionalesTests
{
    [Fact]
    public async Task Agregar_solo_prepara_y_commit_persiste_todo()
    {
        await using var store = await AlmacenSqlite.CrearAsync();
        await using var db = store.Contexto();
        var repo = new OrdenTrabajoRepositorio(db);
        await repo.AgregarAsync(new OrdenHexagonal("Axia", "Acero", 20));
        await repo.AgregarAsync(new OrdenHexagonal("Norte", "Chapa", 30));
        await using (var antes = store.Contexto()) Assert.Empty(await antes.Ordenes.ToListAsync());
        Assert.Equal(2, await new EfUnitOfWork(db).CommitAsync());
        await using var despues = store.Contexto();
        Assert.Equal(2, await despues.Ordenes.CountAsync());
    }

    [Fact]
    public async Task Fallo_despues_de_una_escritura_revierte_el_lote_y_control_sin_transaccion_lo_demuestra()
    {
        foreach (var transacciones in new[] { AutoTransactionBehavior.WhenNeeded, AutoTransactionBehavior.Never })
        {
            await using var store = await AlmacenSqlite.CrearAsync();
            var fallo = new FalloSegundoInsert();
            await using var db = store.Contexto(fallo);
            db.Database.AutoTransactionBehavior = transacciones;
            var repo = new OrdenTrabajoRepositorio(db);
            await repo.AgregarAsync(new OrdenHexagonal("Axia", "Acero", 20));
            await repo.AgregarAsync(new OrdenHexagonal("Norte", "Chapa", 30));
            await Assert.ThrowsAsync<DbUpdateException>(() => new EfUnitOfWork(db).CommitAsync());
            Assert.Equal(1, fallo.InsertsEjecutados);
            await using var verificacion = store.Contexto();
            // Control negativo: Never deja la primera escritura. Producción usa WhenNeeded.
            var filasEsperadas = transacciones == AutoTransactionBehavior.Never ? 1 : 0;
            Assert.Equal(filasEsperadas, await verificacion.Ordenes.CountAsync());
        }
    }

    [Fact]
    public async Task Descartar_el_ambito_sin_commit_descarta_cambios()
    {
        await using var store = await AlmacenSqlite.CrearAsync();
        await using (var db = store.Contexto())
            await new OrdenTrabajoRepositorio(db).AgregarAsync(new OrdenHexagonal("Axia", "Acero", 20));
        await using var verificacion = store.Contexto();
        Assert.Empty(await verificacion.Ordenes.ToListAsync());
    }

    [Fact]
    public async Task Caso_de_uso_confirma_y_permita_leer_desde_otro_contexto()
    {
        await using var store = await AlmacenSqlite.CrearAsync();
        Guid id;
        await using (var db = store.Contexto())
        {
            var caso = new OrdenesTransaccionales(new OrdenTrabajoRepositorio(db), new EfUnitOfWork(db));
            id = (await caso.CrearAsync("Axia", "Acero", 20)).Id;
        }
        await using var verificacion = store.Contexto();
        Assert.Equal("Axia", (await verificacion.Ordenes.SingleAsync(x => x.Id == id)).Cliente);
    }

    private sealed class FalloSegundoInsert : DbCommandInterceptor
    {
        public int InsertsEjecutados { get; private set; }
        public override ValueTask<InterceptionResult<DbDataReader>> ReaderExecutingAsync(
            DbCommand command, CommandEventData data, InterceptionResult<DbDataReader> result, CancellationToken ct = default)
        {
            if (command.CommandText.StartsWith("INSERT", StringComparison.OrdinalIgnoreCase) && InsertsEjecutados == 1)
                throw new InvalidOperationException("Fallo de prueba después de ejecutar el primer INSERT.");
            return ValueTask.FromResult(result);
        }
        public override ValueTask<DbDataReader> ReaderExecutedAsync(
            DbCommand command, CommandExecutedEventData data, DbDataReader result, CancellationToken ct = default)
        {
            if (command.CommandText.StartsWith("INSERT", StringComparison.OrdinalIgnoreCase)) InsertsEjecutados++;
            return ValueTask.FromResult(result);
        }
    }

    private sealed class AlmacenSqlite(SqliteConnection conexion) : IAsyncDisposable
    {
        public HexagonalDbContext Contexto(params IInterceptor[] interceptores) =>
            new(new DbContextOptionsBuilder<HexagonalDbContext>().UseSqlite(conexion).AddInterceptors(interceptores).Options);
        public static async Task<AlmacenSqlite> CrearAsync()
        {
            var cn = new SqliteConnection("Data Source=:memory:");
            await cn.OpenAsync();
            var store = new AlmacenSqlite(cn);
            await using var db = store.Contexto();
            await db.Database.EnsureCreatedAsync();
            return store;
        }
        public ValueTask DisposeAsync() => conexion.DisposeAsync();
    }
}
