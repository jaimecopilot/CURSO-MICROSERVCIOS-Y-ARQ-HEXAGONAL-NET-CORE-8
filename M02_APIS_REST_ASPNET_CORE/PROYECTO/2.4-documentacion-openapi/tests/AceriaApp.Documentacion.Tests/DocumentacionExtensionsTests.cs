using System.Net;
using System.Text.Json;
using AceriaApp.Monolito.Api.Documentacion;
using FluentAssertions;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace AceriaApp.Documentacion.Tests;

public class DocumentacionExtensionsTests
{
    [Fact]
    public async Task SwaggerJson_EnDevelopment_ContieneMetadatosV1()
    {
        using var factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(b => b.UseEnvironment("Development"));
        using var client = factory.CreateClient();
        using var response = await client.GetAsync("/swagger/v1/swagger.json");

        response.StatusCode.Should().Be(HttpStatusCode.OK);
        using var json = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        var info = json.RootElement.GetProperty("info");
        info.GetProperty("title").GetString().Should().Be("AceriaApp.Monolito.Api");
        info.GetProperty("version").GetString().Should().Be("v1");
    }

    [Fact]
    public async Task SwaggerJson_EnDevelopment_DescribeLosEndpointsReales()
    {
        using var factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(b => b.UseEnvironment("Development"));
        using var client = factory.CreateClient();
        using var response = await client.GetAsync("/swagger/v1/swagger.json");

        response.StatusCode.Should().Be(HttpStatusCode.OK);
        using var json = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        var ordenes = json.RootElement.GetProperty("paths")
            .GetProperty("/api/v1/ordenes");
        ordenes.TryGetProperty("get", out _).Should().BeTrue();
        ordenes.TryGetProperty("post", out _).Should().BeTrue();
    }

    [Fact]
    public async Task SwaggerJson_EnProduction_NoEstaPublicado()
    {
        using var factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(b => b.UseEnvironment("Production"));
        using var client = factory.CreateClient();
        using var response = await client.GetAsync("/swagger/v1/swagger.json");

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
}
