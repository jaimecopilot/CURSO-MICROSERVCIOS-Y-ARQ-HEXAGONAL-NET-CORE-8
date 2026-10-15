using AceriaApp.Monolito.Api.Documentacion;
using Xunit;
namespace AceriaApp.Documentacion.Tests;
public class ConfiguracionOpenApiTests
{
    private readonly ConfiguracionOpenApi _c=new();
    [Fact] public void ValoresPorDefecto() => Assert.Equal("/swagger/v1/swagger.json",_c.RutaDocumento);
    [Fact] public void Desarrollo_IgnoraMayusculas() => Assert.True(_c.EsEntornoDeDesarrollo("development"));
    [Fact] public void Produccion_NoEsDesarrollo() => Assert.False(_c.EsEntornoDeDesarrollo("Production"));
}
