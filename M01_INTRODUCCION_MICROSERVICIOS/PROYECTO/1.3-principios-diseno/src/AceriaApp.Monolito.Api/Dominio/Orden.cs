namespace AceriaApp.Monolito.Api.Dominio;

// PASO 1.1.11: entidad de orden de producción.
public class Orden
{
    public Guid Id { get; set; }
    public string Cliente { get; set; } = string.Empty;
    public string Material { get; set; } = string.Empty;
    public int Cantidad { get; set; }
    public DateTime FechaCreacion { get; set; }
}
