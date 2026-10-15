#!/usr/bin/env python3
"""M02 reconstruido: cuatro estados ejecutables de una Minimal API .NET 8."""
from pathlib import Path
import argparse, shutil

BASE = Path("M02_APIS_REST_ASPNET_CORE/PROYECTO")
NAMES = ["2.1-diseno-apis-rest","2.2-recursos-verbos-codigos",
         "2.3-validacion-peticiones","2.4-documentacion-openapi"]

def write(root, path, content):
    p=root/path
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(content.strip()+"\n",encoding="utf-8")

MODEL = """
namespace AceriaApp.Api.Modelo;
// INICIO PASO 2.1.4
public sealed class Orden
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Cliente { get; set; } = string.Empty;
    public string Material { get; set; } = string.Empty;
    public int Cantidad { get; set; }
    public string Estado { get; set; } = "Pendiente";
    public DateTime FechaCreacion { get; set; } = DateTime.UtcNow;
}
// FIN PASO 2.1.4
"""
DTO = """
namespace AceriaApp.Api.Modelo;
// INICIO PASO 2.1.5
public sealed record OrdenDto(Guid Id, string Cliente, string Material,
    int Cantidad, string Estado, DateTime FechaCreacion)
{
    public static OrdenDto Desde(Orden x) =>
        new(x.Id,x.Cliente,x.Material,x.Cantidad,x.Estado,x.FechaCreacion);
}
// FIN PASO 2.1.5
"""
DB = """
using AceriaApp.Api.Modelo;
using Microsoft.EntityFrameworkCore;
namespace AceriaApp.Api.Datos;
// INICIO PASO 2.1.6
public sealed class AceriaDbContext(DbContextOptions<AceriaDbContext> options) : DbContext(options)
{
    public DbSet<Orden> Ordenes => Set<Orden>();
    protected override void OnModelCreating(ModelBuilder b)
    {
        var e=b.Entity<Orden>();
        e.HasKey(x=>x.Id);
        e.Property(x=>x.Cliente).HasMaxLength(100).IsRequired();
        e.Property(x=>x.Material).HasMaxLength(100).IsRequired();
        e.Property(x=>x.Estado).HasMaxLength(24).IsRequired();
    }
}
// FIN PASO 2.1.6
"""
CONTRACTS = """
namespace AceriaApp.Api.Contratos;
// INICIO PASO 2.2.4
public sealed record CrearOrdenRequest(string Cliente,string Material,int Cantidad);
public sealed record ActualizarCantidadRequest(int Cantidad);
// FIN PASO 2.2.4
"""
VALIDATORS = """
using AceriaApp.Api.Contratos;
using FluentValidation;
namespace AceriaApp.Api.Validacion;
// INICIO PASO 2.3.3
public sealed class CrearOrdenValidator : AbstractValidator<CrearOrdenRequest>
{
    public CrearOrdenValidator()
    {
        RuleFor(x=>x.Cliente).NotEmpty().MaximumLength(100);
        RuleFor(x=>x.Material).NotEmpty().MaximumLength(100);
        RuleFor(x=>x.Cantidad).InclusiveBetween(1,10000);
    }
}
public sealed class ActualizarCantidadValidator : AbstractValidator<ActualizarCantidadRequest>
{
    public ActualizarCantidadValidator() => RuleFor(x=>x.Cantidad).InclusiveBetween(1,10000);
}
// FIN PASO 2.3.3
"""
FILTER = """
using FluentValidation;
namespace AceriaApp.Api.Validacion;
// INICIO PASO 2.3.4
public sealed class ValidationFilter<T>(IValidator<T> validator): IEndpointFilter where T:class
{
    public async ValueTask<object?> InvokeAsync(EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var request=context.Arguments.OfType<T>().FirstOrDefault();
        if(request is null) return Results.ValidationProblem(
            new Dictionary<string,string[]> { ["body"]=new[]{"Falta el cuerpo."} });
        var result=await validator.ValidateAsync(request,context.HttpContext.RequestAborted);
        if(!result.IsValid)
        {
            var errors=result.Errors.GroupBy(x=>x.PropertyName)
                .ToDictionary(x=>x.Key,x=>x.Select(e=>e.ErrorMessage).ToArray());
            return Results.ValidationProblem(errors);
        }
        return await next(context);
    }
}
// FIN PASO 2.3.4
"""
SWAGGER = """
using AceriaApp.Api.Contratos;
using Microsoft.OpenApi.Any;
using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.SwaggerGen;
namespace AceriaApp.Api.Documentacion;
// INICIO PASO 2.4.3
public static class DocumentacionExtensions
{
    public static IServiceCollection AddDocumentacion(this IServiceCollection services)
    {
        services.AddEndpointsApiExplorer();
        services.AddSwaggerGen(options=>
        {
            options.SwaggerDoc("v1",new OpenApiInfo{
                Title="AceriaApp — Órdenes de producción",Version="v1",
                Description="API REST educativa creada con ASP.NET Core 8.",
                Contact=new OpenApiContact{Name="Equipo AceriaApp",Email="equipo@acerialocal"}
            });
            options.SchemaFilter<EjemploCrearOrden>();
        });
        return services;
    }
    public static WebApplication UseDocumentacion(this WebApplication app)
    {
        if(app.Environment.IsDevelopment())
        {
            app.UseSwagger();
            app.UseSwaggerUI(o=>o.SwaggerEndpoint("/swagger/v1/swagger.json","AceriaApp v1"));
        }
        return app;
    }
}
// FIN PASO 2.4.3
// INICIO PASO 2.4.5
public sealed class EjemploCrearOrden : ISchemaFilter
{
    public void Apply(OpenApiSchema schema,SchemaFilterContext context)
    {
        if(context.Type!=typeof(CrearOrdenRequest)) return;
        schema.Example=new OpenApiObject{
            ["cliente"]=new OpenApiString("ACX-001"),
            ["material"]=new OpenApiString("CHAPA-3MM"),
            ["cantidad"]=new OpenApiInteger(10)
        };
    }
}
// FIN PASO 2.4.5
"""
GETS = """
// INICIO PASO 2.1.8: colección de recursos, consulta real con EF Core.
app.MapGet("/api/v1/ordenes",async (AceriaDbContext db,CancellationToken ct)=>
{
    var ordenes=await db.Ordenes.AsNoTracking().OrderBy(x=>x.FechaCreacion).ToListAsync(ct);
    return Results.Ok(ordenes.Select(OrdenDto.Desde));
})
.WithName("ListarOrdenes").WithTags("Ordenes")
{getmeta}
;
// INICIO PASO 2.1.9: recurso individual.
app.MapGet("/api/v1/ordenes/{{id:guid}}",async (Guid id,AceriaDbContext db)=>
{
    var orden=await db.Ordenes.AsNoTracking().FirstOrDefaultAsync(x=>x.Id==id);
    IResult response=orden is null ? Results.NotFound() : Results.Ok(OrdenDto.Desde(orden));
    return response;
})
.WithName("ObtenerOrdenPorId").WithTags("Ordenes")
{onemeta}
;
"""
POST = """
// INICIO PASO 2.2.5: crear una orden, persistirla, devolver 201 + Location.
app.MapPost("/api/v1/ordenes",async (CrearOrdenRequest request,AceriaDbContext db)=>
{{
{check}    if(request.Cantidad>500)
        return Results.Problem(title:"El taller solo admite lotes de hasta 500.",
            statusCode:StatusCodes.Status422UnprocessableEntity);
    var orden=new Orden{{Cliente=request.Cliente,Material=request.Material,Cantidad=request.Cantidad}};
    db.Ordenes.Add(orden);
    await db.SaveChangesAsync();
    return Results.CreatedAtRoute("ObtenerOrdenPorId",new{{id=orden.Id}},OrdenDto.Desde(orden));
}})
.WithName("CrearOrden").WithTags("Ordenes")
{filter}
{meta}
;
"""
PUT = """
// INICIO PASO 2.2.7: sustitución completa de los campos editables.
app.MapPut("/api/v1/ordenes/{{id:guid}}",async (Guid id,CrearOrdenRequest request,AceriaDbContext db)=>
{{
{check}    var orden=await db.Ordenes.FindAsync(id);
    if(orden is null) return Results.NotFound();
    if(orden.Estado=="Finalizada") return Results.Problem(
        title:"No se puede modificar una orden finalizada.",statusCode:409);
    if(request.Cantidad>500) return Results.Problem(
        title:"El taller solo admite lotes de hasta 500.",statusCode:422);
    orden.Cliente=request.Cliente;orden.Material=request.Material;
    orden.Cantidad=request.Cantidad;
    await db.SaveChangesAsync();
    return Results.NoContent();
}})
.WithName("ReemplazarOrden").WithTags("Ordenes")
{filter}
{meta}
;
"""
PATCH = """
// INICIO PASO 2.2.8: cambiar SOLO la cantidad.
app.MapPatch("/api/v1/ordenes/{{id:guid}}/cantidad",
    async (Guid id,ActualizarCantidadRequest request,AceriaDbContext db)=>
{{
{check}    var orden=await db.Ordenes.FindAsync(id);
    if(orden is null) return Results.NotFound();
    if(orden.Estado=="Finalizada") return Results.Problem(
        title:"No se puede modificar una orden finalizada.",statusCode:409);
    if(request.Cantidad>500) return Results.Problem(
        title:"El taller solo admite lotes de hasta 500.",statusCode:422);
    orden.Cantidad=request.Cantidad;
    await db.SaveChangesAsync();
    return Results.Ok(OrdenDto.Desde(orden));
}})
.WithName("CambiarCantidad").WithTags("Ordenes")
{filter}
{meta}
;
"""
DELETE = """
// INICIO PASO 2.2.9: eliminar recurso persistido.
app.MapDelete("/api/v1/ordenes/{id:guid}",async (Guid id,AceriaDbContext db)=>
{
    var orden=await db.Ordenes.FindAsync(id);
    if(orden is null) return Results.NotFound();
    if(orden.Estado=="Finalizada") return Results.Problem(
        title:"No se puede eliminar una orden finalizada.",statusCode:409);
    db.Ordenes.Remove(orden);
    await db.SaveChangesAsync();
    return Results.NoContent();
})
.WithName("EliminarOrden").WithTags("Ordenes")
{meta}
;
// INICIO PASO 2.2.10: transición explícita del dominio.
app.MapPost("/api/v1/ordenes/{id:guid}/finalizar",async (Guid id,AceriaDbContext db)=>
{
    var orden=await db.Ordenes.FindAsync(id);
    if(orden is null) return Results.NotFound();
    if(orden.Estado=="Finalizada") return Results.Problem(
        title:"La orden ya estaba finalizada.",statusCode:409);
    orden.Estado="Finalizada";
    await db.SaveChangesAsync();
    return Results.Ok(OrdenDto.Desde(orden));
})
.WithName("FinalizarOrden").WithTags("Ordenes")
{finishmeta}
;
"""
def program(stage):
    parts=["using AceriaApp.Api.Datos;","using AceriaApp.Api.Modelo;",
           "using Microsoft.EntityFrameworkCore;"]
    if stage>=2: parts.append("using AceriaApp.Api.Contratos;")
    if stage>=3: parts+=["using AceriaApp.Api.Validacion;","using FluentValidation;"]
    if stage>=4: parts.append("using AceriaApp.Api.Documentacion;")
    parts+=["","var builder=WebApplication.CreateBuilder(args);",
    "// INICIO PASO 2.1.7: SQL Server Express LocalDB, no SQLite.",
    "builder.Services.AddDbContext<AceriaDbContext>(o=>",
    '    o.UseSqlServer(builder.Configuration.GetConnectionString("AceriaApp")));']
    if stage>=3:parts.append("builder.Services.AddValidatorsFromAssemblyContaining<CrearOrdenValidator>(); // PASO 2.3.5")
    if stage>=4:parts.append("builder.Services.AddDocumentacion(); // PASO 2.4.3")
    parts+=["","var app=builder.Build();",
    "// EnsureCreated se utiliza SOLO como ayuda didáctica en Development.",
    "// Para un sistema productivo se utilizarían migraciones controladas.",
    'if(app.Environment.IsDevelopment()&&!app.Configuration.GetValue<bool>("SkipDatabaseInitialization"))',
    "{","    using var scope=app.Services.CreateScope();",
    "    await scope.ServiceProvider.GetRequiredService<AceriaDbContext>().Database.EnsureCreatedAsync();","}"]
    getcode=GETS.replace("{getmeta}",('.WithSummary("Lista las órdenes de producción").Produces<IEnumerable<OrdenDto>>(200)' if stage>=4 else ""))
    getcode=getcode.replace("{onemeta}",('.WithSummary("Obtiene una orden por ID").Produces<OrdenDto>(200).Produces(404)' if stage>=4 else ""))
    getcode=getcode.replace("{{id:guid}}","{id:guid}")
    parts.append(getcode)
    if stage>=2:
        check=('    if(string.IsNullOrWhiteSpace(request.Cliente)||string.IsNullOrWhiteSpace(request.Material)||request.Cantidad<=0)\n        return Results.BadRequest(new {error="Cliente, material y cantidad son obligatorios."});\n' if stage==2 else '')
        patchcheck=('    if(request.Cantidad<=0) return Results.BadRequest(new {error="Cantidad debe ser positiva."});\n' if stage==2 else '')
        filt=(".AddEndpointFilter<ValidationFilter<CrearOrdenRequest>>()" if stage>=3 else "")
        patchfilt=(".AddEndpointFilter<ValidationFilter<ActualizarCantidadRequest>>()" if stage>=3 else "")
        parts.append(POST.format(check=check,filter=filt,meta=('.WithSummary("Crea una orden").Produces<OrdenDto>(201).ProducesValidationProblem(400).ProducesProblem(422)' if stage>=4 else '')))
        parts.append(PUT.format(check=check,filter=filt,meta=('.WithSummary("Sustituye campos editables").Produces(204).Produces(404).ProducesProblem(409).ProducesValidationProblem(400)' if stage>=4 else '')))
        parts.append(PATCH.format(check=patchcheck,filter=patchfilt,meta=('.WithSummary("Modifica cantidad").Produces<OrdenDto>(200).ProducesValidationProblem(400)' if stage>=4 else '')))
        deletecode=DELETE.replace("{meta}",('.WithSummary("Elimina una orden pendiente").Produces(204).Produces(404)' if stage>=4 else ''))
        deletecode=deletecode.replace("{finishmeta}",('.WithSummary("Finaliza una orden").Produces<OrdenDto>(200).ProducesProblem(409)' if stage>=4 else ''))
        parts.append(deletecode)
    if stage>=4:parts.append("app.UseDocumentacion(); // PASO 2.4.4")
    parts+=["app.Run();","public partial class Program {} // permite WebApplicationFactory en tests"]
    return "\n".join(parts)

