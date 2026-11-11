using AceriaApp.Api.DominioAceria;
using FluentAssertions;
using Xunit;

namespace AceriaApp.DominioAceria.Tests;

public class ValidadorDominioAceriaTests
{
    private readonly ValidadorDominioAceria _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoAceria.ElementosPorDefecto());

        resultado.EsValido.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinElementos_DevuelveError()
    {
        var resultado = _validador.Validar(new List<ElementoAceria>());

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay elementos"));
    }

    [Fact]
    public void Validar_ContextoNoPermitido_DevuelveError()
    {
        var elementos = new List<ElementoAceria>
        {
            new() { Nombre = "X", Contexto = "ContextoInventado", Tipo = "Entidad", TieneInvariantes = true }
        };

        var resultado = _validador.Validar(elementos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Contexto no permitido"));
    }

    [Fact]
    public void Validar_TipoNoPermitido_DevuelveError()
    {
        var elementos = new List<ElementoAceria>
        {
            new() { Nombre = "X", Contexto = "Produccion", Tipo = "TipoInventado", TieneInvariantes = true }
        };

        var resultado = _validador.Validar(elementos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Tipo no permitido"));
    }

    [Fact]
    public void Validar_SinInvariantes_DevuelveError()
    {
        var elementos = new List<ElementoAceria>
        {
            new() { Nombre = "X", Contexto = "Produccion", Tipo = "Entidad", TieneInvariantes = false }
        };

        var resultado = _validador.Validar(elementos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene invariantes"));
    }
}
