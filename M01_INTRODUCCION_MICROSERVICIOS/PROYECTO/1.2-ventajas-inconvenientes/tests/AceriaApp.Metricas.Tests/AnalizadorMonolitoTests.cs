// INICIO PASO 1.2.15 — SELECCIONAR EL BLOQUE COMENTADO Y DESCOMENTAR (Ctrl+K, Ctrl+U).
// using AceriaApp.Monolito.Api.Metricas;
// using FluentAssertions;
// using Xunit;
// namespace AceriaApp.Metricas.Tests;
// public class AnalizadorMonolitoTests
// {
//     [Fact]
//     public void CalcularAcoplamientoGlobal_ConServicios_AgregaMetricas()
//     {
//         var servicios = new List<MetricasServicio>
//         {
//             new() { Nombre="Ordenes", NumeroDeDependenciasExternas=2, NumeroDeTablas=3 },
//             new() { Nombre="Inventario", NumeroDeDependenciasExternas=1, NumeroDeTablas=2 }
//         };
//         var analizador = new AnalizadorMonolito(servicios);
//         var resultado = analizador.CalcularAcoplamientoGlobal();
//         resultado.NumeroDeProyectos.Should().Be(2);
//         resultado.NumeroDeReferenciasEntreProyectos.Should().Be(3);
//         resultado.NumeroDeTablasCompartidas.Should().Be(5);
//     }
//     [Fact]
//     public void ServiciosCandidatosAExtraccion_FiltraCorrectamente()
//     {
//         var servicios = new List<MetricasServicio>
//         {
//             new() { Nombre="Ordenes", NumeroDeDependenciasExternas=3, NumeroDeTablas=4 },
//             new() { Nombre="Inventario", NumeroDeDependenciasExternas=1, NumeroDeTablas=2 }
//         };
//         var analizador = new AnalizadorMonolito(servicios);
//         var candidatos = analizador.ServiciosCandidatosAExtraccion().ToList();
//         candidatos.Should().HaveCount(1);
//         candidatos[0].Nombre.Should().Be("Inventario");
//     }
//     // RETO 1.2: habilitar después de descomentar ServicioMenosAcoplado().
//     // [Fact]
//     // public void ServicioMenosAcoplado_ConEmpate_DesempataPorNombre()
//     // {
//     //     var servicios = new List<MetricasServicio>
//     //     {
//     //         new() { Nombre="Ordenes", NumeroDeEndpoints=1, NumeroDeTablas=1, NumeroDeDependenciasExternas=1 },
//     //         new() { Nombre="Inventario", NumeroDeEndpoints=1, NumeroDeTablas=1, NumeroDeDependenciasExternas=1 }
//     //     };
//     //     var resultado = new AnalizadorMonolito(servicios).ServicioMenosAcoplado();
//     //     resultado.Should().NotBeNull();
//     //     resultado!.Nombre.Should().Be("Inventario");
//     // }
// }
// FIN PASO 1.2.15
