using AceriaApp.Api.InyeccionDependencias;
using FluentAssertions;
using Xunit;

namespace AceriaApp.InyeccionDependencias.Tests;

public class CatalogoInyeccionTests
{
    [Fact]
    public void RegistrosPorDefecto_ContieneCincoRegistros()
    {
        var registros = CatalogoInyeccion.RegistrosPorDefecto();

        registros.Should().HaveCount(5);
    }

    [Fact]
    public void RegistrosPorDefecto_TodosResueltosPorConstructor()
    {
        var registros = CatalogoInyeccion.RegistrosPorDefecto();

        registros.Should().OnlyContain(r => r.RegistradoPorConstructor);
    }

    [Fact]
    public void RegistrosPorDefecto_NingunoResuelveManualmente()
    {
        var registros = CatalogoInyeccion.RegistrosPorDefecto();

        registros.Should().OnlyContain(r => !r.ResuelveManualmente);
    }

    [Fact]
    public void RegistrosPorDefecto_NingunoCapturaContenedor()
    {
        var registros = CatalogoInyeccion.RegistrosPorDefecto();

        registros.Should().OnlyContain(r => !r.CapturaContenedor);
    }
}
