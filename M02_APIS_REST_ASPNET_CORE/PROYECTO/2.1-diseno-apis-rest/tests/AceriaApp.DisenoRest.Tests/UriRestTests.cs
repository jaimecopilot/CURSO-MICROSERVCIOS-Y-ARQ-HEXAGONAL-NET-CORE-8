using AceriaApp.Monolito.Api.DisenoRest;
using Xunit;
namespace AceriaApp.DisenoRest.Tests;
public class UriRestTests
{
    [Fact] public void Construir_Coleccion() => Assert.Equal("/api/v1/ordenes",new UriRest {Recurso="ordenes"}.Construir());
    [Fact] public void Construir_Identificador() => Assert.Equal("/api/v1/ordenes/123",new UriRest {Recurso="ordenes", Identificador="123"}.Construir());
    [Fact] public void Construir_SubRecurso() => Assert.Equal("/api/v1/ordenes/123/lineas",new UriRest {Recurso="ordenes", Identificador="123", SubRecurso="lineas"}.Construir());
}
