using AceriaApp.Api.Datos;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;

namespace AceriaApp.Api.Tests;

public sealed class HexagonalFactory : WebApplicationFactory<Program>
{
    private readonly string _db = "hex-test-" + Guid.NewGuid();
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Development");
        builder.UseSetting("SkipDatabaseInitialization", "true");
        builder.ConfigureTestServices(services =>
        {
            services.RemoveAll<DbContextOptions<AceriaDbContext>>();
            services.AddDbContext<AceriaDbContext>(o => o.UseInMemoryDatabase(_db + "-legacy"));
            services.RemoveAll<DbContextOptions<HexagonalDbContext>>();
            services.AddDbContext<HexagonalDbContext>(o => o.UseInMemoryDatabase(_db + "-hex"));
        });
    }
}
