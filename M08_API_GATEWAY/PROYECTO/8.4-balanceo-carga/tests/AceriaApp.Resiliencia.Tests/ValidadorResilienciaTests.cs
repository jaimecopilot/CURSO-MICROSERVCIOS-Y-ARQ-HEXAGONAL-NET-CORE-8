using AceriaApp.Api.Resiliencia;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Resiliencia.Tests;

public class ValidadorResilienciaTests
{
    private readonly ValidadorResiliencia _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValida()
    {
        var resultado = _validador.Validar(CatalogoPoliticas.PoliticasPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinPoliticas_DevuelveError()
    {
        var resultado = _validador.Validar(new List<PoliticaResiliencia>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay políticas"));
    }

    [Fact]
    public void Validar_TipoNoPermitido_DevuelveError()
    {
        var politicas = new List<PoliticaResiliencia>
        {
            new() { Nombre = "X", Tipo = "TipoInventado", TieneTimeout = true, RegistraEventos = true }
        };

        var resultado = _validador.Validar(politicas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Tipo no permitido"));
    }

    [Fact]
    public void Validar_RetrySinReintentos_DevuelveError()
    {
        var politicas = new List<PoliticaResiliencia>
        {
            new() { Nombre = "X", Tipo = "Retry", NumeroDeReintentos = 0, TieneTimeout = true, RegistraEventos = true }
        };

        var resultado = _validador.Validar(politicas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara reintentos"));
    }

    [Fact]
    public void Validar_CircuitBreakerSinMinimoDeMuestras_DevuelveError()
    {
        var politicas = new List<PoliticaResiliencia>
        {
            new() { Nombre = "X", Tipo = "CircuitBreaker", MinimoDeMuestras = 0, TieneTimeout = true, RegistraEventos = true }
        };

        var resultado = _validador.Validar(politicas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara mínimo de muestras"));
    }

    [Fact]
    public void Validar_SinTimeout_DevuelveError()
    {
        var politicas = new List<PoliticaResiliencia>
        {
            new() { Nombre = "X", Tipo = "Timeout", TieneTimeout = false, RegistraEventos = true }
        };

        var resultado = _validador.Validar(politicas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene timeout"));
    }

    [Fact]
    public void Validar_SinRegistro_DevuelveError()
    {
        var politicas = new List<PoliticaResiliencia>
        {
            new() { Nombre = "X", Tipo = "Timeout", TieneTimeout = true, RegistraEventos = false }
        };

        var resultado = _validador.Validar(politicas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no registra eventos"));
    }
    [Fact]
    public void Validar_RetryNoIdempotente_DevuelveError()
    {
        var politicas = new List<PoliticaResiliencia>
        {
            new() { Nombre = "X", Tipo = "Retry", NumeroDeReintentos = 2, OperacionIdempotente = false, TieneTimeout = true, RegistraEventos = true }
        };

        var resultado = _validador.Validar(politicas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara una operación idempotente"));
    }
    [Fact]
    public void Validar_CircuitBreakerConUnaMuestra_DevuelveError()
    {
        var politicas = new List<PoliticaResiliencia>
        {
            new() { Nombre = "X", Tipo = "CircuitBreaker", MinimoDeMuestras = 1, TieneTimeout = true, RegistraEventos = true }
        };

        var resultado = _validador.Validar(politicas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara mínimo de muestras"));
    }
    [Fact]
    public void Validar_CircuitBreakerConProporcionCero_DevuelveError()
    {
        var politicas = new List<PoliticaResiliencia>
        {
            new() { Nombre = "X", Tipo = "CircuitBreaker", MinimoDeMuestras = 4, ProporcionDeFallos = 0, TieneTimeout = true, RegistraEventos = true }
        };

        var resultado = _validador.Validar(politicas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("proporción de fallos fuera"));
    }
    [Fact]
    public void Validar_CircuitBreakerConProporcionInvalida_DevuelveError()
    {
        foreach (var proporcion in new[] { 1.1, double.NaN, double.PositiveInfinity, double.NegativeInfinity })
        {
            var politicas = new List<PoliticaResiliencia>
            {
                new() { Nombre = "X", Tipo = "CircuitBreaker", MinimoDeMuestras = 4, ProporcionDeFallos = proporcion, TieneTimeout = true, RegistraEventos = true }
            };

            var resultado = _validador.Validar(politicas);

            resultado.EsValida.Should().BeFalse();
            resultado.Errores.Should().Contain(e => e.Contains("proporción de fallos fuera"));
        }
    }
    [Fact]
    public void Validar_CircuitBreakerSinVentana_DevuelveError()
    {
        var politicas = new List<PoliticaResiliencia>
        {
            new() { Nombre = "X", Tipo = "CircuitBreaker", MinimoDeMuestras = 4, VentanaMuestreoSegundos = 0, TieneTimeout = true, RegistraEventos = true }
        };

        var resultado = _validador.Validar(politicas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("ventana de muestreo positiva"));
    }
    [Fact]
    public void Validar_CircuitBreakerSinDuracionApertura_DevuelveError()
    {
        var politicas = new List<PoliticaResiliencia>
        {
            new() { Nombre = "X", Tipo = "CircuitBreaker", MinimoDeMuestras = 4, DuracionAperturaSegundos = 0, TieneTimeout = true, RegistraEventos = true }
        };

        var resultado = _validador.Validar(politicas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("duración de apertura positiva"));
    }
}
