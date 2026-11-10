namespace AceriaApp.Produccion.Dominio;

// Producción tiene identidad y ciclo de vida propios; no reutiliza Orden de M2/M4.
public sealed class OrdenProduccion : IEquatable<OrdenProduccion>
{
    public const int CapacidadMaxima = 500;
    public Guid Id { get; private set; }
    public string Cliente { get; private set; }
    public string Material { get; private set; }
    public int Cantidad { get; private set; }
    public EstadoOrdenProduccion Estado { get; private set; }

    public OrdenProduccion(string cliente, string material, int cantidad)
    {
        if (string.IsNullOrWhiteSpace(cliente) || cliente.Trim().Length > 100)
            throw new ReglaProduccionException("cliente.invalido", "El cliente debe tener entre 1 y 100 caracteres.");
        if (string.IsNullOrWhiteSpace(material) || material.Trim().Length > 100)
            throw new ReglaProduccionException("material.invalido", "El material debe tener entre 1 y 100 caracteres.");
        if (cantidad is < 1 or > CapacidadMaxima)
            throw new ReglaProduccionException("cantidad.invalida", "La cantidad debe estar entre 1 y 500 unidades.");
        Id = Guid.NewGuid();
        Cliente = cliente.Trim();
        Material = material.Trim();
        Cantidad = cantidad;
        Estado = EstadoOrdenProduccion.Borrador;
    }

    public void Planificar()
    {
        if (Estado != EstadoOrdenProduccion.Borrador)
            throw new ReglaProduccionException("estado.invalido", "Solo se puede planificar una orden en borrador.");
        Estado = EstadoOrdenProduccion.Planificada;
    }

    public void Finalizar()
    {
        if (Estado != EstadoOrdenProduccion.Planificada)
            throw new ReglaProduccionException("estado.invalido", "Solo se puede finalizar una orden planificada.");
        Estado = EstadoOrdenProduccion.Finalizada;
    }

    public bool Equals(OrdenProduccion? otra) => otra is not null && Id == otra.Id;
    public override bool Equals(object? otra) => otra is OrdenProduccion orden && Equals(orden);
    public override int GetHashCode() => Id.GetHashCode();
}
