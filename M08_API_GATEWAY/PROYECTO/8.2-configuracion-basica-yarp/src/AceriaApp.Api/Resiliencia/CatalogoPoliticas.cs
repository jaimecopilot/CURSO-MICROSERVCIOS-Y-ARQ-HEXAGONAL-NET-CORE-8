using System.Collections.Generic;

namespace AceriaApp.Api.Resiliencia;

public class CatalogoPoliticas
{
    public static List<PoliticaResiliencia> PoliticasPorDefecto()
    {
        return new List<PoliticaResiliencia>
        {
            new() { Nombre = "RetryHttp", Tipo = "Retry", OperacionIdempotente = true, NumeroDeReintentos = 3, MinimoDeMuestras = 0, TieneTimeout = true, RegistraEventos = true },
            new() { Nombre = "CircuitBreakerHttp", Tipo = "CircuitBreaker", NumeroDeReintentos = 0, MinimoDeMuestras = 5, TieneTimeout = true, RegistraEventos = true },
            new() { Nombre = "TimeoutHttp", Tipo = "Timeout", NumeroDeReintentos = 0, MinimoDeMuestras = 0, TieneTimeout = true, RegistraEventos = true },
            new() { Nombre = "RetryEventos", Tipo = "Retry", OperacionIdempotente = true, NumeroDeReintentos = 5, MinimoDeMuestras = 0, TieneTimeout = true, RegistraEventos = true },
            new() { Nombre = "CircuitBreakerEventos", Tipo = "CircuitBreaker", NumeroDeReintentos = 0, MinimoDeMuestras = 3, TieneTimeout = true, RegistraEventos = true }
        };
    }
}
