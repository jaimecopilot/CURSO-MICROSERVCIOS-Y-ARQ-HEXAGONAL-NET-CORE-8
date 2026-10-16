using System.Net;
using System.Text.Json;
using Microsoft.AspNetCore.Hosting;
using Xunit;
namespace AceriaApp.Api.Tests;
// INICIO PASO 2.4.8: abrir OpenAPI JSON REAL mediante HTTP.
public class ContratoOpenApiTests
{
    [Fact] public async Task OpenApi_ContieneRutasYVersion()
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().GetAsync("/swagger/v1/swagger.json");
        Assert.Equal(HttpStatusCode.OK,r.StatusCode);
        using var json=JsonDocument.Parse(await r.Content.ReadAsStringAsync());
        Assert.Equal("v1",json.RootElement.GetProperty("info").GetProperty("version").GetString());
        var paths=json.RootElement.GetProperty("paths");
        Assert.True(paths.TryGetProperty("/api/v1/ordenes",out var resource));
        Assert.True(resource.TryGetProperty("get",out _));
        Assert.True(resource.TryGetProperty("post",out _));
    }
    [Fact] public async Task OpenApi_IncluyeEjemplo()
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().GetAsync("/swagger/v1/swagger.json");
        using var json=JsonDocument.Parse(await r.Content.ReadAsStringAsync());
        var schemas=json.RootElement.GetProperty("components").GetProperty("schemas");
        Assert.True(schemas.TryGetProperty("CrearOrdenRequest",out var schema));
        Assert.True(schema.TryGetProperty("example",out _));
    }
    [Fact] public async Task OpenApi_DeclaraErroresDeOperacionesReales()
    {
        using var f=new ApiFactory();
        var response=await f.CreateClient().GetAsync("/swagger/v1/swagger.json");
        Assert.Equal(HttpStatusCode.OK,response.StatusCode);
        using var json=JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        var paths=json.RootElement.GetProperty("paths");
        var coleccion=paths.GetProperty("/api/v1/ordenes");
        Assert.True(coleccion.GetProperty("post").GetProperty("responses").TryGetProperty("422",out _));
        var recurso=paths.EnumerateObject()
            .First(p=>p.Name.StartsWith("/api/v1/ordenes/")
                && p.Value.TryGetProperty("delete",out _)).Value;
        Assert.True(recurso.GetProperty("put").GetProperty("responses").TryGetProperty("422",out _));
        Assert.True(recurso.GetProperty("delete").GetProperty("responses").TryGetProperty("409",out _));
        var rutaCantidad=paths.EnumerateObject()
            .First(p=>p.Name.EndsWith("/cantidad")).Value;
        Assert.True(rutaCantidad.GetProperty("patch").GetProperty("responses").TryGetProperty("409",out _));
        Assert.True(rutaCantidad.GetProperty("patch").GetProperty("responses").TryGetProperty("422",out _));
    }

    [Fact] public async Task Produccion_NoExponeSwagger()
    {
        using var f=new ApiFactory();
        using var other=f.WithWebHostBuilder(b=>b.UseEnvironment("Production"));
        var r=await other.CreateClient().GetAsync("/swagger/v1/swagger.json");
        Assert.Equal(HttpStatusCode.NotFound,r.StatusCode);
    }
}
