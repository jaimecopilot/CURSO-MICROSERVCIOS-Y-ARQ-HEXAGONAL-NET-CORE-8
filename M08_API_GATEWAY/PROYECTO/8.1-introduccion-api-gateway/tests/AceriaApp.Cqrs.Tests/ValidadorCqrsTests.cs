using AceriaApp.Api.Cqrs;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Cqrs.Tests;

public class ValidadorCqrsTests
{
    private readonly ValidadorCqrs _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoCqrs.MensajesPorDefecto());

        resultado.EsValido.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinMensajes_DevuelveError()
    {
        var resultado = _validador.Validar(new List<MensajeCqrs>());

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay mensajes"));
    }

    [Fact]
    public void Validar_TipoNoPermitido_DevuelveError()
    {
        var mensajes = new List<MensajeCqrs>
        {
            new() { Nombre = "X", Tipo = "TipoInventado", TieneManejador = true, DevuelveResult = true }
        };

        var resultado = _validador.Validar(mensajes);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Tipo no permitido"));
    }

    [Fact]
    public void Validar_SinManejador_DevuelveError()
    {
        var mensajes = new List<MensajeCqrs>
        {
            new() { Nombre = "X", Tipo = "Command", TieneManejador = false, UsaEscritura = true, DevuelveResult = true }
        };

        var resultado = _validador.Validar(mensajes);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene manejador"));
    }

    [Fact]
    public void Validar_CommandSinEscritura_DevuelveError()
    {
        var mensajes = new List<MensajeCqrs>
        {
            new() { Nombre = "X", Tipo = "Command", TieneManejador = true, UsaEscritura = false, DevuelveResult = true }
        };

        var resultado = _validador.Validar(mensajes);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no usa escritura"));
    }

    [Fact]
    public void Validar_QuerySinSoloLectura_DevuelveError()
    {
        var mensajes = new List<MensajeCqrs>
        {
            new() { Nombre = "X", Tipo = "Query", TieneManejador = true, UsaSoloLectura = false, DevuelveResult = true }
        };

        var resultado = _validador.Validar(mensajes);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no es de solo lectura"));
    }

    [Fact]
    public void Validar_QueryConEscritura_DevuelveError()
    {
        var mensajes = new List<MensajeCqrs>
        {
            new() { Nombre = "X", Tipo = "Query", TieneManejador = true, UsaSoloLectura = true, UsaEscritura = true, DevuelveResult = true }
        };

        var resultado = _validador.Validar(mensajes);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("usa escritura"));
    }
}