FACTORY = """
using AceriaApp.Api.Datos;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
namespace AceriaApp.Api.Tests;
// INICIO PASO 2.1.12: HTTP real; base en memoria SOLO en tests automatizados.
public sealed class ApiFactory:WebApplicationFactory<Program>
{
    private readonly string _databaseName="Tests-"+Guid.NewGuid();
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Development");
        builder.UseSetting("SkipDatabaseInitialization","true");
        builder.ConfigureTestServices(services=>
        {
            services.RemoveAll<DbContextOptions<AceriaDbContext>>();
            services.AddDbContext<AceriaDbContext>(opt=>
                opt.UseInMemoryDatabase(_databaseName));
        });
    }
}
"""
TEST_GET = """
using System.Net;
using System.Net.Http.Json;
using AceriaApp.Api.Datos;
using AceriaApp.Api.Modelo;
using Microsoft.Extensions.DependencyInjection;
using Xunit;
namespace AceriaApp.Api.Tests;
// INICIO PASO 2.1.13: dos peticiones HTTP, código y DTO.
public class GetTests
{
    [Fact] public async Task ListaVacia_Es200()
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().GetAsync("/api/v1/ordenes");
        Assert.Equal(HttpStatusCode.OK,r.StatusCode);
    }
    [Fact] public async Task RecursoInexistente_Es404()
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().GetAsync("/api/v1/ordenes/"+Guid.NewGuid());
        Assert.Equal(HttpStatusCode.NotFound,r.StatusCode);
    }
    [Fact] public async Task RecursoExistente_ExponeDto()
    {
        using var f=new ApiFactory();
        var id=Guid.NewGuid();
        using(var scope=f.Services.CreateScope())
        {
            var db=scope.ServiceProvider.GetRequiredService<AceriaDbContext>();
            db.Ordenes.Add(new Orden{Id=id,Cliente="ACX-001",Material="CHAPA",Cantidad=10});
            await db.SaveChangesAsync();
        }
        var r=await f.CreateClient().GetAsync("/api/v1/ordenes/"+id);
        var dto=await r.Content.ReadFromJsonAsync<OrdenDto>();
        Assert.Equal(HttpStatusCode.OK,r.StatusCode);
        Assert.Equal(id,dto?.Id);
    }
}
"""
TEST_WRITE = """
using System.Net;
using System.Net.Http.Json;
using AceriaApp.Api.Contratos;
using AceriaApp.Api.Modelo;
using Xunit;
namespace AceriaApp.Api.Tests;
// INICIO PASO 2.2.11: probar POST/GET/PUT/PATCH/DELETE con HTTP.
public class EscrituraTests
{
    [Fact] public async Task CrearYConsultar_Es201Y200()
    {
        using var f=new ApiFactory();using var client=f.CreateClient();
        var created=await client.PostAsJsonAsync("/api/v1/ordenes",
            new CrearOrdenRequest("ACX","CHAPA",10));
        Assert.Equal(HttpStatusCode.Created,created.StatusCode);
        Assert.NotNull(created.Headers.Location);
        var get=await client.GetAsync(created.Headers.Location);
        Assert.Equal(HttpStatusCode.OK,get.StatusCode);
    }
    [Fact] public async Task EditarYEliminar_CambiaPersistencia()
    {
        using var f=new ApiFactory();using var c=f.CreateClient();
        var made=await c.PostAsJsonAsync("/api/v1/ordenes",
            new CrearOrdenRequest("ACX","CHAPA",10));
        var dto=await made.Content.ReadFromJsonAsync<OrdenDto>();
        Assert.NotNull(dto);
        var put=await c.PutAsJsonAsync("/api/v1/ordenes/"+dto.Id,
            new CrearOrdenRequest("ACX2","CHAPA",11));
        Assert.Equal(HttpStatusCode.NoContent,put.StatusCode);
        var patch=await c.PatchAsJsonAsync("/api/v1/ordenes/"+dto.Id+"/cantidad",
            new ActualizarCantidadRequest(12));
        Assert.Equal(HttpStatusCode.OK,patch.StatusCode);
        var changed=await patch.Content.ReadFromJsonAsync<OrdenDto>();
        Assert.Equal(12,changed?.Cantidad);
        var del=await c.DeleteAsync("/api/v1/ordenes/"+dto.Id);
        Assert.Equal(HttpStatusCode.NoContent,del.StatusCode);
        var gone=await c.GetAsync("/api/v1/ordenes/"+dto.Id);
        Assert.Equal(HttpStatusCode.NotFound,gone.StatusCode);
    }
    [Fact] public async Task ReglaCapacidad_Es422()
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().PostAsJsonAsync("/api/v1/ordenes",
            new CrearOrdenRequest("ACX","CHAPA",501));
        Assert.Equal(HttpStatusCode.UnprocessableEntity,r.StatusCode);
    }
    [Fact] public async Task OrdenFinalizada_NoSeEdita409()
    {
        using var f=new ApiFactory();using var c=f.CreateClient();
        var made=await c.PostAsJsonAsync("/api/v1/ordenes",
            new CrearOrdenRequest("ACX","CHAPA",2));
        var dto=await made.Content.ReadFromJsonAsync<OrdenDto>();
        Assert.NotNull(dto);
        var done=await c.PostAsync("/api/v1/ordenes/"+dto.Id+"/finalizar",null);
        Assert.Equal(HttpStatusCode.OK,done.StatusCode);
        var put=await c.PutAsJsonAsync("/api/v1/ordenes/"+dto.Id,
            new CrearOrdenRequest("ACX","CHAPA",3));
        Assert.Equal(HttpStatusCode.Conflict,put.StatusCode);
    }
}
"""
TEST_VALID = """
using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using AceriaApp.Api.Contratos;
using Xunit;
namespace AceriaApp.Api.Tests;
// INICIO PASO 2.3.8: se verifica el filtro ACTIVO, no su mera existencia.
public class ValidacionHttpTests
{
    [Theory]
    [InlineData("","CHAPA",10)]
    [InlineData("ACX","",10)]
    [InlineData("ACX","CHAPA",0)]
    public async Task DatosInvalidos_Es400ConErrors(string cliente,string material,int cantidad)
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().PostAsJsonAsync("/api/v1/ordenes",
            new CrearOrdenRequest(cliente,material,cantidad));
        Assert.Equal(HttpStatusCode.BadRequest,r.StatusCode);
        using var json=JsonDocument.Parse(await r.Content.ReadAsStringAsync());
        Assert.True(json.RootElement.TryGetProperty("errors",out _));
    }
    [Fact] public async Task CantidadMasDe10000_Es400()
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().PostAsJsonAsync("/api/v1/ordenes",
            new CrearOrdenRequest("ACX","CHAPA",10001));
        Assert.Equal(HttpStatusCode.BadRequest,r.StatusCode);
    }
    [Fact] public async Task ReglaDeNegocio_501_Es422()
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().PostAsJsonAsync("/api/v1/ordenes",
            new CrearOrdenRequest("ACX","CHAPA",501));
        Assert.Equal(HttpStatusCode.UnprocessableEntity,r.StatusCode);
    }
}
"""
TEST_OPENAPI = """
using System.Net;
using System.Text.Json;
using Microsoft.AspNetCore.Hosting;
using Xunit;
namespace AceriaApp.Api.Tests;
// INICIO PASO 2.4.8: abrir OpenAPI JSON REAL mediante HTTP.
public class ContratoOpenApiTests
{
    [Fact] public async Task OpenApi_ContieneRutasYVersion()
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().GetAsync("/swagger/v1/swagger.json");
        Assert.Equal(HttpStatusCode.OK,r.StatusCode);
        using var json=JsonDocument.Parse(await r.Content.ReadAsStringAsync());
        Assert.Equal("v1",json.RootElement.GetProperty("info").GetProperty("version").GetString());
        var paths=json.RootElement.GetProperty("paths");
        Assert.True(paths.TryGetProperty("/api/v1/ordenes",out var resource));
        Assert.True(resource.TryGetProperty("get",out _));
        Assert.True(resource.TryGetProperty("post",out _));
    }
    [Fact] public async Task OpenApi_IncluyeEjemplo()
    {
        using var f=new ApiFactory();
        var r=await f.CreateClient().GetAsync("/swagger/v1/swagger.json");
        using var json=JsonDocument.Parse(await r.Content.ReadAsStringAsync());
        var schemas=json.RootElement.GetProperty("components").GetProperty("schemas");
        Assert.True(schemas.TryGetProperty("CrearOrdenRequest",out var schema));
        Assert.True(schema.TryGetProperty("example",out _));
    }
    [Fact] public async Task Produccion_NoExponeSwagger()
    {
        using var f=new ApiFactory();
        using var other=f.WithWebHostBuilder(b=>b.UseEnvironment("Production"));
        var r=await other.CreateClient().GetAsync("/swagger/v1/swagger.json");
        Assert.Equal(HttpStatusCode.NotFound,r.StatusCode);
    }
}
"""

