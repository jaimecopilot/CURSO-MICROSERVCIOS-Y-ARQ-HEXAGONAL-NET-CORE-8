using AceriaApp.Produccion.Dominio;
namespace AceriaApp.Produccion.Aplicacion;
public interface IOrdenProduccionRepositorio
{
    Task<OrdenProduccion?> ObtenerAsync(Guid id, CancellationToken ct = default);
    Task AgregarAsync(OrdenProduccion orden, CancellationToken ct = default);
}
public interface IProduccionUnitOfWork
{
    Task CommitAsync(CancellationToken ct = default);
}
