using AceriaApp.Monolito.Api.Documentacion;
using Xunit;
namespace AceriaApp.Documentacion.Tests;
public class MetadatosApiTests
{
    [Fact] public void Metadatos_PorDefecto()
    {
        var m=new MetadatosApi();
        Assert.Equal("v1",m.Version); Assert.Equal("AceriaApp.Monolito.Api",m.Titulo);
        Assert.Equal("equipo@aceria.local",m.ContactoEmail);
    }
    [Fact] public void Metadatos_Personalizables()
    {
        var m=new MetadatosApi{Titulo="AceriaApp.Ordenes.Api",Version="v2"};
        Assert.Equal("v2",m.Version); Assert.Equal("AceriaApp.Ordenes.Api",m.Titulo);
    }
}
