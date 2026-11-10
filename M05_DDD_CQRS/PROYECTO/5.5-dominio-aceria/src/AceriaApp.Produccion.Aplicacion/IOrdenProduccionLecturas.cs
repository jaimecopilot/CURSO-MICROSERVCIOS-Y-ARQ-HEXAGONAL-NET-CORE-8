namespace AceriaApp.Produccion.Aplicacion;
// Contrato de consulta: no permite modificar entidades ni confirmar cambios.
public interface IOrdenProduccionLecturas
{
    Task<OrdenProduccionDto?> ObtenerAsync(Guid id, CancellationToken ct = default);
    Task<IReadOnlyList<OrdenProduccionDto>> ListarAsync(CancellationToken ct = default);
}
