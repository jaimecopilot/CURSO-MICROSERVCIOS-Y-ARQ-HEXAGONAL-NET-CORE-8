using AceriaApp.Comunicacion.Contratos;
namespace AceriaApp.Comunicacion.Aplicacion;
public enum EstadoPlanificacion { Aceptada, NoExiste, Conflicto, SinDisponibilidad }
public interface IPlanificadorIntegrado
{
    Task<IReadOnlyList<LineaPlanificadaV1>?> ObtenerLineasAsync(Guid id, CancellationToken ct);
    Task<EstadoPlanificacion> PlanificarAsync(Guid id, CancellationToken ct);
}
public interface ITransporteEventos
{
    Task PublicarAsync(string contenido, CancellationToken ct);
}
