using System.Net;
using System.Net.Http.Headers;
using System.Text;
using AceriaApp.Comunicacion.Aplicacion;
using AceriaApp.Comunicacion.Infraestructura;
using AceriaApp.Observabilidad;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Time.Testing;
using Polly.CircuitBreaker;
using Polly.Timeout;
using Xunit;
namespace AceriaApp.Resiliencia.Tests;

public sealed class ResilienciaFuncionalTests
{
    [Fact]
    public async Task Un_503_se_reintenta_y_libera_su_respuesta_antes_del_200()
    {
        var contenido = new ContenidoRastreado("fallo temporal");
        using var prueba = new Banco((_, intento, _) => Task.FromResult(intento == 1
            ? new HttpResponseMessage(HttpStatusCode.ServiceUnavailable) { Content = contenido }
            : Respuesta(HttpStatusCode.OK)));
        using var http = prueba.CrearCliente();
        using var respuesta = await prueba.CompletarAsync(http.GetAsync("material"));
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        Assert.Equal(2, prueba.Transporte.Intentos);
        Assert.True(contenido.Liberado);
        var evento = Assert.Single(prueba.Logs.Entradas, x => x.Id == 7401);
        Assert.Equal("AceriaApp.Resiliencia", evento.Categoria);
        Assert.Null(evento.Excepcion);
        Assert.Equal(1, evento.Propiedades["Intento"]);
        Assert.Equal(503, evento.Propiedades["EstadoHttp"]);
        Assert.DoesNotContain("fallo temporal", evento.Mensaje);
    }

    [Theory]
    [InlineData(408)] [InlineData(429)] [InlineData(500)] [InlineData(502)] [InlineData(503)] [InlineData(504)]
    public async Task Estados_transitorios_permiten_recuperar_la_lectura(int estado)
    {
        using var prueba = new Banco((_, intento, _) => Task.FromResult(Respuesta(intento == 1 ? (HttpStatusCode)estado : HttpStatusCode.OK)));
        using var http = prueba.CrearCliente();
        using var respuesta = await prueba.CompletarAsync(http.GetAsync("material"));
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        Assert.Equal(2, prueba.Transporte.Intentos);
    }

    [Theory]
    [InlineData("GET")] [InlineData("HEAD")] [InlineData("OPTIONS")]
    public async Task Solo_los_metodos_de_lectura_permiten_reintento(string metodo)
    {
        using var prueba = new Banco((_, intento, _) => Task.FromResult(Respuesta(intento == 1 ? HttpStatusCode.ServiceUnavailable : HttpStatusCode.OK)));
        using var http = prueba.CrearCliente();
        using var peticion = new HttpRequestMessage(new HttpMethod(metodo), "material");
        using var respuesta = await prueba.CompletarAsync(http.SendAsync(peticion));
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        Assert.Equal(2, prueba.Transporte.Intentos);
    }

    [Theory]
    [InlineData(400)] [InlineData(401)] [InlineData(403)] [InlineData(404)]
    public async Task Errores_no_transitorios_no_se_reintentan(int estado)
    {
        using var prueba = new Banco((_, _, _) => Task.FromResult(Respuesta((HttpStatusCode)estado)));
        using var http = prueba.CrearCliente();
        using var respuesta = await prueba.CompletarAsync(http.GetAsync("material"));
        Assert.Equal((HttpStatusCode)estado, respuesta.StatusCode);
        Assert.Equal(1, prueba.Transporte.Intentos);
    }

    [Theory]
    [InlineData("POST")] [InlineData("PUT")] [InlineData("PATCH")] [InlineData("DELETE")]
    public async Task Un_metodo_mutante_no_repite_el_cuerpo_tras_un_503(string metodo)
    {
        var cuerpos = new List<string>();
        using var prueba = new Banco(async (peticion, _, ct) =>
        {
            cuerpos.Add(await peticion.Content!.ReadAsStringAsync(ct));
            return Respuesta(HttpStatusCode.ServiceUnavailable);
        });
        using var http = prueba.CrearCliente();
        using var peticion = new HttpRequestMessage(new HttpMethod(metodo), "material") { Content = new StringContent("orden irrepetible") };
        using var respuesta = await prueba.CompletarAsync(http.SendAsync(peticion));
        Assert.Equal(HttpStatusCode.ServiceUnavailable, respuesta.StatusCode);
        Assert.Equal(new[] { "orden irrepetible" }, cuerpos);
        Assert.Equal(1, prueba.Transporte.Intentos);
    }

