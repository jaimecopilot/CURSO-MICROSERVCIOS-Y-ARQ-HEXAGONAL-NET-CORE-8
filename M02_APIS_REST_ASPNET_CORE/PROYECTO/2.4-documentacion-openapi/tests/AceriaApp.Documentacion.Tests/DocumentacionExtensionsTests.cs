using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.Hosting;
using System.Text.Json;
using System.Net.Http.Json;
using Xunit;
namespace AceriaApp.Documentacion.Tests;
public class DocumentacionExtensionsTests
{
    [Fact] public async Task Swagger_EnDesarrollo_DevuelveJsonOpenApi()
    {
        using var f=new WebApplicationFactory<Program>().WithWebHostBuilder(b=>b.UseEnvironment("Development"));
        using var cliente=f.CreateClient();
        var respuesta=await cliente.GetAsync("/swagger/v1/swagger.json");
        respuesta.EnsureSuccessStatusCode();
        using var json=JsonDocument.Parse(await respuesta.Content.ReadAsStringAsync());
        Assert.True(json.RootElement.TryGetProperty("openapi",out _));
    }
    [Fact] public async Task Swagger_ContieneVersion()
    {
        using var f=new WebApplicationFactory<Program>().WithWebHostBuilder(b=>b.UseEnvironment("Development"));
        using var json=JsonDocument.Parse(await f.CreateClient().GetStringAsync("/swagger/v1/swagger.json"));
        Assert.Equal("v1",json.RootElement.GetProperty("info").GetProperty("version").GetString());
    }
    [Fact] public async Task Swagger_DocumentaOrdenes()
    {
        using var f=new WebApplicationFactory<Program>().WithWebHostBuilder(b=>b.UseEnvironment("Development"));
        using var json=JsonDocument.Parse(await f.CreateClient().GetStringAsync("/swagger/v1/swagger.json"));
        Assert.True(json.RootElement.GetProperty("paths").TryGetProperty("/api/v1/ordenes",out _));
        var invalid = await f.CreateClient().PostAsJsonAsync("/api/v1/ordenes", new { cliente="", material="CHAPA-3MM", cantidad=-1 });
        Assert.Equal(System.Net.HttpStatusCode.BadRequest, invalid.StatusCode);
    }
    [Fact] public async Task Swagger_NoSePublicaEnProduccion()
    {
        using var f=new WebApplicationFactory<Program>().WithWebHostBuilder(b=>b.UseEnvironment("Production"));
        var response=await f.CreateClient().GetAsync("/swagger/v1/swagger.json");
        Assert.Equal(System.Net.HttpStatusCode.NotFound,response.StatusCode);
    }
}
