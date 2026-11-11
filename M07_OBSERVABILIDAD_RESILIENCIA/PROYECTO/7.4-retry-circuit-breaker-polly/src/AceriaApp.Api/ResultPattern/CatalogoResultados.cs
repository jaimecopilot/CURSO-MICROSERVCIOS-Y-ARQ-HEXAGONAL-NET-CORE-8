using System.Collections.Generic;
namespace AceriaApp.Api.ResultPattern;

public class CatalogoResultados
{
    public static List<ResultadoOperacion> OperacionesPorDefecto()
    {
        return new List<ResultadoOperacion>
        {
            new() { Nombre = "CrearOrden", UsaResult = true, UsaExcepcionesParaErroresEsperados = false, NumeroDeErroresEsperados = 3 },
            new() { Nombre = "CancelarOrden", UsaResult = true, UsaExcepcionesParaErroresEsperados = false, NumeroDeErroresEsperados = 2 },
            new() { Nombre = "ObtenerOrden", UsaResult = true, UsaExcepcionesParaErroresEsperados = false, NumeroDeErroresEsperados = 1 },
            new() { Nombre = "ListarOrdenes", UsaResult = true, UsaExcepcionesParaErroresEsperados = false, NumeroDeErroresEsperados = 0 }
        };
    }
}
