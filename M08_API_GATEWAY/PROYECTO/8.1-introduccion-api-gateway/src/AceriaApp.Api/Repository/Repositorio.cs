namespace AceriaApp.Api.Repository;

public class Repositorio
{
    public string Nombre { get; init; } = string.Empty;
    public string Entidad { get; init; } = string.Empty;
    public int NumeroDeMetodos { get; init; }
    public bool TieneReglasDeNegocio { get; init; }
    public bool GestionaTransacciones { get; init; }
}
