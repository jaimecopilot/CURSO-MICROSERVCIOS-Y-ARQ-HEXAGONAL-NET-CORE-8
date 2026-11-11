using AceriaApp.Api.ComunicacionSincrona;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ComunicacionSincrona.Tests;

public class CatalogoLlamadasTests
{
    [Fact]
    public void LlamadasPorDefecto_ContieneTresLlamadas()
    {
        var llamadas = CatalogoLlamadas.LlamadasPorDefecto();

        llamadas.Should().HaveCount(3);
    }

    [Fact]
    public void LlamadasPorDefecto_TodasUsanGet()
    {
        var llamadas = CatalogoLlamadas.LlamadasPorDefecto();

        llamadas.Should().OnlyContain(l => l.Metodo == "GET");
    }

    [Fact]
    public void LlamadasPorDefecto_TodasTienenTimeout()
    {
        var llamadas = CatalogoLlamadas.LlamadasPorDefecto();

        llamadas.Should().OnlyContain(l => l.TieneTimeout);
    }

    [Fact]
    public void LlamadasPorDefecto_TodasTienenReintentos()
    {
        var llamadas = CatalogoLlamadas.LlamadasPorDefecto();

        llamadas.Should().OnlyContain(l => l.TieneReintentos);
    }

    [Fact]
    public void LlamadasPorDefecto_NingunaApuntaASiMisma()
    {
        var llamadas = CatalogoLlamadas.LlamadasPorDefecto();

        llamadas.Should().OnlyContain(l => l.ServicioOrigen != l.ServicioDestino);
    }
}
