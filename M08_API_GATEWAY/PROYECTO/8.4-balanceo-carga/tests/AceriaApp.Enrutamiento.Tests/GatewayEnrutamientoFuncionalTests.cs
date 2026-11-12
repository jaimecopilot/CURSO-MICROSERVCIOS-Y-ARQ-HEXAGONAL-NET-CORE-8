using System.Net;
using System.Net.Http.Json;
using AceriaApp.Pruebas.Gateway;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Configuration;
using Xunit;

namespace AceriaApp.Enrutamiento.Tests;

public sealed class GatewayEnrutamientoFuncionalTests
{
    // Detecta prefijo sin retirar y Set convertido por error en Append o literal no admitido.
    [Theory]
    [InlineData("materiales/Acero")] [InlineData("planificaciones/42")]
    public async Task El_alias_retira_el_prefijo_y_fija_cabecera_y_query(string recurso)
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        using var peticion = new HttpRequestMessage(HttpMethod.Get, "/inventario/api/v1/" + recurso + "?pagina=2&canal=cliente");
        peticion.Headers.Add("X-Canal", "Cliente");
        using var respuesta = await prueba.Cliente.SendAsync(peticion);
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        var eco = await respuesta.Content.ReadFromJsonAsync<EcoPeticion>();
        Assert.Equal("inventario-1", eco!.Instancia);
        Assert.Equal("/api/v1/" + recurso, eco.Ruta);
        Assert.Equal("Gateway", eco.Canal);
        var query = Microsoft.AspNetCore.WebUtilities.QueryHelpers.ParseQuery(eco.Query);
        Assert.Equal("2", query["pagina"].ToString());
        Assert.Equal("gateway", Assert.Single(query["canal"]));
    }

    [Fact]
    public async Task La_ruta_publica_directa_conserva_la_query_y_la_cabecera_originales()
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        using var peticion = new HttpRequestMessage(HttpMethod.Get, "/api/v1/materiales/Acero?canal=cliente");
        peticion.Headers.Add("X-Canal", "Cliente");
        using var respuesta = await prueba.Cliente.SendAsync(peticion);
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        var eco = await respuesta.Content.ReadFromJsonAsync<EcoPeticion>();
        Assert.Equal("?canal=cliente", eco!.Query);
        Assert.Equal("Cliente", eco.Canal);
    }

    [Theory]
    [InlineData("/inventario/diagnostico")] [InlineData("/inventario/diagnostico/error")]
    [InlineData("/inventario/health/ready")] [InlineData("/inventario/health/live")]
    [InlineData("/inventario/api/v1/ordenes")] [InlineData("/inventario/desconocida")]
    public async Task El_alias_no_abre_rutas_internas_ni_recursos_no_publicados(string ruta)
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        using var respuesta = await prueba.Cliente.GetAsync(ruta);
        Assert.Equal(HttpStatusCode.NotFound, respuesta.StatusCode);
        Assert.Equal(0, prueba.Produccion.Peticiones + prueba.Inventario1.Peticiones);
    }

    [Theory]
    [InlineData("POST")] [InlineData("PUT")] [InlineData("PATCH")] [InlineData("DELETE")]
    public async Task El_alias_de_inventario_sigue_siendo_de_solo_lectura(string metodo)
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        using var respuesta = await prueba.Cliente.SendAsync(new HttpRequestMessage(new HttpMethod(metodo), "/inventario/api/v1/materiales/Acero"));
        Assert.Equal(HttpStatusCode.MethodNotAllowed, respuesta.StatusCode);
        Assert.Equal(0, prueba.Inventario1.Escrituras);
    }

    [Fact]
    public async Task El_orden_explicito_del_alias_precede_a_una_ruta_competidora()
    {
        await using var prueba = await GatewayPruebas.CrearAsync(configurar: builder =>
            builder.Configuration.AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["ReverseProxy:Routes:competidora:ClusterId"] = "produccion-cluster",
                ["ReverseProxy:Routes:competidora:Order"] = "-5",
                ["ReverseProxy:Routes:competidora:Match:Path"] = "/inventario/{**resto}"
            }));
        using var respuesta = await prueba.Cliente.GetAsync("/inventario/api/v1/materiales/Acero");
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        Assert.Equal("inventario-1", (await respuesta.Content.ReadFromJsonAsync<EcoPeticion>())!.Instancia);
    }

    [Fact]
    public async Task El_alias_acepta_HEAD_y_no_devuelve_cuerpo()
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        using var respuesta = await prueba.Cliente.SendAsync(new HttpRequestMessage(HttpMethod.Head, "/inventario/api/v1/materiales/Acero"));
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        Assert.Equal("inventario-1", Assert.Single(respuesta.Headers.GetValues("X-Instancia")));
        Assert.Equal("", await respuesta.Content.ReadAsStringAsync());
        Assert.Equal(1, prueba.Inventario1.Peticiones);
    }
}
