using AceriaApp.Api.Datos;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using AceriaApp.PruebasSqlServer;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Microsoft.Extensions.Hosting;

namespace AceriaApp.Api.Tests;

public sealed class HexagonalFactory : WebApplicationFactory<Program>
{
    private readonly BaseSqlServer _legacy = BaseSqlServer.Crear();
    private readonly BaseSqlServer _hexagonal;
    public HexagonalFactory()
    {
        try { _hexagonal = BaseSqlServer.Crear(); }
        catch { _legacy.Dispose(); throw; }
    }
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Development");
        builder.UseSetting("SkipDatabaseInitialization", "true");
        builder.ConfigureTestServices(services =>
        {
            services.RemoveAll<DbContextOptions<AceriaDbContext>>();
            services.AddDbContext<AceriaDbContext>(o => o.UseSqlServer(_legacy.ConnectionString));
            services.RemoveAll<DbContextOptions<HexagonalDbContext>>();
            services.AddDbContext<HexagonalDbContext>(o => o.UseSqlServer(_hexagonal.ConnectionString));
        });
    }
    protected override IHost CreateHost(IHostBuilder builder)
    {
        var host = base.CreateHost(builder);
        using var scope = host.Services.CreateScope();
        // Cada modelo crea sus tablas en una base distinta del mismo motor SQL Server.
        scope.ServiceProvider.GetRequiredService<AceriaDbContext>().Database.EnsureCreated();
        scope.ServiceProvider.GetRequiredService<HexagonalDbContext>().Database.EnsureCreated();
        return host;
    }
    protected override void Dispose(bool disposing)
    {
        try { base.Dispose(disposing); }
        finally
        {
            if (disposing)
            {
                try { _hexagonal.Dispose(); }
                finally { _legacy.Dispose(); }
            }
        }
    }
    public override async ValueTask DisposeAsync()
    {
        try { await base.DisposeAsync(); }
        finally
        {
            try { await _hexagonal.DisposeAsync(); }
            finally { await _legacy.DisposeAsync(); }
        }
    }
}
