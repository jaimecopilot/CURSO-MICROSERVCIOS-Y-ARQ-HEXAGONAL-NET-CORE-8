using System.Collections.Generic;
using System.Linq;

namespace AceriaApp.Api.GestionExcepciones;

public class ValidadorGestionExcepciones
{
    private static readonly int[] CodigosPermitidos = { 400, 401, 403, 404, 409, 422, 500, 503 };

    public ResultadoGestionExcepciones Validar(IEnumerable<ManejadorExcepcion> manejadores)
    {
        var errores = new List<string>();
        var lista = manejadores.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay manejadores declarados.");
        }

        foreach (var manejador in lista)
        {
            if (string.IsNullOrWhiteSpace(manejador.TipoExcepcion))
            {
                errores.Add("Un manejador no declara el tipo de excepción.");
            }

            if (!CodigosPermitidos.Contains(manejador.CodigoHttp))
            {
                errores.Add($"Código HTTP no permitido en '{manejador.TipoExcepcion}': '{manejador.CodigoHttp}'.");
            }

            if (string.IsNullOrWhiteSpace(manejador.Titulo))
            {
                errores.Add($"El manejador '{manejador.TipoExcepcion}' no declara título.");
            }

            if (!manejador.UsaProblemDetails)
            {
                errores.Add($"El manejador '{manejador.TipoExcepcion}' no usa problem details.");
            }

            if (manejador.CodigoHttp >= 500 && !manejador.RegistraError)
            {
                errores.Add($"El manejador '{manejador.TipoExcepcion}' no registra el error.");
            }
        }

        return new ResultadoGestionExcepciones(errores.Count == 0, errores);
    }
}

public record ResultadoGestionExcepciones(bool EsValida, IReadOnlyList<string> Errores);
