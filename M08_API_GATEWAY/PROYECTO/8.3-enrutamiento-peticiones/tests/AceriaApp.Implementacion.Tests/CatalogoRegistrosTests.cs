using AceriaApp.Api.Implementacion;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Implementacion.Tests;

public class CatalogoRegistrosTests
{
    [Fact]
    public void RegistrosPorDefecto_ContieneCincoRegistros()
    {
        var registros = CatalogoRegistros.RegistrosPorDefecto();

        registros.Should().HaveCount(5);
    }

    [Fact]
    public void RegistrosPorDefecto_ContieneTresAdaptadoresDeSalidaYDosPuertosDeEntrada()
    {
        var registros = CatalogoRegistros.RegistrosPorDefecto();

        registros.Count(r => r.EsAdaptadorDeSalida).Should().Be(3);
        registros.Count(r => !r.EsAdaptadorDeSalida).Should().Be(2);
    }

    [Fact]
    public void RegistrosPorDefecto_TodosLosPuertosTienenImplementacion()
    {
        var registros = CatalogoRegistros.RegistrosPorDefecto();

        registros.Should().OnlyContain(r => !string.IsNullOrWhiteSpace(r.Implementacion));
    }
}
