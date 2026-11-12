using AceriaApp.Api.ComunicacionAsincrona;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ComunicacionAsincrona.Tests;

public class CatalogoEventosTests
{
    [Fact]
    public void EventosPorDefecto_ContieneCuatroEventos()
    {
        var eventos = CatalogoEventos.EventosPorDefecto();

        eventos.Should().HaveCount(4);
    }

    [Fact]
    public void EventosPorDefecto_TodosDeIntegracion()
    {
        var eventos = CatalogoEventos.EventosPorDefecto();

        eventos.Should().OnlyContain(e => e.Tipo == "Integracion");
    }

    [Fact]
    public void EventosPorDefecto_TodosTienenIdempotencia()
    {
        var eventos = CatalogoEventos.EventosPorDefecto();

        eventos.Should().OnlyContain(e => e.TieneIdempotencia);
    }

    [Fact]
    public void EventosPorDefecto_TodosTienenReintentos()
    {
        var eventos = CatalogoEventos.EventosPorDefecto();

        eventos.Should().OnlyContain(e => e.TieneReintentos);
    }

    [Fact]
    public void EventosPorDefecto_TodosTienenConsumidores()
    {
        var eventos = CatalogoEventos.EventosPorDefecto();

        eventos.Should().OnlyContain(e => e.NumeroDeConsumidores >= 1);
    }
}
