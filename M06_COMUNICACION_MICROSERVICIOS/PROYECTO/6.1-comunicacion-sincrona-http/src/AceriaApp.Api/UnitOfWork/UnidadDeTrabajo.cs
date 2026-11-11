namespace AceriaApp.Api.UnitOfWork;

public class UnidadDeTrabajo
{
    public string Nombre { get; init; } = string.Empty;
    public int RepositoriosCoordinados { get; init; }
    public bool ExponeCommit { get; init; }
    public bool ExponeRollback { get; init; }
    public bool ContieneReglasDeNegocio { get; init; }
    public bool ConoceEntidadesConcretas { get; init; }
}
