using AceriaApp.Monolito.Api.Validacion;
using Xunit;
namespace AceriaApp.Validacion.Tests;
public class CrearOrdenRequestValidatorTests
{
    private readonly CrearOrdenRequestValidator _v=new();
    [Fact] public void Acepta_PeticionValida() => Assert.True(_v.Validate(new CrearOrdenRequest("ACX-001","CHAPA-3MM",10)).IsValid);
    [Fact] public void Rechaza_ClienteVacio() => Assert.False(_v.Validate(new CrearOrdenRequest("","CHAPA-3MM",10)).IsValid);
    [Fact] public void Rechaza_CantidadNegativa() => Assert.False(_v.Validate(new CrearOrdenRequest("ACX-001","CHAPA-3MM",-5)).IsValid);
    [Fact] public void Rechaza_CantidadExcesiva() => Assert.False(_v.Validate(new CrearOrdenRequest("ACX-001","CHAPA-3MM",20000)).IsValid);
}
