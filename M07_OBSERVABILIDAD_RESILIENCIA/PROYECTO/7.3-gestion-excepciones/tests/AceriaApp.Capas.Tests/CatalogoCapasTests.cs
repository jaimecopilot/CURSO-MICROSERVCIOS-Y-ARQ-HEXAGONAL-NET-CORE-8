using AceriaApp.Api.Capas;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Capas.Tests;

public class CatalogoCapasTests
{
    [Fact]
    public void ReglasPorDefecto_ContieneCuatroCapas()
    {
        var reglas = CatalogoCapas.ReglasPorDefecto();

        reglas.Should().HaveCount(4);
        reglas.Should().ContainKey("Presentacion");
        reglas.Should().ContainKey("Aplicacion");
        reglas.Should().ContainKey("Infraestructura");
        reglas.Should().ContainKey("Dominio");
    }

    [Fact]
    public void ReglasPorDefecto_DominioNoDependeDeNadie()
    {
        var reglas = CatalogoCapas.ReglasPorDefecto();

        reglas["Dominio"].Should().BeEmpty();
    }

    [Fact]
    public void ReglasPorDefecto_InfraestructuraDependeDeAplicacionYDominio()
    {
        var reglas = CatalogoCapas.ReglasPorDefecto();

        reglas["Infraestructura"].Should().Contain("Aplicacion");
        reglas["Infraestructura"].Should().Contain("Dominio");
    }
}
