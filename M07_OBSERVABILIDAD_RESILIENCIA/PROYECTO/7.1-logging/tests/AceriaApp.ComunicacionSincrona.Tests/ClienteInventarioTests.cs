using System.Net;
using System.Text;
using AceriaApp.Comunicacion.Aplicacion;
using AceriaApp.Comunicacion.Infraestructura;
using Xunit;
namespace AceriaApp.ComunicacionSincrona.Tests;
public class ClienteInventarioTests
{
    private sealed class Servidor(Func<HttpRequestMessage,CancellationToken,Task<HttpResponseMessage>> respuesta) : HttpMessageHandler
    {
        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage r,CancellationToken ct) => respuesta(r,ct);
    }
    private static ClienteInventarioHttp Cliente(HttpStatusCode estado,string json) =>
        new(new HttpClient(new Servidor((_,_)=>Task.FromResult(new HttpResponseMessage(estado)
        {Content=new StringContent(json,Encoding.UTF8,"application/json")}))) {BaseAddress=new Uri("http://inventario/")});
    [Fact, Trait("Tipo","Unidad")]
    public async Task Json_valido_se_traduce_al_contrato()
    { var r=await Cliente(HttpStatusCode.OK,"{\"material\":\"Acero\",\"stock\":80}").ObtenerAsync("Acero",default); Assert.Equal(80,r!.Stock); }
    [Fact, Trait("Tipo","Unidad")]
    public async Task Solo_404_se_traduce_a_ausencia()
    { Assert.Null(await Cliente(HttpStatusCode.NotFound,"{}").ObtenerAsync("Acero",default)); }
    [Fact, Trait("Tipo","Unidad")]
    public async Task Error_500_no_se_disfraza_de_material_ausente()
    { await Assert.ThrowsAsync<InventarioNoDisponibleException>(()=>Cliente(HttpStatusCode.InternalServerError,"{}").ObtenerAsync("Acero",default)); }
    [Fact, Trait("Tipo","Unidad")]
    public async Task Json_invalido_es_fallo_del_servicio()
    { await Assert.ThrowsAsync<InventarioNoDisponibleException>(()=>Cliente(HttpStatusCode.OK,"{").ObtenerAsync("Acero",default)); }
    [Fact, Trait("Tipo","Unidad")]
    public async Task Json_nulo_no_es_404()
    { await Assert.ThrowsAsync<InventarioNoDisponibleException>(()=>Cliente(HttpStatusCode.OK,"null").ObtenerAsync("Acero",default)); }
    [Fact, Trait("Tipo","Unidad")]
    public async Task Stock_negativo_es_contrato_invalido()
    { await Assert.ThrowsAsync<InventarioNoDisponibleException>(()=>Cliente(HttpStatusCode.OK,"{\"material\":\"Acero\",\"stock\":-1}").ObtenerAsync("Acero",default)); }
    [Fact, Trait("Tipo","Unidad")]
    public async Task Cancelacion_del_llamador_se_propaga()
    { using var ct=new CancellationTokenSource();ct.Cancel();await Assert.ThrowsAnyAsync<OperationCanceledException>(()=>Cliente(HttpStatusCode.OK,"{}").ObtenerAsync("Acero",ct.Token)); }
    [Fact, Trait("Tipo","Unidad")]
    public async Task Ruta_escapa_espacios_y_no_inyecta_query()
    {
        string? ruta=null;
        using var http=new HttpClient(new Servidor((r,_)=>{ruta=r.RequestUri!.AbsoluteUri;return Task.FromResult(new HttpResponseMessage(HttpStatusCode.NotFound));})){BaseAddress=new Uri("http://inventario/")};
        await new ClienteInventarioHttp(http).ObtenerAsync("Acero ?x=1",default);
        Assert.Equal("http://inventario/api/v1/materiales/Acero%20%3Fx%3D1",ruta);
    }
}
