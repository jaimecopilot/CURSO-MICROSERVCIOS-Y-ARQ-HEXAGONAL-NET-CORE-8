using System.Net;
using System.Net.Http.Json;
using AceriaApp.Api.Contratos;
using AceriaApp.Api.Modelo;
using Xunit;
namespace AceriaApp.Api.Tests;
// INICIO PASO 2.2.11: probar POST/GET/PUT/PATCH/DELETE con HTTP.
public class EscrituraTests
{
    [Fact] public async Task CrearYConsultar_Es201Y200()
    {
        using var f=new ApiFactory();using var client=f.CreateClient();
        var created=await client.PostAsJsonAsync("/api/v1/ordenes",
            new CrearOrdenRequest("ACX","CHAPA",10));
        Assert.Equal(HttpStatusCode.Created,created.StatusCode);
        Assert.NotNull(created.Headers.Location);
        var get=await client.GetAsync(created.Headers.Location);
        Assert.Equal(HttpStatusCode.OK,get.StatusCode);
    }
    [Fact] public async Task EditarYEliminar_CambiaPersistencia()
    {
        using var f=new ApiFactory();using var c=f.CreateClient();
        var made=await c.PostAsJsonAsync("/api/v1/ordenes",
            new CrearOrdenRequest("ACX","CHAPA",10));
        var dto=await made.Content.ReadFromJsonAsync<OrdenDto>();
        Assert.NotNull(dto);
        var put=await c.PutAsJsonAsync("/api/v1/ordenes/"+dto.Id,
            new CrearOrdenRequest("ACX2","CHAPA",11));
        Assert.Equal(HttpStatusCode.NoContent,put.StatusCode);
        var patch=await c.PatchAsJsonAsync("/api/v1/ordenes/"+dto.Id+"/cantidad",
            new ActualizarCantidadRequest(12));
        Assert.Equal(HttpStatusCode.OK,patch.StatusCode);
        var changed=await patch.Content.ReadFromJsonAsync<OrdenDto>();
        Assert.Equal(12,changed?.Cantidad);
        var del=await c.DeleteAsync("/api/v1/ordenes/"+dto.Id);
        Assert.Equal(HttpStatusCode.NoContent,del.StatusCode);
        var gone=await c.GetAsync("/api/v1/ordenes/"+dto.Id);
        Assert.Equal(HttpStatusCode.NotFound,gone.StatusCode);
    }
    [Fact] public async Task ReglaCapacidad_Es422()
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().PostAsJsonAsync("/api/v1/ordenes",
            new CrearOrdenRequest("ACX","CHAPA",501));
        Assert.Equal(HttpStatusCode.UnprocessableEntity,r.StatusCode);
    }
    [Fact] public async Task OrdenFinalizada_NoSeEdita409()
    {
        using var f=new ApiFactory();using var c=f.CreateClient();
        var made=await c.PostAsJsonAsync("/api/v1/ordenes",
            new CrearOrdenRequest("ACX","CHAPA",2));
        var dto=await made.Content.ReadFromJsonAsync<OrdenDto>();
        Assert.NotNull(dto);
        var done=await c.PostAsync("/api/v1/ordenes/"+dto.Id+"/finalizar",null);
        Assert.Equal(HttpStatusCode.OK,done.StatusCode);
        var put=await c.PutAsJsonAsync("/api/v1/ordenes/"+dto.Id,
            new CrearOrdenRequest("ACX","CHAPA",3));
        Assert.Equal(HttpStatusCode.Conflict,put.StatusCode);
    }
}
