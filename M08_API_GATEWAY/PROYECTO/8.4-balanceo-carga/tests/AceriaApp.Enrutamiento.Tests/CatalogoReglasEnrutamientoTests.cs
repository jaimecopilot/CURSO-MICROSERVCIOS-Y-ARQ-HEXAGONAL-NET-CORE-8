using AceriaApp.Api.Enrutamiento;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Enrutamiento.Tests;

public class CatalogoReglasEnrutamientoTests
{
    [Fact]
    public void ReglasPorDefecto_ContieneCuatroReglas()
    {
        var reglas = CatalogoReglasEnrutamiento.ReglasPorDefecto();

        reglas.Should().HaveCount(4);
    }

    [Fact]
    public void ReglasPorDefecto_OrdenadasAscendentemente()
    {
        var reglas = CatalogoReglasEnrutamiento.ReglasPorDefecto();

        var ordenes = reglas.Select(r => r.Orden).ToList();
        ordenes.Should().BeInAscendingOrder();
    }

    [Fact]
    public void ReglasPorDefecto_TodasTienenTransformacionDeRuta()
    {
        var reglas = CatalogoReglasEnrutamiento.ReglasPorDefecto();

        reglas.Should().OnlyContain(r => r.TieneTransformacionDeRuta);
    }

    [Fact]
    public void ReglasPorDefecto_TodasTienenTransformacionDeCabecera()
    {
        var reglas = CatalogoReglasEnrutamiento.ReglasPorDefecto();

        reglas.Should().OnlyContain(r => r.TieneTransformacionDeCabecera);
    }

    [Fact]
    public void ReglasPorDefecto_PrimeraReglaEsOrdenesPorId()
    {
        var reglas = CatalogoReglasEnrutamiento.ReglasPorDefecto();

        reglas[0].Patron.Should().Be("/api/v1/ordenes/{id:guid}");
    }
}
