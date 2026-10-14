// INICIO PASO 1.4.14 — SELECCIONAR EL BLOQUE COMENTADO Y DESCOMENTAR (Ctrl+K, Ctrl+U).
// using AceriaApp.Monolito.Api.Organizacion;
// using FluentAssertions;
// using Xunit;
// namespace AceriaApp.Organizacion.Tests;
// public class ValidadorConvencionNombresTests
// {
//     private readonly ValidadorConvencionNombres _validador = new(
//         "AceriaApp", new[] { "Api", "Domain", "Infrastructure", "Application", "Tests" });
//
//     [Fact]
//     public void Validar_NombreCorrecto_DevuelveValido()
//     {
//         var resultado = _validador.Validar("AceriaApp.Ordenes.Api");
//         resultado.EsValido.Should().BeTrue();
//         resultado.Errores.Should().BeEmpty();
//     }
//     [Fact]
//     public void Validar_SinPrefijo_DevuelveError()
//     {
//         var resultado = _validador.Validar("Ordenes.Api");
//         resultado.EsValido.Should().BeFalse();
//         resultado.Errores.Should().Contain(e => e.Contains("no empieza por"));
//     }
//     [Fact]
//     public void Validar_TipoNoPermitido_DevuelveError()
//     {
//         var resultado = _validador.Validar("AceriaApp.Ordenes.Controlador");
//         resultado.EsValido.Should().BeFalse();
//         resultado.Errores.Should().Contain(e => e.Contains("no está permitido"));
//     }
//     [Fact]
//     public void Validar_NumeroDePartesIncorrecto_DevuelveError()
//     {
//         var resultado = _validador.Validar("AceriaApp.Ordenes");
//         resultado.EsValido.Should().BeFalse();
//         resultado.Errores.Should().Contain(e => e.Contains("Prefijo.Componente.Tipo"));
//     }
// }
// FIN PASO 1.4.14
