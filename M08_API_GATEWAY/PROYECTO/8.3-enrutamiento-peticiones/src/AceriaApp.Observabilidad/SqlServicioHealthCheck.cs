using Microsoft.Data.SqlClient;
using Microsoft.Extensions.Diagnostics.HealthChecks;
namespace AceriaApp.Observabilidad;
public sealed class SqlServicioHealthCheck(string cadena) : IHealthCheck
{
    public async Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken ct = default)
    {
        ct.ThrowIfCancellationRequested();
        using var plazo = CancellationTokenSource.CreateLinkedTokenSource(ct);
        plazo.CancelAfter(TimeSpan.FromSeconds(2));
        try
        {
            if (string.IsNullOrWhiteSpace(cadena)) return HealthCheckResult.Unhealthy("SQL sin configurar.");
            var opciones = new SqlConnectionStringBuilder(cadena) { ConnectTimeout = 2 };
            await using var conexion = new SqlConnection(opciones.ConnectionString);
            await conexion.OpenAsync(plazo.Token);
            await using var consulta = conexion.CreateCommand();
            consulta.CommandText = "SELECT 1"; consulta.CommandTimeout = 2;
            var valor = await consulta.ExecuteScalarAsync(plazo.Token);
            return Convert.ToInt32(valor) == 1 ? HealthCheckResult.Healthy() : HealthCheckResult.Unhealthy("SQL no responde correctamente.");
        }
        catch (Exception ex) when (ex is SqlException or ArgumentException or OperationCanceledException)
        {
            ct.ThrowIfCancellationRequested();
            return HealthCheckResult.Unhealthy("SQL no disponible dentro del plazo.");
        }
    }
}
