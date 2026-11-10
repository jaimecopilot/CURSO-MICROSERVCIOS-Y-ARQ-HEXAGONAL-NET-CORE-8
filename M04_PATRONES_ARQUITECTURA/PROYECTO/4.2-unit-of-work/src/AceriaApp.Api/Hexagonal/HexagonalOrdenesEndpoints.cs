using AceriaApp.Hexagonal.Aplicacion.CasosUso;
using AceriaApp.Hexagonal.Dominio;

namespace AceriaApp.Api.Hexagonal;

public sealed record CrearOrdenHexagonalRequest(string Cliente, string Material, int Cantidad);
public sealed record OrdenHexagonalDto(Guid Id, string Cliente, string Material,
    int Cantidad, string Estado, DateTime FechaCreacion)
{
    public static OrdenHexagonalDto Desde(OrdenHexagonal orden) =>
        new(orden.Id, orden.Cliente, orden.Material, orden.Cantidad, orden.Estado, orden.FechaCreacion);
}

/// <summary>Adaptador HTTP: traduce peticiones en llamadas a los casos de uso.</summary>
public static class HexagonalOrdenesEndpoints
{
    public static IEndpointRouteBuilder MapHexagonalOrdenes(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/v1/hexagonal/ordenes").WithTags("Ordenes hexagonales");
        group.MapGet("", async (OrdenesCasoUso uso, CancellationToken ct) =>
        {
            var ordenes = await uso.ListarAsync(ct);
            return Results.Ok(ordenes.Select(OrdenHexagonalDto.Desde));
        }).WithName("ListarOrdenesHexagonales").Produces<IEnumerable<OrdenHexagonalDto>>(200);

        group.MapGet("/{id:guid}", async (Guid id, OrdenesCasoUso uso, CancellationToken ct) =>
        {
            var orden = await uso.ObtenerAsync(id, ct);
            IResult response = orden is null ? Results.NotFound() : Results.Ok(OrdenHexagonalDto.Desde(orden));
            return response;
        }).WithName("ObtenerOrdenHexagonal").Produces<OrdenHexagonalDto>(200).Produces(404);

        group.MapPost("", async (CrearOrdenHexagonalRequest body, OrdenesCasoUso uso, CancellationToken ct) =>
        {
            if (string.IsNullOrWhiteSpace(body.Cliente) || string.IsNullOrWhiteSpace(body.Material) || body.Cantidad <= 0)
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["body"] = new[] { "Cliente, material y cantidad positiva son obligatorios." } });
            if (body.Cantidad > 500)
                return Results.Problem(title: "Capacidad del taller superada.", statusCode: 422);
            var orden = await uso.CrearAsync(body.Cliente, body.Material, body.Cantidad, ct);
            return Results.CreatedAtRoute("ObtenerOrdenHexagonal", new { id = orden.Id }, OrdenHexagonalDto.Desde(orden));
        }).WithName("CrearOrdenHexagonal").Produces<OrdenHexagonalDto>(201)
          .ProducesValidationProblem(400).ProducesProblem(422);

        group.MapPost("/{id:guid}/finalizar", async (Guid id, OrdenesCasoUso uso, CancellationToken ct) =>
        {
            try
            {
                var orden = await uso.FinalizarAsync(id, ct);
                IResult response = orden is null ? Results.NotFound() : Results.Ok(OrdenHexagonalDto.Desde(orden));
            return response;
            }
            catch (InvalidOperationException)
            {
                return Results.Problem(title: "La orden ya está finalizada.", statusCode: 409);
            }
        }).WithName("FinalizarOrdenHexagonal").Produces<OrdenHexagonalDto>(200).Produces(404).ProducesProblem(409);
        return app;
    }
}
