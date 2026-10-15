using AceriaApp.Monolito.Api.DisenoRest;
using Xunit;
namespace AceriaApp.DisenoRest.Tests;
public class CatalogoUrisTests
{
    [Fact] public void Separa_ValidasYNoValidas()
    {
        var c=new CatalogoUris(new[]{"/api/v1/ordenes","/api/v1/ordenes/123","/ordenes","/api/v1/crear"});
        Assert.Equal(2,c.UrisValidas(new ValidadorUriRest()).Count());
        Assert.Equal(2,c.UrisInvalidas(new ValidadorUriRest()).Count());
    }
}
