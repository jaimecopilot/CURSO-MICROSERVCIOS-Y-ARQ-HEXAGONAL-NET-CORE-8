using AceriaApp.Api.Mediator;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Mediator.Tests;

public class CatalogoMensajesTests
{
    [Fact]
    public void MensajesPorDefecto_ContieneCincoMensajes()
    {
        var mensajes = CatalogoMensajes.MensajesPorDefecto();

        mensajes.Should().HaveCount(5);
    }

    [Fact]
    public void MensajesPorDefecto_ContieneDosComandos()
    {
        var mensajes = CatalogoMensajes.MensajesPorDefecto();

        mensajes.Count(m => m.Tipo == "Comando").Should().Be(2);
    }

    [Fact]
    public void MensajesPorDefecto_ContieneDosConsultas()
    {
        var mensajes = CatalogoMensajes.MensajesPorDefecto();

        mensajes.Count(m => m.Tipo == "Consulta").Should().Be(2);
    }

    [Fact]
    public void MensajesPorDefecto_ContieneUnaNotificacion()
    {
        var mensajes = CatalogoMensajes.MensajesPorDefecto();

        mensajes.Count(m => m.Tipo == "Notificacion").Should().Be(1);
    }

    [Fact]
    public void MensajesPorDefecto_TodosTienenManejador()
    {
        var mensajes = CatalogoMensajes.MensajesPorDefecto();

        mensajes.Should().OnlyContain(m => m.TieneManejador);
    }
}