    [Fact]
    public async Task Una_lectura_agota_tres_intentos_y_conserva_la_ultima_respuesta()
    {
        var contenidos = new List<ContenidoRastreado>();
        using var prueba = new Banco((_, _, _) =>
        {
            var contenido = new ContenidoRastreado("sigue caído"); contenidos.Add(contenido);
            return Task.FromResult(new HttpResponseMessage(HttpStatusCode.ServiceUnavailable) { Content = contenido });
        });
        using var http = prueba.CrearCliente();
        using var respuesta = await prueba.CompletarAsync(http.GetAsync("material"));
        Assert.Equal(HttpStatusCode.ServiceUnavailable, respuesta.StatusCode);
        Assert.Equal(3, prueba.Transporte.Intentos);
        Assert.True(contenidos[0].Liberado);
        Assert.True(contenidos[1].Liberado);
        Assert.False(contenidos[2].Liberado);
        Assert.Equal("sigue caído", await respuesta.Content.ReadAsStringAsync());
    }

    [Fact]
    public async Task Un_error_de_transporte_se_reintenta()
    {
        using var prueba = new Banco((_, intento, _) => intento == 1
            ? Task.FromException<HttpResponseMessage>(new HttpRequestException("conexión rechazada"))
            : Task.FromResult(Respuesta(HttpStatusCode.OK)));
        using var http = prueba.CrearCliente();
        using var respuesta = await prueba.CompletarAsync(http.GetAsync("material"));
        Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        Assert.Equal(2, prueba.Transporte.Intentos);
    }

    [Fact]
    public async Task Cancelar_la_peticion_interrumpe_el_transporte_sin_reintentar()
    {
        var entrada = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
        using var prueba = new Banco(async (_, _, ct) =>
        { entrada.TrySetResult(); await Task.Delay(Timeout.InfiniteTimeSpan, ct); return Respuesta(HttpStatusCode.OK); });
        using var http = prueba.CrearCliente();
        using var cancelacion = new CancellationTokenSource();
        var tarea = new ClienteInventarioResiliente(http).ObtenerAsync("CH-01", cancelacion.Token);
        await entrada.Task.WaitAsync(TimeSpan.FromSeconds(3));
        cancelacion.Cancel();
        await Assert.ThrowsAnyAsync<OperationCanceledException>(async () => await tarea);
        Assert.Equal(1, prueba.Transporte.Intentos);
    }

    [Fact]
    public async Task Cancelar_durante_retry_after_impide_un_segundo_envio()
    {
        using var prueba = new Banco((_, _, _) =>
        {
            var respuesta = Respuesta(HttpStatusCode.TooManyRequests);
            respuesta.Headers.RetryAfter = new RetryConditionHeaderValue(TimeSpan.FromSeconds(30));
            return Task.FromResult(respuesta);
        });
        using var http = prueba.CrearCliente();
        using var cancelacion = new CancellationTokenSource();
        var tarea = http.GetAsync("material", cancelacion.Token);
        cancelacion.Cancel();
        await Assert.ThrowsAnyAsync<OperationCanceledException>(async () => await tarea);
        Assert.Equal(1, prueba.Transporte.Intentos);
    }

    [Fact]
    public async Task Un_timeout_de_intento_cancela_transporte_o_cuerpo_y_permite_recuperar()
    {
        foreach (var cuerpoLento in new[] { false, true })
        {
            var cancelados = 0;
            ContenidoLento? contenido = null;
            using var prueba = new Banco(async (_, intento, ct) =>
            {
                if (intento == 1)
                {
                    if (cuerpoLento)
                        return new HttpResponseMessage(HttpStatusCode.OK)
                        { Content = contenido = new ContenidoLento(() => Interlocked.Increment(ref cancelados)) };
                    try { await Task.Delay(Timeout.InfiniteTimeSpan, ct); }
                    catch (OperationCanceledException) { Interlocked.Increment(ref cancelados); throw; }
                }
                return Respuesta(HttpStatusCode.OK);
            });
            using var http = prueba.CrearCliente();
            using var respuesta = await prueba.CompletarAsync(http.GetAsync("material"));
            Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
            Assert.Equal(2, prueba.Transporte.Intentos);
            Assert.Equal(1, cancelados);
            if (cuerpoLento) Assert.True(contenido!.Liberado);
        }
    }

