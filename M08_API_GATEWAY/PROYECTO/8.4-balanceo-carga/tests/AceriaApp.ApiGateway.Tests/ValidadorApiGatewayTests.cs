using AceriaApp.Api.ApiGateway;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ApiGateway.Tests;

public class ValidadorApiGatewayTests
{
    private readonly ValidadorApiGateway _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoRutas.RutasPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinRutas_DevuelveError()
    {
        var resultado = _validador.Validar(new List<RutaGateway>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay rutas"));
    }

    [Fact]
    public void Validar_SinServicioDestino_DevuelveError()
    {
        var rutas = new List<RutaGateway>
        {
            new() { RutaExterna = "/api/v1/x", ServicioDestino = string.Empty, RutaInterna = "/api/v1/x", AplicaAutenticacion = true, AplicaRateLimit = true, AplicaCorrelacion = true }
        };

        var resultado = _validador.Validar(rutas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara el servicio destino"));
    }

    [Fact]
    public void Validar_SinRutaInterna_DevuelveError()
    {
        var rutas = new List<RutaGateway>
        {
            new() { RutaExterna = "/api/v1/x", ServicioDestino = "X.Api", RutaInterna = string.Empty, AplicaAutenticacion = true, AplicaRateLimit = true, AplicaCorrelacion = true }
        };

        var resultado = _validador.Validar(rutas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara la ruta interna"));
    }

    [Fact]
    public void Validar_SinAutenticacion_DevuelveError()
    {
        var rutas = new List<RutaGateway>
        {
            new() { RutaExterna = "/api/v1/x", ServicioDestino = "X.Api", RutaInterna = "/api/v1/x", AplicaAutenticacion = false, AplicaRateLimit = true, AplicaCorrelacion = true }
        };

        var resultado = _validador.Validar(rutas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no aplica autenticación"));
    }

    [Fact]
    public void Validar_SinRateLimit_DevuelveError()
    {
        var rutas = new List<RutaGateway>
        {
            new() { RutaExterna = "/api/v1/x", ServicioDestino = "X.Api", RutaInterna = "/api/v1/x", AplicaAutenticacion = true, AplicaRateLimit = false, AplicaCorrelacion = true }
        };

        var resultado = _validador.Validar(rutas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no aplica limitación de tasa"));
    }

    [Fact]
    public void Validar_SinCorrelacion_DevuelveError()
    {
        var rutas = new List<RutaGateway>
        {
            new() { RutaExterna = "/api/v1/x", ServicioDestino = "X.Api", RutaInterna = "/api/v1/x", AplicaAutenticacion = true, AplicaRateLimit = true, AplicaCorrelacion = false }
        };

        var resultado = _validador.Validar(rutas);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no aplica correlación"));
    }
}
