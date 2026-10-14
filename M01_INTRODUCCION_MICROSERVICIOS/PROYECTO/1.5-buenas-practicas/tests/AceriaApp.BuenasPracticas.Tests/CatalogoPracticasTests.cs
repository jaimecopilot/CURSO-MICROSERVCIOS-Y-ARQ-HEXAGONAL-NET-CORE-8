// INICIO PASO 1.5.15 — SELECCIONAR EL BLOQUE COMENTADO Y DESCOMENTAR (Ctrl+K, Ctrl+U).
// using AceriaApp.Monolito.Api.BuenasPracticas;
// using FluentAssertions;
// using Xunit;
// namespace AceriaApp.BuenasPracticas.Tests;
//
// public class CatalogoPracticasTests
// {
//     [Fact]
//     public void PracticasAplicadas_FiltraCorrectamente()
//     {
//         var practicas = new List<Practica>
//         {
//             new() { Codigo="C-01", Categoria="Contrato", EstaAplicada=true },
//             new() { Codigo="O-01", Categoria="Operación", EstaAplicada=false },
//             new() { Codigo="M-01", Categoria="Comunicación", EstaAplicada=true }
//         };
//         var catalogo = new CatalogoPracticas(practicas);
//         var aplicadas = catalogo.PracticasAplicadas().ToList();
//         var pendientes = catalogo.PracticasPendientes().ToList();
//         aplicadas.Should().HaveCount(2);
//         pendientes.Should().HaveCount(1);
//         pendientes[0].Codigo.Should().Be("O-01");
//     }
//
//     // RETO 1.5: descomentar una vez habilitado CatalogoPracticas.Resumen().
//     // [Fact]
//     // public void Resumen_ConTresAplicadasYDosPendientes_CalculaPorcentaje()
//     // {
//     //     var practicas = new List<Practica>
//     //     {
//     //         new() { Codigo="C-01", Categoria="Contrato", EstaAplicada=true },
//     //         new() { Codigo="C-02", Categoria="Contrato", EstaAplicada=true },
//     //         new() { Codigo="O-01", Categoria="Operación", EstaAplicada=true },
//     //         new() { Codigo="M-01", Categoria="Comunicación", EstaAplicada=false },
//     //         new() { Codigo="E-01", Categoria="Evolución", EstaAplicada=false }
//     //     };
//     //     var resumen = new CatalogoPracticas(practicas).Resumen();
//     //     resumen.Aplicadas.Should().Be(3);
//     //     resumen.Pendientes.Should().Be(2);
//     //     resumen.PorcentajeAplicacion.Should().Be(60.0);
//     // }
// }
// FIN PASO 1.5.15
