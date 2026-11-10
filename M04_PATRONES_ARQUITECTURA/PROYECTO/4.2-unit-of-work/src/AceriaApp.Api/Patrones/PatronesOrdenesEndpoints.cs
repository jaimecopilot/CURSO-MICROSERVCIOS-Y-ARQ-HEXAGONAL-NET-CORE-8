using AceriaApp.Api.Hexagonal;
using AceriaApp.Hexagonal.Aplicacion.Patrones;
namespace AceriaApp.Api.Patrones;

public static class PatronesOrdenesEndpoints
{
    public static IEndpointRouteBuilder MapPatronesOrdenes(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/v1/patrones/ordenes").WithTags("Patrones");
        group.MapGet("/{id:guid}", async (Guid id, OrdenesTransaccionales caso, CancellationToken ct) =>
        {
            var orden = await caso.ObtenerAsync(id, ct);
            return orden is null ? Results.NotFound() : Results.Ok(OrdenHexagonalDto.Desde(orden));
        }).WithName("ObtenerOrdenPatrones").Produces<OrdenHexagonalDto>(200).Produces(404);
        group.MapPost("", async (CrearOrdenHexagonalRequest body, OrdenesTransaccionales caso, CancellationToken ct) =>
        {
            if (string.IsNullOrWhiteSpace(body.Cliente) || string.IsNullOrWhiteSpace(body.Material)
                || body.Cliente.Trim().Length > 100 || body.Material.Trim().Length > 100
                || body.Cantidad <= 0 || body.Cantidad > 500)
                return Results.Problem(title: "Datos de la orden inválidos.", statusCode: 400);
            var orden = await caso.CrearAsync(body.Cliente, body.Material, body.Cantidad, ct);
            return Results.CreatedAtRoute("ObtenerOrdenPatrones", new { id = orden.Id }, OrdenHexagonalDto.Desde(orden));
        }).WithName("CrearOrdenPatrones").Produces<OrdenHexagonalDto>(201).ProducesProblem(400);
        return app;
    }
}
