using System.Collections.Generic;
namespace AceriaApp.Api.Decisiones;

public class CatalogoDecisiones
{
    public static List<DecisionComunicacion> DecisionesPorDefecto()
    {
        return new List<DecisionComunicacion>
        {
            new() { Interaccion = "Ordenes->Inventario consulta stock", Enfoque = "Sincrona", RequiereRespuestaInmediata = true, ToleraConsistenciaEventual = false, TienePatronHibrido = false },
            new() { Interaccion = "Ordenes->Clientes consulta cliente", Enfoque = "Sincrona", RequiereRespuestaInmediata = true, ToleraConsistenciaEventual = false, TienePatronHibrido = false },
            new() { Interaccion = "Ordenes->Inventario reserva material", Enfoque = "Asincrona", RequiereRespuestaInmediata = false, ToleraConsistenciaEventual = true, TienePatronHibrido = false },
            new() { Interaccion = "Ordenes->Facturacion emision factura", Enfoque = "Asincrona", RequiereRespuestaInmediata = false, ToleraConsistenciaEventual = true, TienePatronHibrido = false },
            new() { Interaccion = "Ordenes->Inventario notificacion y consulta", Enfoque = "Hibrida", RequiereRespuestaInmediata = true, ToleraConsistenciaEventual = true, TienePatronHibrido = true }
        };
    }
}
