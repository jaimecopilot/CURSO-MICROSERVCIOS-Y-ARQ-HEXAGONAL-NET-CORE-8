// INICIO PASO 2.4.14 — Activar en el paso correspondiente.
// using AceriaApp.Monolito.Api.Documentacion;
// using FluentAssertions;
// using Xunit;
//
// namespace AceriaApp.Documentacion.Tests;
//
// public class ConfiguracionOpenApiTests
// {
//     private readonly ConfiguracionOpenApi _configuracion = new();
//
//     [Fact]
//     public void ConfiguracionOpenApi_ConValoresPorDefecto_DevuelveValoresEsperados()
//     {
//         _configuracion.PublicarSwaggerUI.Should().BeTrue();
//         _configuracion.RutaDocumento.Should().Be("/swagger/v1/swagger.json");
//         _configuracion.NombreDocumento.Should().Be("AceriaApp.Monolito.Api v1");
//     }
//
//     [Fact]
//     public void EsEntornoDeDesarrollo_ConDevelopment_DevuelveTrue()
//     {
//         _configuracion.EsEntornoDeDesarrollo("Development").Should().BeTrue();
//     }
//
//     [Fact]
//     public void EsEntornoDeDesarrollo_ConProduction_DevuelveFalse()
//     {
//         _configuracion.EsEntornoDeDesarrollo("Production").Should().BeFalse();
//     }
//
//     [Fact]
//     public void EsEntornoDeDesarrollo_IgnoraMayusculas()
//     {
//         _configuracion.EsEntornoDeDesarrollo("development").Should().BeTrue();
//     }
// }
// FIN PASO 2.4.14
