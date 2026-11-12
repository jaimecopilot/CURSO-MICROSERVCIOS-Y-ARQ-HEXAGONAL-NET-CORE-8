using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.InyeccionDependencias;

public class ValidadorInyeccionDependencias
{
    private static readonly string[] CiclosPermitidos = { "Transient", "Scoped", "Singleton" };

    public ResultadoInyeccion Validar(IEnumerable<RegistroInyeccion> registros)
    {
        var errores = new List<string>();
        var lista = registros.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay registros declarados.");
        }

        foreach (var registro in lista)
        {
            if (string.IsNullOrWhiteSpace(registro.Interfaz))
            {
                errores.Add("Un registro no declara la interfaz.");
            }

            if (string.IsNullOrWhiteSpace(registro.Implementacion))
            {
                errores.Add($"El registro de '{registro.Interfaz}' no declara implementación.");
            }

            if (!CiclosPermitidos.Contains(registro.Ciclo))
            {
                errores.Add($"Ciclo no permitido en '{registro.Interfaz}': '{registro.Ciclo}'.");
            }

            if (!registro.RegistradoPorConstructor)
            {
                errores.Add($"El registro de '{registro.Interfaz}' no se resuelve por constructor.");
            }

            if (registro.ResuelveManualmente)
            {
                errores.Add($"El registro de '{registro.Interfaz}' resuelve manualmente.");
            }

            if (registro.CapturaContenedor)
            {
                errores.Add($"El registro de '{registro.Interfaz}' captura el contenedor.");
            }
        }

        return new ResultadoInyeccion(errores.Count == 0, errores);
    }
}

public record ResultadoInyeccion(bool EsValido, IReadOnlyList<string> Errores);
