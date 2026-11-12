using AceriaApp.Comunicacion.Infraestructura;
using Testcontainers.RabbitMq;
namespace AceriaApp.PruebasRabbitMq;
public sealed class RabbitPruebas : IAsyncDisposable
{
    private static readonly Lazy<Task<RabbitMqContainer>> Local = new(async () =>
    {
        var contenedor = new RabbitMqBuilder().WithImage("rabbitmq:4.1.5-management")
            .WithUsername("curso").WithPassword("curso-local").Build();
        await contenedor.StartAsync();return contenedor;
    });
    public RabbitMqTransporte Bus { get; }
    private RabbitPruebas(string uri) { Bus = new(new RabbitMqOpciones(uri, "prueba-" + Guid.NewGuid().ToString("N"))); }
    public static async Task<RabbitPruebas> CrearAsync()
    {
        var uri = Environment.GetEnvironmentVariable("ACERIA_TEST_RABBITMQ");
        if (string.IsNullOrWhiteSpace(uri)) uri = (await Local.Value).GetConnectionString();
        return new RabbitPruebas(uri);
    }
    public async ValueTask DisposeAsync()
    {
        try { await Bus.EliminarTopologiaAsync(default); }
        finally { await Bus.DisposeAsync(); }
    }
}
