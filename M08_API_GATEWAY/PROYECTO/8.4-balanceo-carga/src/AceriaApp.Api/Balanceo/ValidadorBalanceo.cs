using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.Balanceo;

public class ValidadorBalanceo
{
    private static readonly string[] PoliticasPermitidas = { "RoundRobin", "Random", "LeastRequests", "PowerOfTwoChoices" };

    public ResultadoBalanceo Validar(IEnumerable<ClusterBalanceo> clusters)
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

            if (!PoliticasPermitidas.Contains(cluster.Politica))
            {
                errores.Add($"Política no permitida en '{cluster.Identificador}': '{cluster.Politica}'.");
            }

            if (cluster.NumeroDeDestinos < 2)
            {
                errores.Add($"El cluster '{cluster.Identificador}' no tiene al menos dos destinos.");
            }

            if (!cluster.CombinadoConHealthChecks)
            {
                errores.Add($"El cluster '{cluster.Identificador}' no está combinado con health checks.");
            }
        }

        return new ResultadoBalanceo(errores.Count == 0, errores);
    }
}

public record ResultadoBalanceo(bool EsValida, IReadOnlyList<string> Errores);
