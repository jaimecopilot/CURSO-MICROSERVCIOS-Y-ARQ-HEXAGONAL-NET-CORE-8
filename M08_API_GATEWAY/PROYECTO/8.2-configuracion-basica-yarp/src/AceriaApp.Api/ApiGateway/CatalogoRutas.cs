using System.Collections.Generic;
namespace AceriaApp.Api.ApiGateway;

public class CatalogoRutas
{
    public static List<RutaGateway> RutasPorDefecto()
    {
        return new List<RutaGateway>
        {
            new()
            {
                RutaExterna = "/api/v1/ordenes/{**catch-all}",
                ServicioDestino = "Ordenes.Api",
                RutaInterna = "/api/v1/ordenes/{**catch-all}",
                AplicaAutenticacion = true,
                AplicaRateLimit = true,
                AplicaCorrelacion = true
            },
            new()
            {
                RutaExterna = "/api/v1/inventario/{**catch-all}",
                ServicioDestino = "Inventario.Api",
                RutaInterna = "/api/v1/inventario/{**catch-all}",
                AplicaAutenticacion = true,
                AplicaRateLimit = true,
                AplicaCorrelacion = true
            },
            new()
            {
                RutaExterna = "/api/v1/clientes/{**catch-all}",
                ServicioDestino = "Clientes.Api",
                RutaInterna = "/api/v1/clientes/{**catch-all}",
                AplicaAutenticacion = true,
                AplicaRateLimit = true,
                AplicaCorrelacion = true
            }
        };
    }
}
