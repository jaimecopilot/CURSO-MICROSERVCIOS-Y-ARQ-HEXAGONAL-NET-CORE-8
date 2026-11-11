using AceriaApp.Hexagonal.Aplicacion.Patrones;
using AceriaApp.Hexagonal.Dominio;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using AceriaApp.Hexagonal.Infraestructura.Patrones;
using MediatR;
using AceriaApp.PruebasSqlServer;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Xunit;
namespace AceriaApp.InyeccionDependencias.Tests;

public sealed class InyeccionFuncionalesTests
{
    [Fact]
    public async Task Ambitos_distintos_no_confirman_cambios_pendientes_del_otro()
    {
        await using var store = BaseSqlServer.Crear();
        await using var provider = CrearServicios(store.ConnectionString).BuildServiceProvider(Opciones());
        using var primero = provider.CreateScope(); using var segundo = provider.CreateScope();
        var db = primero.ServiceProvider.GetRequiredService<HexagonalDbContext>();
        Assert.Equal("Microsoft.EntityFrameworkCore.SqlServer", db.Database.ProviderName);
        await db.Database.EnsureCreatedAsync();
        var repo = primero.ServiceProvider.GetRequiredService<IOrdenTrabajoRepositorio>();
        Assert.Same(repo, primero.ServiceProvider.GetRequiredService<IOrdenTrabajoRepositorio>());
        Assert.NotSame(repo, segundo.ServiceProvider.GetRequiredService<IOrdenTrabajoRepositorio>());
        await repo.AgregarAsync(new OrdenHexagonal("Axia", "Acero", 20));
        Assert.Equal(0, await segundo.ServiceProvider.GetRequiredService<IUnitOfWork>().CommitAsync());
        Assert.Equal(1, await primero.ServiceProvider.GetRequiredService<IUnitOfWork>().CommitAsync());
        Assert.Equal(1, await segundo.ServiceProvider.GetRequiredService<HexagonalDbContext>().Ordenes.CountAsync());
    }

    [Fact]
    public async Task Extension_resuelve_flujo_completo_en_un_ambito_valido()
    {
        await using var store = BaseSqlServer.Crear();
        await using var provider = CrearServicios(store.ConnectionString).BuildServiceProvider(Opciones());
        using var scope = provider.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<HexagonalDbContext>();
        Assert.Equal("Microsoft.EntityFrameworkCore.SqlServer", db.Database.ProviderName);
        await db.Database.EnsureCreatedAsync();
        var sender = scope.ServiceProvider.GetRequiredService<ISender>();
        var creada = await sender.Send(new CrearOrdenCommand("Axia", "Acero", 20));
        Assert.True(creada.EsExito);
        var resultado = await sender.Send(new FinalizarOrdenCommand(creada.Valor.Id));
        Assert.True(resultado.EsExito); Assert.Equal("Finalizada", resultado.Valor.Estado);
        Assert.Throws<InvalidOperationException>(() => provider.GetRequiredService<IUnitOfWork>());
    }

    [Fact]
    public void ValidateScopes_detecta_singleton_que_captura_unidad_de_trabajo_scoped()
    {
        var services = CrearServicios("Server=localhost;Database=ValidacionDi;Integrated Security=True;TrustServerCertificate=True");
        services.AddSingleton<ConsumidorCautivo>(); // Registro incorrecto solo en esta prueba.
        var error = Assert.Throws<AggregateException>(() => services.BuildServiceProvider(Opciones()));
        Assert.Contains(nameof(IUnitOfWork), error.ToString());
    }

    private static ServiceProviderOptions Opciones() => new() { ValidateOnBuild = true, ValidateScopes = true };
    private static IServiceCollection CrearServicios(string connectionString)
    {
        var services = new ServiceCollection();
        services.AddDbContext<HexagonalDbContext>(o => o.UseSqlServer(connectionString));
        services.AddPatronesOrdenes();
        return services;
    }
    private sealed class ConsumidorCautivo(IUnitOfWork trabajo)
    {
        public IUnitOfWork Trabajo { get; } = trabajo;
    }
}
