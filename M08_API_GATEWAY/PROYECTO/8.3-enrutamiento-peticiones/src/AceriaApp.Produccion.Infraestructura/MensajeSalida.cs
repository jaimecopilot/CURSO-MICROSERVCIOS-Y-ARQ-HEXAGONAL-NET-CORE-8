namespace AceriaApp.Produccion.Infraestructura;
public sealed class MensajeSalida
{
    public Guid Id { get; set; }
    public Guid OrdenId { get; set; }
    public string Contenido { get; set; } = "";
    public DateTimeOffset CreadoEnUtc { get; set; }
    public DateTimeOffset? EnviadoEnUtc { get; set; }
}
