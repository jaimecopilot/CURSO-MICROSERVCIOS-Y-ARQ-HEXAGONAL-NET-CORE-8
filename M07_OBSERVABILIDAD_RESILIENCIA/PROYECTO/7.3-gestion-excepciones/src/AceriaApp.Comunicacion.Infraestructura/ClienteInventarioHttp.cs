using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using AceriaApp.Comunicacion.Aplicacion;
using AceriaApp.Comunicacion.Contratos;
namespace AceriaApp.Comunicacion.Infraestructura;
public sealed class ClienteInventarioHttp(HttpClient http) : IClienteInventario
{
    public async Task<MaterialDto?> ObtenerAsync(string material, CancellationToken ct)
    {
        ct.ThrowIfCancellationRequested();
        if (string.IsNullOrWhiteSpace(material)) throw new ArgumentException("Material obligatorio.", nameof(material));
        try
        {
            using var respuesta = await http.GetAsync("api/v1/materiales/" + Uri.EscapeDataString(material), ct);
            if (respuesta.StatusCode == HttpStatusCode.NotFound) return null;
            respuesta.EnsureSuccessStatusCode();
            var dto = await respuesta.Content.ReadFromJsonAsync<MaterialDto>(cancellationToken: ct);
            if (dto is null || string.IsNullOrWhiteSpace(dto.Material) || dto.Stock < 0)
                throw new InventarioNoDisponibleException("Inventario devolvió un contrato inválido.");
            return dto;
        }
        catch (OperationCanceledException) when (ct.IsCancellationRequested) { throw; }
        catch (Exception ex) when (ex is HttpRequestException or JsonException or OperationCanceledException)
        { throw new InventarioNoDisponibleException("No se pudo consultar Inventario.", ex); }
    }
}
