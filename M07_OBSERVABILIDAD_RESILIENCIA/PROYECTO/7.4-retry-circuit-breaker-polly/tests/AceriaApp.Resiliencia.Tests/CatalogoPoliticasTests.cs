using AceriaApp.Api.Resiliencia;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Resiliencia.Tests;

public class CatalogoPoliticasTests
{
    [Fact]
    public void PoliticasPorDefecto_ContieneCincoPoliticas()
    {
        var politicas = CatalogoPoliticas.PoliticasPorDefecto();

        politicas.Should().HaveCount(5);
    }

    [Fact]
    public void PoliticasPorDefecto_ContieneDosRetry()
    {
        var politicas = CatalogoPoliticas.PoliticasPorDefecto();

        politicas.Count(p => p.Tipo == "Retry").Should().Be(2);
    }

    [Fact]
    public void PoliticasPorDefecto_ContieneDosCircuitBreaker()
    {
        var politicas = CatalogoPoliticas.PoliticasPorDefecto();

        politicas.Count(p => p.Tipo == "CircuitBreaker").Should().Be(2);
    }

    [Fact]
    public void PoliticasPorDefecto_ContieneUnTimeout()
    {
        var politicas = CatalogoPoliticas.PoliticasPorDefecto();

        politicas.Count(p => p.Tipo == "Timeout").Should().Be(1);
    }

    [Fact]
    public void PoliticasPorDefecto_TodasTienenTimeoutYRegistranEventos()
    {
        var politicas = CatalogoPoliticas.PoliticasPorDefecto();

        politicas.Should().OnlyContain(p => p.TieneTimeout);
        politicas.Should().OnlyContain(p => p.RegistraEventos);
    }
}
