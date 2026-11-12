using AceriaApp.Api.UnitOfWork;
using FluentAssertions;
using Xunit;

namespace AceriaApp.UnitOfWork.Tests;

public class CatalogoUnidadesDeTrabajoTests
{
    [Fact]
    public void UnidadesPorDefecto_ContieneDosUnidades()
    {
        var unidades = CatalogoUnidadesDeTrabajo.UnidadesPorDefecto();

        unidades.Should().HaveCount(2);
    }

    [Fact]
    public void UnidadesPorDefecto_TodasExponenCommitYRollback()
    {
        var unidades = CatalogoUnidadesDeTrabajo.UnidadesPorDefecto();

        unidades.Should().OnlyContain(u => u.ExponeCommit);
        unidades.Should().OnlyContain(u => u.ExponeRollback);
    }

    [Fact]
    public void UnidadesPorDefecto_NingunaContieneReglasDeNegocio()
    {
        var unidades = CatalogoUnidadesDeTrabajo.UnidadesPorDefecto();

        unidades.Should().OnlyContain(u => !u.ContieneReglasDeNegocio);
    }

    [Fact]
    public void UnidadesPorDefecto_NingunaConoceEntidadesConcretas()
    {
        var unidades = CatalogoUnidadesDeTrabajo.UnidadesPorDefecto();

        unidades.Should().OnlyContain(u => !u.ConoceEntidadesConcretas);
    }
}
