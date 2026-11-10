using AceriaApp.Hexagonal.Aplicacion.Patrones;
using AceriaApp.Hexagonal.Infraestructura.Datos;
namespace AceriaApp.Hexagonal.Infraestructura.Patrones;

/// <summary>Un SaveChanges: transacción automática para los cambios de este contexto relacional.</summary>
public sealed class EfUnitOfWork(HexagonalDbContext db) : IUnitOfWork
{
    public Task<int> CommitAsync(CancellationToken ct = default) => db.SaveChangesAsync(ct);
}
