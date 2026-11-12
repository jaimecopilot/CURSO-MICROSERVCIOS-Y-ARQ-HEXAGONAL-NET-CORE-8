using AceriaApp.Hexagonal.Dominio;
namespace AceriaApp.Hexagonal.Aplicacion.Patrones;

/// <summary>Prepara cambios; la unidad de trabajo decide cuándo confirmarlos.</summary>
public interface IOrdenTrabajoRepositorio
{
    Task<OrdenHexagonal?> ObtenerAsync(Guid id, CancellationToken ct = default);
    Task AgregarAsync(OrdenHexagonal orden, CancellationToken ct = default);
}
