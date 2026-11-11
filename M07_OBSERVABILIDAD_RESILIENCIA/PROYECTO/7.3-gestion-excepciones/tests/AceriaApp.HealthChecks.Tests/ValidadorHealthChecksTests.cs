using AceriaApp.Api.HealthChecks;
using FluentAssertions;
using Xunit;

namespace AceriaApp.HealthChecks.Tests;

public class ValidadorHealthChecksTests
{
    private readonly ValidadorHealthChecks _validador = new();

    [Fact]
    public void Validar_CatalogoPorDefecto_DevuelveValido()
    {
        var resultado = _validador.Validar(CatalogoHealthChecks.HealthChecksPorDefecto());

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }

    [Fact]
    public void Validar_SinHealthChecks_DevuelveError()
    {
        var resultado = _validador.Validar(new List<HealthCheck>());

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("No hay health checks"));
    }

    [Fact]
    public void Validar_TipoNoPermitido_DevuelveError()
    {
        var healthChecks = new List<HealthCheck>
        {
            new() { Nombre = "X", Tipo = "TipoInventado", Recurso = "A", TieneTimeout = true }
        };

        var resultado = _validador.Validar(healthChecks);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("Tipo no permitido"));
    }

    [Fact]
    public void Validar_SinRecurso_DevuelveError()
    {
        var healthChecks = new List<HealthCheck>
        {
            new() { Nombre = "X", Tipo = "Readiness", Recurso = string.Empty, TieneTimeout = true }
        };

        var resultado = _validador.Validar(healthChecks);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no declara el recurso"));
    }

    [Fact]
    public void Validar_SinTimeout_DevuelveError()
    {
        var healthChecks = new List<HealthCheck>
        {
            new() { Nombre = "X", Tipo = "Readiness", Recurso = "A", TieneTimeout = false }
        };

        var resultado = _validador.Validar(healthChecks);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("no tiene timeout"));
    }

    [Fact]
    public void Validar_InformacionSensible_DevuelveError()
    {
        var healthChecks = new List<HealthCheck>
        {
            new() { Nombre = "X", Tipo = "Readiness", Recurso = "A", TieneTimeout = true, ExponeInformacionSensible = true }
        };

        var resultado = _validador.Validar(healthChecks);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("expone información sensible"));
    }
    [Fact]
    public void Validar_LivenessConDependenciaExterna_DevuelveError()
    {
        var checks = new List<HealthCheck>
        {
            new() { Nombre = "Self", Tipo = "Liveness", Recurso = "SQL Server", ConsultaDependenciaExterna = true, TieneTimeout = true }
        };

        var resultado = _validador.Validar(checks);

        resultado.EsValida.Should().BeFalse();
        resultado.Errores.Should().Contain(e => e.Contains("consulta una dependencia externa"));
    }

    [Fact]
    public void Validar_ReadinessConDependenciaExterna_DevuelveValido()
    {
        var checks = new List<HealthCheck>
        {
            new() { Nombre = "SQL", Tipo = "Readiness", Recurso = "SQL Server", ConsultaDependenciaExterna = true, TieneTimeout = true }
        };

        var resultado = _validador.Validar(checks);

        resultado.EsValida.Should().BeTrue();
        resultado.Errores.Should().BeEmpty();
    }
}
