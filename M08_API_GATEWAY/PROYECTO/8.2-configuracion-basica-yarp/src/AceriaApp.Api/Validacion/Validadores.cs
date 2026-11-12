using AceriaApp.Api.Contratos;
using FluentValidation;

namespace AceriaApp.Api.Validacion;

public sealed class CrearOrdenValidator : AbstractValidator<CrearOrdenRequest>
{
    public CrearOrdenValidator()
    {
        RuleFor(x => x.Cliente).NotEmpty().MaximumLength(100);
        RuleFor(x => x.Material).NotEmpty().MaximumLength(100);
        RuleFor(x => x.Cantidad).InclusiveBetween(1, 10000);
    }
}

// Añade al final de Validadores.cs, fuera de CrearOrdenValidator:
public sealed class ActualizarCantidadValidator
    : AbstractValidator<ActualizarCantidadRequest>
{
    public ActualizarCantidadValidator()
    {
        RuleFor(x => x.Cantidad).InclusiveBetween(1, 10000);
    }
}
