using AceriaApp.Hexagonal.Dominio;
using MediatR;
namespace AceriaApp.Hexagonal.Aplicacion.Patrones;

public sealed record CrearOrdenCommand(string Cliente, string Material, int Cantidad) : IRequest<Result<OrdenHexagonal>>;
public sealed record ObtenerOrdenQuery(Guid Id) : IRequest<Result<OrdenHexagonal>>;
public sealed record FinalizarOrdenCommand(Guid Id) : IRequest<Result<OrdenHexagonal>>;

public sealed class CrearOrdenHandler(OrdenesConResultado caso) : IRequestHandler<CrearOrdenCommand, Result<OrdenHexagonal>>
{
    public Task<Result<OrdenHexagonal>> Handle(CrearOrdenCommand request, CancellationToken ct) =>
        caso.CrearAsync(request.Cliente, request.Material, request.Cantidad, ct);
}
public sealed class ObtenerOrdenHandler(OrdenesConResultado caso) : IRequestHandler<ObtenerOrdenQuery, Result<OrdenHexagonal>>
{
    public Task<Result<OrdenHexagonal>> Handle(ObtenerOrdenQuery request, CancellationToken ct) => caso.ObtenerAsync(request.Id, ct);
}
public sealed class FinalizarOrdenHandler(OrdenesConResultado caso) : IRequestHandler<FinalizarOrdenCommand, Result<OrdenHexagonal>>
{
    public Task<Result<OrdenHexagonal>> Handle(FinalizarOrdenCommand request, CancellationToken ct) => caso.FinalizarAsync(request.Id, ct);
}
