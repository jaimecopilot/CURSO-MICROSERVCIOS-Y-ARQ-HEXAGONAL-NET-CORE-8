using AceriaApp.Monolito.Api.Diseno;
using FluentAssertions;
using Xunit;
namespace AceriaApp.Diseno.Tests;
public class CatalogoLimitesTests
{
    [Fact]
    public void LimitesValidos_FiltraCorrectamente()
    {
        var limites = new List<LimiteServicio>
        {
            new() { Nombre="Ordenes", CapacidadDeNegocio="Gestion de ordenes",
                    ContextoDelimitado="Produccion", NumeroDeConceptos=2,
                    NumeroDeDependenciasSalientes=1 },
            new() { Nombre="Cajon", CapacidadDeNegocio="Multiples",
                    ContextoDelimitado="Mixto", NumeroDeConceptos=5,
                    NumeroDeDependenciasSalientes=5 }
        };
        var catalogo = new CatalogoLimites(limites);
        var validador = new ValidadorLimiteServicio();
        var validos = catalogo.LimitesValidos(validador).ToList();
        var invalidos = catalogo.LimitesInvalidos(validador).ToList();
        validos.Should().HaveCount(1);
        validos[0].Nombre.Should().Be("Ordenes");
        invalidos.Should().HaveCount(1);
        invalidos[0].Nombre.Should().Be("Cajon");
    }

    // RETO 1.3: activar solo después de descomentar CatalogoLimites.Resumen().
    // [Fact]
    // public void Resumen_ConTresValidosYUnInvalido_CalculaPorcentaje()
    // {
    //     var limites = new List<LimiteServicio>
    //     {
    //         new() { CapacidadDeNegocio="A", ContextoDelimitado="X", NumeroDeConceptos=1, NumeroDeDependenciasSalientes=1 },
    //         new() { CapacidadDeNegocio="B", ContextoDelimitado="X", NumeroDeConceptos=1, NumeroDeDependenciasSalientes=1 },
    //         new() { CapacidadDeNegocio="C", ContextoDelimitado="X", NumeroDeConceptos=1, NumeroDeDependenciasSalientes=1 },
    //         new() { CapacidadDeNegocio=string.Empty, ContextoDelimitado="X" }
    //     };
    //     var resumen = new CatalogoLimites(limites).Resumen(new ValidadorLimiteServicio());
    //     resumen.Validos.Should().Be(3);
    //     resumen.Invalidos.Should().Be(1);
    //     resumen.PorcentajeValidez.Should().Be(75.0);
    // }
}
