using System.Collections.Generic;
namespace AceriaApp.Api.DominioAceria;

public class CatalogoAceria
{
    public static List<ElementoAceria> ElementosPorDefecto()
    {
        return new List<ElementoAceria>
        {
            new() { Nombre = "OrdenProduccion", Contexto = "Produccion", Tipo = "Agregado", TieneInvariantes = true, EsRaizDeAgregado = true },
            new() { Nombre = "LineaProduccion", Contexto = "Produccion", Tipo = "Entidad", TieneInvariantes = true, EsRaizDeAgregado = false },
            new() { Nombre = "ProductoTerminado", Contexto = "Produccion", Tipo = "Entidad", TieneInvariantes = true, EsRaizDeAgregado = false },
            new() { Nombre = "Cantidad", Contexto = "Produccion", Tipo = "ValueObject", TieneInvariantes = true, EsRaizDeAgregado = false },
            new() { Nombre = "OrdenCompra", Contexto = "Aprovisionamiento", Tipo = "Agregado", TieneInvariantes = true, EsRaizDeAgregado = true },
            new() { Nombre = "Proveedor", Contexto = "Aprovisionamiento", Tipo = "Entidad", TieneInvariantes = true, EsRaizDeAgregado = false },
            new() { Nombre = "Precio", Contexto = "Aprovisionamiento", Tipo = "ValueObject", TieneInvariantes = true, EsRaizDeAgregado = false },
            new() { Nombre = "Cliente", Contexto = "Clientes", Tipo = "Agregado", TieneInvariantes = true, EsRaizDeAgregado = true },
            new() { Nombre = "Contacto", Contexto = "Clientes", Tipo = "Entidad", TieneInvariantes = true, EsRaizDeAgregado = false },
            new() { Nombre = "Direccion", Contexto = "Clientes", Tipo = "ValueObject", TieneInvariantes = true, EsRaizDeAgregado = false }
        };
    }
}
