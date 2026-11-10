using AceriaApp.Api.Capas;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Capas.Tests;

public class ValidadorReglaDependenciaTests
{
    private readonly ValidadorReglaDependencia _validador = new(CatalogoCapas.ReglasPorDefecto());

    [Fact]
    public void Validar_PresentacionDependeDeAplicacion_DevuelveValida()
    {
        var resultado = _validador.Validar("Presentacion", "Aplicacion");

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_AplicacionDependeDeDominio_DevuelveValida()
    {
        var resultado = _validador.Validar("Aplicacion", "Dominio");

        resultado.EsValida.Should().BeTrue();
    }

    [Fact]
    public void Validar_DominioDependeDeAplicacion_DevuelveError()
    {
        var resultado = _validador.Validar("Dominio", "Aplicacion");

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no puede depender"));
    }

    [Fact]
    public void Validar_CapaOrigenDesconocida_DevuelveError()
    {
        var resultado = _validador.Validar("CapaInventada", "Dominio");

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("desconocida"));
    }
}
