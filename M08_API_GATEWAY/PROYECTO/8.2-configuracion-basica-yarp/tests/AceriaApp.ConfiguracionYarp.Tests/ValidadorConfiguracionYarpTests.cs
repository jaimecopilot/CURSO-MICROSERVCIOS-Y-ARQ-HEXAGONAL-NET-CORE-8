using AceriaApp.Api.ConfiguracionYarp;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ConfiguracionYarp.Tests;

public class ValidadorConfiguracionYarpTests
{
    private readonly ValidadorConfiguracionYarp _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoClusters.ClustersPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinClusters_DevuelveError()
    {
        var resultado = _validador.Validar(new List<ClusterYarp>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay clusters"));
    }

    [Fact]
    public void Validar_SinDestinos_DevuelveError()
    {
        var clusters = new List<ClusterYarp>
        {
            new() { Identificador = "X", Destinos = Array.Empty<string>(), TieneDireccionValida = true, TieneConfiguracionPorEntorno = true }
        };

        var resultado = _validador.Validar(clusters);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara destinos"));
    }

    [Fact]
    public void Validar_DireccionInvalida_DevuelveError()
    {
        var clusters = new List<ClusterYarp>
        {
            new() { Identificador = "X", Destinos = new[] { "http://x" }, TieneDireccionValida = false, TieneConfiguracionPorEntorno = true }
        };

        var resultado = _validador.Validar(clusters);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene dirección válida"));
    }

    [Fact]
    public void Validar_SinConfiguracionPorEntorno_DevuelveError()
    {
        var clusters = new List<ClusterYarp>
        {
            new() { Identificador = "X", Destinos = new[] { "http://x" }, TieneDireccionValida = true, TieneConfiguracionPorEntorno = false }
        };

        var resultado = _validador.Validar(clusters);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene configuración por entorno"));
    }
}
