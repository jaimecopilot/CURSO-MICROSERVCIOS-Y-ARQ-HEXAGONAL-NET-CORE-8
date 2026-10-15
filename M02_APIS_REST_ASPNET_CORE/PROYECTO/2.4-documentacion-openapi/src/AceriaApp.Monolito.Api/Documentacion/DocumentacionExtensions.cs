using Microsoft.OpenApi.Models;
namespace AceriaApp.Monolito.Api.Documentacion;
public static class DocumentacionExtensions
{
    public static IServiceCollection AddDocumentacionOpenApi(
        this IServiceCollection services,MetadatosApi metadatos)
    {
        services.AddEndpointsApiExplorer();
        services.AddSwaggerGen(options => options.SwaggerDoc(metadatos.Version,new OpenApiInfo
        {
            Title=metadatos.Titulo,Version=metadatos.Version,
            Description=metadatos.Descripcion,
            Contact=new OpenApiContact { Name=metadatos.ContactoNombre,Email=metadatos.ContactoEmail}
        }));
        return services;
    }
    public static WebApplication UseDocumentacionOpenApi(
        this WebApplication app,ConfiguracionOpenApi configuracion)
    {
        if(configuracion.EsEntornoDeDesarrollo(app.Environment.EnvironmentName))
        {
            app.UseSwagger();
            if(configuracion.PublicarSwaggerUI)
                app.UseSwaggerUI(options=>options.SwaggerEndpoint(
                    configuracion.RutaDocumento,configuracion.NombreDocumento));
        }
        return app;
    }
}
