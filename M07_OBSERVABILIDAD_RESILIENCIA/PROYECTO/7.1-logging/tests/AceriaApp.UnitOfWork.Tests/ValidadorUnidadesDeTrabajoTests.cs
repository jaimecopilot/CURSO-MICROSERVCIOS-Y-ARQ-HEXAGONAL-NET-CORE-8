using AceriaApp.Api.UnitOfWork;
using FluentAssertions;
using Xunit;

namespace AceriaApp.UnitOfWork.Tests;

public class ValidadorUnidadesDeTrabajoTests
{
    private readonly ValidadorUnidadesDeTrabajo _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoUnidadesDeTrabajo.UnidadesPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinUnidades_DevuelveError()
    {
        var resultado = _validador.Validar(new List<UnidadDeTrabajo>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay unidades"));
    }

    [Fact]
    public void Validar_SinRepositoriosCoordinados_DevuelveError()
    {
        var unidades = new List<UnidadDeTrabajo>
        {
            new() { Nombre = "UoWX", RepositoriosCoordinados = 0, ExponeCommit = true, ExponeRollback = true }
        };

        var resultado = _validador.Validar(unidades);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no coordina ningún repositorio"));
    }

    [Fact]
    public void Validar_SinCommit_DevuelveError()
    {
        var unidades = new List<UnidadDeTrabajo>
        {
            new() { Nombre = "UoWX", RepositoriosCoordinados = 1, ExponeCommit = false, ExponeRollback = true }
        };

        var resultado = _validador.Validar(unidades);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("confirmación"));
    }

    [Fact]
    public void Validar_SinRollback_DevuelveError()
    {
        var unidades = new List<UnidadDeTrabajo>
        {
            new() { Nombre = "UoWX", RepositoriosCoordinados = 1, ExponeCommit = true, ExponeRollback = false }
        };

        var resultado = _validador.Validar(unidades);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("reversión"));
    }

    [Fact]
    public void Validar_ConReglasDeNegocio_DevuelveError()
    {
        var unidades = new List<UnidadDeTrabajo>
        {
            new() { Nombre = "UoWX", RepositoriosCoordinados = 1, ExponeCommit = true, ExponeRollback = true, ContieneReglasDeNegocio = true }
        };

        var resultado = _validador.Validar(unidades);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("reglas de negocio"));
    }

    [Fact]
    public void Validar_ConEntidadesConcretas_DevuelveError()
    {
        var unidades = new List<UnidadDeTrabajo>
        {
            new() { Nombre = "UoWX", RepositoriosCoordinados = 1, ExponeCommit = true, ExponeRollback = true, ConoceEntidadesConcretas = true }
        };

        var resultado = _validador.Validar(unidades);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("entidades concretas"));
    }
}
