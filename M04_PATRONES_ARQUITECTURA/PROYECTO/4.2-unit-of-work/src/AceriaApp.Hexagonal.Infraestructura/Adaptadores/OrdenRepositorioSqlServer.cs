using AceriaApp.Hexagonal.Aplicacion.Puertos;
using AceriaApp.Hexagonal.Dominio;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using Microsoft.EntityFrameworkCore;

namespace AceriaApp.Hexagonal.Infraestructura.Adaptadores;

public sealed class OrdenRepositorioSqlServer(HexagonalDbContext db) : IOrdenRepositorio
{
    public async Task<IReadOnlyList<OrdenHexagonal>> ListarAsync(CancellationToken ct = default) =>
        await db.Ordenes.AsNoTracking().OrderBy(o => o.FechaCreacion).ToListAsync(ct);

    public Task<OrdenHexagonal?> ObtenerAsync(Guid id, CancellationToken ct = default) =>
        db.Ordenes.FirstOrDefaultAsync(o => o.Id == id, ct);

    public async Task AgregarAsync(OrdenHexagonal orden, CancellationToken ct = default)
    {
        await db.Ordenes.AddAsync(orden, ct);
        await db.SaveChangesAsync(ct);
    }

    public async Task GuardarAsync(OrdenHexagonal orden, CancellationToken ct = default)
    {
        db.Ordenes.Update(orden);
        await db.SaveChangesAsync(ct);
    }
}
