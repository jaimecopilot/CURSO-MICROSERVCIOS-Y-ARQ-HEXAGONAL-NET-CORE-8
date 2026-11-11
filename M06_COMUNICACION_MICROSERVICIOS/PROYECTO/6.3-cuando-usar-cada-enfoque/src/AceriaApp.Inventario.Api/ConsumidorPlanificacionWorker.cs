using System.Text.Json;
using AceriaApp.Comunicacion.Contratos;
using AceriaApp.Comunicacion.Infraestructura;
namespace AceriaApp.Inventario.Api;
public sealed class ConsumidorPlanificacionWorker(RabbitMqTransporte bus, IServiceScopeFactory scopes,
    ILogger<ConsumidorPlanificacionWorker> log) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            try
            {
                await bus.ConsumirUnoAsync(async (json, token) =>
                {
                    var evento = JsonSerializer.Deserialize<OrdenPlanificadaV1>(json)
                        ?? throw new InvalidDataException("Evento nulo.");
                    using var scope = scopes.CreateScope();
                    await scope.ServiceProvider.GetRequiredService<ReceptorPlanificacion>().ProcesarAsync(evento, token);
                }, ct);
            }
            catch (OperationCanceledException) when (ct.IsCancellationRequested) { break; }
            catch (Exception ex) { log.LogWarning(ex, "La entrega no se confirma; se reintentará."); }
            try { await Task.Delay(TimeSpan.FromMilliseconds(250), ct); }
            catch (OperationCanceledException) when (ct.IsCancellationRequested) { break; }
        }
    }
}
