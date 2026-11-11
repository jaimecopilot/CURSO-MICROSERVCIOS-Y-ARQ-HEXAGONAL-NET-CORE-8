using AceriaApp.Api.Datos;
using AceriaApp.PruebasSqlServer;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Microsoft.Extensions.Hosting;
namespace AceriaApp.Api.Tests;
// INICIO PASO 2.1.22: HTTP y SQL Server reales; base exclusiva por factoría.
public sealed class ApiFactory : WebApplicationFactory<Program>
{
    private readonly BaseSqlServer _base = BaseSqlServer.Crear();
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Development");
        builder.UseSetting("SkipDatabaseInitialization", "true");
        builder.ConfigureTestServices(services =>
        {
            services.RemoveAll<DbContextOptions<AceriaDbContext>>();
            services.AddDbContext<AceriaDbContext>(opt => opt.UseSqlServer(_base.ConnectionString));
        });
    }
    protected override IHost CreateHost(IHostBuilder builder)
    {
        var host = base.CreateHost(builder);
        using var scope = host.Services.CreateScope();
        // El esquema se crea explícitamente sobre la base SQL exclusiva de esta prueba.
        scope.ServiceProvider.GetRequiredService<AceriaDbContext>().Database.EnsureCreated();
        return host;
    }
    protected override void Dispose(bool disposing)
    {
        try { base.Dispose(disposing); }
        finally { if (disposing) _base.Dispose(); }
    }
    public override async ValueTask DisposeAsync()
    {
        try { await base.DisposeAsync(); }
        finally { await _base.DisposeAsync(); }
    }
}
