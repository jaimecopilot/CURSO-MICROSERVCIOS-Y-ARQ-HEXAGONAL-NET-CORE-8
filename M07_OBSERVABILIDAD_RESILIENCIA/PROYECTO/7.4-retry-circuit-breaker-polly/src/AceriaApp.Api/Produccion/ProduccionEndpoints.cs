using MediatR;
using AceriaApp.Produccion.Aplicacion;
namespace AceriaApp.Api.Produccion;
public sealed record CrearOrdenProduccionRequest(string Cliente, string Material, int Cantidad);
public sealed record AgregarLineaProduccionRequest(string Material, int Cantidad);
public static class ProduccionEndpoints
{
    public static IEndpointRouteBuilder MapProduccion(this IEndpointRouteBuilder app)
    {
        var grupo = app.MapGroup("/api/v1/produccion/ordenes").WithTags("Produccion");
        grupo.MapPost("", async (CrearOrdenProduccionRequest request, ISender sender, CancellationToken ct) =>
        {
            var resultado = await sender.Send(new CrearOrdenProduccionCommand(request.Cliente, request.Material, request.Cantidad), ct);
            return resultado.EsExito
                ? Results.Created($"/api/v1/produccion/ordenes/{resultado.Valor}", new { id = resultado.Valor })
                : ErrorHttp(resultado.Error);
        });
        grupo.MapGet("/{id:guid}", async (Guid id, ISender sender, CancellationToken ct) =>
            Responder(await sender.Send(new ObtenerOrdenProduccionQuery(id), ct)));
        grupo.MapPost("/{id:guid}/planificar", async (Guid id, ISender sender, CancellationToken ct) =>
            Responder(await sender.Send(new PlanificarOrdenProduccionCommand(id), ct)));
        grupo.MapPost("/{id:guid}/finalizar", async (Guid id, ISender sender, CancellationToken ct) =>
            Responder(await sender.Send(new FinalizarOrdenProduccionCommand(id), ct)));
        grupo.MapGet("", async (ISender sender, CancellationToken ct) =>
            Results.Ok(await sender.Send(new ListarOrdenesProduccionQuery(), ct)));
        grupo.MapPost("/{id:guid}/lineas", async (Guid id, AgregarLineaProduccionRequest request, ISender sender, CancellationToken ct) =>
            Responder(await sender.Send(new AgregarLineaProduccionCommand(id, request.Material, request.Cantidad), ct)));
        return app;
    }
    private static IResult Responder<T>(ResultadoProduccion<T> resultado) =>
        resultado.EsExito ? Results.Ok(resultado.Valor) : ErrorHttp(resultado.Error);
    private static IResult ErrorHttp(ErrorProduccion error) => Results.Problem(
        title: error.Mensaje,
        statusCode: error.Tipo switch
        {
            TipoErrorProduccion.Validacion => 400,
            TipoErrorProduccion.NoEncontrado => 404,
            TipoErrorProduccion.Conflicto => 409,
            _ => throw new ArgumentOutOfRangeException(nameof(error))
        }, extensions: new Dictionary<string, object?> { ["codigo"] = error.Codigo });
}
