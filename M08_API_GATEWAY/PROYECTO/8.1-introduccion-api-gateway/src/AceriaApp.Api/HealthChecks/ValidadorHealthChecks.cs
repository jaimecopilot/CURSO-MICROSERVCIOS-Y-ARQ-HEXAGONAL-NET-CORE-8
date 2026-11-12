using System.Collections.Generic;
using System.Linq;

namespace AceriaApp.Api.HealthChecks;

public class ValidadorHealthChecks
{
    private static readonly string[] TiposPermitidos = { "Liveness", "Readiness", "Startup" };

    public ResultadoHealthChecks Validar(IEnumerable<HealthCheck> healthChecks)
    {
        var errores = new List<string>();
        var lista = healthChecks.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay health checks declarados.");
        }

        foreach (var healthCheck in lista)
        {
            if (string.IsNullOrWhiteSpace(healthCheck.Nombre))
            {
                errores.Add("Un health check no declara el nombre.");
            }

            if (!TiposPermitidos.Contains(healthCheck.Tipo))
            {
                errores.Add($"Tipo no permitido en '{healthCheck.Nombre}': '{healthCheck.Tipo}'.");
            }

            if (string.IsNullOrWhiteSpace(healthCheck.Recurso))
            {
                errores.Add($"El health check '{healthCheck.Nombre}' no declara el recurso.");
            }

            if (healthCheck.Tipo == "Liveness" && healthCheck.ConsultaDependenciaExterna)
            {
                errores.Add($"El liveness '{healthCheck.Nombre}' consulta una dependencia externa.");
            }

            if (!healthCheck.TieneTimeout)
            {
                errores.Add($"El health check '{healthCheck.Nombre}' no tiene timeout.");
            }

            if (healthCheck.ExponeInformacionSensible)
            {
                errores.Add($"El health check '{healthCheck.Nombre}' expone información sensible.");
            }
        }

        return new ResultadoHealthChecks(errores.Count == 0, errores);
    }
}

public record ResultadoHealthChecks(bool EsValida, IReadOnlyList<string> Errores);
