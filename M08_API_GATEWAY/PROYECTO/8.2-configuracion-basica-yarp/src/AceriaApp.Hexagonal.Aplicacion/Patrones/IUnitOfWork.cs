namespace AceriaApp.Hexagonal.Aplicacion.Patrones;

public interface IUnitOfWork
{
    Task<int> CommitAsync(CancellationToken ct = default);
}
