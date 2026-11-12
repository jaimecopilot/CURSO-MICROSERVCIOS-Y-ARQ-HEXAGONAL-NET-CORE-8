using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.ConfiguracionYarp;

public class ValidadorConfiguracionYarp
{
    public ResultadoConfiguracionYarp Validar(IEnumerable<ClusterYarp> clusters)
    {
        var errores = new List<string>();
        var lista = clusters.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay clusters declarados.");
        }

        foreach (var cluster in lista)
        {
            if (string.IsNullOrWhiteSpace(cluster.Identificador))
            {
                errores.Add("Un cluster no declara el identificador.");
            }

            if (cluster.Destinos.Count == 0)
            {
                errores.Add($"El cluster '{cluster.Identificador}' no declara destinos.");
            }

            if (!cluster.TieneDireccionValida)
            {
                errores.Add($"El cluster '{cluster.Identificador}' no tiene dirección válida.");
            }

            if (!cluster.TieneConfiguracionPorEntorno)
            {
                errores.Add($"El cluster '{cluster.Identificador}' no tiene configuración por entorno.");
            }
        }

        return new ResultadoConfiguracionYarp(errores.Count == 0, errores);
    }
}

public record ResultadoConfiguracionYarp(bool EsValida, IReadOnlyList<string> Errores);
