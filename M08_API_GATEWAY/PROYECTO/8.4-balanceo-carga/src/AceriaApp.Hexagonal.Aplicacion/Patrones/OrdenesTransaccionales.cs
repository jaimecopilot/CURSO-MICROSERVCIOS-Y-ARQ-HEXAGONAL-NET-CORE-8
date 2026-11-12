using AceriaApp.Hexagonal.Dominio;
namespace AceriaApp.Hexagonal.Aplicacion.Patrones;

public sealed class OrdenesTransaccionales(IOrdenTrabajoRepositorio repositorio, IUnitOfWork trabajo)
{
    public async Task<OrdenHexagonal> CrearAsync(string cliente, string material, int cantidad, CancellationToken ct = default)
    {
        if (cantidad > 500) throw new ArgumentOutOfRangeException(nameof(cantidad), "Capacidad máxima: 500.");
        var orden = new OrdenHexagonal(cliente, material, cantidad);
        await repositorio.AgregarAsync(orden, ct);
        await trabajo.CommitAsync(ct);
        return orden;
    }
    public Task<OrdenHexagonal?> ObtenerAsync(Guid id, CancellationToken ct = default) =>
        repositorio.ObtenerAsync(id, ct);
}
