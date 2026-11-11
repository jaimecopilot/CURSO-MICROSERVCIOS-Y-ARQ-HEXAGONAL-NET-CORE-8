using System.Net;
using System.Net.Http.Json;
using AceriaApp.Api.Hexagonal;
using AceriaApp.Api.Datos;
using AceriaApp.Hexagonal.Infraestructura.Datos;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Xunit;

namespace AceriaApp.Api.Tests;

public class HexagonalHttpTests
{
    [Fact]
    public async Task Get_ColeccionVacia_Es200()
    {
        using var factory = new HexagonalFactory();
        var response = await factory.CreateClient().GetAsync("/api/v1/hexagonal/ordenes");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task Post_CreaYGetConsultaPorPuerto()
    {
        using var factory = new HexagonalFactory();
        var client = factory.CreateClient();
        using var scope = factory.Services.CreateScope();
        var legacy = scope.ServiceProvider.GetRequiredService<AceriaDbContext>();
        var hexagonal = scope.ServiceProvider.GetRequiredService<HexagonalDbContext>();
        Assert.Equal("Microsoft.EntityFrameworkCore.SqlServer", legacy.Database.ProviderName);
        Assert.Equal("Microsoft.EntityFrameworkCore.SqlServer", hexagonal.Database.ProviderName);
        Assert.NotEqual(legacy.Database.GetDbConnection().Database, hexagonal.Database.GetDbConnection().Database);
        var created = await client.PostAsJsonAsync("/api/v1/hexagonal/ordenes",
            new CrearOrdenHexagonalRequest("ACX-001", "CHAPA", 10));
        Assert.Equal(HttpStatusCode.Created, created.StatusCode);
        Assert.NotNull(created.Headers.Location);
        var retrieved = await client.GetAsync(created.Headers.Location);
        Assert.Equal(HttpStatusCode.OK, retrieved.StatusCode);
        var dto = await retrieved.Content.ReadFromJsonAsync<OrdenHexagonalDto>();
        Assert.Equal("ACX-001", dto?.Cliente);
        Assert.Equal(10, dto?.Cantidad);
    }

    [Fact]
    public async Task Post_ValidacionYCapacidadRespetan400Y422()
    {
        using var factory = new HexagonalFactory();
        var client = factory.CreateClient();
        var invalid = await client.PostAsJsonAsync("/api/v1/hexagonal/ordenes",
            new CrearOrdenHexagonalRequest("", "CHAPA", 10));
        Assert.Equal(HttpStatusCode.BadRequest, invalid.StatusCode);
        var excess = await client.PostAsJsonAsync("/api/v1/hexagonal/ordenes",
            new CrearOrdenHexagonalRequest("ACX", "CHAPA", 501));
        Assert.Equal(HttpStatusCode.UnprocessableEntity, excess.StatusCode);
    }

    [Fact]
    public async Task Finalizar_DosVeces_Responde200Y409()
    {
        using var factory = new HexagonalFactory();
        var client = factory.CreateClient();
        var created = await client.PostAsJsonAsync("/api/v1/hexagonal/ordenes",
            new CrearOrdenHexagonalRequest("ACX", "CHAPA", 5));
        var orden = await created.Content.ReadFromJsonAsync<OrdenHexagonalDto>();
        Assert.NotNull(orden);
        var url = $"/api/v1/hexagonal/ordenes/{orden.Id}/finalizar";
        Assert.Equal(HttpStatusCode.OK, (await client.PostAsync(url, null)).StatusCode);
        Assert.Equal(HttpStatusCode.Conflict, (await client.PostAsync(url, null)).StatusCode);
    }
}