    [Fact]
    public async Task Tres_intentos_lentos_terminan_en_indisponibilidad_y_no_exponen_Polly_al_puerto()
    {
        using var prueba = new Banco(async (_, _, ct) =>
        { await Task.Delay(Timeout.InfiniteTimeSpan, ct); return Respuesta(HttpStatusCode.OK); });
        using var http = prueba.CrearCliente();
        var error = await Assert.ThrowsAsync<InventarioNoDisponibleException>(async () =>
            await prueba.CompletarAsync(new ClienteInventarioResiliente(http).ObtenerAsync("CH-01", CancellationToken.None)));
        Assert.IsType<TimeoutRejectedException>(error.InnerException);
        Assert.Equal(3, prueba.Transporte.Intentos);
    }

    [Theory]
    [InlineData(false)] [InlineData(true)]
    public async Task El_presupuesto_total_acota_retry_after_en_segundos_y_fecha(bool fecha)
    {
        using var prueba = new Banco((_, _, _) => Task.FromResult(Respuesta(HttpStatusCode.TooManyRequests)));
        prueba.Transporte.Responder = (_, _, _) =>
        {
            var respuesta = Respuesta(HttpStatusCode.TooManyRequests);
            respuesta.Headers.RetryAfter = fecha
                ? new RetryConditionHeaderValue(prueba.Reloj.GetUtcNow().AddMinutes(1))
                : new RetryConditionHeaderValue(TimeSpan.FromMinutes(1));
            return Task.FromResult(respuesta);
        };
        using var http = prueba.CrearCliente();
        var inicio = prueba.Reloj.GetUtcNow();
        await Assert.ThrowsAsync<TimeoutRejectedException>(async () => await prueba.CompletarAsync(http.GetAsync("material")));
        Assert.InRange((prueba.Reloj.GetUtcNow() - inicio).TotalSeconds, 6, 7);
        Assert.Equal(1, prueba.Transporte.Intentos);
    }

    [Fact]
    public async Task El_circuito_se_comparte_entre_clientes_y_recupera_con_una_sonda_half_open()
    {
        var sondaEntrada = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
        var sondaSalida = new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
        using var prueba = new Banco(async (_, intento, ct) =>
        {
            if (intento <= 4) return Respuesta(HttpStatusCode.ServiceUnavailable);
            if (intento == 5) { sondaEntrada.TrySetResult(); await sondaSalida.Task.WaitAsync(ct); }
            return Respuesta(HttpStatusCode.OK);
        });
        using (var primero = prueba.CrearCliente())
            for (var i = 0; i < 4; i++)
            { using var fallo = await primero.PostAsync("material", null); Assert.Equal(HttpStatusCode.ServiceUnavailable, fallo.StatusCode); }
        using var segundo = prueba.CrearCliente();
        await Assert.ThrowsAsync<BrokenCircuitException>(async () => await segundo.GetAsync("material").WaitAsync(TimeSpan.FromSeconds(2)));
        Assert.Equal(4, prueba.Transporte.Intentos);
        prueba.Reloj.Advance(TimeSpan.FromSeconds(5));
        var sonda = segundo.GetAsync("material");
        await sondaEntrada.Task.WaitAsync(TimeSpan.FromSeconds(3));
        using var tercero = prueba.CrearCliente();
        await Assert.ThrowsAsync<BrokenCircuitException>(async () => await tercero.GetAsync("material").WaitAsync(TimeSpan.FromSeconds(2)));
        Assert.Equal(5, prueba.Transporte.Intentos);
        sondaSalida.TrySetResult();
        using var recuperada = await sonda;
        using var siguiente = await tercero.GetAsync("material");
        Assert.Equal(HttpStatusCode.OK, recuperada.StatusCode);
        Assert.Equal(HttpStatusCode.OK, siguiente.StatusCode);
        Assert.Equal(6, prueba.Transporte.Intentos);
        Assert.Single(prueba.Logs.Entradas, x => x.Id == 7402 && x.Propiedades["Estado"]?.ToString() == "abierto");
        Assert.Single(prueba.Logs.Entradas, x => x.Id == 7403 && x.Propiedades["Estado"]?.ToString() == "cerrado");
        Assert.All(prueba.Logs.Entradas.Where(x => x.Categoria == "AceriaApp.Resiliencia"), x => Assert.Null(x.Excepcion));
    }

    [Fact]
    public async Task Un_destino_caido_no_abre_el_circuito_de_otro_destino()
    {
        using var prueba = new Banco((peticion, _, _) => Task.FromResult(Respuesta(
            peticion.RequestUri!.Host == "caido.test" ? HttpStatusCode.ServiceUnavailable : HttpStatusCode.OK)));
        using var http = prueba.CrearCliente();
        for (var i = 0; i < 4; i++) { using var fallo = await http.PostAsync("http://caido.test/material", null); }
        await Assert.ThrowsAsync<BrokenCircuitException>(async () => await http.GetAsync("http://caido.test/material"));
        using var sana = await http.GetAsync("http://sano.test/material");
        Assert.Equal(HttpStatusCode.OK, sana.StatusCode);
        Assert.Equal(5, prueba.Transporte.Intentos);
    }

