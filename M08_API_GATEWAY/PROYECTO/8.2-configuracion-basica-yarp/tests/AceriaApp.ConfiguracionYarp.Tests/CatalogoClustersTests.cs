using AceriaApp.Api.ConfiguracionYarp;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ConfiguracionYarp.Tests;

public class CatalogoClustersTests
{
    [Fact]
    public void ClustersPorDefecto_ContieneTresClusters()
    {
        var clusters = CatalogoClusters.ClustersPorDefecto();

        clusters.Should().HaveCount(3);
    }

    [Fact]
    public void ClustersPorDefecto_ContieneOrdenesInventarioYClientes()
    {
        var clusters = CatalogoClusters.ClustersPorDefecto();

        clusters.Should().Contain(c => c.Identificador == "ordenes-cluster");
        clusters.Should().Contain(c => c.Identificador == "inventario-cluster");
        clusters.Should().Contain(c => c.Identificador == "clientes-cluster");
    }

    [Fact]
    public void ClustersPorDefecto_TodosTienenDestinos()
    {
        var clusters = CatalogoClusters.ClustersPorDefecto();

        clusters.Should().OnlyContain(c => c.Destinos.Count > 0);
    }

    [Fact]
    public void ClustersPorDefecto_TodosTienenDireccionValida()
    {
        var clusters = CatalogoClusters.ClustersPorDefecto();

        clusters.Should().OnlyContain(c => c.TieneDireccionValida);
    }

    [Fact]
    public void ClustersPorDefecto_TodosTienenConfiguracionPorEntorno()
    {
        var clusters = CatalogoClusters.ClustersPorDefecto();

        clusters.Should().OnlyContain(c => c.TieneConfiguracionPorEntorno);
    }
}
