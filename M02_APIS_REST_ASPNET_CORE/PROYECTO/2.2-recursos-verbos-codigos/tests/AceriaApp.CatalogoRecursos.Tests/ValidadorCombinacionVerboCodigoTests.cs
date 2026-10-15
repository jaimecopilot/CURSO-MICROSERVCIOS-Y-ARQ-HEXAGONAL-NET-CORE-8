// INICIO PASO 2.2.14 — Activar el código de este paso con Ctrl+K, Ctrl+U.
// using AceriaApp.Monolito.Api.CatalogoRecursos;
// using Xunit;
// namespace AceriaApp.CatalogoRecursos.Tests;
// public class ValidadorCombinacionVerboCodigoTests
// {
//     private readonly ValidadorCombinacionVerboCodigo _v=new();
//     [Theory] [InlineData("GET",200)] [InlineData("POST",201)]
//     public void Acepta_CombinacionesDelContrato(string verbo,int codigo) =>
//         Assert.True(_v.Validar(new(){Verbo=verbo,Codigo=codigo}).EsValida);
//     [Fact] public void Rechaza_Get201() => Assert.False(_v.Validar(new(){Verbo="GET",Codigo=201}).EsValida);
//     [Fact] public void Rechaza_VerboNoDeclarado() => Assert.False(_v.Validar(new(){Verbo="OPTIONS",Codigo=200}).EsValida);
// }
// FIN PASO 2.2.14
