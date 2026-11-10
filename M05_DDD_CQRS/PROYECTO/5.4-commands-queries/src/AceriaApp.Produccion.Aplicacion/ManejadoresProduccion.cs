using MediatR;
namespace AceriaApp.Produccion.Aplicacion;
public sealed class CrearOrdenProduccionHandler(OrdenesProduccionCasosUso casos)
    : IRequestHandler<CrearOrdenProduccionCommand, ResultadoProduccion<Guid>>
{
    public Task<ResultadoProduccion<Guid>> Handle(CrearOrdenProduccionCommand request, CancellationToken ct) =>
        casos.CrearAsync(request.Cliente, request.Material, request.Cantidad, ct);
}
public sealed class PlanificarOrdenProduccionHandler(OrdenesProduccionCasosUso casos)
    : IRequestHandler<PlanificarOrdenProduccionCommand, ResultadoProduccion<OrdenProduccionDto>>
{
    public Task<ResultadoProduccion<OrdenProduccionDto>> Handle(PlanificarOrdenProduccionCommand request, CancellationToken ct) =>
        casos.PlanificarAsync(request.Id, ct);
}
public sealed class FinalizarOrdenProduccionHandler(OrdenesProduccionCasosUso casos)
    : IRequestHandler<FinalizarOrdenProduccionCommand, ResultadoProduccion<OrdenProduccionDto>>
{
    public Task<ResultadoProduccion<OrdenProduccionDto>> Handle(FinalizarOrdenProduccionCommand request, CancellationToken ct) =>
        casos.FinalizarAsync(request.Id, ct);
}
public sealed class ObtenerOrdenProduccionHandler(IOrdenProduccionLecturas lecturas)
    : IRequestHandler<ObtenerOrdenProduccionQuery, ResultadoProduccion<OrdenProduccionDto>>
{
    public async Task<ResultadoProduccion<OrdenProduccionDto>> Handle(ObtenerOrdenProduccionQuery request, CancellationToken ct)
    {
        var dto = await lecturas.ObtenerAsync(request.Id, ct);
        return dto is null
            ? ResultadoProduccion<OrdenProduccionDto>.Fallo(new("orden.ausente", "La orden de producción no existe.", TipoErrorProduccion.NoEncontrado))
            : ResultadoProduccion<OrdenProduccionDto>.Exito(dto);
    }
}
public sealed class ListarOrdenesProduccionHandler(IOrdenProduccionLecturas lecturas)
    : IRequestHandler<ListarOrdenesProduccionQuery, IReadOnlyList<OrdenProduccionDto>>
{
    public Task<IReadOnlyList<OrdenProduccionDto>> Handle(ListarOrdenesProduccionQuery request, CancellationToken ct) =>
        lecturas.ListarAsync(ct);
}
