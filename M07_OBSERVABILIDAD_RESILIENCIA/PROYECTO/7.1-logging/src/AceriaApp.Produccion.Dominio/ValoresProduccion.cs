namespace AceriaApp.Produccion.Dominio;

// Clases record selladas: igualdad por valor, sin default(struct) inválido ni init público.
public sealed record NombreMaterial
{
    public string Valor { get; }
    public NombreMaterial(string valor)
    {
        if (string.IsNullOrWhiteSpace(valor) || valor.Trim().Length > 100)
            throw new ReglaProduccionException("material.invalido", "El material debe tener entre 1 y 100 caracteres.");
        Valor = valor.Trim();
    }
}

public sealed record CantidadProduccion
{
    public int Valor { get; }
    public CantidadProduccion(int valor)
    {
        if (valor is < 1 or > OrdenProduccion.CapacidadMaxima)
            throw new ReglaProduccionException("cantidad.invalida", "La cantidad debe estar entre 1 y 500 unidades.");
        Valor = valor;
    }
}
