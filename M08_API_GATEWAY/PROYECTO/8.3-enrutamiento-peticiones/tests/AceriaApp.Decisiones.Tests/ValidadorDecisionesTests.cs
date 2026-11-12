using AceriaApp.Api.Decisiones;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Decisiones.Tests;

public class ValidadorDecisionesTests
{
    private readonly ValidadorDecisiones _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoDecisiones.DecisionesPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinDecisiones_DevuelveError()
    {
        var resultado = _validador.Validar(new List<DecisionComunicacion>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay decisiones"));
    }

    [Fact]
    public void Validar_EnfoqueNoPermitido_DevuelveError()
    {
        var decisiones = new List<DecisionComunicacion>
        {
            new() { Interaccion = "X", Enfoque = "EnfoqueInventado" }
        };

        var resultado = _validador.Validar(decisiones);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Enfoque no permitido"));
    }

    [Fact]
    public void Validar_SincronaSinRespuestaInmediata_DevuelveValido()
    {
        var decisiones = new List<DecisionComunicacion>
        {
            new() { Interaccion = "X", Enfoque = "Sincrona", RequiereRespuestaInmediata = false }
        };

        var resultado = _validador.Validar(decisiones);

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_AsincronaSinToleranciaEventual_DevuelveError()
    {
        var decisiones = new List<DecisionComunicacion>
        {
            new() { Interaccion = "X", Enfoque = "Asincrona", ToleraConsistenciaEventual = false }
        };

        var resultado = _validador.Validar(decisiones);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tolera consistencia eventual"));
    }

    [Fact]
    public void Validar_HibridaSinPatron_DevuelveError()
    {
        var decisiones = new List<DecisionComunicacion>
        {
            new() { Interaccion = "X", Enfoque = "Hibrida", TienePatronHibrido = false }
        };

        var resultado = _validador.Validar(decisiones);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara patrón híbrido"));
    }
    [Fact]
    public void Validar_AsincronaConRespuestaInmediata_DevuelveError()
    {
        var decisiones = new List<DecisionComunicacion>
        {
            new() { Interaccion = "X", Enfoque = "Asincrona", RequiereRespuestaInmediata = true, ToleraConsistenciaEventual = true }
        };

        var resultado = _validador.Validar(decisiones);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("requiere respuesta inmediata del consumidor"));
    }
}
