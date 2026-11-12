using System.Collections.Generic;
namespace AceriaApp.Api.Balanceo;

public class CatalogoClustersBalanceo
{
    public static List<ClusterBalanceo> ClustersPorDefecto()
    {
        return new List<ClusterBalanceo>
        {
            new() { Identificador = "ordenes-cluster", Politica = "RoundRobin", NumeroDeDestinos = 3, TienePesos = false, CombinadoConHealthChecks = true },
            new() { Identificador = "inventario-cluster", Politica = "PowerOfTwoChoices", NumeroDeDestinos = 2, TienePesos = true, CombinadoConHealthChecks = true },
            new() { Identificador = "clientes-cluster", Politica = "LeastRequests", NumeroDeDestinos = 2, TienePesos = false, CombinadoConHealthChecks = true }
        };
    }
}
