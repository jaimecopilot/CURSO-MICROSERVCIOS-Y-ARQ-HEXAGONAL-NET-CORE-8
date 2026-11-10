using AceriaApp.Hexagonal.Aplicacion.Patrones;
using AceriaApp.Hexagonal.Dominio;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using Microsoft.EntityFrameworkCore;
namespace AceriaApp.Hexagonal.Infraestructura.Patrones;

public sealed class OrdenTrabajoRepositorio(HexagonalDbContext db) : IOrdenTrabajoRepositorio
{
    public Task<OrdenHexagonal?> ObtenerAsync(Guid id, CancellationToken ct = default) =>
        db.Ordenes.FirstOrDefaultAsync(x => x.Id == id, ct);
    public async Task AgregarAsync(OrdenHexagonal orden, CancellationToken ct = default) =>
        await db.Ordenes.AddAsync(orden, ct);
}
