using System.Text.Json;
using AceriaApp.Comunicacion.Aplicacion;
using AceriaApp.Comunicacion.Contratos;
using AceriaApp.Produccion.Dominio;
using AceriaApp.Produccion.Infraestructura;
using Microsoft.EntityFrameworkCore;
using Microsoft.Data.SqlClient;
namespace AceriaApp.Comunicacion.Infraestructura;
public sealed class PlanificadorIntegrado(ProduccionDbContext db) : IPlanificadorIntegrado
{
    public async Task<IReadOnlyList<LineaPlanificadaV1>?> ObtenerLineasAsync(Guid id, CancellationToken ct)
    {
        var orden = await db.Ordenes.AsNoTracking().Include(x => x.Lineas).SingleOrDefaultAsync(x => x.Id == id, ct);
        return orden?.Lineas.Select(x => new LineaPlanificadaV1(x.Material.Valor, x.Cantidad.Valor)).ToArray();
    }
    public async Task<EstadoPlanificacion> PlanificarAsync(Guid id, CancellationToken ct)
    {
        var orden = await db.Ordenes.Include(x => x.Lineas).SingleOrDefaultAsync(x => x.Id == id, ct);
        if (orden is null) return EstadoPlanificacion.NoExiste;
        if (orden.Estado != EstadoOrdenProduccion.Borrador) return EstadoPlanificacion.Conflicto;
        orden.Planificar();
        var evento = new OrdenPlanificadaV1(Guid.NewGuid(), orden.Id, DateTimeOffset.UtcNow,
            orden.Lineas.Select(x => new LineaPlanificadaV1(x.Material.Valor, x.Cantidad.Valor)).ToArray());
        evento.Validar();
        db.MensajesSalida.Add(new MensajeSalida { Id = evento.EventoId, OrdenId = orden.Id,
            Contenido = JsonSerializer.Serialize(evento), CreadoEnUtc = evento.OcurridoEnUtc });
        try { await db.SaveChangesAsync(ct); }
        catch (DbUpdateConcurrencyException) { db.ChangeTracker.Clear(); return EstadoPlanificacion.Conflicto; }
        catch (DbUpdateException ex) when (ex.InnerException is SqlException sql && (sql.Number == 2601 || sql.Number == 2627))
        { db.ChangeTracker.Clear(); return EstadoPlanificacion.Conflicto; }
        return EstadoPlanificacion.Aceptada;
    }
}
public sealed class DespachadorOutbox(ProduccionDbContext db, ITransporteEventos transporte)
{
    public async Task<int> DespacharAsync(CancellationToken ct)
    {
        var pendientes = await db.MensajesSalida.Where(x => x.EnviadoEnUtc == null)
            .OrderBy(x => x.CreadoEnUtc).ThenBy(x => x.Id).Take(20).ToListAsync(ct);
        foreach (var mensaje in pendientes)
        {
            await transporte.PublicarAsync(mensaje.Contenido, ct);
            mensaje.EnviadoEnUtc = DateTimeOffset.UtcNow;
            await db.SaveChangesAsync(ct);
        }
        return pendientes.Count;
    }
}
