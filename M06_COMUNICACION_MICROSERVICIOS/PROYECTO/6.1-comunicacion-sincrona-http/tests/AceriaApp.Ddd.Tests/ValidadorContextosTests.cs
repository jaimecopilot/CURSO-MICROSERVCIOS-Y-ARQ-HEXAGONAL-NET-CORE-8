using AceriaApp.Api.Ddd;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Ddd.Tests;

public class ValidadorContextosTests
{
    private readonly ValidadorContextos _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoContextos.ContextosPorDefecto());

        resultado.EsValido.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinContextos_DevuelveError()
    {
        var resultado = _validador.Validar(new List<ContextoDelimitado>());

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay contextos"));
    }

    [Fact]
    public void Validar_TipoNoPermitido_DevuelveError()
    {
        var contextos = new List<ContextoDelimitado>
        {
            new() { Nombre = "ContextoX", TipoDeSubdominio = "TipoInventado", LenguajeUbicuo = "lenguaje", TieneModeloPropio = true }
        };

        var resultado = _validador.Validar(contextos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Tipo de subdominio no permitido"));
    }

    [Fact]
    public void Validar_SinLenguajeUbicuo_DevuelveError()
    {
        var contextos = new List<ContextoDelimitado>
        {
            new() { Nombre = "ContextoX", TipoDeSubdominio = "Nucleo", LenguajeUbicuo = string.Empty, TieneModeloPropio = true }
        };

        var resultado = _validador.Validar(contextos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara lenguaje ubicuo"));
    }

    [Fact]
    public void Validar_SinModeloPropio_DevuelveError()
    {
        var contextos = new List<ContextoDelimitado>
        {
            new() { Nombre = "ContextoX", TipoDeSubdominio = "Nucleo", LenguajeUbicuo = "lenguaje", TieneModeloPropio = false }
        };

        var resultado = _validador.Validar(contextos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene modelo propio"));
    }

    [Fact]
    public void Validar_ModeloCompartido_DevuelveError()
    {
        var contextos = new List<ContextoDelimitado>
        {
            new() { Nombre = "ContextoX", TipoDeSubdominio = "Nucleo", LenguajeUbicuo = "lenguaje", TieneModeloPropio = true, ComparteModeloConOtro = true }
        };

        var resultado = _validador.Validar(contextos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("comparte modelo"));
    }
}
