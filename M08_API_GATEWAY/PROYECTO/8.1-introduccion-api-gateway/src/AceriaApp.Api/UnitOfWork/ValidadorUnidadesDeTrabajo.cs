using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.UnitOfWork;

public class ValidadorUnidadesDeTrabajo
{
    public ResultadoUnidadesDeTrabajo Validar(IEnumerable<UnidadDeTrabajo> unidades)
    {
        var errores = new List<string>();
        var lista = unidades.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay unidades de trabajo declaradas.");
        }

        foreach (var unidad in lista)
        {
            if (string.IsNullOrWhiteSpace(unidad.Nombre))
            {
                errores.Add("Una unidad de trabajo no declara el nombre.");
            }

            if (unidad.RepositoriosCoordinados < 1)
            {
                errores.Add($"La unidad '{unidad.Nombre}' no coordina ningún repositorio.");
            }

            if (!unidad.ExponeCommit)
            {
                errores.Add($"La unidad '{unidad.Nombre}' no expone la operación de confirmación.");
            }

            if (!unidad.ExponeRollback)
            {
                errores.Add($"La unidad '{unidad.Nombre}' no expone la operación de reversión.");
            }

            if (unidad.ContieneReglasDeNegocio)
            {
                errores.Add($"La unidad '{unidad.Nombre}' contiene reglas de negocio.");
            }

            if (unidad.ConoceEntidadesConcretas)
            {
                errores.Add($"La unidad '{unidad.Nombre}' conoce entidades concretas.");
            }
        }

        return new ResultadoUnidadesDeTrabajo(errores.Count == 0, errores);
    }
}

public record ResultadoUnidadesDeTrabajo(bool EsValida, IReadOnlyList<string> Errores);
