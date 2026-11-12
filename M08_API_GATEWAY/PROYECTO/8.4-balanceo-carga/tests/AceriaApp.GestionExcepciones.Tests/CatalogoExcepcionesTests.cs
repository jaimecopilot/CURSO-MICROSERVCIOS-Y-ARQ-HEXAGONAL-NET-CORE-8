using AceriaApp.Api.GestionExcepciones;
using FluentAssertions;
using Xunit;

namespace AceriaApp.GestionExcepciones.Tests;

public class CatalogoExcepcionesTests
{
    [Fact]
    public void ManejadoresPorDefecto_ContieneCincoManejadores()
    {
        var manejadores = CatalogoExcepciones.ManejadoresPorDefecto();

        manejadores.Should().HaveCount(5);
    }

    [Fact]
    public void ManejadoresPorDefecto_TodosUsanProblemDetails()
    {
        var manejadores = CatalogoExcepciones.ManejadoresPorDefecto();

        manejadores.Should().OnlyContain(m => m.UsaProblemDetails);
    }

    [Fact]
    public void ManejadoresPorDefecto_TodosRegistranError()
    {
        var manejadores = CatalogoExcepciones.ManejadoresPorDefecto();

        manejadores.Should().OnlyContain(m => m.RegistraError);
    }

    [Fact]
    public void ManejadoresPorDefecto_ContieneCuatroErroresDelClienteYUnErrorDelServidor()
    {
        var manejadores = CatalogoExcepciones.ManejadoresPorDefecto();

        manejadores.Count(m => m.CodigoHttp >= 400 && m.CodigoHttp < 500).Should().Be(4);
        manejadores.Count(m => m.CodigoHttp >= 500).Should().Be(1);
    }

    [Fact]
    public void ManejadoresPorDefecto_ContieneUnError500()
    {
        var manejadores = CatalogoExcepciones.ManejadoresPorDefecto();

        manejadores.Count(m => m.CodigoHttp == 500).Should().Be(1);
    }
}
