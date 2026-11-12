using AceriaApp.Api.DominioAceria;
using FluentAssertions;
using Xunit;

namespace AceriaApp.DominioAceria.Tests;

public class CatalogoAceriaTests
{
    [Fact]
    public void ElementosPorDefecto_ContieneDiezElementos()
    {
        var elementos = CatalogoAceria.ElementosPorDefecto();

        elementos.Should().HaveCount(10);
    }

    [Fact]
    public void ElementosPorDefecto_ContieneTresAgregados()
    {
        var elementos = CatalogoAceria.ElementosPorDefecto();

        elementos.Count(e => e.Tipo == "Agregado").Should().Be(3);
    }

    [Fact]
    public void ElementosPorDefecto_ContieneUnNucleo()
    {
        var elementos = CatalogoAceria.ElementosPorDefecto();

        elementos.Count(e => e.Contexto == "Produccion").Should().Be(4);
    }

    [Fact]
    public void ElementosPorDefecto_TodosTienenInvariantes()
    {
        var elementos = CatalogoAceria.ElementosPorDefecto();

        elementos.Should().OnlyContain(e => e.TieneInvariantes);
    }

    [Fact]
    public void ElementosPorDefecto_RaicesDeAgregadoSonAgregados()
    {
        var elementos = CatalogoAceria.ElementosPorDefecto();

        elementos.Where(e => e.EsRaizDeAgregado).Should().OnlyContain(e => e.Tipo == "Agregado");
    }
}
