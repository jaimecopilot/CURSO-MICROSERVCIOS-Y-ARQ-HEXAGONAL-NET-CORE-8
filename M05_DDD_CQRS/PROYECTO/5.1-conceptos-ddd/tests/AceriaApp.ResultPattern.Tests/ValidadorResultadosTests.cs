using AceriaApp.Api.ResultPattern;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ResultPattern.Tests;

public class ValidadorResultadosTests
{
    private readonly ValidadorResultados _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoResultados.OperacionesPorDefecto());

        resultado.EsValido.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinOperaciones_DevuelveError()
    {
        var resultado = _validador.Validar(new List<ResultadoOperacion>());

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay operaciones"));
    }

    [Fact]
    public void Validar_SinNombre_DevuelveError()
    {
        var operaciones = new List<ResultadoOperacion>
        {
            new() { Nombre = string.Empty, UsaResult = true }
        };

        var resultado = _validador.Validar(operaciones);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara el nombre"));
    }

    [Fact]
    public void Validar_ErroresEsperadosSinResult_DevuelveError()
    {
        var operaciones = new List<ResultadoOperacion>
        {
            new() { Nombre = "OperacionX", UsaResult = false, NumeroDeErroresEsperados = 2 }
        };

        var resultado = _validador.Validar(operaciones);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no usa el patrón Result"));
    }

    [Fact]
    public void Validar_ExcepcionesParaErroresEsperados_DevuelveError()
    {
        var operaciones = new List<ResultadoOperacion>
        {
            new() { Nombre = "OperacionX", UsaResult = true, UsaExcepcionesParaErroresEsperados = true }
        };

        var resultado = _validador.Validar(operaciones);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("usa excepciones"));
    }
}
