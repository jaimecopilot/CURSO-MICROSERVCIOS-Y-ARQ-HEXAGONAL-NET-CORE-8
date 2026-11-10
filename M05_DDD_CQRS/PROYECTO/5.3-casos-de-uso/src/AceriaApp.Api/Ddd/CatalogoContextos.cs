using System.Collections.Generic;
namespace AceriaApp.Api.Ddd;

public class CatalogoContextos
{
    public static List<ContextoDelimitado> ContextosPorDefecto()
    {
        return new List<ContextoDelimitado>
        {
            new()
            {
                Nombre = "Produccion",
                TipoDeSubdominio = "Nucleo",
                LenguajeUbicuo = "orden de produccion, material, cantidad solicitada",
                TieneModeloPropio = true,
                ComparteModeloConOtro = false
            },
            new()
            {
                Nombre = "Aprovisionamiento",
                TipoDeSubdominio = "Soporte",
                LenguajeUbicuo = "orden de compra, proveedor, fecha de entrega",
                TieneModeloPropio = true,
                ComparteModeloConOtro = false
            },
            new()
            {
                Nombre = "Clientes",
                TipoDeSubdominio = "Soporte",
                LenguajeUbicuo = "cliente, razon social, contacto",
                TieneModeloPropio = true,
                ComparteModeloConOtro = false
            },
            new()
            {
                Nombre = "Identidad",
                TipoDeSubdominio = "Generico",
                LenguajeUbicuo = "usuario, rol, permiso",
                TieneModeloPropio = true,
                ComparteModeloConOtro = false
            }
        };
    }
}
