using AceriaApp.Produccion.Aplicacion;
namespace AceriaApp.Api.Produccion;
public sealed record CrearOrdenProduccionRequest(string Cliente, string Material, int Cantidad);
public static class ProduccionEndpoints
{
    public static IEndpointRouteBuilder MapProduccion(this IEndpointRouteBuilder app)
    {
        var grupo = app.MapGroup("/api/v1/produccion/ordenes").WithTags("Produccion");
        grupo.MapPost("", async (CrearOrdenProduccionRequest request, OrdenesProduccionCasosUso casos, CancellationToken ct) =>
        {
            var resultado = await casos.CrearAsync(request.Cliente, request.Material, request.Cantidad, ct);
            return resultado.EsExito
                ? Results.Created($"/api/v1/produccion/ordenes/{resultado.Valor}", new { id = resultado.Valor })
                : ErrorHttp(resultado.Error);
        });
        grupo.MapGet("/{id:guid}", async (Guid id, OrdenesProduccionCasosUso casos, CancellationToken ct) =>
            Responder(await casos.ObtenerAsync(id, ct)));
        grupo.MapPost("/{id:guid}/planificar", async (Guid id, OrdenesProduccionCasosUso casos, CancellationToken ct) =>
            Responder(await casos.PlanificarAsync(id, ct)));
        grupo.MapPost("/{id:guid}/finalizar", async (Guid id, OrdenesProduccionCasosUso casos, CancellationToken ct) =>
            Responder(await casos.FinalizarAsync(id, ct)));
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
