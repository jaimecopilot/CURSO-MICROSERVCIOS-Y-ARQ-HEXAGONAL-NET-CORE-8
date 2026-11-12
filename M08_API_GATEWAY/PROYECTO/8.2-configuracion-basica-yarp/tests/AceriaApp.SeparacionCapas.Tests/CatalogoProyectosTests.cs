using AceriaApp.Api.SeparacionCapas;
using FluentAssertions;
using Xunit;

namespace AceriaApp.SeparacionCapas.Tests;

public class CatalogoProyectosTests
{
    [Fact]
    public void ProyectosPorDefecto_ContieneCuatroProyectos()
    {
        var proyectos = CatalogoProyectos.ProyectosPorDefecto();

        proyectos.Should().HaveCount(4);
    }

    [Fact]
    public void ProyectosPorDefecto_DominioSinReferencias()
    {
        var proyectos = CatalogoProyectos.ProyectosPorDefecto();

        var dominio = proyectos.First(p => p.Capa == "Dominio");
        dominio.Referencias.Should().BeEmpty();
    }

    [Fact]
    public void ProyectosPorDefecto_AplicacionSoloReferenciaDominio()
    {
        var proyectos = CatalogoProyectos.ProyectosPorDefecto();

        var aplicacion = proyectos.First(p => p.Capa == "Aplicacion");
        aplicacion.Referencias.Should().HaveCount(1);
        aplicacion.Referencias.Should().Contain("Dominio");
    }
}
