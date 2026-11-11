using System.Collections.Generic;
namespace AceriaApp.Api.ComunicacionAsincrona;

public class CatalogoEventos
{
    public static List<Evento> EventosPorDefecto()
    {
        return new List<Evento>
        {
            new() { Nombre = "OrdenCreada", Tipo = "Integracion", Publicador = "Ordenes.Api", NumeroDeConsumidores = 2, TieneIdempotencia = true, TieneReintentos = true },
            new() { Nombre = "OrdenCancelada", Tipo = "Integracion", Publicador = "Ordenes.Api", NumeroDeConsumidores = 2, TieneIdempotencia = true, TieneReintentos = true },
            new() { Nombre = "MaterialReservado", Tipo = "Integracion", Publicador = "Inventario.Api", NumeroDeConsumidores = 1, TieneIdempotencia = true, TieneReintentos = true },
            new() { Nombre = "FacturaEmitida", Tipo = "Integracion", Publicador = "Facturacion.Api", NumeroDeConsumidores = 1, TieneIdempotencia = true, TieneReintentos = true }
        };
    }
}
