using System.Collections.Generic;
using System.Linq;

namespace AceriaApp.Api.Resiliencia;

public class ValidadorResiliencia
{
    private static readonly string[] TiposPermitidos = { "Retry", "CircuitBreaker", "Timeout" };

    public ResultadoResiliencia Validar(IEnumerable<PoliticaResiliencia> politicas)
    {
        var errores = new List<string>();
        var lista = politicas.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay políticas declaradas.");
        }

        foreach (var politica in lista)
        {
            if (string.IsNullOrWhiteSpace(politica.Nombre))
            {
                errores.Add("Una política no declara el nombre.");
            }

            if (!TiposPermitidos.Contains(politica.Tipo))
            {
                errores.Add($"Tipo no permitido en '{politica.Nombre}': '{politica.Tipo}'.");
            }

            if (politica.Tipo == "Retry" && politica.NumeroDeReintentos < 1)
            {
                errores.Add($"La política de retry '{politica.Nombre}' no declara reintentos.");
            }

            if (politica.Tipo == "CircuitBreaker" && politica.MinimoDeMuestras < 2)
            {
                errores.Add($"La política de circuit breaker '{politica.Nombre}' no declara mínimo de muestras.");
            }

            if (politica.Tipo == "Retry" && !politica.OperacionIdempotente)
            {
                errores.Add($"La política de retry '{politica.Nombre}' no declara una operación idempotente.");
            }

            if (politica.Tipo == "CircuitBreaker" &&
                (!double.IsFinite(politica.ProporcionDeFallos) || politica.ProporcionDeFallos <= 0 || politica.ProporcionDeFallos > 1))
            {
                errores.Add($"La política de circuit breaker '{politica.Nombre}' tiene una proporción de fallos fuera de (0, 1].");
            }

            if (politica.Tipo == "CircuitBreaker" && politica.VentanaMuestreoSegundos < 1)
            {
                errores.Add($"La política de circuit breaker '{politica.Nombre}' no declara una ventana de muestreo positiva.");
            }

            if (politica.Tipo == "CircuitBreaker" && politica.DuracionAperturaSegundos < 1)
            {
                errores.Add($"La política de circuit breaker '{politica.Nombre}' no declara una duración de apertura positiva.");
            }

            if (!politica.TieneTimeout)
            {
                errores.Add($"La política '{politica.Nombre}' no tiene timeout.");
            }

            if (!politica.RegistraEventos)
            {
                errores.Add($"La política '{politica.Nombre}' no registra eventos.");
            }
        }

        return new ResultadoResiliencia(errores.Count == 0, errores);
    }
}

public record ResultadoResiliencia(bool EsValida, IReadOnlyList<string> Errores);
