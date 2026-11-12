using AceriaApp.Api.Enrutamiento;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Enrutamiento.Tests;

public class ValidadorEnrutamientoTests
{
    private readonly ValidadorEnrutamiento _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValida()
    {
        var resultado = _validador.Validar(CatalogoReglasEnrutamiento.ReglasPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinReglas_DevuelveError()
    {
        var resultado = _validador.Validar(new List<ReglaEnrutamiento>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay reglas"));
    }

    [Fact]
    public void Validar_MetodoNoPermitido_DevuelveError()
    {
        var reglas = new List<ReglaEnrutamiento>
        {
            new() { Patron = "/api/v1/x", MetodoHttp = "TRACE", Orden = 1, TieneTransformacionDeRuta = true }
        };

        var resultado = _validador.Validar(reglas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Método HTTP no permitido"));
    }

    [Fact]
    public void Validar_OrdenNegativo_DevuelveError()
    {
        var reglas = new List<ReglaEnrutamiento>
        {
            new() { Patron = "/api/v1/x", MetodoHttp = "GET", Orden = -1, TieneTransformacionDeRuta = true }
        };

        var resultado = _validador.Validar(reglas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("orden de la regla"));
    }

    [Fact]
    public void Validar_SinTransformaciones_DevuelveError()
    {
        var reglas = new List<ReglaEnrutamiento>
        {
            new() { Patron = "/api/v1/x", MetodoHttp = "GET", Orden = 1 }
        };

        var resultado = _validador.Validar(reglas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara ninguna transformación"));
    }
}
