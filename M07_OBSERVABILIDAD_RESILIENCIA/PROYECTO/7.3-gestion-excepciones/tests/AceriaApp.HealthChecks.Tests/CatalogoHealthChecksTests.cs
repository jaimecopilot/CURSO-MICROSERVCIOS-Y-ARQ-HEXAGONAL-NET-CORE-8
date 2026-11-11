using AceriaApp.Api.HealthChecks;
using FluentAssertions;
using Xunit;

namespace AceriaApp.HealthChecks.Tests;

public class CatalogoHealthChecksTests
{
    [Fact]
    public void HealthChecksPorDefecto_ContieneTresHealthChecks()
    {
        var healthChecks = CatalogoHealthChecks.HealthChecksPorDefecto();

        healthChecks.Should().HaveCount(3);
    }

    [Fact]
    public void HealthChecksPorDefecto_ContieneUnLiveness()
    {
        var healthChecks = CatalogoHealthChecks.HealthChecksPorDefecto();

        healthChecks.Count(h => h.Tipo == "Liveness").Should().Be(1);
    }

    [Fact]
    public void HealthChecksPorDefecto_ContieneDosReadiness()
    {
        var healthChecks = CatalogoHealthChecks.HealthChecksPorDefecto();

        healthChecks.Count(h => h.Tipo == "Readiness").Should().Be(2);
    }

    [Fact]
    public void HealthChecksPorDefecto_TodosTienenTimeout()
    {
        var healthChecks = CatalogoHealthChecks.HealthChecksPorDefecto();

        healthChecks.Should().OnlyContain(h => h.TieneTimeout);
    }

    [Fact]
    public void HealthChecksPorDefecto_NingunoExponeInformacionSensible()
    {
        var healthChecks = CatalogoHealthChecks.HealthChecksPorDefecto();

        healthChecks.Should().OnlyContain(h => !h.ExponeInformacionSensible);
    }
}
