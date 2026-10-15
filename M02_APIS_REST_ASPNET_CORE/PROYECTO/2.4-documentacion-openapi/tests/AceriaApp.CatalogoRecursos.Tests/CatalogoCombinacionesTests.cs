using AceriaApp.Monolito.Api.CatalogoRecursos;
using Xunit;
namespace AceriaApp.CatalogoRecursos.Tests;
public class CatalogoCombinacionesTests
{
    [Fact] public void Catalogo_SeparaConjuntos()
    {
        var c=new CatalogoCombinaciones(new CombinacionVerboCodigo[]{
            new(){Verbo="GET",Codigo=200},new(){Verbo="POST",Codigo=201},
            new(){Verbo="GET",Codigo=201},new(){Verbo="OPTIONS",Codigo=200}});
        var v=new ValidadorCombinacionVerboCodigo();
        Assert.Equal(2,c.CombinacionesValidas(v).Count());
        Assert.Equal(2,c.CombinacionesInvalidas(v).Count());
    }
}
