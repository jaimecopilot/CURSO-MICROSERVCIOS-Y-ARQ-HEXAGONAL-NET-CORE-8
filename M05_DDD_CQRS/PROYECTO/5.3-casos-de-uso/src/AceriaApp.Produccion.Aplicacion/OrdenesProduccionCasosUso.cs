using AceriaApp.Produccion.Dominio;
namespace AceriaApp.Produccion.Aplicacion;

// La aplicación coordina; las reglas de capacidad y de estado viven en el agregado.
public sealed class OrdenesProduccionCasosUso(
    IOrdenProduccionRepositorio repositorio, IProduccionUnitOfWork unidad)
{
    public async Task<ResultadoProduccion<Guid>> CrearAsync(string cliente, string material, int cantidad, CancellationToken ct = default)
    {
        try
        {
            var orden = new OrdenProduccion(cliente, material, cantidad);
            await repositorio.AgregarAsync(orden, ct);
            await unidad.CommitAsync(ct);
            return ResultadoProduccion<Guid>.Exito(orden.Id);
        }
        catch (ReglaProduccionException ex) { return ResultadoProduccion<Guid>.Fallo(Traducir(ex)); }
    }
    public async Task<ResultadoProduccion<OrdenProduccionDto>> ObtenerAsync(Guid id, CancellationToken ct = default)
    {
        var orden = await repositorio.ObtenerAsync(id, ct);
        return orden is null ? Ausente() : ResultadoProduccion<OrdenProduccionDto>.Exito(OrdenProduccionDto.Desde(orden));
    }
    public Task<ResultadoProduccion<OrdenProduccionDto>> PlanificarAsync(Guid id, CancellationToken ct = default) =>
        ModificarAsync(id, o => o.Planificar(), ct);
    public Task<ResultadoProduccion<OrdenProduccionDto>> FinalizarAsync(Guid id, CancellationToken ct = default) =>
        ModificarAsync(id, o => o.Finalizar(), ct);

    private async Task<ResultadoProduccion<OrdenProduccionDto>> ModificarAsync(Guid id, Action<OrdenProduccion> cambio, CancellationToken ct)
    {
        var orden = await repositorio.ObtenerAsync(id, ct);
        if (orden is null) return Ausente();
        try
        {
            cambio(orden);
            await unidad.CommitAsync(ct);
            return ResultadoProduccion<OrdenProduccionDto>.Exito(OrdenProduccionDto.Desde(orden));
        }
        catch (ReglaProduccionException ex) { return ResultadoProduccion<OrdenProduccionDto>.Fallo(Traducir(ex)); }
    }
    private static ResultadoProduccion<OrdenProduccionDto> Ausente() =>
        ResultadoProduccion<OrdenProduccionDto>.Fallo(new("orden.ausente", "La orden de producción no existe.", TipoErrorProduccion.NoEncontrado));
    private static ErrorProduccion Traducir(ReglaProduccionException ex) => new(ex.Codigo, ex.Message,
        ex.Codigo == "estado.invalido" ? TipoErrorProduccion.Conflicto : TipoErrorProduccion.Validacion);
}
