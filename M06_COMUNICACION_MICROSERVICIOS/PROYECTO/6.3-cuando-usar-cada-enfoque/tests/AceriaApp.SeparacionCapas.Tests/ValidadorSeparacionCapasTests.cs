using AceriaApp.Api.SeparacionCapas;
using FluentAssertions;
using Xunit;

namespace AceriaApp.SeparacionCapas.Tests;

public class ValidadorSeparacionCapasTests
{
    private readonly ValidadorSeparacionCapas _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoProyectos.ProyectosPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_DominioConReferencia_DevuelveError()
    {
        var proyectos = new List<Proyecto>
        {
            new()
            {
                Nombre = "AceriaApp.Hexagonal.Dominio",
                Capa = "Dominio",
                Referencias = new[] { "Infraestructura" }
            }
        };

        var resultado = _validador.Validar(proyectos);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no puede referenciar"));
    }

    [Fact]
    public void Validar_AplicacionReferenciandoInfraestructura_DevuelveError()
    {
        var proyectos = new List<Proyecto>
        {
            new()
            {
                Nombre = "AceriaApp.Hexagonal.Aplicacion",
                Capa = "Aplicacion",
                Referencias = new[] { "Infraestructura" }
            }
        };

        var resultado = _validador.Validar(proyectos);

        resultado.EsValida.Should().BeFalse();
    }

    [Fact]
    public void Validar_CapaDesconocida_DevuelveError()
    {
        var proyectos = new List<Proyecto>
        {
            new() { Nombre = "ProyectoX", Capa = "Inventada" }
        };

        var resultado = _validador.Validar(proyectos);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Capa desconocida"));
    }
}
