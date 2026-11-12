using System.Net;
using System.Text.Json;
using AceriaApp.Observabilidad;
using AceriaApp.PruebasSqlServer;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Data.SqlClient;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Microsoft.Extensions.Hosting;
using Testcontainers.RabbitMq;
using Xunit;
namespace AceriaApp.HealthChecks.Tests;
public class SaludFuncionalTests
{
    private static Task<IHost> Servidor(Action<IHealthChecksBuilder> registrar) => new HostBuilder()
        .ConfigureWebHost(web => web.UseTestServer()
            .ConfigureServices(services => { services.AddRouting(); registrar(services.AddHealthChecks()); })
            .Configure(app => { app.UseRouting(); app.UseEndpoints(endpoints => endpoints.MapSaludAceria()); }))
        .StartAsync();
    [Fact]
    public async Task Liveness_no_ejecuta_dependencias_y_readiness_si()
    {
        var consultas = 0;
        using var host = await Servidor(b => b.AddCheck("sql", () => { consultas++; return HealthCheckResult.Unhealthy("interno"); }, tags: new[] { "ready" }));
        using var http = host.GetTestClient();
        using var live = await http.GetAsync("/health/live");
        Assert.Equal(HttpStatusCode.OK, live.StatusCode); Assert.Equal(0, consultas);
        using var ready = await http.GetAsync("/health/ready");
        Assert.Equal(HttpStatusCode.ServiceUnavailable, ready.StatusCode); Assert.Equal(1, consultas);
    }
    [Fact]
    public async Task Readiness_expone_estado_y_nombre_sin_credenciales_ni_excepcion()
    {
        using var host = await Servidor(b => b.AddCheck("sql", () => HealthCheckResult.Unhealthy("Password=secreto-descripcion", new Exception("secreto-excepcion")), tags: new[] { "ready" }));
        using var http = host.GetTestClient(); using var response = await http.GetAsync("/health/ready");
        var texto = await response.Content.ReadAsStringAsync(); using var doc = JsonDocument.Parse(texto);
        Assert.Equal(HttpStatusCode.ServiceUnavailable, response.StatusCode);
        Assert.Equal("Unhealthy", doc.RootElement.GetProperty("estado").GetString());
        Assert.Equal("sql", Assert.Single(doc.RootElement.GetProperty("componentes").EnumerateArray()).GetProperty("nombre").GetString());
        Assert.DoesNotContain("secreto", texto); Assert.DoesNotContain("Password", texto); Assert.DoesNotContain("exception", texto, StringComparison.OrdinalIgnoreCase);
    }
    [Fact]
    public async Task Readiness_sana_responde_200_y_JSON_comprobable()
    {
        using var host = await Servidor(b => b.AddCheck("sql", () => HealthCheckResult.Healthy(), tags: new[] { "ready" }));
        using var http = host.GetTestClient(); using var response = await http.GetAsync("/health/ready");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        using var doc = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        Assert.Equal("Healthy", doc.RootElement.GetProperty("estado").GetString());
    }
    [Fact]
    public async Task SQL_no_accesible_no_se_presenta_como_sano()
    {
        var check = new SqlServicioHealthCheck("Server=127.0.0.1,1;User Id=sa;Password=secreto-sql;TrustServerCertificate=True;Connect Timeout=1");
        var resultado = await check.CheckHealthAsync(new HealthCheckContext());
        Assert.Equal(HealthStatus.Unhealthy, resultado.Status);
        Assert.Null(resultado.Exception); Assert.DoesNotContain("secreto", resultado.Description ?? "");
    }
    [Fact]
    public async Task SQL_cancelado_no_intenta_recuperarse_ni_inventa_resultado()
    {
        using var cancelacion = new CancellationTokenSource(); cancelacion.Cancel();
        await Assert.ThrowsAnyAsync<OperationCanceledException>(() => new SqlServicioHealthCheck("Server=127.0.0.1,1").CheckHealthAsync(new HealthCheckContext(), cancelacion.Token));
    }
    [Fact]
    public async Task Rabbit_no_accesible_devuelve_no_sano_sin_detalles_internos()
    {
        var resultado = await new RabbitServicioHealthCheck("amqp://usuario:secreto-rabbit@127.0.0.1:1/").CheckHealthAsync(new HealthCheckContext());
        Assert.Equal(HealthStatus.Unhealthy, resultado.Status); Assert.Null(resultado.Exception);
        Assert.DoesNotContain("secreto", resultado.Description ?? "");
    }
    [Fact]
    public async Task Rabbit_cancelado_respeta_el_token_del_llamador()
    {
        using var cancelacion = new CancellationTokenSource(); cancelacion.Cancel();
        await Assert.ThrowsAnyAsync<OperationCanceledException>(() => new RabbitServicioHealthCheck("amqp://guest:guest@127.0.0.1:1/").CheckHealthAsync(new HealthCheckContext(), cancelacion.Token));
    }
    [Fact]
    public async Task Sql_real_distingue_base_existente_y_nombre_inexistente()
    {
        await using var bd = BaseSqlServer.Crear();
        var sana = await new SqlServicioHealthCheck(bd.ConnectionString).CheckHealthAsync(new HealthCheckContext());
        var ausente = new SqlConnectionStringBuilder(bd.ConnectionString) { InitialCatalog = "AceriaMissing_" + Guid.NewGuid().ToString("N") };
        var mala = await new SqlServicioHealthCheck(ausente.ConnectionString).CheckHealthAsync(new HealthCheckContext());
        Assert.Equal(HealthStatus.Healthy, sana.Status); Assert.Equal(HealthStatus.Unhealthy, mala.Status);
    }
    [Fact]
    public async Task Rabbit_real_acredita_conexion_AMQP()
    {
        RabbitMqContainer? temporal = null;
        var uri = Environment.GetEnvironmentVariable("ACERIA_TEST_RABBITMQ");
        try
        {
            if (string.IsNullOrWhiteSpace(uri))
            {
                temporal = new RabbitMqBuilder().WithImage("rabbitmq:4.1.5-management").WithUsername("curso").WithPassword("curso-local").Build();
                await temporal.StartAsync(); uri = temporal.GetConnectionString();
            }
            var estado = await new RabbitServicioHealthCheck(uri).CheckHealthAsync(new HealthCheckContext());
            Assert.Equal(HealthStatus.Healthy, estado.Status);
        }
        finally { if (temporal is not null) await temporal.DisposeAsync(); }
    }
}
