using System.Security.Cryptography;
using System.Text.Json;
using AceriaApp.Comunicacion.Contratos;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;
namespace AceriaApp.Inventario.Api;
public sealed class ReceptorPlanificacion(InventarioDbContext db)
{
    public async Task<bool> ProcesarAsync(OrdenPlanificadaV1 evento, CancellationToken ct)
    {
        evento.Validar();
        var huella = Convert.ToHexString(SHA256.HashData(JsonSerializer.SerializeToUtf8Bytes(evento)));
        var previo = await db.Planificaciones.AsNoTracking().SingleOrDefaultAsync(x => x.EventoId == evento.EventoId, ct);
        if (previo is not null) return Comparar(previo.HuellaContenido, huella);
        db.Planificaciones.Add(new PlanificacionRecibida { EventoId = evento.EventoId, OrdenId = evento.OrdenId,
            CantidadTotal = evento.Lineas.Sum(x => x.Cantidad), HuellaContenido = huella, RecibidoEnUtc = DateTimeOffset.UtcNow });
        try { await db.SaveChangesAsync(ct); return true; }
        catch (DbUpdateException ex) when (ex.InnerException is SqlException sql && (sql.Number == 2601 || sql.Number == 2627))
        {
            db.ChangeTracker.Clear();
            var guardado = await db.Planificaciones.AsNoTracking().SingleOrDefaultAsync(x => x.EventoId == evento.EventoId, ct);
            if (guardado is null) throw new InvalidDataException("La orden ya tiene otro evento de planificación.", ex);
            return Comparar(guardado.HuellaContenido, huella);
        }
    }
    private static bool Comparar(string anterior, string nueva)
    {
        if (anterior != nueva) throw new InvalidDataException("EventoId reutilizado con contenido diferente.");
        return false;
    }
}
