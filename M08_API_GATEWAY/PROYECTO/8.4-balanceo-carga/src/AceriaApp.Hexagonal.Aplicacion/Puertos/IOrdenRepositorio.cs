using AceriaApp.Hexagonal.Dominio;

namespace AceriaApp.Hexagonal.Aplicacion.Puertos;

/// <summary>Puerto de salida. Aplicación no conoce EF Core ni el proveedor SQL.</summary>
public interface IOrdenRepositorio
{
    Task<IReadOnlyList<OrdenHexagonal>> ListarAsync(CancellationToken ct = default);
    Task<OrdenHexagonal?> ObtenerAsync(Guid id, CancellationToken ct = default);
    Task AgregarAsync(OrdenHexagonal orden, CancellationToken ct = default);
    Task GuardarAsync(OrdenHexagonal orden, CancellationToken ct = default);
}
