using AceriaApp.Api.ModeloDominio;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ModeloDominio.Tests;

public class ValidadorModeloDominioTests
{
    private readonly ValidadorModeloDominio _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoModelo.ElementosPorDefecto());

        resultado.EsValido.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinElementos_DevuelveError()
    {
        var resultado = _validador.Validar(new List<ElementoModelo>());

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay elementos"));
    }

    [Fact]
    public void Validar_TipoNoPermitido_DevuelveError()
    {
        var elementos = new List<ElementoModelo>
        {
            new() { Nombre = "X", Tipo = "TipoInventado", TieneIdentidad = true }
        };

        var resultado = _validador.Validar(elementos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Tipo no permitido"));
    }

    [Fact]
    public void Validar_EntidadSinIdentidad_DevuelveError()
    {
        var elementos = new List<ElementoModelo>
        {
            new() { Nombre = "X", Tipo = "Entidad", TieneIdentidad = false, ValidaInvariantes = true }
        };

        var resultado = _validador.Validar(elementos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene identidad"));
    }

    [Fact]
    public void Validar_ValueObjectConIdentidad_DevuelveError()
    {
        var elementos = new List<ElementoModelo>
        {
            new() { Nombre = "X", Tipo = "ValueObject", TieneIdentidad = true, EsInmutable = true, ValidaInvariantes = true }
        };

        var resultado = _validador.Validar(elementos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no debería tener identidad"));
    }

    [Fact]
    public void Validar_ValueObjectMutable_DevuelveError()
    {
        var elementos = new List<ElementoModelo>
        {
            new() { Nombre = "X", Tipo = "ValueObject", TieneIdentidad = false, EsInmutable = false, ValidaInvariantes = true }
        };

        var resultado = _validador.Validar(elementos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no es inmutable"));
    }

    [Fact]
    public void Validar_SinValidarInvariantes_DevuelveError()
    {
        var elementos = new List<ElementoModelo>
        {
            new() { Nombre = "X", Tipo = "Entidad", TieneIdentidad = true, ValidaInvariantes = false }
        };

        var resultado = _validador.Validar(elementos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no valida invariantes"));
    }
}
