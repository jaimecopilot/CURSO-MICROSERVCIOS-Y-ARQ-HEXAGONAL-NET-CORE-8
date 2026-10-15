using AceriaApp.Monolito.Api.DisenoRest;
using Xunit;
namespace AceriaApp.DisenoRest.Tests;
public class ValidadorUriRestTests
{
    private readonly ValidadorUriRest _v = new();
    [Fact] public void Valida_UriDeColeccion() { Assert.True(_v.Validar("/api/v1/ordenes").EsValida); }
    [Fact] public void Rechaza_SinPrefijo() { Assert.False(_v.Validar("/ordenes").EsValida); }
    [Fact] public void Rechaza_SinVersion() { Assert.False(_v.Validar("/api/ordenes").EsValida); }
    [Fact] public void Rechaza_SegmentoDeAccion() { Assert.False(_v.Validar("/api/v1/crear").EsValida); }
}
