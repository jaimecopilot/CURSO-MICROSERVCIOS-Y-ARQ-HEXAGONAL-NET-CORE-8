// INICIO PASO 2.3.15 — Activar el código correspondiente a este paso.
// using AceriaApp.Monolito.Api.Validacion;
// using FluentAssertions;
// using Xunit;
//
// namespace AceriaApp.Validacion.Tests;
//
// public class CrearOrdenRequestTests
// {
//     // PASO 2.3.15 — Verifica el record; no son pruebas del filtro HTTP.
//     [Fact]
//     public void CrearOrdenRequest_ConDatosValidos_AsignaValores()
//     {
//         var peticion = new CrearOrdenRequest("ACX-001", "CHAPA-3MM", 10);
//
//         peticion.Cliente.Should().Be("ACX-001");
//         peticion.Material.Should().Be("CHAPA-3MM");
//         peticion.Cantidad.Should().Be(10);
//     }
//
//     [Fact]
//     public void CrearOrdenRequest_ConClienteVacio_AsignaCadenaVacia()
//     {
//         var peticion = new CrearOrdenRequest(string.Empty, "CHAPA-3MM", 10);
//
//         peticion.Cliente.Should().BeEmpty();
//     }
// }
// FIN PASO 2.3.15
