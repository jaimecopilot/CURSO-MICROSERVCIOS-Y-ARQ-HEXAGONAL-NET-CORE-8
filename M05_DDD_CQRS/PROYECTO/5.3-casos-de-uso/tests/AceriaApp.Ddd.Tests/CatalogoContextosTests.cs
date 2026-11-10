using AceriaApp.Api.Ddd;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Ddd.Tests;

public class CatalogoContextosTests
{
    [Fact]
    public void ContextosPorDefecto_ContieneCuatroContextos()
    {
        var contextos = CatalogoContextos.ContextosPorDefecto();

        contextos.Should().HaveCount(4);
    }

    [Fact]
    public void ContextosPorDefecto_ContieneUnNucleo()
    {
        var contextos = CatalogoContextos.ContextosPorDefecto();

        contextos.Count(c => c.TipoDeSubdominio == "Nucleo").Should().Be(1);
    }

    [Fact]
    public void ContextosPorDefecto_ContieneDosSoportes()
    {
        var contextos = CatalogoContextos.ContextosPorDefecto();

        contextos.Count(c => c.TipoDeSubdominio == "Soporte").Should().Be(2);
    }

    [Fact]
    public void ContextosPorDefecto_ContieneUnGenerico()
    {
        var contextos = CatalogoContextos.ContextosPorDefecto();

        contextos.Count(c => c.TipoDeSubdominio == "Generico").Should().Be(1);
    }

    [Fact]
    public void ContextosPorDefecto_NingunoComparteModelo()
    {
        var contextos = CatalogoContextos.ContextosPorDefecto();

        contextos.Should().OnlyContain(c => !c.ComparteModeloConOtro);
    }
}
