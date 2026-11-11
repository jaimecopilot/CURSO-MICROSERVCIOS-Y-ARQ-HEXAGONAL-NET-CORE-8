using AceriaApp.Produccion.Aplicacion;
using AceriaApp.Produccion.Dominio;
using Microsoft.EntityFrameworkCore;
namespace AceriaApp.Produccion.Infraestructura;
public sealed class OrdenProduccionRepositorio(ProduccionDbContext db) : IOrdenProduccionRepositorio
{
    public Task<OrdenProduccion?> ObtenerAsync(Guid id, CancellationToken ct = default) =>
        db.Ordenes.Include(o => o.Lineas).SingleOrDefaultAsync(o => o.Id == id, ct);
    public async Task AgregarAsync(OrdenProduccion orden, CancellationToken ct = default) =>
        await db.Ordenes.AddAsync(orden, ct);
}
public sealed class ProduccionUnitOfWork(ProduccionDbContext db) : IProduccionUnitOfWork
{
    public async Task CommitAsync(CancellationToken ct = default)
    {
        try { await db.SaveChangesAsync(ct); }
        catch (DbUpdateConcurrencyException)
        {
            db.ChangeTracker.Clear();
            throw new ConflictoProduccionException();
        }
    }
}
