using AceriaApp.Api.ModeloDominio;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ModeloDominio.Tests;

public class CatalogoModeloTests
{
    [Fact]
    public void ElementosPorDefecto_ContieneSeisElementos()
    {
        var elementos = CatalogoModelo.ElementosPorDefecto();

        elementos.Should().HaveCount(6);
    }

    [Fact]
    public void ElementosPorDefecto_ContieneTresEntidades()
    {
        var elementos = CatalogoModelo.ElementosPorDefecto();

        elementos.Count(e => e.Tipo == "Entidad").Should().Be(3);
    }

    [Fact]
    public void ElementosPorDefecto_ContieneTresValueObjects()
    {
        var elementos = CatalogoModelo.ElementosPorDefecto();

        elementos.Count(e => e.Tipo == "ValueObject").Should().Be(3);
    }

    [Fact]
    public void ElementosPorDefecto_TodasLasEntidadesTienenIdentidad()
    {
        var elementos = CatalogoModelo.ElementosPorDefecto();

        elementos.Where(e => e.Tipo == "Entidad").Should().OnlyContain(e => e.TieneIdentidad);
    }

    [Fact]
    public void ElementosPorDefecto_TodosLosValueObjectsSonInmutables()
    {
        var elementos = CatalogoModelo.ElementosPorDefecto();

        elementos.Where(e => e.Tipo == "ValueObject").Should().OnlyContain(e => e.EsInmutable);
    }
}
