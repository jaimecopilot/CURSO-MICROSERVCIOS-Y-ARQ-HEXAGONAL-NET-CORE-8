using AceriaApp.Api.Balanceo;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Balanceo.Tests;

public class ValidadorBalanceoTests
{
    private readonly ValidadorBalanceo _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoClustersBalanceo.ClustersPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinClusters_DevuelveError()
    {
        var resultado = _validador.Validar(new List<ClusterBalanceo>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay clusters"));
    }

    [Fact]
    public void Validar_PoliticaNoPermitida_DevuelveError()
    {
        var clusters = new List<ClusterBalanceo>
        {
            new() { Identificador = "X", Politica = "PoliticaInventada", NumeroDeDestinos = 2, CombinadoConHealthChecks = true }
        };

        var resultado = _validador.Validar(clusters);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Política no permitida"));
    }

    [Fact]
    public void Validar_MenosDeDosDestinos_DevuelveError()
    {
        var clusters = new List<ClusterBalanceo>
        {
            new() { Identificador = "X", Politica = "RoundRobin", NumeroDeDestinos = 1, CombinadoConHealthChecks = true }
        };

        var resultado = _validador.Validar(clusters);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene al menos dos destinos"));
    }

    [Fact]
    public void Validar_SinHealthChecks_DevuelveError()
    {
        var clusters = new List<ClusterBalanceo>
        {
            new() { Identificador = "X", Politica = "RoundRobin", NumeroDeDestinos = 2, CombinadoConHealthChecks = false }
        };

        var resultado = _validador.Validar(clusters);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no está combinado con health checks"));
    }
}
