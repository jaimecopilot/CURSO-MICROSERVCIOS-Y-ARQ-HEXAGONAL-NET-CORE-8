using System.Text;
using System.Text.Json;
using AceriaApp.Comunicacion.Aplicacion;
using RabbitMQ.Client;
namespace AceriaApp.Comunicacion.Infraestructura;
public sealed record RabbitMqOpciones(string Uri, string Prefijo = "aceria");
public sealed class RabbitMqTransporte(RabbitMqOpciones opciones) : ITransporteEventos, IAsyncDisposable
{
    private IConnection? conexion;
    private readonly SemaphoreSlim acceso = new(1, 1);
    private string Exchange => opciones.Prefijo + ".eventos";
    private string Cola => opciones.Prefijo + ".inventario.planificada.v1";
    private const string Ruta = "orden.planificada.v1";
    private async Task<IChannel> CanalAsync(bool confirmar, CancellationToken ct)
    {
        await acceso.WaitAsync(ct);
        try
        {
            if (conexion is null || !conexion.IsOpen)
            {
                if (conexion is not null) await conexion.DisposeAsync();
                conexion = await new ConnectionFactory { Uri = new Uri(opciones.Uri),
                    AutomaticRecoveryEnabled = true, RequestedConnectionTimeout = TimeSpan.FromSeconds(5) }
                    .CreateConnectionAsync(ct);
            }
            var canal = await conexion.CreateChannelAsync(new CreateChannelOptions(confirmar, confirmar), ct);
            await canal.ExchangeDeclareAsync(Exchange, ExchangeType.Direct, durable: true, autoDelete: false, cancellationToken: ct);
            await canal.QueueDeclareAsync(Cola + ".errores", durable: true, exclusive: false, autoDelete: false, cancellationToken: ct);
            await canal.QueueDeclareAsync(Cola, durable: true, exclusive: false, autoDelete: false,
                arguments: new Dictionary<string, object?> { ["x-dead-letter-exchange"] = "", ["x-dead-letter-routing-key"] = Cola + ".errores" }, cancellationToken: ct);
            await canal.QueueBindAsync(Cola, Exchange, Ruta, cancellationToken: ct);
            return canal;
        }
        finally { acceso.Release(); }
    }
    public async Task PublicarAsync(string contenido, CancellationToken ct)
    {
        using var plazo = CancellationTokenSource.CreateLinkedTokenSource(ct);
        plazo.CancelAfter(TimeSpan.FromSeconds(10));
        await using var canal = await CanalAsync(true, plazo.Token);
        await canal.BasicPublishAsync(Exchange, Ruta, mandatory: true,
            basicProperties: new BasicProperties { Persistent = true, ContentType = "application/json", Type = "orden.planificada.v1" },
            body: Encoding.UTF8.GetBytes(contenido), cancellationToken: plazo.Token);
    }
    public async Task<bool> ConsumirUnoAsync(Func<string, CancellationToken, Task> procesar, CancellationToken ct)
    {
        await using var canal = await CanalAsync(false, ct);
        var entrega = await canal.BasicGetAsync(Cola, autoAck: false, cancellationToken: ct);
        if (entrega is null) return false;
        try
        {
            await procesar(Encoding.UTF8.GetString(entrega.Body.Span), ct);
            await canal.BasicAckAsync(entrega.DeliveryTag, multiple: false, cancellationToken: ct);
        }
        catch (Exception ex) when (ex is JsonException or InvalidDataException)
        { await canal.BasicNackAsync(entrega.DeliveryTag, multiple: false, requeue: false, cancellationToken: ct); }
        catch
        {
            // Si el canal ya se cerró, RabbitMQ vuelve a poner en cola la entrega sin confirmar.
            if (canal.IsOpen) await canal.BasicNackAsync(entrega.DeliveryTag, multiple: false, requeue: true, cancellationToken: CancellationToken.None);
            throw;
        }
        return true;
    }
    public async Task<uint> ContarErroresAsync(CancellationToken ct)
    {
        await using var canal = await CanalAsync(false, ct);
        return (await canal.QueueDeclarePassiveAsync(Cola + ".errores", ct)).MessageCount;
    }
    public async Task EliminarTopologiaAsync(CancellationToken ct)
    {
        await using var canal = await CanalAsync(false, ct);
        await canal.QueueDeleteAsync(Cola, false, false, ct);
        await canal.QueueDeleteAsync(Cola + ".errores", false, false, ct);
        await canal.ExchangeDeleteAsync(Exchange, cancellationToken: ct);
    }
    public async ValueTask DisposeAsync()
    {
        if (conexion is not null) await conexion.DisposeAsync();
        acceso.Dispose();
    }
}
