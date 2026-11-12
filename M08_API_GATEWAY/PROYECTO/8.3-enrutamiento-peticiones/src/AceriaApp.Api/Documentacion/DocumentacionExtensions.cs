using AceriaApp.Api.Contratos;
using Microsoft.OpenApi.Any;
using Swashbuckle.AspNetCore.SwaggerGen;
using Microsoft.OpenApi.Models;
// Crea src/AceriaApp.Api/Documentacion/DocumentacionExtensions.cs:
namespace AceriaApp.Api.Documentacion;

public static class DocumentacionExtensions
{
    // En 2.4.4 se añadirá AddDocumentacion.
    // En 2.4.7 se añadirá UseDocumentacion.
// Dentro de DocumentacionExtensions:
public static IServiceCollection AddDocumentacion(
    this IServiceCollection services)
{
    services.AddEndpointsApiExplorer();
    // Sustituye services.AddSwaggerGen() dentro de AddDocumentacion:
services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "AceriaApp — Órdenes de producción",
        Version = "v1",
        Description = "API REST educativa creada con ASP.NET Core 8.",
        Contact = new OpenApiContact
        {
            Name = "Equipo AceriaApp",
            Email = "equipo@acerialocal"
        }
    });
    options.SchemaFilter<EjemploCrearOrden>();
});
    return services;
}

// Añade a la misma clase DocumentacionExtensions:
public static WebApplication UseDocumentacion(this WebApplication app)
{
    if (app.Environment.IsDevelopment())
    {
        app.UseSwagger();
        app.UseSwaggerUI(o =>
            o.SwaggerEndpoint("/swagger/v1/swagger.json", "AceriaApp v1"));
    }
    return app;
}

}

// Añade al archivo, fuera de la clase DocumentacionExtensions:
public sealed class EjemploCrearOrden : ISchemaFilter
{
    public void Apply(OpenApiSchema schema, SchemaFilterContext context)
    {
        if (context.Type != typeof(CrearOrdenRequest)) return;
        schema.Example = new OpenApiObject
        {
            ["cliente"] = new OpenApiString("ACX-001"),
            ["material"] = new OpenApiString("CHAPA-3MM"),
            ["cantidad"] = new OpenApiInteger(10)
        };
    }
}
