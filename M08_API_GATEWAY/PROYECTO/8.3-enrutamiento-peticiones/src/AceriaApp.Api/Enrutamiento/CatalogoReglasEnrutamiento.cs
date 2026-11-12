using System.Collections.Generic;
namespace AceriaApp.Api.Enrutamiento;

public class CatalogoReglasEnrutamiento
{
    public static List<ReglaEnrutamiento> ReglasPorDefecto()
    {
        return new List<ReglaEnrutamiento>
        {
            new()
            {
                Patron = "/api/v1/ordenes/{id:guid}",
                MetodoHttp = "GET",
                Orden = 1,
                TieneTransformacionDeRuta = true,
                TieneTransformacionDeCabecera = true,
                TieneTransformacionDeConsulta = false
            },
            new()
            {
                Patron = "/api/v1/ordenes/{**catch-all}",
                MetodoHttp = "GET",
                Orden = 2,
                TieneTransformacionDeRuta = true,
                TieneTransformacionDeCabecera = true,
                TieneTransformacionDeConsulta = false
            },
            new()
            {
                Patron = "/api/v1/inventario/{**catch-all}",
                MetodoHttp = "GET",
                Orden = 3,
                TieneTransformacionDeRuta = true,
                TieneTransformacionDeCabecera = true,
                TieneTransformacionDeConsulta = true
            },
            new()
            {
                Patron = "/api/v1/clientes/{**catch-all}",
                MetodoHttp = "GET",
                Orden = 4,
                TieneTransformacionDeRuta = true,
                TieneTransformacionDeCabecera = true,
                TieneTransformacionDeConsulta = true
            }
        };
    }
}
