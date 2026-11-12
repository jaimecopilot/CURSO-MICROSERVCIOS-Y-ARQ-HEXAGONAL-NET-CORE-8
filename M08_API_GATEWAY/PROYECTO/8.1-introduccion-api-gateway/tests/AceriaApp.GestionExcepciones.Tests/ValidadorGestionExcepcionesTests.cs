using AceriaApp.Api.GestionExcepciones;
using FluentAssertions;
using Xunit;

namespace AceriaApp.GestionExcepciones.Tests;

public class ValidadorGestionExcepcionesTests
{
    private readonly ValidadorGestionExcepciones _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoExcepciones.ManejadoresPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinManejadores_DevuelveError()
    {
        var resultado = _validador.Validar(new List<ManejadorExcepcion>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay manejadores"));
    }

    [Fact]
    public void Validar_CodigoNoPermitido_DevuelveError()
    {
        var manejadores = new List<ManejadorExcepcion>
        {
            new() { TipoExcepcion = "X", CodigoHttp = 999, Titulo = "T", UsaProblemDetails = true, RegistraError = true }
        };

        var resultado = _validador.Validar(manejadores);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Código HTTP no permitido"));
    }

    [Fact]
    public void Validar_SinTitulo_DevuelveError()
    {
        var manejadores = new List<ManejadorExcepcion>
        {
            new() { TipoExcepcion = "X", CodigoHttp = 404, Titulo = string.Empty, UsaProblemDetails = true, RegistraError = true }
        };

        var resultado = _validador.Validar(manejadores);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara título"));
    }

    [Fact]
    public void Validar_SinProblemDetails_DevuelveError()
    {
        var manejadores = new List<ManejadorExcepcion>
        {
            new() { TipoExcepcion = "X", CodigoHttp = 404, Titulo = "T", UsaProblemDetails = false, RegistraError = true }
        };

        var resultado = _validador.Validar(manejadores);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no usa problem details"));
    }

    [Fact]
    public void Validar_ErrorServidorSinRegistro_DevuelveError()
    {
        var manejadores = new List<ManejadorExcepcion>
        {
            new() { TipoExcepcion = "X", CodigoHttp = 500, Titulo = "T", UsaProblemDetails = true, RegistraError = false }
        };

        var resultado = _validador.Validar(manejadores);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no registra el error"));
    }
    [Fact]
    public void Validar_Indisponibilidad503_DevuelveValido()
    {
        var manejadores = new List<ManejadorExcepcion>
        {
            new() { TipoExcepcion = "InventarioNoDisponibleException", CodigoHttp = 503, Titulo = "Servicio no disponible", UsaProblemDetails = true, RegistraError = true }
        };

        var resultado = _validador.Validar(manejadores);

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_ErrorClienteSinNivelError_DevuelveValido()
    {
        var manejadores = new List<ManejadorExcepcion>
        {
            new() { TipoExcepcion = "ValidacionException", CodigoHttp = 400, Titulo = "Validación", UsaProblemDetails = true, RegistraError = false }
        };

        var resultado = _validador.Validar(manejadores);

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }
}
