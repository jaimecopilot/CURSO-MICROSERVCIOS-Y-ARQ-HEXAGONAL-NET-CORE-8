using AceriaApp.Api.CasosDeUso;
using FluentAssertions;
using Xunit;

namespace AceriaApp.CasosDeUso.Tests;

public class ValidadorCasosDeUsoTests
{
    private readonly ValidadorCasosDeUso _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoCasosDeUso.CasosPorDefecto());

        resultado.EsValido.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinCasos_DevuelveError()
    {
        var resultado = _validador.Validar(new List<CasoDeUso>());

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay casos de uso"));
    }

    [Fact]
    public void Validar_TipoNoPermitido_DevuelveError()
    {
        var casos = new List<CasoDeUso>
        {
            new() { Nombre = "X", Tipo = "TipoInventado", TieneManejador = true, DevuelveResult = true }
        };

        var resultado = _validador.Validar(casos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Tipo no permitido"));
    }

    [Fact]
    public void Validar_SinManejador_DevuelveError()
    {
        var casos = new List<CasoDeUso>
        {
            new() { Nombre = "X", Tipo = "Lectura", TieneManejador = false, DevuelveResult = true }
        };

        var resultado = _validador.Validar(casos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene manejador"));
    }

    [Fact]
    public void Validar_SinResult_DevuelveError()
    {
        var casos = new List<CasoDeUso>
        {
            new() { Nombre = "X", Tipo = "Lectura", TieneManejador = true, DevuelveResult = false }
        };

        var resultado = _validador.Validar(casos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no devuelve Result"));
    }

    [Fact]
    public void Validar_EscrituraSinUnidadDeTrabajo_DevuelveError()
    {
        var casos = new List<CasoDeUso>
        {
            new() { Nombre = "X", Tipo = "Escritura", TieneManejador = true, DevuelveResult = true, CoordinaUnidadDeTrabajo = false }
        };

        var resultado = _validador.Validar(casos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no coordina la unidad de trabajo"));
    }

    [Fact]
    public void Validar_ConReglasDeNegocio_DevuelveError()
    {
        var casos = new List<CasoDeUso>
        {
            new() { Nombre = "X", Tipo = "Lectura", TieneManejador = true, DevuelveResult = true, ContieneReglasDeNegocio = true }
        };

        var resultado = _validador.Validar(casos);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("contiene reglas de negocio"));
    }
}
