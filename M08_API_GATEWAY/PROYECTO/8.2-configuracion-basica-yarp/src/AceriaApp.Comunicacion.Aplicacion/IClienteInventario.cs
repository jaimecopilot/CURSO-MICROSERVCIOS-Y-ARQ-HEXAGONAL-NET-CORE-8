using AceriaApp.Comunicacion.Contratos;
namespace AceriaApp.Comunicacion.Aplicacion;
public interface IClienteInventario
{
    Task<MaterialDto?> ObtenerAsync(string material, CancellationToken ct);
}
public sealed class InventarioNoDisponibleException(string mensaje, Exception? causa = null)
    : Exception(mensaje, causa);
