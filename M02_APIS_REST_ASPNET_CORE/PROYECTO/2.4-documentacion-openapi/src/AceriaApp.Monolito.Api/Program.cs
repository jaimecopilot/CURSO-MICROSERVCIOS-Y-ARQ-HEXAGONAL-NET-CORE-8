using AceriaApp.Monolito.Api.Documentacion;
using AceriaApp.Monolito.Api.Validacion;
using AceriaApp.Monolito.Api.Dominio;
using AceriaApp.Monolito.Api.Infraestructura;
using Microsoft.EntityFrameworkCore;

// PASO 1.1.13 — Registro de EF Core y OpenAPI.
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<AceriaDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("AceriaDb")));
builder.Services.AddDocumentacionOpenApi(new MetadatosApi());
builder.Services.AddValidacion();

var app = builder.Build();

app.UseDocumentacionOpenApi(new ConfiguracionOpenApi());

// PASO 1.1.13 — Consultar las órdenes.
app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) =>
    await db.Ordenes.AsNoTracking().ToListAsync())
    .WithName("ListarOrdenes").WithSummary("Lista las órdenes").WithTags("Ordenes")
    .Produces<List<Orden>>(StatusCodes.Status200OK);

// PASO 1.1.13 — Crear una orden.
app.MapPost("/api/v1/ordenes", async (AceriaDbContext db, CrearOrdenRequest request) =>
{
    var orden = new Orden { Id = Guid.NewGuid(), FechaCreacion = DateTime.UtcNow, Cliente = request.Cliente, Material = request.Material, Cantidad = request.Cantidad };
    db.Ordenes.Add(orden);
    await db.SaveChangesAsync();
    return Results.Created($"/api/v1/ordenes/{orden.Id}", orden);
})
    .WithName("CrearOrden").WithSummary("Crea una orden").WithTags("Ordenes")
    .Produces<Orden>(StatusCodes.Status201Created)
    .AddEndpointFilter<ValidationFilter<CrearOrdenRequest>>()
    .ProducesValidationProblem(StatusCodes.Status400BadRequest);

// RETO 1.1: descomentar este bloque completo para activar GET por id.
// app.MapGet("/api/v1/ordenes/{id:guid}", async (Guid id, AceriaDbContext db) =>
// {
//     var orden = await db.Ordenes.AsNoTracking().FirstOrDefaultAsync(o => o.Id == id);
//     return orden is not null ? Results.Ok(orden) : Results.NotFound();
// });

app.Run();

// Permite las pruebas reales de integración con WebApplicationFactory.
public partial class Program { }
