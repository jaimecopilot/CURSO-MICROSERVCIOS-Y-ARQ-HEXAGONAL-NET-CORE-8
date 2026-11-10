using AceriaApp.Hexagonal.Dominio;
using MediatR;
namespace AceriaApp.Hexagonal.Aplicacion.Patrones;

public sealed record CrearOrdenCommand(string Cliente, string Material, int Cantidad) : IRequest<OrdenHexagonal>;
public sealed record ObtenerOrdenQuery(Guid Id) : IRequest<OrdenHexagonal?>;

public sealed class CrearOrdenHandler(OrdenesTransaccionales caso) : IRequestHandler<CrearOrdenCommand, OrdenHexagonal>
{
    public Task<OrdenHexagonal> Handle(CrearOrdenCommand request, CancellationToken ct) =>
        caso.CrearAsync(request.Cliente, request.Material, request.Cantidad, ct);
}
public sealed class ObtenerOrdenHandler(OrdenesTransaccionales caso) : IRequestHandler<ObtenerOrdenQuery, OrdenHexagonal?>
{
    public Task<OrdenHexagonal?> Handle(ObtenerOrdenQuery request, CancellationToken ct) => caso.ObtenerAsync(request.Id, ct);
}
