using AceriaApp.Api.CasosDeUso;
using FluentAssertions;
using Xunit;

namespace AceriaApp.CasosDeUso.Tests;

public class CatalogoCasosDeUsoTests
{
    [Fact]
    public void CasosPorDefecto_ContieneCuatroCasos()
    {
        var casos = CatalogoCasosDeUso.CasosPorDefecto();

        casos.Should().HaveCount(4);
    }

    [Fact]
    public void CasosPorDefecto_ContieneDosEscriturasYDosLecturas()
    {
        var casos = CatalogoCasosDeUso.CasosPorDefecto();

        casos.Count(c => c.Tipo == "Escritura").Should().Be(2);
        casos.Count(c => c.Tipo == "Lectura").Should().Be(2);
    }

    [Fact]
    public void CasosPorDefecto_TodosDevuelvenResult()
    {
        var casos = CatalogoCasosDeUso.CasosPorDefecto();

        casos.Should().OnlyContain(c => c.DevuelveResult);
    }

    [Fact]
    public void CasosPorDefecto_EscriturasCoordinanUnidadDeTrabajo()
    {
        var casos = CatalogoCasosDeUso.CasosPorDefecto();

        casos.Where(c => c.Tipo == "Escritura").Should().OnlyContain(c => c.CoordinaUnidadDeTrabajo);
    }

    [Fact]
    public void CasosPorDefecto_LecturasNoCoordinanUnidadDeTrabajo()
    {
        var casos = CatalogoCasosDeUso.CasosPorDefecto();

        casos.Where(c => c.Tipo == "Lectura").Should().OnlyContain(c => !c.CoordinaUnidadDeTrabajo);
    }
}
