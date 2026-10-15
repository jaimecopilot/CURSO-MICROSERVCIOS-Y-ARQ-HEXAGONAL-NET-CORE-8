// INICIO PASO 2.3.9 — Activar el código correspondiente a este paso.
// using FluentValidation;
// namespace AceriaApp.Monolito.Api.Validacion;
// public class ValidationFilter<T>:IEndpointFilter where T:class
// {
//     private readonly IValidator<T> _validator;
//     public ValidationFilter(IValidator<T> validator) => _validator=validator;
//     public async ValueTask<object?> InvokeAsync(EndpointFilterInvocationContext context,EndpointFilterDelegate next)
//     {
//         var request=context.Arguments.OfType<T>().FirstOrDefault();
//         if(request is null) return Results.BadRequest();
//         var result=await _validator.ValidateAsync(request);
//         if(!result.IsValid)
//         {
//             var errors=result.Errors.GroupBy(e=>e.PropertyName)
//                 .ToDictionary(g=>g.Key,g=>g.Select(e=>e.ErrorMessage).ToArray());
//             return Results.ValidationProblem(errors);
//         }
//         return await next(context);
//     }
// }
// FIN PASO 2.3.9
