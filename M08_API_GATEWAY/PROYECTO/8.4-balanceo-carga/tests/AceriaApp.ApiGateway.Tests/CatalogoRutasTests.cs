using AceriaApp.Api.ApiGateway;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ApiGateway.Tests;

public class CatalogoRutasTests
{
    [Fact]
    public void RutasPorDefecto_ContieneTresRutas()
    {
        var rutas = CatalogoRutas.RutasPorDefecto();

        rutas.Should().HaveCount(3);
    }

    [Fact]
    public void RutasPorDefecto_ContieneOrdenesInventarioYClientes()
    {
        var rutas = CatalogoRutas.RutasPorDefecto();

        rutas.Should().Contain(r => r.ServicioDestino == "Ordenes.Api");
        rutas.Should().Contain(r => r.ServicioDestino == "Inventario.Api");
        rutas.Should().Contain(r => r.ServicioDestino == "Clientes.Api");
    }

    [Fact]
    public void RutasPorDefecto_TodasAplicanAutenticacion()
    {
        var rutas = CatalogoRutas.RutasPorDefecto();

        rutas.Should().OnlyContain(r => r.AplicaAutenticacion);
    }

    [Fact]
    public void RutasPorDefecto_TodasAplicanRateLimit()
    {
        var rutas = CatalogoRutas.RutasPorDefecto();

        rutas.Should().OnlyContain(r => r.AplicaRateLimit);
    }

    [Fact]
    public void RutasPorDefecto_TodasAplicanCorrelacion()
    {
        var rutas = CatalogoRutas.RutasPorDefecto();

        rutas.Should().OnlyContain(r => r.AplicaCorrelacion);
    }
}
