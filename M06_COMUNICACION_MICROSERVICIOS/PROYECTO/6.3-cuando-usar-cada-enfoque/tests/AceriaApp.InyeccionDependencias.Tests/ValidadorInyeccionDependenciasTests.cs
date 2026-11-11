using AceriaApp.Api.InyeccionDependencias;
using FluentAssertions;
using Xunit;

namespace AceriaApp.InyeccionDependencias.Tests;

public class ValidadorInyeccionDependenciasTests
{
    private readonly ValidadorInyeccionDependencias _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoInyeccion.RegistrosPorDefecto());

        resultado.EsValido.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinRegistros_DevuelveError()
    {
        var resultado = _validador.Validar(new List<RegistroInyeccion>());

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay registros"));
    }

    [Fact]
    public void Validar_CicloNoPermitido_DevuelveError()
    {
        var registros = new List<RegistroInyeccion>
        {
            new() { Interfaz = "IX", Implementacion = "X", Ciclo = "CicloInvalido", RegistradoPorConstructor = true }
        };

        var resultado = _validador.Validar(registros);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Ciclo no permitido"));
    }

    [Fact]
    public void Validar_SinRegistroPorConstructor_DevuelveError()
    {
        var registros = new List<RegistroInyeccion>
        {
            new() { Interfaz = "IX", Implementacion = "X", Ciclo = "Scoped", RegistradoPorConstructor = false }
        };

        var resultado = _validador.Validar(registros);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no se resuelve por constructor"));
    }

    [Fact]
    public void Validar_ResolucionManual_DevuelveError()
    {
        var registros = new List<RegistroInyeccion>
        {
            new() { Interfaz = "IX", Implementacion = "X", Ciclo = "Scoped", RegistradoPorConstructor = true, ResuelveManualmente = true }
        };

        var resultado = _validador.Validar(registros);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("resuelve manualmente"));
    }

    [Fact]
    public void Validar_CapturaContenedor_DevuelveError()
    {
        var registros = new List<RegistroInyeccion>
        {
            new() { Interfaz = "IX", Implementacion = "X", Ciclo = "Scoped", RegistradoPorConstructor = true, CapturaContenedor = true }
        };

        var resultado = _validador.Validar(registros);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("captura el contenedor"));
    }
}
