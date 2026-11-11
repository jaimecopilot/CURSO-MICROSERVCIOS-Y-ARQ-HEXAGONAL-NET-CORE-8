using System.Collections.Generic;
namespace AceriaApp.Api.UnitOfWork;

public class CatalogoUnidadesDeTrabajo
{
    public static List<UnidadDeTrabajo> UnidadesPorDefecto()
    {
        return new List<UnidadDeTrabajo>
        {
            new()
            {
                Nombre = "UnitOfWorkEfCore",
                RepositoriosCoordinados = 3,
                ExponeCommit = true,
                ExponeRollback = true,
                ContieneReglasDeNegocio = false,
                ConoceEntidadesConcretas = false
            },
            new()
            {
                Nombre = "UnitOfWorkEnMemoria",
                RepositoriosCoordinados = 3,
                ExponeCommit = true,
                ExponeRollback = true,
                ContieneReglasDeNegocio = false,
                ConoceEntidadesConcretas = false
            }
        };
    }
}
