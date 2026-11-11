using AceriaApp.Api.Cqrs;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Cqrs.Tests;

public class CatalogoCqrsTests
{
    [Fact]
    public void MensajesPorDefecto_ContieneCuatroMensajes()
    {
        var mensajes = CatalogoCqrs.MensajesPorDefecto();

        mensajes.Should().HaveCount(4);
    }

    [Fact]
    public void MensajesPorDefecto_ContieneDosCommandsYDosQueries()
    {
        var mensajes = CatalogoCqrs.MensajesPorDefecto();

        mensajes.Count(m => m.Tipo == "Command").Should().Be(2);
        mensajes.Count(m => m.Tipo == "Query").Should().Be(2);
    }

    [Fact]
    public void MensajesPorDefecto_CommandsUsanEscritura()
    {
        var mensajes = CatalogoCqrs.MensajesPorDefecto();

        mensajes.Where(m => m.Tipo == "Command").Should().OnlyContain(m => m.UsaEscritura);
    }

    [Fact]
    public void MensajesPorDefecto_QueriesSonDeSoloLectura()
    {
        var mensajes = CatalogoCqrs.MensajesPorDefecto();

        mensajes.Where(m => m.Tipo == "Query").Should().OnlyContain(m => m.UsaSoloLectura);
    }

    [Fact]
    public void MensajesPorDefecto_TodosDevuelvenResult()
    {
        var mensajes = CatalogoCqrs.MensajesPorDefecto();

        mensajes.Should().OnlyContain(m => m.DevuelveResult);
    }
}
