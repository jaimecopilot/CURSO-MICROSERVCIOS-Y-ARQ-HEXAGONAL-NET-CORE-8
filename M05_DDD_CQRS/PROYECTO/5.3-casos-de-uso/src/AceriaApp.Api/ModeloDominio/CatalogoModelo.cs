using System.Collections.Generic;
namespace AceriaApp.Api.ModeloDominio;

public class CatalogoModelo
{
    public static List<ElementoModelo> ElementosPorDefecto()
    {
        return new List<ElementoModelo>
        {
            new() { Nombre = "Orden", Tipo = "Entidad", TieneIdentidad = true, EsInmutable = false, ValidaInvariantes = true },
            new() { Nombre = "Material", Tipo = "Entidad", TieneIdentidad = true, EsInmutable = false, ValidaInvariantes = true },
            new() { Nombre = "Cliente", Tipo = "Entidad", TieneIdentidad = true, EsInmutable = false, ValidaInvariantes = true },
            new() { Nombre = "Dinero", Tipo = "ValueObject", TieneIdentidad = false, EsInmutable = true, ValidaInvariantes = true },
            new() { Nombre = "Direccion", Tipo = "ValueObject", TieneIdentidad = false, EsInmutable = true, ValidaInvariantes = true },
            new() { Nombre = "Cantidad", Tipo = "ValueObject", TieneIdentidad = false, EsInmutable = true, ValidaInvariantes = true }
        };
    }
}
