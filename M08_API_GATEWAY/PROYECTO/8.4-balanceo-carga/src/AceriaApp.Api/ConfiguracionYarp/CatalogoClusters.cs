using System.Collections.Generic;
namespace AceriaApp.Api.ConfiguracionYarp;

public class CatalogoClusters
{
    public static List<ClusterYarp> ClustersPorDefecto()
    {
        return new List<ClusterYarp>
        {
            new() { Identificador = "ordenes-cluster", Destinos = new[] { "http://aceria-ordenes:5001/" }, TieneDireccionValida = true, TieneConfiguracionPorEntorno = true },
            new() { Identificador = "inventario-cluster", Destinos = new[] { "http://aceria-inventario:5002/" }, TieneDireccionValida = true, TieneConfiguracionPorEntorno = true },
            new() { Identificador = "clientes-cluster", Destinos = new[] { "http://aceria-clientes:5003/" }, TieneDireccionValida = true, TieneConfiguracionPorEntorno = true }
        };
    }
}
