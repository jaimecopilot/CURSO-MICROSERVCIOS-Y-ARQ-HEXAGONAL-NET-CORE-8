using AceriaApp.Api.PuertosAdaptadores;
using FluentAssertions;
using Xunit;

namespace AceriaApp.PuertosAdaptadores.Tests;

public class CatalogoPuertosAdaptadoresTests
{
    [Fact]
    public void PuertosPorDefecto_ContieneCincoPuertos()
    {
        var puertos = CatalogoPuertosAdaptadores.PuertosPorDefecto();

        puertos.Should().HaveCount(5);
    }

    [Fact]
    public void PuertosPorDefecto_ContieneDosEntradasYTresSalidas()
    {
        var puertos = CatalogoPuertosAdaptadores.PuertosPorDefecto();

        puertos.Count(p => p.Tipo == "Entrada").Should().Be(2);
        puertos.Count(p => p.Tipo == "Salida").Should().Be(3);
    }

    [Fact]
    public void AdaptadoresPorDefecto_ContieneTresAdaptadores()
    {
        var adaptadores = CatalogoPuertosAdaptadores.AdaptadoresPorDefecto();

        adaptadores.Should().HaveCount(3);
    }
}
