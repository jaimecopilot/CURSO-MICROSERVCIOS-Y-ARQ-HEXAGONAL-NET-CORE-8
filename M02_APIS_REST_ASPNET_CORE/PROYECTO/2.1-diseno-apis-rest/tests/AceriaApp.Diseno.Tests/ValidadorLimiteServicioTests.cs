using AceriaApp.Monolito.Api.Diseno;
using FluentAssertions;
using Xunit;
namespace AceriaApp.Diseno.Tests;
public class ValidadorLimiteServicioTests
{
    private readonly ValidadorLimiteServicio _validador = new();

    [Fact]
    public void Validar_LimiteCompleto_DevuelveValido()
    {
        var limite = new LimiteServicio
        {
            Nombre="Ordenes", CapacidadDeNegocio="Gestion de ordenes de produccion",
            ContextoDelimitado="Produccion", NumeroDeConceptos=2,
            NumeroDeDependenciasSalientes=1, ExponeEntidadesDeDominio=false,
            ComparteBaseDeDatos=false
        };
        var resultado = _validador.Validar(limite);
        resultado.EsValido.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinCapacidadDeNegocio_DevuelveError()
    {
        var limite = new LimiteServicio
        {
            Nombre="Ordenes", CapacidadDeNegocio=string.Empty, ContextoDelimitado="Produccion"
        };
        var resultado = _validador.Validar(limite);
        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("capacidad de negocio"));
    }

    [Fact]
    public void Validar_ConMuchosConceptos_DevuelveErrorDeCohesion()
    {
        var limite = new LimiteServicio
        {
            CapacidadDeNegocio="Gestion multiple", ContextoDelimitado="Produccion",
            NumeroDeConceptos=5
        };
        var resultado = _validador.Validar(limite);
        resultado.EsValido.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("cohesión baja"));
    }
}