    [Fact]
    public async Task Los_404_y_las_cancelaciones_no_abren_el_circuito()
    {
        using var prueba = new Banco((_, _, _) => Task.FromResult(Respuesta(HttpStatusCode.NotFound)));
        using var http = prueba.CrearCliente();
        for (var i = 0; i < 5; i++) { using var noExiste = await http.GetAsync("material"); Assert.Equal(HttpStatusCode.NotFound, noExiste.StatusCode); }
        for (var i = 0; i < 5; i++)
        {
            using var cancelacion = new CancellationTokenSource();
            prueba.Transporte.Responder = async (_, _, ct) => { cancelacion.Cancel(); await Task.Delay(Timeout.InfiniteTimeSpan, ct); return Respuesta(HttpStatusCode.OK); };
            await Assert.ThrowsAnyAsync<OperationCanceledException>(async () => await http.GetAsync("material", cancelacion.Token));
        }
        prueba.Transporte.Responder = (_, _, _) => Task.FromResult(Respuesta(HttpStatusCode.OK));
        using var sana = await http.GetAsync("material");
        Assert.Equal(HttpStatusCode.OK, sana.StatusCode);
        Assert.Equal(11, prueba.Transporte.Intentos);
    }

    [Fact]
    public async Task El_registro_sustituye_el_cliente_M6_y_mantiene_el_contrato_del_puerto()
    {
        using var prueba = new Banco((_, intento, _) => Task.FromResult(intento == 1
            ? Respuesta(HttpStatusCode.ServiceUnavailable)
            : new HttpResponseMessage(HttpStatusCode.OK) { Content = new StringContent("{\"material\":\"CH-01\",\"stock\":20}", Encoding.UTF8, "application/json") }), registroCompleto: true);
        var cliente = prueba.Servicios.GetRequiredService<IClienteInventario>();
        var material = await prueba.CompletarAsync(cliente.ObtenerAsync("CH-01", CancellationToken.None));
        Assert.NotNull(material);
        Assert.Equal("CH-01", material.Material);
        Assert.Equal(20, material.Stock);
        Assert.Equal(2, prueba.Transporte.Intentos);
        Assert.Equal("http://inventario.test/api/v1/materiales/CH-01", prueba.Transporte.UltimaUri!.AbsoluteUri);
        Assert.Single(prueba.Servicios.GetServices<IClienteInventario>());
    }

    [Fact]
    public async Task El_adaptador_conserva_el_404_como_ausencia_de_material()
    {
        using var prueba = new Banco((_, _, _) => Task.FromResult(Respuesta(HttpStatusCode.NotFound)), registroCompleto: true);
        var resultado = await prueba.Servicios.GetRequiredService<IClienteInventario>().ObtenerAsync("NO-EXISTE", CancellationToken.None);
        Assert.Null(resultado);
        Assert.Equal(1, prueba.Transporte.Intentos);
    }

    [Fact]
    public async Task Un_circuito_abierto_se_traduce_a_indisponibilidad_en_el_puerto()
    {
        using var prueba = new Banco((_, _, _) => Task.FromResult(Respuesta(HttpStatusCode.ServiceUnavailable)));
        using var http = prueba.CrearCliente();
        for (var i = 0; i < 4; i++) { using var fallo = await http.PostAsync("material", null); }
        var error = await Assert.ThrowsAsync<InventarioNoDisponibleException>(() => new ClienteInventarioResiliente(http).ObtenerAsync("CH-01", CancellationToken.None));
        Assert.IsAssignableFrom<BrokenCircuitException>(error.InnerException);
        Assert.Equal(4, prueba.Transporte.Intentos);
    }

    private static HttpResponseMessage Respuesta(HttpStatusCode estado) => new(estado) { Content = new StringContent("respuesta") };

