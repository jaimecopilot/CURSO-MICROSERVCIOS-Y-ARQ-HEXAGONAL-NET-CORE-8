using AceriaApp.Api.Decisiones;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Decisiones.Tests;

public class CatalogoDecisionesTests
{
    [Fact]
    public void DecisionesPorDefecto_ContieneCincoDecisiones()
    {
        var decisiones = CatalogoDecisiones.DecisionesPorDefecto();

        decisiones.Should().HaveCount(5);
    }

    [Fact]
    public void DecisionesPorDefecto_ContieneDosSincronas()
    {
        var decisiones = CatalogoDecisiones.DecisionesPorDefecto();

        decisiones.Count(d => d.Enfoque == "Sincrona").Should().Be(2);
    }

    [Fact]
    public void DecisionesPorDefecto_ContieneDosAsincronas()
    {
        var decisiones = CatalogoDecisiones.DecisionesPorDefecto();

        decisiones.Count(d => d.Enfoque == "Asincrona").Should().Be(2);
    }

    [Fact]
    public void DecisionesPorDefecto_ContieneUnaHibrida()
    {
        var decisiones = CatalogoDecisiones.DecisionesPorDefecto();

        decisiones.Count(d => d.Enfoque == "Hibrida").Should().Be(1);
    }

    [Fact]
    public void DecisionesPorDefecto_HibridaTienePatron()
    {
        var decisiones = CatalogoDecisiones.DecisionesPorDefecto();

        decisiones.Where(d => d.Enfoque == "Hibrida").Should().OnlyContain(d => d.TienePatronHibrido);
    }
}