def generate(root):
    for stage,folder in enumerate(NAMES,1):
        out=root/BASE/folder
        if out.exists():shutil.rmtree(out)
        sdk=Path("src/AceriaApp.Api")
        tst=Path("tests/AceriaApp.Api.Tests")
        packages=['<PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.21" />']
        if stage>=3:packages.append('<PackageReference Include="FluentValidation.DependencyInjectionExtensions" Version="11.11.0" />')
        if stage>=4:packages.append('<PackageReference Include="Swashbuckle.AspNetCore" Version="6.6.2" />')
        csproj='<Project Sdk="Microsoft.NET.Sdk.Web"><PropertyGroup><TargetFramework>net8.0</TargetFramework><Nullable>enable</Nullable><ImplicitUsings>enable</ImplicitUsings></PropertyGroup><ItemGroup>'+"".join(packages)+'</ItemGroup></Project>'
        write(out,sdk/"AceriaApp.Api.csproj",csproj)
        testpackages=["Microsoft.NET.Test.Sdk|17.12.0","xunit|2.9.2","xunit.runner.visualstudio|2.8.2",
                      "Microsoft.AspNetCore.Mvc.Testing|8.0.21","Microsoft.EntityFrameworkCore.InMemory|8.0.21"]
        titems="".join(f'<PackageReference Include="{x}" Version="{v}" />' for x,v in (pair.split("|") for pair in testpackages))
        write(out,tst/"AceriaApp.Api.Tests.csproj",'<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net8.0</TargetFramework><Nullable>enable</Nullable><ImplicitUsings>enable</ImplicitUsings><IsPackable>false</IsPackable><IsTestProject>true</IsTestProject></PropertyGroup><ItemGroup>'+titems+'<ProjectReference Include="../../src/AceriaApp.Api/AceriaApp.Api.csproj" /></ItemGroup></Project>')
        write(out,sdk/"appsettings.json",'{"ConnectionStrings":{"AceriaApp":"Server=(localdb)\\\\MSSQLLocalDB;Database=AceriaAppM02;Trusted_Connection=True;TrustServerCertificate=True"}}')
        write(out,sdk/"Properties/launchSettings.json",'{"profiles":{"AceriaApp.Api":{"commandName":"Project","launchBrowser":false,"applicationUrl":"http://localhost:5082","environmentVariables":{"ASPNETCORE_ENVIRONMENT":"Development"}}}}')
        write(out,sdk/"Modelo/Orden.cs",MODEL)
        write(out,sdk/"Modelo/OrdenDto.cs",DTO)
        write(out,sdk/"Datos/AceriaDbContext.cs",DB)
        if stage>=2:write(out,sdk/"Contratos/ContratosOrden.cs",CONTRACTS)
        if stage>=3:
            write(out,sdk/"Validacion/Validadores.cs",VALIDATORS)
            write(out,sdk/"Validacion/ValidationFilter.cs",FILTER)
        if stage>=4:write(out,sdk/"Documentacion/DocumentacionExtensions.cs",SWAGGER)
        write(out,sdk/"Program.cs",program(stage))
        write(out,tst/"ApiFactory.cs",FACTORY)
        write(out,tst/"GetTests.cs",TEST_GET)
        if stage>=2:write(out,tst/"EscrituraTests.cs",TEST_WRITE)
        if stage>=3:write(out,tst/"ValidacionHttpTests.cs",TEST_VALID)
        if stage>=4:write(out,tst/"ContratoOpenApiTests.cs",TEST_OPENAPI)
        write(out,"AceriaApp.http",'''@Host = http://localhost:5082
GET {{Host}}/api/v1/ordenes

### Detalle inexistente
GET {{Host}}/api/v1/ordenes/00000000-0000-0000-0000-000000000001
'''+('''
### Crear 201 (guardar el ID del cuerpo y Location)
POST {{Host}}/api/v1/ordenes
Content-Type: application/json

{"cliente":"ACX-001","material":"CHAPA-3MM","cantidad":10}

### Validación 400 en 2.3
POST {{Host}}/api/v1/ordenes
Content-Type: application/json

{"cliente":"","material":"CHAPA-3MM","cantidad":0}

### Negocio 422
POST {{Host}}/api/v1/ordenes
Content-Type: application/json

{"cliente":"ACX-001","material":"CHAPA-3MM","cantidad":501}

### Sustituir {id} por ID real
PUT {{Host}}/api/v1/ordenes/{id}
Content-Type: application/json

{"cliente":"ACX-002","material":"CHAPA-5MM","cantidad":14}

PATCH {{Host}}/api/v1/ordenes/{id}/cantidad
Content-Type: application/json

{"cantidad":15}

POST {{Host}}/api/v1/ordenes/{id}/finalizar

DELETE {{Host}}/api/v1/ordenes/{id}
''' if stage>=2 else ""))
        write(out,"README.md",f'''# M02 — Etapa {stage}/4 · API REST en ASP.NET Core 8

Este proyecto funciona independientemente del resto. El alumnado lo construye
de forma progresiva siguiendo M02_PRACTICAS.md, con Visual Studio y SQL Server
Express LocalDB (Windows). NO requiere comandos Git.

## Ejecución
1. Abrir src/AceriaApp.Api/AceriaApp.Api.csproj en Visual Studio.
2. Comprobar que está instalado .NET 8 y SQL Server Express LocalDB.
3. Ejecutar `dotnet restore` y `dotnet run --project src/AceriaApp.Api`.
4. Probar las peticiones HTTP del archivo AceriaApp.http.
5. Ejecutar `dotnet test tests/AceriaApp.Api.Tests`.

En Development, EnsureCreated crea la base de aprendizaje sin migraciones.
No debe usarse como estrategia de despliegue productivo.
La API emplea SQL Server Express LocalDB; EF Core InMemory está solo en tests.
Etapa: {'GET de colección y detalle' if stage==1 else 'POST PUT PATCH DELETE y reglas de dominio' if stage==2 else 'FluentValidation y filtros ejecutados por endpoints' if stage==3 else 'OpenAPI real, Swagger UI y pruebas de documento'}.
'''.replace("`","`"))
        print(f"Punto 2.{stage}: {len(list(out.rglob('*.cs')))} archivos C#, API ejecutable.")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",type=Path,default=Path("."))
    generate(ap.parse_args().out)
