using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.Decisiones;

public class ValidadorDecisiones
{
    private static readonly string[] EnfoquesPermitidos = { "Sincrona", "Asincrona", "Hibrida" };

    public ResultadoDecisiones Validar(IEnumerable<DecisionComunicacion> decisiones)
    {
        var errores = new List<string>();
        var lista = decisiones.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay decisiones declaradas.");
        }

        foreach (var decision in lista)
        {
            if (string.IsNullOrWhiteSpace(decision.Interaccion))
            {
                errores.Add("Una decisión no declara la interacción.");
            }

            if (!EnfoquesPermitidos.Contains(decision.Enfoque))
            {
                errores.Add($"Enfoque no permitido en '{decision.Interaccion}': '{decision.Enfoque}'.");
            }

            if (decision.Enfoque == "Asincrona" && decision.RequiereRespuestaInmediata)
            {
                errores.Add($"La interacción '{decision.Interaccion}' es asíncrona pero requiere respuesta inmediata del consumidor.");
            }

            if (decision.Enfoque == "Asincrona" && !decision.ToleraConsistenciaEventual)
            {
                errores.Add($"La interacción '{decision.Interaccion}' es asíncrona pero no tolera consistencia eventual.");
            }

            if (decision.Enfoque == "Hibrida" && !decision.TienePatronHibrido)
            {
                errores.Add($"La interacción '{decision.Interaccion}' es híbrida pero no declara patrón híbrido.");
            }
        }

        return new ResultadoDecisiones(errores.Count == 0, errores);
    }
}

public record ResultadoDecisiones(bool EsValida, IReadOnlyList<string> Errores);
