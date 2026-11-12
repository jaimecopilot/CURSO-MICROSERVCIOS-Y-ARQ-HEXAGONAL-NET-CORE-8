namespace AceriaApp.Hexagonal.Dominio;

/// <summary>Entidad del núcleo: no depende de HTTP, EF Core ni SQL Server.</summary>
public sealed class OrdenHexagonal
{
    private OrdenHexagonal() { } // Materialización por EF Core.
    public OrdenHexagonal(string cliente, string material, int cantidad)
    {
        if (string.IsNullOrWhiteSpace(cliente) || string.IsNullOrWhiteSpace(material))
            throw new ArgumentException("Cliente y material son obligatorios.");
        if (cantidad <= 0) throw new ArgumentOutOfRangeException(nameof(cantidad));
        Id = Guid.NewGuid();
        Cliente = cliente.Trim(); Material = material.Trim(); Cantidad = cantidad;
        FechaCreacion = DateTime.UtcNow;
    }
    public Guid Id { get; private set; }
    public string Cliente { get; private set; } = string.Empty;
    public string Material { get; private set; } = string.Empty;
    public int Cantidad { get; private set; }
    public string Estado { get; private set; } = "Pendiente";
    public DateTime FechaCreacion { get; private set; }
    public void Finalizar()
    {
        if (Estado == "Finalizada") throw new InvalidOperationException("La orden ya estaba finalizada.");
        Estado = "Finalizada";
    }
}
