using System.Net;
using System.Text.Json;
using Microsoft.AspNetCore.Hosting;
using Xunit;
namespace AceriaApp.Api.Tests;
// INICIO PASO 2.4.20: abrir OpenAPI JSON REAL mediante HTTP.
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
    // PASO 2.4.22: esquema y ejemplo.
    [Fact] public async Task OpenApi_IncluyeEjemplo()
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().GetAsync("/swagger/v1/swagger.json");
        using var json=JsonDocument.Parse(await r.Content.ReadAsStringAsync());
        var schemas=json.RootElement.GetProperty("components").GetProperty("schemas");
        Assert.True(schemas.TryGetProperty("CrearOrdenRequest",out var schema));
        Assert.True(schema.TryGetProperty("example",out _));
    }
    // PASO 2.4.23: comprobar que OpenAPI refleja las ramas HTTP del servidor.
    [Fact] public async Task OpenApi_DeclaraErroresDeOperacionesReales()
    {
        using var factory = new ApiFactory();
        var response = await factory.CreateClient().GetAsync("/swagger/v1/swagger.json");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        using var document = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        var paths = document.RootElement.GetProperty("paths");
        var collection = paths.GetProperty("/api/v1/ordenes");
        Assert.True(collection.GetProperty("post").GetProperty("responses").TryGetProperty("422", out _));

        var member = paths.EnumerateObject()
            .First(path => path.Name.StartsWith("/api/v1/ordenes/")
                && path.Value.TryGetProperty("delete", out _)).Value;
        var putResponses = member.GetProperty("put").GetProperty("responses");
        foreach (var code in new[] { "204", "400", "404", "409", "422" })
            Assert.True(putResponses.TryGetProperty(code, out _), $"PUT debe declarar {code}");
        var deleteResponses = member.GetProperty("delete").GetProperty("responses");
        foreach (var code in new[] { "204", "404", "409" })
            Assert.True(deleteResponses.TryGetProperty(code, out _), $"DELETE debe declarar {code}");

        var quantity = paths.EnumerateObject()
            .First(path => path.Name.EndsWith("/cantidad")).Value;
        var patchResponses = quantity.GetProperty("patch").GetProperty("responses");
        foreach (var code in new[] { "200", "400", "404", "409", "422" })
            Assert.True(patchResponses.TryGetProperty(code, out _), $"PATCH debe declarar {code}");

        var finish = paths.EnumerateObject()
            .First(path => path.Name.EndsWith("/finalizar")).Value;
        var finishResponses = finish.GetProperty("post").GetProperty("responses");
        foreach (var code in new[] { "200", "404", "409" })
            Assert.True(finishResponses.TryGetProperty(code, out _), $"Finalizar debe declarar {code}");
    }

    // PASO 2.4.23: documentacion no publicada en Production.
    [Fact] public async Task Produccion_NoExponeSwagger()
    {
        using var f=new ApiFactory();
        using var other=f.WithWebHostBuilder(b=>b.UseEnvironment("Production"));
        var r=await other.CreateClient().GetAsync("/swagger/v1/swagger.json");
        Assert.Equal(HttpStatusCode.NotFound,r.StatusCode);
    }
}
