using AceriaApp.Api.Logging;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Logging.Tests;

public class ValidadorLoggingTests
{
    private readonly ValidadorLogging _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoLogging.ConfiguracionesPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinConfiguraciones_DevuelveError()
    {
        var resultado = _validador.Validar(new List<ConfiguracionLogging>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay configuraciones"));
    }

    [Fact]
    public void Validar_NivelNoPermitido_DevuelveError()
    {
        var configuraciones = new List<ConfiguracionLogging>
        {
            new() { NivelMinimo = "NivelInventado", UsaLoggingEstructurado = true, TieneCorrelacion = true, EvitaDatosSensibles = true, ConfiguradoPorEntorno = true }
        };

        var resultado = _validador.Validar(configuraciones);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Nivel mínimo no permitido"));
    }

    [Fact]
    public void Validar_SinLoggingEstructurado_DevuelveError()
    {
        var configuraciones = new List<ConfiguracionLogging>
        {
            new() { NivelMinimo = "Information", UsaLoggingEstructurado = false, TieneCorrelacion = true, EvitaDatosSensibles = true, ConfiguradoPorEntorno = true }
        };

        var resultado = _validador.Validar(configuraciones);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no usa logging estructurado"));
    }

    [Fact]
    public void Validar_SinCorrelacion_DevuelveError()
    {
        var configuraciones = new List<ConfiguracionLogging>
        {
            new() { NivelMinimo = "Information", UsaLoggingEstructurado = true, TieneCorrelacion = false, EvitaDatosSensibles = true, ConfiguradoPorEntorno = true }
        };

        var resultado = _validador.Validar(configuraciones);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene correlación"));
    }

    [Fact]
    public void Validar_DatosSensibles_DevuelveError()
    {
        var configuraciones = new List<ConfiguracionLogging>
        {
            new() { NivelMinimo = "Information", UsaLoggingEstructurado = true, TieneCorrelacion = true, EvitaDatosSensibles = false, ConfiguradoPorEntorno = true }
        };

        var resultado = _validador.Validar(configuraciones);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no evita datos sensibles"));
    }

    [Fact]
    public void Validar_SinConfiguracionPorEntorno_DevuelveError()
    {
        var configuraciones = new List<ConfiguracionLogging>
        {
            new() { NivelMinimo = "Information", UsaLoggingEstructurado = true, TieneCorrelacion = true, EvitaDatosSensibles = true, ConfiguradoPorEntorno = false }
        };

        var resultado = _validador.Validar(configuraciones);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no está configurada por entorno"));
    }
}
