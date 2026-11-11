using AceriaApp.Hexagonal.Aplicacion.Puertos;
using AceriaApp.Hexagonal.Dominio;

namespace AceriaApp.Hexagonal.Aplicacion.CasosUso;

/// <summary>Casos de uso, independientes de HTTP y del adaptador de persistencia.</summary>
public sealed class OrdenesCasoUso(IOrdenRepositorio repositorio)
{
    public Task<IReadOnlyList<OrdenHexagonal>> ListarAsync(CancellationToken ct = default) =>
        repositorio.ListarAsync(ct);

    public Task<OrdenHexagonal?> ObtenerAsync(Guid id, CancellationToken ct = default) =>
        repositorio.ObtenerAsync(id, ct);

    public async Task<OrdenHexagonal> CrearAsync(string cliente, string material, int cantidad, CancellationToken ct = default)
    {
        if (cantidad > 500) throw new ArgumentOutOfRangeException(nameof(cantidad), "Capacidad máxima: 500.");
        var orden = new OrdenHexagonal(cliente, material, cantidad);
        await repositorio.AgregarAsync(orden, ct);
        return orden;
    }

    public async Task<OrdenHexagonal?> FinalizarAsync(Guid id, CancellationToken ct = default)
    {
        var orden = await repositorio.ObtenerAsync(id, ct);
        if (orden is null) return null;
        orden.Finalizar();
        await repositorio.GuardarAsync(orden, ct);
        return orden;
    }
}
