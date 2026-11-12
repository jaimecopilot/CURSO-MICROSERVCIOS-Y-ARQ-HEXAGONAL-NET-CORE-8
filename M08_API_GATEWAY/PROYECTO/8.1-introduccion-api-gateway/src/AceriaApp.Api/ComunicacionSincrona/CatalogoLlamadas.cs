using System.Collections.Generic;
namespace AceriaApp.Api.ComunicacionSincrona;

public class CatalogoLlamadas
{
    public static List<LlamadaSincrona> LlamadasPorDefecto()
    {
        return new List<LlamadaSincrona>
        {
            new() { ServicioOrigen = "Ordenes.Api", ServicioDestino = "Inventario.Api", Metodo = "GET", TieneTimeout = true, TieneReintentos = true, TieneCircuitBreaker = true },
            new() { ServicioOrigen = "Ordenes.Api", ServicioDestino = "Clientes.Api", Metodo = "GET", TieneTimeout = true, TieneReintentos = true, TieneCircuitBreaker = true },
            new() { ServicioOrigen = "Facturacion.Api", ServicioDestino = "Ordenes.Api", Metodo = "GET", TieneTimeout = true, TieneReintentos = true, TieneCircuitBreaker = true }
        };
    }
}
