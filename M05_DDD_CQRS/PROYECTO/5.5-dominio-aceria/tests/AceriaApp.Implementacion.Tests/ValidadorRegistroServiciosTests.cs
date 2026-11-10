using AceriaApp.Api.Implementacion;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Implementacion.Tests;

public class ValidadorRegistroServiciosTests
{
    private readonly ValidadorRegistroServicios _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoRegistros.RegistrosPorDefecto());

        resultado.EsValido.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinRegistros_DevuelveError()
    {
        var resultado = _validador.Validar(new List<RegistroServicio>());

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay registros"));
    }

    [Fact]
    public void Validar_CicloNoPermitido_DevuelveError()
    {
        var registros = new List<RegistroServicio>
        {
            new() { Puerto = "IPuertoX", Implementacion = "ImplementacionX", Ciclo = "CicloInvalido" }
        };

        var resultado = _validador.Validar(registros);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Ciclo no permitido"));
    }

    [Fact]
    public void Validar_AdaptadorDeSalidaTransient_DevuelveError()
    {
        var registros = new List<RegistroServicio>
        {
            new() { Puerto = "IOrdenRepositorio", Implementacion = "OrdenRepositorioSqlServer", Ciclo = "Transient", EsAdaptadorDeSalida = true }
        };

        var resultado = _validador.Validar(registros);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Transient"));
    }

    [Fact]
    public void Validar_SinImplementacion_DevuelveError()
    {
        var registros = new List<RegistroServicio>
        {
            new() { Puerto = "IPuertoX", Implementacion = string.Empty, Ciclo = "Scoped" }
        };

        var resultado = _validador.Validar(registros);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara implementación"));
    }
}
