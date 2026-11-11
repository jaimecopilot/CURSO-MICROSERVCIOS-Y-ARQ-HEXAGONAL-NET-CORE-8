namespace AceriaApp.Inventario.Api;
public sealed class PlanificacionRecibida
{
    public Guid EventoId { get; set; }
    public Guid OrdenId { get; set; }
    public int CantidadTotal { get; set; }
    public string HuellaContenido { get; set; } = "";
    public DateTimeOffset RecibidoEnUtc { get; set; }
}
