using AceriaApp.Api.PuertosAdaptadores;
using FluentAssertions;
using Xunit;

namespace AceriaApp.PuertosAdaptadores.Tests;

public class ValidadorPuertosAdaptadoresTests
{
    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var validador = new ValidadorPuertosAdaptadores(
            CatalogoPuertosAdaptadores.PuertosPorDefecto(),
            CatalogoPuertosAdaptadores.AdaptadoresPorDefecto());

        var resultado = validador.Validar();

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_PuertoFueraDeAplicacion_DevuelveError()
    {
        var puertos = new List<Puerto>
        {
            new() { Nombre = "IPuertoMal", Tipo = "Entrada", Capa = "Infraestructura" }
        };
        var validador = new ValidadorPuertosAdaptadores(puertos, new List<Adaptador>());

        var resultado = validador.Validar();

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no está en la capa de aplicación"));
    }

    [Fact]
    public void Validar_AdaptadorDePuertoDesconocido_DevuelveError()
    {
        var adaptadores = new List<Adaptador>
        {
            new() { Nombre = "AdaptadorHuerfano", Tipo = "Salida", PuertoImplementado = "IPuertoInexistente", Capa = "Infraestructura" }
        };
        var validador = new ValidadorPuertosAdaptadores(new List<Puerto>(), adaptadores);

        var resultado = validador.Validar();

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("puerto desconocido"));
    }

    [Fact]
    public void Validar_AdaptadorDeEntradaFueraDePresentacion_DevuelveError()
    {
        var puertos = new List<Puerto>
        {
            new() { Nombre = "IOrdenServicio", Tipo = "Entrada", Capa = "Aplicacion" }
        };
        var adaptadores = new List<Adaptador>
        {
            new() { Nombre = "AdaptadorMalUbicado", Tipo = "Entrada", PuertoImplementado = "IOrdenServicio", Capa = "Infraestructura" }
        };
        var validador = new ValidadorPuertosAdaptadores(puertos, adaptadores);

        var resultado = validador.Validar();

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no está en la capa de presentación"));
    }

    [Fact]
    public void Validar_AdaptadorDeSalidaFueraDeInfraestructura_DevuelveError()
    {
        var puertos = new List<Puerto>
        {
            new() { Nombre = "IOrdenRepositorio", Tipo = "Salida", Capa = "Aplicacion" }
        };
        var adaptadores = new List<Adaptador>
        {
            new() { Nombre = "AdaptadorMalUbicado", Tipo = "Salida", PuertoImplementado = "IOrdenRepositorio", Capa = "Presentacion" }
        };
        var validador = new ValidadorPuertosAdaptadores(puertos, adaptadores);

        var resultado = validador.Validar();

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no está en la capa de infraestructura"));
    }
}
