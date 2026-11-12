using AceriaApp.Api.Balanceo;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Balanceo.Tests;

public class CatalogoClustersBalanceoTests
{
    [Fact]
    public void ClustersPorDefecto_ContieneTresClusters()
    {
        var clusters = CatalogoClustersBalanceo.ClustersPorDefecto();

        clusters.Should().HaveCount(3);
    }

    [Fact]
    public void ClustersPorDefecto_TodosTienenAlMenosDosDestinos()
    {
        var clusters = CatalogoClustersBalanceo.ClustersPorDefecto();

        clusters.Should().OnlyContain(c => c.NumeroDeDestinos >= 2);
    }

    [Fact]
    public void ClustersPorDefecto_TodosCombinadosConHealthChecks()
    {
        var clusters = CatalogoClustersBalanceo.ClustersPorDefecto();

        clusters.Should().OnlyContain(c => c.CombinadoConHealthChecks);
    }

    [Fact]
    public void ClustersPorDefecto_ContieneOrdenesInventarioYClientes()
    {
        var clusters = CatalogoClustersBalanceo.ClustersPorDefecto();

        clusters.Should().Contain(c => c.Identificador == "ordenes-cluster");
        clusters.Should().Contain(c => c.Identificador == "inventario-cluster");
        clusters.Should().Contain(c => c.Identificador == "clientes-cluster");
    }

    [Fact]
    public void ClustersPorDefecto_ContieneAlgunoConPesos()
    {
        var clusters = CatalogoClustersBalanceo.ClustersPorDefecto();

        clusters.Should().Contain(c => c.TienePesos);
    }
}
