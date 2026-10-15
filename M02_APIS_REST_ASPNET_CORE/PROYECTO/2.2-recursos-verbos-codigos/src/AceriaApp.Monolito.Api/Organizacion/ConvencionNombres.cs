namespace AceriaApp.Monolito.Api.Organizacion;

// PASO 1.4.6: convención para nombres de proyectos.
public class ConvencionNombres
{
    public string Prefijo { get; init; } = "AceriaApp";
    public string Componente { get; init; } = string.Empty;
    public string Tipo { get; init; } = string.Empty;
    public string NombreCompleto() => $"{Prefijo}.{Componente}.{Tipo}";
}
