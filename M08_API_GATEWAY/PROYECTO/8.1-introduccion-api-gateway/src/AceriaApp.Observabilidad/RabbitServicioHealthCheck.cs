using Microsoft.Extensions.Diagnostics.HealthChecks;
using RabbitMQ.Client;
namespace AceriaApp.Observabilidad;
public sealed class RabbitServicioHealthCheck(string uri) : IHealthCheck
{
    public async Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken ct = default)
    {
        ct.ThrowIfCancellationRequested();
        using var plazo = CancellationTokenSource.CreateLinkedTokenSource(ct);
        plazo.CancelAfter(TimeSpan.FromSeconds(2));
        IConnection? conexion = null;
        try
        {
            var factory = new ConnectionFactory { Uri = new Uri(uri), AutomaticRecoveryEnabled = false,
                RequestedConnectionTimeout = TimeSpan.FromSeconds(2) };
            conexion = await factory.CreateConnectionAsync(plazo.Token);
            return conexion.IsOpen ? HealthCheckResult.Healthy() : HealthCheckResult.Unhealthy("AMQP no disponible.");
        }
        catch
        {
            ct.ThrowIfCancellationRequested();
            return HealthCheckResult.Unhealthy("AMQP no disponible dentro del plazo.");
        }
        finally
        {
            if (conexion is not null)
            {
                await conexion.AbortAsync(TimeSpan.FromMilliseconds(200));
                await conexion.DisposeAsync();
            }
        }
    }
}
