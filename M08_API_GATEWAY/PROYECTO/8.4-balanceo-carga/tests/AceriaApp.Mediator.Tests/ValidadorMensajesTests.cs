using AceriaApp.Api.Mediator;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Mediator.Tests;

public class ValidadorMensajesTests
{
    private readonly ValidadorMensajes _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoMensajes.MensajesPorDefecto());

        resultado.EsValido.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinMensajes_DevuelveError()
    {
        var resultado = _validador.Validar(new List<Mensaje>());

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay mensajes"));
    }

    [Fact]
    public void Validar_TipoNoPermitido_DevuelveError()
    {
        var mensajes = new List<Mensaje>
        {
            new() { Nombre = "MensajeX", Tipo = "TipoInventado", TieneManejador = true }
        };

        var resultado = _validador.Validar(mensajes);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Tipo de mensaje no permitido"));
    }

    [Fact]
    public void Validar_SinManejador_DevuelveError()
    {
        var mensajes = new List<Mensaje>
        {
            new() { Nombre = "MensajeX", Tipo = "Comando", TieneManejador = false }
        };

        var resultado = _validador.Validar(mensajes);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene manejador"));
    }

    [Fact]
    public void Validar_NotificacionConResultado_DevuelveError()
    {
        var mensajes = new List<Mensaje>
        {
            new() { Nombre = "NotificacionX", Tipo = "Notificacion", TieneManejador = true, DevuelveResultado = true }
        };

        var resultado = _validador.Validar(mensajes);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no puede devolver resultado"));
    }
}
