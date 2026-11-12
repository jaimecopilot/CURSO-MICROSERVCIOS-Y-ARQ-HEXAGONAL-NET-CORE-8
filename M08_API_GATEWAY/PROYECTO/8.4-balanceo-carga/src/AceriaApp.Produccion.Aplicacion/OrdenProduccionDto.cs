using AceriaApp.Produccion.Dominio;
namespace AceriaApp.Produccion.Aplicacion;
public sealed record LineaProduccionDto(Guid Id, string Material, int Cantidad);
public sealed record OrdenProduccionDto(Guid Id, string Cliente, string Estado,
    int CantidadTotal, IReadOnlyList<LineaProduccionDto> Lineas)
{
    public static OrdenProduccionDto Desde(OrdenProduccion orden) => new(
        orden.Id, orden.Cliente, orden.Estado.ToString(), orden.CantidadTotal,
        orden.Lineas.Select(l => new LineaProduccionDto(l.Id, l.Material.Valor, l.Cantidad.Valor)).ToList().AsReadOnly());
}
