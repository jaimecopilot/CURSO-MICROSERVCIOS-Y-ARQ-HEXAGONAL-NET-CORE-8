using System.Net;
using System.Net.Http.Json;
using System.Text;
using AceriaApp.Pruebas.Gateway;
using Xunit;

namespace AceriaApp.ConfiguracionYarp.Tests;

public sealed class GatewayConfiguracionFuncionalTests
{
    // Detecta destinos cruzados y pérdida del método/cuerpo/query al atravesar YARP real.
    [Theory]
    [InlineData("GET", "/api/v1/ordenes/42", "produccion")]
    [InlineData("POST", "/api/v1/ordenes", "produccion")]
    [InlineData("PUT", "/api/v1/produccion/ordenes/42", "produccion")]
    [InlineData("PATCH", "/api/v1/comunicacion/ordenes/42", "produccion")]
    [InlineData("DELETE", "/api/v1/ordenes/42", "produccion")]
    [InlineData("GET", "/api/v1/materiales/Acero", "inventario-1")]
    [InlineData("GET", "/api/v1/planificaciones/42", "inventario-1")]
    public async Task Publica_solo_el_servicio_y_conserva_la_peticion(string metodo, string ruta, string instancia)
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        using var peticion = new HttpRequestMessage(new HttpMethod(metodo), ruta + "?material=Acero%20inoxidable&pagina=2")
        { Content = new StringContent("{\"cantidad\":17}", Encoding.UTF8, "application/json") };
        using var respuesta = await prueba.Cliente.SendAsync(peticion);
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        var eco = await respuesta.Content.ReadFromJsonAsync<EcoPeticion>();
        Assert.Equal(instancia, eco!.Instancia);
        Assert.Equal(metodo, eco.Metodo);
        Assert.Equal(ruta, eco.Ruta);
        Assert.Equal("?material=Acero%20inoxidable&pagina=2", eco.Query);
        Assert.Equal("{\"cantidad\":17}", eco.Cuerpo);
    }

    [Theory]
    [InlineData(400)] [InlineData(404)] [InlineData(409)] [InlineData(422)]
    public async Task Conserva_el_estado_y_el_ProblemDetails_del_backend(int estado)
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        using var respuesta = await prueba.Cliente.GetAsync($"/api/v1/ordenes/42?estado={estado}");
        Assert.Equal(estado, (int)respuesta.StatusCode);
        Assert.Equal("application/problem+json", respuesta.Content.Headers.ContentType!.MediaType);
        Assert.Equal($"{{\"type\":\"https://aceria.test/problemas/regla\",\"title\":\"Regla del servicio\",\"status\":{estado},\"detail\":\"Respuesta original\",\"codigo\":\"ACERIA-001\"}}", await respuesta.Content.ReadAsStringAsync());
    }

    [Fact]
    public async Task El_Location_absoluto_interno_del_201_se_puede_seguir_por_el_gateway()
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        using var respuesta = await prueba.Cliente.PostAsync("/api/v1/ordenes?estado=201", new StringContent("{}"));
        Assert.Equal(HttpStatusCode.Created, respuesta.StatusCode);
        Assert.Equal("/api/v1/ordenes/creada?version=1", respuesta.Headers.Location!.OriginalString);
        using var creada = await prueba.Cliente.GetAsync(respuesta.Headers.Location);
        Assert.Equal(HttpStatusCode.OK, creada.StatusCode);
        Assert.Equal("produccion", (await creada.Content.ReadFromJsonAsync<EcoPeticion>())!.Instancia);
    }

    [Theory]
    [InlineData("curso_42-A", true)] [InlineData("invalida con espacios", false)] [InlineData("", false)]
    public async Task La_correlacion_validada_en_el_borde_es_la_que_recibe_el_backend(string entrada, bool valida)
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        using var peticion = new HttpRequestMessage(HttpMethod.Get, "/api/v1/ordenes");
        if (entrada.Length > 0) peticion.Headers.TryAddWithoutValidation("X-Correlation-ID", entrada);
        using var respuesta = await prueba.Cliente.SendAsync(peticion);
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        var correlacion = Assert.Single(respuesta.Headers.GetValues("X-Correlation-ID"));
        Assert.Equal(correlacion, (await respuesta.Content.ReadFromJsonAsync<EcoPeticion>())!.Correlacion);
        if (valida) Assert.Equal(entrada, correlacion);
        else { Assert.NotEqual(entrada, correlacion); Assert.Matches("^[a-f0-9]{32}$", correlacion); }
    }

    [Theory]
    [InlineData("/diagnostico")] [InlineData("/diagnostico/error")]
    [InlineData("/health/ready")] [InlineData("/swagger/index.html")]
    [InlineData("/desconocida")] [InlineData("/api/v1/clientes")]
    public async Task Una_ruta_no_publicada_no_llega_a_ningun_backend(string ruta)
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        using var respuesta = await prueba.Cliente.GetAsync(ruta);
        Assert.Equal(HttpStatusCode.NotFound, respuesta.StatusCode);
        Assert.Equal(0, prueba.Produccion.Peticiones + prueba.Inventario1.Peticiones);
    }

    [Theory]
    [InlineData("POST")] [InlineData("PUT")] [InlineData("PATCH")] [InlineData("DELETE")]
    public async Task Inventario_no_publica_escrituras(string metodo)
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        using var respuesta = await prueba.Cliente.SendAsync(new HttpRequestMessage(new HttpMethod(metodo), "/api/v1/materiales/Acero"));
        Assert.Equal(HttpStatusCode.MethodNotAllowed, respuesta.StatusCode);
        Assert.Equal(0, prueba.Inventario1.Peticiones);
    }

    [Fact]
    public async Task Live_responde_del_gateway_aunque_los_backends_esten_detenidos()
    {
        await using var prueba = await GatewayPruebas.CrearAsync();
        await prueba.Produccion.DetenerAsync();
        await prueba.Inventario1.DetenerAsync();
        using var respuesta = await prueba.Cliente.GetAsync("/health/live");
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        Assert.Contains("Gateway", await respuesta.Content.ReadAsStringAsync());
    }
}
