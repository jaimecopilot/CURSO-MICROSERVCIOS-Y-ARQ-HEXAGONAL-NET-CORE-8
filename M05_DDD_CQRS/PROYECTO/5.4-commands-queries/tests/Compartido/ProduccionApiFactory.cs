using AceriaApp.Produccion.Infraestructura;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
namespace AceriaApp.PruebasProduccion;

// Una conexión abierta mantiene viva la base SQLite relacional de cada prueba.
public sealed class ProduccionApiFactory : WebApplicationFactory<Program>
{
    private readonly SqliteConnection conexion = new("Data Source=:memory:");
    public ProduccionApiFactory()
    {
        conexion.Open();
        using var db = NuevoContexto();
        db.Database.EnsureCreated();
    }
    public ProduccionDbContext NuevoContexto() => new(
        new DbContextOptionsBuilder<ProduccionDbContext>().UseSqlite(conexion).Options);
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Development");
        builder.UseSetting("SkipDatabaseInitialization", "true");
        builder.ConfigureTestServices(services =>
        {
            services.RemoveAll<DbContextOptions<ProduccionDbContext>>();
            services.AddDbContext<ProduccionDbContext>(o => o.UseSqlite(conexion));
        });
    }
    protected override void Dispose(bool disposing)
    { base.Dispose(disposing); if (disposing) conexion.Dispose(); }
}
