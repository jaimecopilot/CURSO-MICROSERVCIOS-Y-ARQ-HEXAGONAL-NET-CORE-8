using System.Collections.Concurrent;
using System.Net;
using System.Text.Json;
using AceriaApp.Observabilidad;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Http.Features;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Serilog.Core;
using Serilog.Events;
using Serilog.Formatting.Json;
using Xunit;
namespace AceriaApp.GestionExcepciones.Tests;
public class ErroresFuncionalesTests
{
    private sealed class Captura : ILogEventSink
    {
        public ConcurrentQueue<LogEvent> Eventos { get; } = new();
        public void Emit(LogEvent e) => Eventos.Enqueue(e);
    }
    private static async Task<WebApplication> Servidor(string entorno, bool diagnostico, Captura? sink = null)
    {
        var builder = WebApplication.CreateBuilder(new WebApplicationOptions { EnvironmentName = entorno });
        builder.WebHost.UseTestServer();
        builder.Configuration.AddInMemoryCollection(new Dictionary<string, string?> { ["Observabilidad:DiagnosticoActivo"] = diagnostico.ToString() });
        if (sink is not null) builder.Services.AddSingleton<ILogEventSink>(sink);
        builder.Services.AddLoggingAceria("Prueba"); builder.Services.AddErroresAceria();
        var app = builder.Build(); app.UseLoggingAceria(); app.UseErroresAceria(); app.MapDiagnosticoAceria();
        app.MapGet("/inesperado", IResult () => throw new InvalidOperationException("secreto-excepcion-no-publicar"));
        app.MapGet("/inesperado/{secreto}", IResult () => throw new InvalidOperationException("secreto-excepcion-no-publicar"));
        app.MapGet("/esperado", () => Results.Problem(statusCode: 409, title: "La orden ya está planificada."));
        await app.StartAsync(); return app;
    }
    [Fact]
    public async Task Fallo_inesperado_devuelve_ProblemDetails_y_correlacion_sin_detalle_privado()
    {
        await using var app = await Servidor("Production", false); using var http = app.GetTestClient();
        http.DefaultRequestHeaders.Add("X-Correlation-ID", "error-123");
        using var response = await http.GetAsync("/inesperado/secreto-ruta?token=secreto-query");
        var text = await response.Content.ReadAsStringAsync(); using var doc = JsonDocument.Parse(text);
        Assert.Equal(HttpStatusCode.InternalServerError, response.StatusCode);
        Assert.Equal("application/problem+json", response.Content.Headers.ContentType!.MediaType);
        Assert.Equal(500, doc.RootElement.GetProperty("status").GetInt32());
        Assert.Equal("error-123", doc.RootElement.GetProperty("correlationId").GetString());
        Assert.Equal("error-123", Assert.Single(response.Headers.GetValues("X-Correlation-ID")));
        Assert.False(string.IsNullOrWhiteSpace(doc.RootElement.GetProperty("traceId").GetString()));
        Assert.DoesNotContain("secreto", text); Assert.DoesNotContain("InvalidOperationException", text);
    }
    [Fact]
    public async Task Accept_no_compatible_con_writer_sigue_recibiendo_error_JSON_seguro()
    {
        await using var app = await Servidor("Production", false); using var http = app.GetTestClient();
        http.DefaultRequestHeaders.Accept.ParseAdd("text/plain");
        using var response = await http.GetAsync("/inesperado");
        Assert.Equal(HttpStatusCode.InternalServerError, response.StatusCode);
        using var doc = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        Assert.Equal(500, doc.RootElement.GetProperty("status").GetInt32());
    }
    [Fact]
    public async Task Result_esperado_conserva_su_409()
    {
        await using var app = await Servidor("Production", false); using var http = app.GetTestClient();
        using var response = await http.GetAsync("/esperado");
        Assert.Equal(HttpStatusCode.Conflict, response.StatusCode);
        using var doc = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        Assert.Equal("La orden ya está planificada.", doc.RootElement.GetProperty("title").GetString());
    }
    [Theory]
    [InlineData("Production", true, 404)]
    [InlineData("Development", false, 404)]
    [InlineData("Development", true, 500)]
    public async Task Diagnostico_solo_se_habilita_en_Development_con_opcion(string entorno, bool activo, int status)
    {
        await using var app = await Servidor(entorno, activo); using var http = app.GetTestClient();
        using var response = await http.GetAsync("/api/diagnostico/fallo");
        Assert.Equal(status, (int)response.StatusCode);
    }
    [Fact]
    public async Task Excepcion_registrada_no_incluye_mensaje_libre_ni_cuerpo()
    {
        var sink = new Captura(); await using var app = await Servidor("Production", false, sink); using var http = app.GetTestClient();
        using var response = await http.GetAsync("/inesperado/secreto-ruta?token=secreto-query");
        Assert.Equal(HttpStatusCode.InternalServerError, response.StatusCode);
        var error = Assert.Single(sink.Eventos, e => e.Properties.ContainsKey("TipoExcepcion"));
        Assert.Equal(LogEventLevel.Error, error.Level); Assert.Null(error.Exception);
        using var output = new StringWriter(); foreach (var e in sink.Eventos) new JsonFormatter().Format(e, output);
        Assert.DoesNotContain("secreto-excepcion", output.ToString());
        Assert.DoesNotContain("secreto-ruta", output.ToString());
        Assert.DoesNotContain("secreto-query", output.ToString());
        Assert.DoesNotContain("RequestPath", output.ToString());
    }
    private static ServiceProvider Servicios()
    {
        var services = new ServiceCollection(); services.AddLoggingAceria("Prueba"); services.AddErroresAceria();
        services.AddSingleton<ManejadorExcepciones>(); return services.BuildServiceProvider();
    }
    [Fact]
    public async Task Cancelacion_del_usuario_no_se_convierte_en_500()
    {
        using var services = Servicios(); using var cancelacion = new CancellationTokenSource(); cancelacion.Cancel();
        var ctx = new DefaultHttpContext { RequestServices = services, RequestAborted = cancelacion.Token };
        ctx.Response.Body = new MemoryStream();
        Assert.True(await services.GetRequiredService<ManejadorExcepciones>().TryHandleAsync(ctx, new OperationCanceledException(cancelacion.Token), cancelacion.Token));
        Assert.Equal(499, ctx.Response.StatusCode); Assert.Equal(0, ctx.Response.Body.Length);
    }
    private sealed class RespuestaIniciada : HttpResponseFeature { public override bool HasStarted => true; }
    [Fact]
    public async Task Respuesta_iniciada_no_se_reescribe()
    {
        using var services = Servicios(); var ctx = new DefaultHttpContext { RequestServices = services };
        ctx.Features.Set<IHttpResponseFeature>(new RespuestaIniciada()); ctx.Response.Body = new MemoryStream();
        Assert.False(await services.GetRequiredService<ManejadorExcepciones>().TryHandleAsync(ctx, new Exception("interno"), default));
        Assert.Equal(0, ctx.Response.Body.Length);
    }
}
