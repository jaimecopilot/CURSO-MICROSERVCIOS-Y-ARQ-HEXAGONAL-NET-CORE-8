using AceriaApp.Hexagonal.Aplicacion.Patrones;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using AceriaApp.Hexagonal.Infraestructura.Patrones;
using MediatR;
using AceriaApp.PruebasSqlServer;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Xunit;
namespace AceriaApp.Mediator.Tests;

public sealed class MediatorFuncionalesTests
{
    [Fact]
    public async Task Command_y_query_ejecutan_el_caso_de_uso_y_devuelven_datos_persistidos()
    {
        await using var fixture = await Entorno.CrearAsync();
        using var scope = fixture.Services.CreateScope();
        var sender = scope.ServiceProvider.GetRequiredService<ISender>();
        await sender.Send(new CrearOrdenCommand("Axia", "Acero", 20));
        await using var db = fixture.Contexto();
        var id = (await db.Ordenes.SingleAsync()).Id;
        var recuperada = await sender.Send(new ObtenerOrdenQuery(id));
        Assert.Equal("Axia", recuperada!.Cliente);
        Assert.Equal(20, recuperada.Cantidad);
    }

    [Fact]
    public async Task Pipeline_registra_inicio_y_fin_sin_datos_de_cliente()
    {
        await using var fixture = await Entorno.CrearAsync();
        using var scope = fixture.Services.CreateScope();
        await scope.ServiceProvider.GetRequiredService<ISender>()
            .Send(new CrearOrdenCommand("Cliente confidencial", "Acero", 20));
        Assert.Contains(fixture.Logs.Mensajes, m => m.Contains("Inicio CrearOrdenCommand"));
        Assert.Contains(fixture.Logs.Mensajes, m => m.Contains("Fin CrearOrdenCommand"));
        Assert.DoesNotContain(fixture.Logs.Mensajes, m => m.Contains("Cliente confidencial"));
    }

    [Fact]
    public async Task Cancelacion_del_command_no_persiste_la_orden()
    {
        await using var fixture = await Entorno.CrearAsync();
        using var scope = fixture.Services.CreateScope();
        using var cancelacion = new CancellationTokenSource();
        cancelacion.Cancel();
        await Assert.ThrowsAnyAsync<OperationCanceledException>(() => scope.ServiceProvider
            .GetRequiredService<ISender>().Send(new CrearOrdenCommand("Axia", "Acero", 20), cancelacion.Token));
        await using var db = fixture.Contexto();
        Assert.Empty(await db.Ordenes.ToListAsync());
    }

    private sealed class Entorno(BaseSqlServer store, ServiceProvider services, RegistroLogs logs) : IAsyncDisposable
    {
        public ServiceProvider Services => services;
        public RegistroLogs Logs => logs;
        public HexagonalDbContext Contexto() => new(new DbContextOptionsBuilder<HexagonalDbContext>().UseSqlServer(store.ConnectionString).Options);
        public static async Task<Entorno> CrearAsync()
        {
            var store = BaseSqlServer.Crear();
            var logs = new RegistroLogs();
            var services = new ServiceCollection();
            services.AddLogging(builder => builder.AddProvider(logs));
            services.AddDbContext<HexagonalDbContext>(o => o.UseSqlServer(store.ConnectionString));
            services.AddScoped<IOrdenTrabajoRepositorio, OrdenTrabajoRepositorio>();
            services.AddScoped<IUnitOfWork, EfUnitOfWork>();
            services.AddScoped<OrdenesTransaccionales>();
            services.AddMediatR(cfg => {
                cfg.RegisterServicesFromAssemblyContaining<CrearOrdenCommand>();
                cfg.Lifetime = ServiceLifetime.Scoped;
                cfg.AddOpenBehavior(typeof(LoggingBehavior<,>));
            });
            var fixture = new Entorno(store, services.BuildServiceProvider(new ServiceProviderOptions { ValidateScopes = true }), logs);
            try
            {
                await using var db = fixture.Contexto();
                Assert.Equal("Microsoft.EntityFrameworkCore.SqlServer", db.Database.ProviderName);
                await db.Database.EnsureCreatedAsync();
            }
            catch { await fixture.DisposeAsync(); throw; }
            return fixture;
        }
        public async ValueTask DisposeAsync() { await services.DisposeAsync(); await store.DisposeAsync(); }
    }

    private sealed class RegistroLogs : ILoggerProvider
    {
        public List<string> Mensajes { get; } = new();
        public ILogger CreateLogger(string name) => new Captura(Mensajes);
        public void Dispose() { }
        private sealed class Captura(List<string> mensajes) : ILogger
        {
            public IDisposable? BeginScope<TState>(TState state) where TState : notnull => null;
            public bool IsEnabled(LogLevel level) => true;
            public void Log<TState>(LogLevel level, EventId id, TState state, Exception? error, Func<TState, Exception?, string> formatter) =>
                mensajes.Add(formatter(state, error));
        }
    }
}
