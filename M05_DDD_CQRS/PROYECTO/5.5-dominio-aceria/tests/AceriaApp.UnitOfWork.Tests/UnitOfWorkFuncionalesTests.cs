using System.Data.Common;
using Microsoft.EntityFrameworkCore.Diagnostics;
using AceriaApp.Hexagonal.Aplicacion.Patrones;
using AceriaApp.Hexagonal.Dominio;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using AceriaApp.Hexagonal.Infraestructura.Patrones;
using AceriaApp.PruebasSqlServer;
using Microsoft.EntityFrameworkCore;
using Xunit;
namespace AceriaApp.UnitOfWork.Tests;

public sealed class UnitOfWorkFuncionalesTests
{
    [Fact]
    public async Task Agregar_solo_prepara_y_commit_persiste_todo()
    {
        await using var store = BaseSqlServer.Crear();
        await using var db = Contexto(store);
        await db.Database.EnsureCreatedAsync();
        var repo = new OrdenTrabajoRepositorio(db);
        await repo.AgregarAsync(new OrdenHexagonal("Axia", "Acero", 20));
        await repo.AgregarAsync(new OrdenHexagonal("Norte", "Chapa", 30));
        await using (var antes = Contexto(store)) Assert.Empty(await antes.Ordenes.ToListAsync());
        Assert.Equal(2, await new EfUnitOfWork(db).CommitAsync());
        await using var despues = Contexto(store);
        Assert.Equal(2, await despues.Ordenes.CountAsync());
    }

    [Fact]
    public async Task Fallo_despues_de_una_escritura_revierte_el_lote_y_control_sin_transaccion_lo_demuestra()
    {
        foreach (var transacciones in new[] { AutoTransactionBehavior.WhenNeeded, AutoTransactionBehavior.Never })
        {
            await using var store = BaseSqlServer.Crear();
            var fallo = new FalloSegundoInsert();
            await using var db = Contexto(store, fallo);
            await db.Database.EnsureCreatedAsync();
            db.Database.AutoTransactionBehavior = transacciones;
            var repo = new OrdenTrabajoRepositorio(db);
            await repo.AgregarAsync(new OrdenHexagonal("Axia", "Acero", 20));
            await repo.AgregarAsync(new OrdenHexagonal("Norte", "Chapa", 30));
            await Assert.ThrowsAsync<DbUpdateException>(() => new EfUnitOfWork(db).CommitAsync());
            Assert.Equal(1, fallo.InsertsEjecutados);
            await using var verificacion = Contexto(store);
            // Control negativo: Never deja la primera escritura. Producción usa WhenNeeded.
            var filasEsperadas = transacciones == AutoTransactionBehavior.Never ? 1 : 0;
            Assert.Equal(filasEsperadas, await verificacion.Ordenes.CountAsync());
        }
    }

    [Fact]
    public async Task Descartar_el_ambito_sin_commit_descarta_cambios()
    {
        await using var store = BaseSqlServer.Crear();
        await using (var db = Contexto(store))
        {
            await db.Database.EnsureCreatedAsync();
            await new OrdenTrabajoRepositorio(db).AgregarAsync(new OrdenHexagonal("Axia", "Acero", 20));
        }
        await using var verificacion = Contexto(store);
        Assert.Empty(await verificacion.Ordenes.ToListAsync());
    }

    [Fact]
    public async Task Caso_de_uso_confirma_y_permita_leer_desde_otro_contexto()
    {
        await using var store = BaseSqlServer.Crear();
        Guid id;
        await using (var db = Contexto(store))
        {
            await db.Database.EnsureCreatedAsync();
            var caso = new OrdenesTransaccionales(new OrdenTrabajoRepositorio(db), new EfUnitOfWork(db));
            id = (await caso.CrearAsync("Axia", "Acero", 20)).Id;
        }
        await using var verificacion = Contexto(store);
        Assert.Equal("Axia", (await verificacion.Ordenes.SingleAsync(x => x.Id == id)).Cliente);
    }

    private sealed class FalloSegundoInsert : DbCommandInterceptor
    {
        public int InsertsEjecutados { get; private set; }
        public override ValueTask<InterceptionResult<DbDataReader>> ReaderExecutingAsync(
            DbCommand command, CommandEventData data, InterceptionResult<DbDataReader> result, CancellationToken ct = default)
        {
            if (command.CommandText.Contains("INSERT INTO", StringComparison.OrdinalIgnoreCase) && InsertsEjecutados == 1)
                throw new InvalidOperationException("Fallo de prueba después de ejecutar el primer INSERT.");
            return ValueTask.FromResult(result);
        }
        public override ValueTask<DbDataReader> ReaderExecutedAsync(
            DbCommand command, CommandExecutedEventData data, DbDataReader result, CancellationToken ct = default)
        {
            if (command.CommandText.Contains("INSERT INTO", StringComparison.OrdinalIgnoreCase)) InsertsEjecutados++;
            return ValueTask.FromResult(result);
        }
    }

    private static HexagonalDbContext Contexto(BaseSqlServer store, IInterceptor? fallo = null)
    {
        var options = new DbContextOptionsBuilder<HexagonalDbContext>();
        if (fallo is null) options.UseSqlServer(store.ConnectionString);
        else options.UseSqlServer(store.ConnectionString, sql => sql.MaxBatchSize(1)).AddInterceptors(fallo);
        var db = new HexagonalDbContext(options.Options);
        Assert.Equal("Microsoft.EntityFrameworkCore.SqlServer", db.Database.ProviderName);
        return db;
    }
}
