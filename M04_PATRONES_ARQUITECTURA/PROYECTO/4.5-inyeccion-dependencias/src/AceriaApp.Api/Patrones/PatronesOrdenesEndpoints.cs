using MediatR;
using AceriaApp.Api.Hexagonal;
using AceriaApp.Hexagonal.Aplicacion.Patrones;
namespace AceriaApp.Api.Patrones;

public static class PatronesOrdenesEndpoints
{
    public static IEndpointRouteBuilder MapPatronesOrdenes(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/v1/patrones/ordenes").WithTags("Patrones");
        group.MapGet("/{id:guid}", async (Guid id, ISender sender, CancellationToken ct) =>
        {
            var resultado = await sender.Send(new ObtenerOrdenQuery(id), ct);
            return resultado.EsExito ? Results.Ok(OrdenHexagonalDto.Desde(resultado.Valor)) : TraducirError(resultado.Error);
        }).WithName("ObtenerOrdenPatrones").Produces<OrdenHexagonalDto>(200).ProducesProblem(404);
        group.MapPost("", async (CrearOrdenHexagonalRequest body, ISender sender, CancellationToken ct) =>
        {
            var resultado = await sender.Send(new CrearOrdenCommand(body.Cliente, body.Material, body.Cantidad), ct);
            if (!resultado.EsExito) return TraducirError(resultado.Error);
            var orden = resultado.Valor;
            return Results.CreatedAtRoute("ObtenerOrdenPatrones", new { id = orden.Id }, OrdenHexagonalDto.Desde(orden));
        }).WithName("CrearOrdenPatrones").Produces<OrdenHexagonalDto>(201).ProducesProblem(400);
        group.MapPost("/{id:guid}/finalizar", async (Guid id, ISender sender, CancellationToken ct) =>
        {
            var resultado = await sender.Send(new FinalizarOrdenCommand(id), ct);
            return resultado.EsExito ? Results.Ok(OrdenHexagonalDto.Desde(resultado.Valor)) : TraducirError(resultado.Error);
        }).WithName("FinalizarOrdenPatrones").Produces<OrdenHexagonalDto>(200).ProducesProblem(404).ProducesProblem(409);
        return app;
    }

    private static IResult TraducirError(Error error) => Results.Problem(
        title: error.Descripcion,
        statusCode: error.Tipo switch
        {
            TipoError.Validacion => 400,
            TipoError.NoEncontrado => 404,
            TipoError.Conflicto => 409,
            _ => throw new ArgumentOutOfRangeException(nameof(error))
        },
        extensions: new Dictionary<string, object?> { ["codigo"] = error.Codigo });
}
