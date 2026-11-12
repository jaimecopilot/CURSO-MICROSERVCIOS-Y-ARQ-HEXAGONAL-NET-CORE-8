using System.Collections.Generic;
namespace AceriaApp.Api.CasosDeUso;

public class CatalogoCasosDeUso
{
    public static List<CasoDeUso> CasosPorDefecto()
    {
        return new List<CasoDeUso>
        {
            new() { Nombre = "CrearOrden", Tipo = "Escritura", TieneManejador = true, DevuelveResult = true, CoordinaUnidadDeTrabajo = true, ContieneReglasDeNegocio = false },
            new() { Nombre = "CancelarOrden", Tipo = "Escritura", TieneManejador = true, DevuelveResult = true, CoordinaUnidadDeTrabajo = true, ContieneReglasDeNegocio = false },
            new() { Nombre = "ObtenerOrden", Tipo = "Lectura", TieneManejador = true, DevuelveResult = true, CoordinaUnidadDeTrabajo = false, ContieneReglasDeNegocio = false },
            new() { Nombre = "ListarOrdenes", Tipo = "Lectura", TieneManejador = true, DevuelveResult = true, CoordinaUnidadDeTrabajo = false, ContieneReglasDeNegocio = false }
        };
    }
}
