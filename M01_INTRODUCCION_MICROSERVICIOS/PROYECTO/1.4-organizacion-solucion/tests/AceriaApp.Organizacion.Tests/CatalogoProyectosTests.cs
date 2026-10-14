// INICIO PASO 1.4.15 — SELECCIONAR EL BLOQUE COMENTADO Y DESCOMENTAR (Ctrl+K, Ctrl+U).
// using AceriaApp.Monolito.Api.Organizacion;
// using FluentAssertions;
// using Xunit;
// namespace AceriaApp.Organizacion.Tests;
// public class CatalogoProyectosTests
// {
//     [Fact]
//     public void ProyectosValidos_FiltraCorrectamente()
//     {
//         var nombres = new List<string>
//         {
//             "AceriaApp.Ordenes.Api", "AceriaApp.Ordenes.Domain",
//             "AceriaApp.Ordenes", "AceriaApp.Ordenes.Controlador"
//         };
//         var catalogo = new CatalogoProyectos(nombres);
//         var validador = new ValidadorConvencionNombres(
//             "AceriaApp", new[] { "Api", "Domain", "Infrastructure", "Application", "Tests" });
//         var validos = catalogo.ProyectosValidos(validador).ToList();
//         var invalidos = catalogo.ProyectosInvalidos(validador).ToList();
//         validos.Should().HaveCount(2);
//         validos.Should().Contain("AceriaApp.Ordenes.Api");
//         validos.Should().Contain("AceriaApp.Ordenes.Domain");
//         invalidos.Should().HaveCount(2);
//         invalidos.Should().Contain("AceriaApp.Ordenes");
//         invalidos.Should().Contain("AceriaApp.Ordenes.Controlador");
//     }
//
//     // RETO 1.4: activar después de descomentar CatalogoProyectos.Resumen().
//     // [Fact]
//     // public void Resumen_ConTresValidosYDosInvalidos_CalculaPorcentaje()
//     // {
//     //     var nombres = new List<string>
//     //     { "AceriaApp.Ordenes.Api", "AceriaApp.Ordenes.Domain",
//     //       "AceriaApp.Inventario.Api", "AceriaApp.Ordenes",
//     //       "AceriaApp.Inventario.Controlador" };
//     //     var validador = new ValidadorConvencionNombres("AceriaApp",
//     //         new[] { "Api", "Domain", "Infrastructure", "Application", "Tests" });
//     //     var resumen = new CatalogoProyectos(nombres).Resumen(validador);
//     //     resumen.Validos.Should().Be(3);
//     //     resumen.Invalidos.Should().Be(2);
//     //     resumen.PorcentajeValidez.Should().Be(60.0);
//     // }
// }
// FIN PASO 1.4.15
