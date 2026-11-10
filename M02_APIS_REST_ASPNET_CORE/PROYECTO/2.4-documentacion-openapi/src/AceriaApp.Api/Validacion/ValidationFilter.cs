using FluentValidation;
namespace AceriaApp.Api.Validacion;
// INICIO PASO 2.3.8
public sealed class ValidationFilter<T>(IValidator<T> validator): IEndpointFilter where T:class
{
    public async ValueTask<object?> InvokeAsync(EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        // PASO 2.3.9: extraer el contrato recibido.
        var request=context.Arguments.OfType<T>().FirstOrDefault();
        if(request is null) return Results.ValidationProblem(
            new Dictionary<string,string[]> { ["body"]=new[]{"Falta el cuerpo."} });
        // PASO 2.3.10: validar y respetar cancelaciones.
        var result=await validator.ValidateAsync(request,context.HttpContext.RequestAborted);
        if(!result.IsValid)
        {
            // PASO 2.3.11: agrupar errores por propiedad.
            var errors=result.Errors.GroupBy(x=>x.PropertyName)
                .ToDictionary(x=>x.Key,x=>x.Select(e=>e.ErrorMessage).ToArray());
            // PASO 2.3.12: responder 400 sin entrar en el manejador.
            return Results.ValidationProblem(errors);
        }
        // PASO 2.3.13: invocar el manejador solo si la entrada es valida.
        return await next(context);
    }
}
// FIN PASO 2.3.8
