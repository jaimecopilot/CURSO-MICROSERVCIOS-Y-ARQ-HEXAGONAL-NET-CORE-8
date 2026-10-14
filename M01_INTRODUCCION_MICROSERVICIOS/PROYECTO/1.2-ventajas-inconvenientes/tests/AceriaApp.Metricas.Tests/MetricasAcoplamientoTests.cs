// INICIO PASO 1.2.13 — SELECCIONAR EL BLOQUE COMENTADO Y DESCOMENTAR (Ctrl+K, Ctrl+U).
// using AceriaApp.Monolito.Api.Metricas;
// using FluentAssertions;
// using Xunit;
// namespace AceriaApp.Metricas.Tests;
// public class MetricasAcoplamientoTests
// {
//     [Fact]
//     public void IndiceAcoplamiento_SinProyectos_DevuelveCero()
//     {
//         var metricas = new MetricasAcoplamiento { NumeroDeProyectos = 0 };
//         metricas.IndiceAcoplamiento().Should().Be(0);
//     }
//     [Fact]
//     public void IndiceAcoplamiento_ConProyectos_DevuelveRatio()
//     {
//         var metricas = new MetricasAcoplamiento
//         {
//             NumeroDeProyectos = 4, NumeroDeReferenciasEntreProyectos = 8
//         };
//         metricas.IndiceAcoplamiento().Should().Be(2.0);
//     }
//     [Fact]
//     public void IndiceComparticionDeDatos_SinTablas_DevuelveCero()
//     {
//         var metricas = new MetricasAcoplamiento { NumeroDeTablasCompartidas = 0 };
//         metricas.IndiceComparticionDeDatos().Should().Be(0);
//     }
// }
// FIN PASO 1.2.13
