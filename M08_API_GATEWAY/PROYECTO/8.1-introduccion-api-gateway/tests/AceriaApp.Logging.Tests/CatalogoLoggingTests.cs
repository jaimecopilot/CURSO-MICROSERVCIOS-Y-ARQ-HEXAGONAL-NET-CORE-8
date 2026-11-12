using AceriaApp.Api.Logging;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Logging.Tests;

public class CatalogoLoggingTests
{
    [Fact]
    public void ConfiguracionesPorDefecto_ContieneTresConfiguraciones()
    {
        var configuraciones = CatalogoLogging.ConfiguracionesPorDefecto();

        configuraciones.Should().HaveCount(3);
    }

    [Fact]
    public void ConfiguracionesPorDefecto_TodasUsanLoggingEstructurado()
    {
        var configuraciones = CatalogoLogging.ConfiguracionesPorDefecto();

        configuraciones.Should().OnlyContain(c => c.UsaLoggingEstructurado);
    }

    [Fact]
    public void ConfiguracionesPorDefecto_TodasTienenCorrelacion()
    {
        var configuraciones = CatalogoLogging.ConfiguracionesPorDefecto();

        configuraciones.Should().OnlyContain(c => c.TieneCorrelacion);
    }

    [Fact]
    public void ConfiguracionesPorDefecto_TodasEvitanDatosSensibles()
    {
        var configuraciones = CatalogoLogging.ConfiguracionesPorDefecto();

        configuraciones.Should().OnlyContain(c => c.EvitaDatosSensibles);
    }

    [Fact]
    public void ConfiguracionesPorDefecto_TodasConfiguradasPorEntorno()
    {
        var configuraciones = CatalogoLogging.ConfiguracionesPorDefecto();

        configuraciones.Should().OnlyContain(c => c.ConfiguradoPorEntorno);
    }
}