    private sealed class Banco : IDisposable
    {
        public FakeTimeProvider Reloj { get; } = new();
        public ProveedorCaptura Logs { get; } = new();
        public TransporteControlado Transporte { get; }
        public ServiceProvider Servicios { get; }
        private readonly string nombre;
        public Banco(Func<HttpRequestMessage, int, CancellationToken, Task<HttpResponseMessage>> responder, bool registroCompleto = false)
        {
            Transporte = new TransporteControlado(responder);
            var services = new ServiceCollection();
            services.AddLogging(logging => logging.AddProvider(Logs));
            services.AddSingleton<TimeProvider>(Reloj);
            nombre = registroCompleto ? "inventario-resiliente" : "lectura-prueba";
            if (registroCompleto)
            {
                var config = new ConfigurationBuilder().AddInMemoryCollection(new Dictionary<string, string?>
                { ["Comunicacion:InventarioUrl"] = "http://inventario.test/" }).Build();
                services.AddComunicacion(config);
                services.AddResilienciaInventario(config);
                services.AddHttpClient(nombre).ConfigurePrimaryHttpMessageHandler(() => Transporte);
            }
            else
                services.AddHttpClient(nombre, http => { http.BaseAddress = new Uri("http://inventario.test/"); http.Timeout = Timeout.InfiniteTimeSpan; })
                    .ConfigurePrimaryHttpMessageHandler(() => Transporte).AddPoliticaResilienciaInventario();
            Servicios = services.BuildServiceProvider();
        }
        public HttpClient CrearCliente() => Servicios.GetRequiredService<IHttpClientFactory>().CreateClient(nombre);
        public async Task<T> CompletarAsync<T>(Task<T> tarea)
        {
            // Cada paso cede al planificador; solo el reloj virtual hace avanzar las políticas.
            for (var paso = 0; paso < 100 && !tarea.IsCompleted; paso++)
            { await Task.Delay(1); if (!tarea.IsCompleted) Reloj.Advance(TimeSpan.FromMilliseconds(100)); }
            return await tarea.WaitAsync(TimeSpan.FromSeconds(2));
        }
        public void Dispose() { Servicios.Dispose(); Transporte.Dispose(); }
    }

    private sealed class TransporteControlado(Func<HttpRequestMessage, int, CancellationToken, Task<HttpResponseMessage>> responder) : HttpMessageHandler
    {
        private int intentos;
        public int Intentos => Volatile.Read(ref intentos);
        public Uri? UltimaUri { get; private set; }
        public Func<HttpRequestMessage, int, CancellationToken, Task<HttpResponseMessage>> Responder { get; set; } = responder;
        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        { UltimaUri = request.RequestUri; return Responder(request, Interlocked.Increment(ref intentos), cancellationToken); }
    }

    private sealed class ContenidoLento(Action cancelado) : HttpContent
    {
        public bool Liberado { get; private set; }
        protected override bool TryComputeLength(out long length) { length = 0; return false; }
        protected override Task SerializeToStreamAsync(Stream stream, TransportContext? context) =>
            SerializeToStreamAsync(stream, context, CancellationToken.None);
        protected override async Task SerializeToStreamAsync(Stream stream, TransportContext? context, CancellationToken cancellationToken)
        {
            try { await Task.Delay(Timeout.InfiniteTimeSpan, cancellationToken); }
            catch (OperationCanceledException) { cancelado(); throw; }
        }
        protected override void Dispose(bool disposing) { Liberado = true; base.Dispose(disposing); }
    }

    private sealed record EntradaLog(string Categoria, int Id, string Mensaje, Exception? Excepcion, Dictionary<string, object?> Propiedades);
    private sealed class ProveedorCaptura : ILoggerProvider
    {
        public System.Collections.Concurrent.ConcurrentQueue<EntradaLog> Entradas { get; } = new();
        public ILogger CreateLogger(string categoryName) => new Captura(categoryName, Entradas);
        public void Dispose() { }
        private sealed class Captura(string categoria, System.Collections.Concurrent.ConcurrentQueue<EntradaLog> entradas) : ILogger
        {
            public IDisposable? BeginScope<TState>(TState state) where TState : notnull => null;
            public bool IsEnabled(LogLevel logLevel) => true;
            public void Log<TState>(LogLevel logLevel, EventId eventId, TState state, Exception? exception, Func<TState, Exception?, string> formatter) =>
                entradas.Enqueue(new EntradaLog(categoria, eventId.Id, formatter(state, exception), exception,
                    state is IEnumerable<KeyValuePair<string, object?>> propiedades ? propiedades.ToDictionary(x => x.Key, x => x.Value) : new()));
        }
    }

    private sealed class ContenidoRastreado(string contenido) : StringContent(contenido)
    {
        public bool Liberado { get; private set; }
        protected override void Dispose(bool disposing) { Liberado = true; base.Dispose(disposing); }
    }
}
