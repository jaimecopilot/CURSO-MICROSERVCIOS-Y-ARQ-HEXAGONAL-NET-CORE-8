using AceriaApp.Api.ResultPattern;
using FluentAssertions;
using Xunit;

namespace AceriaApp.ResultPattern.Tests;

public class ResultTests
{
    [Fact]
    public void Success_ConValor_DevuelveIsSuccessTrue()
    {
        var result = Result<int>.Success(42);

        result.IsSuccess.Should().BeTrue();
        result.Value.Should().Be(42);
        result.Error.Should().BeNull();
    }

    [Fact]
    public void Failure_ConError_DevuelveIsSuccessFalse()
    {
        var result = Result<int>.Failure("Error de prueba");

        result.IsSuccess.Should().BeFalse();
        result.Value.Should().Be(default);
        result.Error.Should().Be("Error de prueba");
    }

    [Fact]
    public void Success_ConTipoComplejo_DevuelveValorCorrecto()
    {
        var result = Result<string>.Success("AceriaApp");

        result.IsSuccess.Should().BeTrue();
        result.Value.Should().Be("AceriaApp");
    }
}
