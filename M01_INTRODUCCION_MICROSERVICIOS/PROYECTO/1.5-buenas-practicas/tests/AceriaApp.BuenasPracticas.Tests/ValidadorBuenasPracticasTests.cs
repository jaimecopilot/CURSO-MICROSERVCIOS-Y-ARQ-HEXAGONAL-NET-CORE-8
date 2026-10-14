// INICIO PASO 1.5.14 — SELECCIONAR EL BLOQUE COMENTADO Y DESCOMENTAR (Ctrl+K, Ctrl+U).
// using AceriaApp.Monolito.Api.BuenasPracticas;
// using FluentAssertions;
// using Xunit;
// namespace AceriaApp.BuenasPracticas.Tests;
//
// public class ValidadorBuenasPracticasTests
// {
//     private readonly ValidadorBuenasPracticas _validador = new(
//         new[] { "Contrato", "Operación", "Comunicación", "Evolución" });
//
//     [Fact]
//     public void Validar_PracticasCompletas_DevuelveValido()
//     {
//         var practicas = new List<Practica>
//         {
//             new() { Codigo="C-01", Categoria="Contrato", EstaAplicada=true },
//             new() { Codigo="O-01", Categoria="Operación", EstaAplicada=true },
//             new() { Codigo="M-01", Categoria="Comunicación", EstaAplicada=true },
//             new() { Codigo="E-01", Categoria="Evolución", EstaAplicada=true }
//         };
//         var resultado = _validador.Validar(practicas);
//         resultado.EsValido.Should().BeTrue();
//         resultado.Errores.Should().BeEmpty();
//     }
//
//     [Fact]
//     public void Validar_CategoriaNoPermitida_DevuelveError()
//     {
//         var practicas = new List<Practica>
//         {
//             new() { Codigo="X-01", Categoria="Inventada", EstaAplicada=true }
//         };
//         var resultado = _validador.Validar(practicas);
//         resultado.EsValido.Should().BeFalse();
//         resultado.Errores.Should().Contain(e => e.Contains("no permitida"));
//     }
//
//     [Fact]
//     public void Validar_PracticaNoAplicada_DevuelveError()
//     {
//         var practicas = new List<Practica>
//         {
//             new() { Codigo="C-01", Categoria="Contrato", EstaAplicada=false }
//         };
//         var resultado = _validador.Validar(practicas);
//         resultado.EsValido.Should().BeFalse();
//         resultado.Errores.Should().Contain(e => e.Contains("no aplicada"));
//     }
//
//     [Fact]
//     public void Validar_SinPracticas_DevuelveError()
//     {
//         var resultado = _validador.Validar(new List<Practica>());
//         resultado.EsValido.Should().BeFalse();
//         resultado.Errores.Should().Contain(e => e.Contains("ninguna práctica"));
//     }
// }
// FIN PASO 1.5.14
