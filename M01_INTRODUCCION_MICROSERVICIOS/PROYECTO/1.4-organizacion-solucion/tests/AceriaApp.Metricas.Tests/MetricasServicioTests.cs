using AceriaApp.Monolito.Api.Metricas;
using FluentAssertions;
using Xunit;
namespace AceriaApp.Metricas.Tests;
public class MetricasServicioTests
{
    [Fact]
    public void EsCandidatoAExtraccion_ConPocasDependencias_DevuelveTrue()
    {
        var metricas = new MetricasServicio
        {
            Nombre = "Inventario", NumeroDeEndpoints = 3,
            NumeroDeTablas = 2, NumeroDeDependenciasExternas = 1
        };
        metricas.EsCandidatoAExtraccion().Should().BeTrue();
    }
    [Fact]
    public void EsCandidatoAExtraccion_ConMuchasDependencias_DevuelveFalse()
    {
        var metricas = new MetricasServicio
        {
            Nombre = "Ordenes", NumeroDeEndpoints = 5,
            NumeroDeTablas = 4, NumeroDeDependenciasExternas = 3
        };
        metricas.EsCandidatoAExtraccion().Should().BeFalse();
    }
    [Fact]
    public void IndiceDeComplejidad_SumaDePropiedades()
    {
        var metricas = new MetricasServicio
        {
            NumeroDeEndpoints = 3, NumeroDeTablas = 2,
            NumeroDeDependenciasExternas = 1
        };
        metricas.IndiceDeComplejidad().Should().Be(6);
    }
}
