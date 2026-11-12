using AceriaApp.Api.ComunicacionAsincrona;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ComunicacionAsincrona.Tests;

public class ValidadorComunicacionAsincronaTests
{
    private readonly ValidadorComunicacionAsincrona _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoEventos.EventosPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinEventos_DevuelveError()
    {
        var resultado = _validador.Validar(new List<Evento>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay eventos"));
    }

    [Fact]
    public void Validar_TipoNoPermitido_DevuelveError()
    {
        var eventos = new List<Evento>
        {
            new() { Nombre = "X", Tipo = "TipoInventado", Publicador = "A", NumeroDeConsumidores = 1, TieneIdempotencia = true, TieneReintentos = true }
        };

        var resultado = _validador.Validar(eventos);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Tipo no permitido"));
    }

    [Fact]
    public void Validar_SinPublicador_DevuelveError()
    {
        var eventos = new List<Evento>
        {
            new() { Nombre = "X", Tipo = "Integracion", Publicador = string.Empty, NumeroDeConsumidores = 1, TieneIdempotencia = true, TieneReintentos = true }
        };

        var resultado = _validador.Validar(eventos);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara el publicador"));
    }

    [Fact]
    public void Validar_SinConsumidores_DevuelveError()
    {
        var eventos = new List<Evento>
        {
            new() { Nombre = "X", Tipo = "Integracion", Publicador = "A", NumeroDeConsumidores = 0, TieneIdempotencia = true, TieneReintentos = true }
        };

        var resultado = _validador.Validar(eventos);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene consumidores"));
    }

    [Fact]
    public void Validar_SinIdempotencia_DevuelveError()
    {
        var eventos = new List<Evento>
        {
            new() { Nombre = "X", Tipo = "Integracion", Publicador = "A", NumeroDeConsumidores = 1, TieneIdempotencia = false, TieneReintentos = true }
        };

        var resultado = _validador.Validar(eventos);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara idempotencia"));
    }

    [Fact]
    public void Validar_SinReintentos_DevuelveError()
    {
        var eventos = new List<Evento>
        {
            new() { Nombre = "X", Tipo = "Integracion", Publicador = "A", NumeroDeConsumidores = 1, TieneIdempotencia = true, TieneReintentos = false }
        };

        var resultado = _validador.Validar(eventos);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara reintentos"));
    }
    [Fact]
    public void Validar_EventoDominioLocalSinPoliticasDeEntrega_DevuelveValido()
    {
        var eventos = new List<Evento>
        {
            new() { Nombre = "OrdenPlanificada", Tipo = "Dominio", Publicador = "Produccion", NumeroDeConsumidores = 0 }
        };

        var resultado = _validador.Validar(eventos);

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }
}
