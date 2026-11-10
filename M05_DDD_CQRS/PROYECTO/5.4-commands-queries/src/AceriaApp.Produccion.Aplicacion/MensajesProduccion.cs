using MediatR;
namespace AceriaApp.Produccion.Aplicacion;
public sealed record CrearOrdenProduccionCommand(string Cliente, string Material, int Cantidad)
    : IRequest<ResultadoProduccion<Guid>>;
public sealed record PlanificarOrdenProduccionCommand(Guid Id)
    : IRequest<ResultadoProduccion<OrdenProduccionDto>>;
public sealed record FinalizarOrdenProduccionCommand(Guid Id)
    : IRequest<ResultadoProduccion<OrdenProduccionDto>>;
public sealed record ObtenerOrdenProduccionQuery(Guid Id)
    : IRequest<ResultadoProduccion<OrdenProduccionDto>>;
public sealed record ListarOrdenesProduccionQuery : IRequest<IReadOnlyList<OrdenProduccionDto>>;
