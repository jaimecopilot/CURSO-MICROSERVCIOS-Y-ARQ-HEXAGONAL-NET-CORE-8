// INICIO PASO 1.1.17 — SELECCIONAR EL BLOQUE COMENTADO Y DESCOMENTAR (Ctrl+K, Ctrl+U).
// using AceriaApp.Monolito.Api.Dominio;
// using FluentAssertions;
// using Xunit;
//
// namespace AceriaApp.Monolito.Tests;
//
// public class OrdenTests
// {
//     // PASO 1.1.17: comprobar la inicialización de una entidad.
//     [Fact]
//     public void Orden_ConDatosValidos_SeCreaCorrectamente()
//     {
//         var orden = new Orden
//         {
//             Id = Guid.NewGuid(),
//             Cliente = "ACX-001",
//             Material = "CHAPA-3MM",
//             Cantidad = 10,
//             FechaCreacion = DateTime.UtcNow
//         };
//         orden.Cliente.Should().Be("ACX-001");
//         orden.Cantidad.Should().Be(10);
//     }
// }
// FIN PASO 1.1.17
