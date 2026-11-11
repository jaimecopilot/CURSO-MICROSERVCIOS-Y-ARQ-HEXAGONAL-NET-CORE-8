using System.Collections.Concurrent;
using System.Text.Json;
using AceriaApp.Observabilidad;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;
using Microsoft.AspNetCore.Routing.Patterns;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Serilog;
using Serilog.Core;
using Serilog.Events;
using Serilog.Extensions.Logging;
using Serilog.Formatting.Json;
using Xunit;
namespace AceriaApp.Logging.Tests;
public class LoggingFuncionalTests
{
    private sealed class Captura : ILogEventSink
    {
        public ConcurrentQueue<LogEvent> Eventos { get; } = new();
        public void Emit(LogEvent evento) => Eventos.Enqueue(evento);
    }
    private static DefaultHttpContext Contexto(string? id = null)
    {
        var ctx = new DefaultHttpContext();
        ctx.Request.Method = "GET";
        ctx.Request.Path = "/material/secreto-en-ruta";
        ctx.Request.QueryString = new QueryString("?token=secreto-query");
        ctx.Request.Headers.Authorization = "Bearer secreto-header";
        ctx.Request.Body = new MemoryStream("secreto-body"u8.ToArray());
        if (id is not null) ctx.Request.Headers["X-Correlation-ID"] = id;
        ctx.SetEndpoint(new RouteEndpoint(_ => Task.CompletedTask,
            RoutePatternFactory.Parse("/material/{nombre}"), 0, EndpointMetadataCollection.Empty, "material"));
        return ctx;
    }
    [Fact]
    public async Task Correlacion_valida_se_conserva_en_respuesta_y_contexto()
    {
        var ctx = Contexto("orden_123-A");
        string? leido = null;
        await new CorrelacionMiddleware(c => { leido = ContextoCorrelacion.Obtener(c); return Task.CompletedTask; }).InvokeAsync(ctx);
        Assert.Equal("orden_123-A", leido);
        Assert.Equal("orden_123-A", ctx.Response.Headers["X-Correlation-ID"]);
    }
    [Theory]
    [InlineData("")]
    [InlineData("valor\r\ninyectado")]
    [InlineData("con espacio")]
    [InlineData("áéí")]
    [InlineData("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")]
    public async Task Correlacion_invalida_se_sustituye_sin_propagar_la_entrada(string entrada)
    {
        var ctx = Contexto(entrada);
        await new CorrelacionMiddleware(_ => Task.CompletedTask).InvokeAsync(ctx);
        var id = ctx.Response.Headers["X-Correlation-ID"].ToString();
        Assert.Matches("^[a-f0-9]{32}$", id);
        Assert.NotEqual(entrada, id);
        Assert.Equal(id, ContextoCorrelacion.Obtener(ctx));
    }
    [Fact]
    public async Task Correlacion_ausente_se_genera()
    {
        var ctx = Contexto();
        await new CorrelacionMiddleware(_ => Task.CompletedTask).InvokeAsync(ctx);
        Assert.Matches("^[a-f0-9]{32}$", ContextoCorrelacion.Obtener(ctx));
    }
    [Fact]
    public async Task Resumen_JSON_contiene_propiedades_tipadas_y_no_datos_de_la_peticion()
    {
        var sink = new Captura();
        using var logger = new LoggerConfiguration().Enrich.FromLogContext().WriteTo.Sink(sink).CreateLogger();
        using var factory = new SerilogLoggerFactory(logger, dispose: false);
        var resumen = new ResumenPeticionMiddleware(c => { c.Response.StatusCode = 503; return Task.CompletedTask; },
            factory.CreateLogger<ResumenPeticionMiddleware>());
        await new CorrelacionMiddleware(resumen.InvokeAsync).InvokeAsync(Contexto("peticion-1"));
        var evento = Assert.Single(sink.Eventos);
        using var writer = new StringWriter(); new JsonFormatter().Format(evento, writer);
        var json = writer.ToString(); using var doc = JsonDocument.Parse(json);
        var props = doc.RootElement.GetProperty("Properties");
        Assert.Equal("peticion-1", props.GetProperty("CorrelationId").GetString());
        Assert.Equal("/material/{nombre}", props.GetProperty("Ruta").GetString());
        Assert.Equal(503, props.GetProperty("Estado").GetInt32());
        Assert.True(props.GetProperty("Milisegundos").GetDouble() >= 0);
        Assert.False(string.IsNullOrWhiteSpace(props.GetProperty("TraceId").GetString()));
        Assert.Equal(LogEventLevel.Error, evento.Level);
        Assert.DoesNotContain("secreto", json);
    }
    [Fact]
    public async Task Ruta_no_encontrada_no_registra_el_texto_libre_de_la_URL()
    {
        var sink = new Captura(); using var logger = new LoggerConfiguration().Enrich.FromLogContext().WriteTo.Sink(sink).CreateLogger();
        using var factory = new SerilogLoggerFactory(logger, false);
        var ctx = Contexto("ausente"); ctx.SetEndpoint(null);
        var resumen = new ResumenPeticionMiddleware(c => { c.Response.StatusCode = 404; return Task.CompletedTask; }, factory.CreateLogger<ResumenPeticionMiddleware>());
        await new CorrelacionMiddleware(resumen.InvokeAsync).InvokeAsync(ctx);
        var e = Assert.Single(sink.Eventos);
        Assert.Equal("[sin-ruta]", ((ScalarValue)e.Properties["Ruta"]).Value);
        Assert.DoesNotContain("secreto", e.RenderMessage());
    }
    [Fact]
    public async Task Peticiones_concurrentes_no_mezclan_su_correlacion()
    {
        var sink = new Captura(); using var logger = new LoggerConfiguration().Enrich.FromLogContext().WriteTo.Sink(sink).CreateLogger();
        using var factory = new SerilogLoggerFactory(logger, false);
        var resumen = new ResumenPeticionMiddleware(async _ => await Task.Yield(), factory.CreateLogger<ResumenPeticionMiddleware>());
        await Task.WhenAll(Enumerable.Range(0, 12).Select(i => new CorrelacionMiddleware(resumen.InvokeAsync).InvokeAsync(Contexto("paralelo-" + i))));
        Assert.Equal(12, sink.Eventos.Count);
        var ids = sink.Eventos.Select(e => (string)((ScalarValue)e.Properties["CorrelationId"]).Value!).Order().ToArray();
        Assert.Equal(Enumerable.Range(0, 12).Select(i => "paralelo-" + i).Order(), ids);
    }
    private sealed class Transporte : HttpMessageHandler
    {
        public string? Recibido;
        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken ct)
        {
            Recibido = request.Headers.TryGetValues("X-Correlation-ID", out var values) ? values.Single() : null;
            return Task.FromResult(new HttpResponseMessage(System.Net.HttpStatusCode.OK));
        }
    }
    [Fact]
    public async Task Cliente_saliente_propaga_la_correlacion_validada()
    {
        var ctx = Contexto("cadena-servicios"); var accessor = new HttpContextAccessor { HttpContext = ctx }; var terminal = new Transporte();
        using var http = new HttpClient(new PropagarCorrelacionHandler(accessor) { InnerHandler = terminal });
        await new CorrelacionMiddleware(async _ => { using var response = await http.GetAsync("http://inventario/material"); }).InvokeAsync(ctx);
        Assert.Equal("cadena-servicios", terminal.Recibido);
    }
    [Fact]
    public async Task Cliente_sin_contexto_HTTP_no_reutiliza_correlacion_anterior()
    {
        var terminal = new Transporte(); var accessor = new HttpContextAccessor { HttpContext = null };
        using var http = new HttpClient(new PropagarCorrelacionHandler(accessor) { InnerHandler = terminal });
        using var response = await http.GetAsync("http://inventario/material");
        Assert.Null(terminal.Recibido);
    }
    [Fact]
    public void Registro_del_servicio_emite_propiedades_estructuradas_por_Serilog()
    {
        var sink = new Captura(); var services = new ServiceCollection(); services.AddSingleton<ILogEventSink>(sink);
        services.AddLoggingAceria("Inventario");
        using var provider = services.BuildServiceProvider();
        provider.GetRequiredService<ILogger<LoggingFuncionalTests>>().LogInformation("Lote {Cantidad}", 23);
        var e = Assert.Single(sink.Eventos);
        Assert.Equal("Inventario", ((ScalarValue)e.Properties["Servicio"]).Value);
        Assert.Equal(23, ((ScalarValue)e.Properties["Cantidad"]).Value);
    }

    [Fact]
    public void Nivel_minimo_configurado_filtra_informacion_y_conserva_avisos()
    {
        var sink = new Captura(); var services = new ServiceCollection(); services.AddSingleton<ILogEventSink>(sink);
        var config = new ConfigurationBuilder().AddInMemoryCollection(new Dictionary<string, string?>
            { ["Observabilidad:NivelMinimo"] = "Warning" }).Build();
        services.AddLoggingAceria("Inventario", config);
        using var provider = services.BuildServiceProvider(); var log = provider.GetRequiredService<ILogger<LoggingFuncionalTests>>();
        log.LogInformation("Lote {Cantidad}", 23); log.LogWarning("Intento {Intento}", 5);
        var e = Assert.Single(sink.Eventos); Assert.Equal(LogEventLevel.Warning, e.Level);
        Assert.Equal(5, ((ScalarValue)e.Properties["Intento"]).Value);
    }
}
