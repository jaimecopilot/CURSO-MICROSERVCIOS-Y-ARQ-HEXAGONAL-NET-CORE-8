using AceriaApp.Monolito.Api.Validacion;
using Xunit;
namespace AceriaApp.Validacion.Tests;
public class CrearOrdenRequestTests
{
    [Fact] public void Contrato_AsignaValores()
    {
        var p=new CrearOrdenRequest("ACX-001","CHAPA-3MM",10);
        Assert.Equal("ACX-001",p.Cliente); Assert.Equal("CHAPA-3MM",p.Material); Assert.Equal(10,p.Cantidad);
    }
    [Fact] public void Contrato_PermiteRepresentarCadenaVacia()
    {
        var p=new CrearOrdenRequest("","CHAPA-3MM",10);
        Assert.Equal("",p.Cliente);
    }
}
