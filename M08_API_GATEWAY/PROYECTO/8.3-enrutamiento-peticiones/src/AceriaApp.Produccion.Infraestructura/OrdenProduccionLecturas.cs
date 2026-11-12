using AceriaApp.Produccion.Aplicacion;
using AceriaApp.Produccion.Dominio;
using Microsoft.EntityFrameworkCore;
namespace AceriaApp.Produccion.Infraestructura;

// CQRS sobre la misma base: SQL selecciona columnas, la aplicación recibe DTOs.
public sealed class OrdenProduccionLecturas(ProduccionDbContext db) : IOrdenProduccionLecturas
{
    public async Task<OrdenProduccionDto?> ObtenerAsync(Guid id, CancellationToken ct = default) =>
        (await ProyectarAsync(db.Ordenes.Where(o => o.Id == id), ct)).SingleOrDefault();
    public Task<IReadOnlyList<OrdenProduccionDto>> ListarAsync(CancellationToken ct = default) =>
        ProyectarAsync(db.Ordenes.OrderBy(o => o.Cliente).ThenBy(o => o.Id), ct);

    private static async Task<IReadOnlyList<OrdenProduccionDto>> ProyectarAsync(
        IQueryable<OrdenProduccion> consulta, CancellationToken ct)
    {
        // Se proyectan valores mapeados; no se materializan raíces con tracking.
        var filas = await consulta.AsNoTracking().Select(o => new
        {
            o.Id, o.Cliente, o.Estado,
            Lineas = o.Lineas.Select(l => new { l.Id, l.Material, l.Cantidad }).ToList()
        }).ToListAsync(ct);
        return filas.Select(o => new OrdenProduccionDto(o.Id, o.Cliente, o.Estado.ToString(),
            o.Lineas.Sum(l => l.Cantidad.Valor),
            o.Lineas.Select(l => new LineaProduccionDto(l.Id, l.Material.Valor, l.Cantidad.Valor)).ToList().AsReadOnly()))
            .ToList().AsReadOnly();
    }
}
