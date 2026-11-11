using AceriaApp.Produccion.Infraestructura;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using AceriaApp.PruebasSqlServer;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
namespace AceriaApp.PruebasProduccion;

// Cada factory posee una base SQL Server aislada y la elimina al terminar.
public sealed class ProduccionApiFactory : WebApplicationFactory<Program>
{
    private readonly BaseSqlServer store = BaseSqlServer.Crear();
    public ProduccionApiFactory()
    {
        try
        {
            using var db = NuevoContexto();
            if (!db.Database.IsSqlServer()) throw new InvalidOperationException("La prueba exige SQL Server.");
            db.Database.EnsureCreated();
        }
        catch { store.Dispose(); throw; }
    }
    public ProduccionDbContext NuevoContexto() => new(
        new DbContextOptionsBuilder<ProduccionDbContext>().UseSqlServer(store.ConnectionString).Options);
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Development");
        builder.UseSetting("SkipDatabaseInitialization", "true");
        builder.ConfigureTestServices(services =>
        {
            services.RemoveAll<DbContextOptions<ProduccionDbContext>>();
            services.AddDbContext<ProduccionDbContext>(o => o.UseSqlServer(store.ConnectionString));
        });
    }
    protected override void Dispose(bool disposing)
    { base.Dispose(disposing); if (disposing) store.Dispose(); }
}
