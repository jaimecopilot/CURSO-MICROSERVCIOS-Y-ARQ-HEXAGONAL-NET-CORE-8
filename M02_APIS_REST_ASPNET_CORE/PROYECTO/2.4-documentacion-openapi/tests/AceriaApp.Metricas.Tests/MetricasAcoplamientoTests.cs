using AceriaApp.Monolito.Api.Metricas;
using FluentAssertions;
using Xunit;
namespace AceriaApp.Metricas.Tests;
public class MetricasAcoplamientoTests
{
    [Fact]
    public void IndiceAcoplamiento_SinProyectos_DevuelveCero()
    {
        var metricas = new MetricasAcoplamiento { NumeroDeProyectos = 0 };
        metricas.IndiceAcoplamiento().Should().Be(0);
    }
    [Fact]
    public void IndiceAcoplamiento_ConProyectos_DevuelveRatio()
    {
        var metricas = new MetricasAcoplamiento
        {
            NumeroDeProyectos = 4, NumeroDeReferenciasEntreProyectos = 8
        };
        metricas.IndiceAcoplamiento().Should().Be(2.0);
    }
    [Fact]
    public void IndiceComparticionDeDatos_SinProyectos_DevuelveCero()
    {
        var metricas = new MetricasAcoplamiento { NumeroDeProyectos = 0, NumeroDeTablasCompartidas = 3 };
        metricas.IndiceComparticionDeDatos().Should().Be(0);
    }
}
