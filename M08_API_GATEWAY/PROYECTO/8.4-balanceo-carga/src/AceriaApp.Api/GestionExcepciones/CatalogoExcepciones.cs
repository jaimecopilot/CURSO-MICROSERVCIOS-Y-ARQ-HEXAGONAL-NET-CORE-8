using System.Collections.Generic;

namespace AceriaApp.Api.GestionExcepciones;

public class CatalogoExcepciones
{
    public static List<ManejadorExcepcion> ManejadoresPorDefecto()
    {
        return new List<ManejadorExcepcion>
        {
            new() { TipoExcepcion = "OrdenNoEncontradaException", CodigoHttp = 404, Titulo = "Recurso no encontrado", UsaProblemDetails = true, RegistraError = true },
            new() { TipoExcepcion = "ValidacionException", CodigoHttp = 400, Titulo = "Error de validación", UsaProblemDetails = true, RegistraError = true },
            new() { TipoExcepcion = "ConflictoException", CodigoHttp = 409, Titulo = "Conflicto de estado", UsaProblemDetails = true, RegistraError = true },
            new() { TipoExcepcion = "RecursoNoProcesableException", CodigoHttp = 422, Titulo = "Entidad no procesable", UsaProblemDetails = true, RegistraError = true },
            new() { TipoExcepcion = "Exception", CodigoHttp = 500, Titulo = "Error interno", UsaProblemDetails = true, RegistraError = true }
        };
    }
}
