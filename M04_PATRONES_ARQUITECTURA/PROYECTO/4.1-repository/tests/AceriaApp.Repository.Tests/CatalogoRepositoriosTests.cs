using AceriaApp.Api.Repository;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Repository.Tests;

public class CatalogoRepositoriosTests
{
    [Fact]
    public void RepositoriosPorDefecto_ContieneTresRepositorios()
    {
        var repositorios = CatalogoRepositorios.RepositoriosPorDefecto();

        repositorios.Should().HaveCount(3);
    }

    [Fact]
    public void RepositoriosPorDefecto_NingunoTieneReglasDeNegocio()
    {
        var repositorios = CatalogoRepositorios.RepositoriosPorDefecto();

        repositorios.Should().OnlyContain(r => !r.TieneReglasDeNegocio);
    }

    [Fact]
    public void RepositoriosPorDefecto_NingunoGestionaTransacciones()
    {
        var repositorios = CatalogoRepositorios.RepositoriosPorDefecto();

        repositorios.Should().OnlyContain(r => !r.GestionaTransacciones);
    }
}
