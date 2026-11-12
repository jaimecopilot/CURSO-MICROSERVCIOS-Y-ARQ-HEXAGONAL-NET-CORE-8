using AceriaApp.Comunicacion.Aplicacion;
using AceriaApp.Comunicacion.Contratos;
using AceriaApp.Comunicacion.Infraestructura;
using Polly.CircuitBreaker;
using Polly.Timeout;
namespace AceriaApp.Observabilidad;

public sealed class ClienteInventarioResiliente(HttpClient http) : IClienteInventario
{
    private readonly ClienteInventarioHttp cliente = new(http);

    public async Task<MaterialDto?> ObtenerAsync(string material, CancellationToken ct)
    {
        try { return await cliente.ObtenerAsync(material, ct); }
        catch (Exception ex) when (ex is BrokenCircuitException or TimeoutRejectedException)
        {
            ct.ThrowIfCancellationRequested();
            throw new InventarioNoDisponibleException("Inventario no está disponible temporalmente.", ex);
        }
    }
}
