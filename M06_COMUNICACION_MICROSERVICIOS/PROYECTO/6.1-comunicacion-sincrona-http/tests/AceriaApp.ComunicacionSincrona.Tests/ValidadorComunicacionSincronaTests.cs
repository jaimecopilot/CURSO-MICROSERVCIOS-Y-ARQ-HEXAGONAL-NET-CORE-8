using AceriaApp.Api.ComunicacionSincrona;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ComunicacionSincrona.Tests;

public class ValidadorComunicacionSincronaTests
{
    private readonly ValidadorComunicacionSincrona _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoLlamadas.LlamadasPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinLlamadas_DevuelveError()
    {
        var resultado = _validador.Validar(new List<LlamadaSincrona>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay llamadas"));
    }

    [Fact]
    public void Validar_MismoOrigenYDestino_DevuelveError()
    {
        var llamadas = new List<LlamadaSincrona>
        {
            new() { ServicioOrigen = "Ordenes.Api", ServicioDestino = "Ordenes.Api", Metodo = "GET", TieneTimeout = true, TieneReintentos = true }
        };

        var resultado = _validador.Validar(llamadas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("apunta al mismo servicio"));
    }

    [Fact]
    public void Validar_MetodoNoPermitido_DevuelveError()
    {
        var llamadas = new List<LlamadaSincrona>
        {
            new() { ServicioOrigen = "A", ServicioDestino = "B", Metodo = "CONNECT", TieneTimeout = true, TieneReintentos = true }
        };

        var resultado = _validador.Validar(llamadas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Método no permitido"));
    }

    [Fact]
    public void Validar_SinTimeout_DevuelveError()
    {
        var llamadas = new List<LlamadaSincrona>
        {
            new() { ServicioOrigen = "A", ServicioDestino = "B", Metodo = "GET", TieneTimeout = false, TieneReintentos = true }
        };

        var resultado = _validador.Validar(llamadas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene timeout"));
    }

    [Fact]
    public void Validar_PostSinReintentos_DevuelveValido()
    {
        var llamadas = new List<LlamadaSincrona>
        {
            new() { ServicioOrigen = "A", ServicioDestino = "B", Metodo = "POST", TieneTimeout = true, TieneReintentos = false }
        };

        var resultado = _validador.Validar(llamadas);

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }
    [Fact]
    public void Validar_PostConReintentosSinIdempotencia_DevuelveError()
    {
        var llamadas = new List<LlamadaSincrona>
        {
            new() { ServicioOrigen = "A", ServicioDestino = "B", Metodo = "POST", TieneTimeout = true, TieneReintentos = true }
        };

        var resultado = _validador.Validar(llamadas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("reintentos no seguros"));
    }

    [Fact]
    public void Validar_PostConReintentosYClaveIdempotente_DevuelveValido()
    {
        var llamadas = new List<LlamadaSincrona>
        {
            new() { ServicioOrigen = "A", ServicioDestino = "B", Metodo = "POST", TieneTimeout = true, TieneReintentos = true, TieneClaveIdempotencia = true }
        };

        var resultado = _validador.Validar(llamadas);

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }
}
