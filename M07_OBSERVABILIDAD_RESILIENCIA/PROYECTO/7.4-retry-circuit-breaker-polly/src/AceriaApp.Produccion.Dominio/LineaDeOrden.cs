namespace AceriaApp.Produccion.Dominio;

public sealed class LineaDeOrden : IEquatable<LineaDeOrden>
{
    public Guid Id { get; private set; }
    public NombreMaterial Material { get; private set; } = null!;
    public CantidadProduccion Cantidad { get; private set; } = null!;

    private LineaDeOrden() { } // Materialización; ningún consumidor crea una línea sin la raíz.
    internal LineaDeOrden(NombreMaterial material, CantidadProduccion cantidad)
    {
        Id = Guid.NewGuid();
        Material = material;
        Cantidad = cantidad;
    }
    internal void CambiarCantidad(CantidadProduccion cantidad) => Cantidad = cantidad;
    public bool Equals(LineaDeOrden? otra) => otra is not null && Id == otra.Id;
    public override bool Equals(object? otra) => otra is LineaDeOrden linea && Equals(linea);
    public override int GetHashCode() => Id.GetHashCode();
}
