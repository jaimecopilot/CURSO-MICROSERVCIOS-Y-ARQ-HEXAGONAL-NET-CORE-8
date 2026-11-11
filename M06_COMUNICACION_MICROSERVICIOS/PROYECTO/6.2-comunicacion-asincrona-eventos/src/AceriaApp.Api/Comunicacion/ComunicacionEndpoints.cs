using AceriaApp.Comunicacion.Aplicacion;
namespace AceriaApp.Api.Comunicacion;
public static class ComunicacionEndpoints
{
    public static void MapComunicacion(this WebApplication app)
    {
        app.MapGet("/api/v1/comunicacion/materiales/{material}", async (string material, IClienteInventario inventario, CancellationToken ct) =>
        {
            try
            {
                var dto = await inventario.ObtenerAsync(material, ct);
                return dto is null ? Results.NotFound() : Results.Ok(dto);
            }
            catch (InventarioNoDisponibleException)
            { return Results.Problem(statusCode: 503, title: "Inventario no está disponible."); }
        }).WithTags("Comunicacion");
        app.MapPost("/api/v1/comunicacion/ordenes/{id:guid}/planificar", async (Guid id, IPlanificadorIntegrado planificador, CancellationToken ct) =>
        {
            var estado = await planificador.PlanificarAsync(id, ct);
            return estado switch
            {
                EstadoPlanificacion.NoExiste => Results.NotFound(),
                EstadoPlanificacion.Conflicto => Results.Problem(statusCode: 409, title: "La orden no está en borrador."),
                _ => Results.Accepted($"/api/v1/produccion/ordenes/{id}", new { ordenId = id, estado = "Planificada", propagacion = "Pendiente" })
            };
        }).WithTags("Comunicacion");
    }
}
