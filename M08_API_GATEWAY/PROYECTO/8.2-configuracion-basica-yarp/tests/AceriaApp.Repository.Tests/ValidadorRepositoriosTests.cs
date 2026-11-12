using AceriaApp.Api.Repository;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Repository.Tests;

public class ValidadorRepositoriosTests
{
    private readonly ValidadorRepositorios _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoRepositorios.RepositoriosPorDefecto());

        resultado.EsValido.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinRepositorios_DevuelveError()
    {
        var resultado = _validador.Validar(new List<Repositorio>());

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay repositorios"));
    }

    [Fact]
    public void Validar_SinEntidad_DevuelveError()
    {
        var repositorios = new List<Repositorio>
        {
            new() { Nombre = "IRepositorioX", Entidad = string.Empty, NumeroDeMetodos = 5 }
        };

        var resultado = _validador.Validar(repositorios);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara la entidad"));
    }

    [Fact]
    public void Validar_ConReglasDeNegocio_DevuelveError()
    {
        var repositorios = new List<Repositorio>
        {
            new() { Nombre = "IRepositorioX", Entidad = "Orden", NumeroDeMetodos = 5, TieneReglasDeNegocio = true }
        };

        var resultado = _validador.Validar(repositorios);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("reglas de negocio"));
    }

    [Fact]
    public void Validar_ConTransacciones_DevuelveError()
    {
        var repositorios = new List<Repositorio>
        {
            new() { Nombre = "IRepositorioX", Entidad = "Orden", NumeroDeMetodos = 5, GestionaTransacciones = true }
        };

        var resultado = _validador.Validar(repositorios);

        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("gestiona transacciones"));
    }
}
