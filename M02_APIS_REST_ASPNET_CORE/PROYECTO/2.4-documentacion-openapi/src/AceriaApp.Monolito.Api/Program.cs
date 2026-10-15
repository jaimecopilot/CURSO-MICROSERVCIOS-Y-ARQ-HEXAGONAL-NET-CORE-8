// INICIO PASO 2.4.9 — Importar la nueva extensión.
// using AceriaApp.Monolito.Api.Documentacion;
// FIN PASO 2.4.9
using AceriaApp.Monolito.Api.Validacion;
using AceriaApp.Monolito.Api.Dominio;
using AceriaApp.Monolito.Api.Infraestructura;
using Microsoft.EntityFrameworkCore;

// PASO 1.1.13 — Registro de EF Core y OpenAPI.
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<AceriaDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("AceriaDb")));
// INICIO SUSTITUCION PASO 2.4.9 — Retirar registros Swagger heredados.
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
// FIN SUSTITUCION PASO 2.4.9
// INICIO PASO 2.4.9 — Usar configuración Swagger real.
// builder.Services.AddDocumentacionOpenApi(new MetadatosApi());
// FIN PASO 2.4.9
builder.Services.AddValidacion();
var app = builder.Build();

// INICIO SUSTITUCION PASO 2.4.9 — Retirar middleware Swagger heredado.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
// FIN SUSTITUCION PASO 2.4.9
// INICIO PASO 2.4.9 — Usar middleware Swagger en Development.
// app.UseDocumentacionOpenApi(new ConfiguracionOpenApi());
// FIN PASO 2.4.9

// PASO 1.1.13 — Consultar las órdenes.
// INICIO SUSTITUCION PASO 2.4.9 — Reemplazar GET sin metadatos.
app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) =>
    await db.Ordenes.AsNoTracking().ToListAsync());
// FIN SUSTITUCION PASO 2.4.9
// INICIO PASO 2.4.9 — Documentar GET con metadatos.
// app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) =>
//     await db.Ordenes.AsNoTracking().ToListAsync())
//     .WithName("ListarOrdenes").WithSummary("Lista las órdenes").WithTags("Ordenes")
//     .Produces<List<Orden>>(StatusCodes.Status200OK);
// FIN PASO 2.4.9

// PASO 1.1.13 — Crear una orden.
// INICIO SUSTITUCION PASO 2.4.9 — Reemplazar POST de entidad por DTO validado.
app.MapPost("/api/v1/ordenes", async (AceriaDbContext db, Orden orden) =>
{
    orden.Id = Guid.NewGuid();
    orden.FechaCreacion = DateTime.UtcNow;
    db.Ordenes.Add(orden);
    await db.SaveChangesAsync();
    return Results.Created($"/api/v1/ordenes/{orden.Id}", orden);
});
// FIN SUSTITUCION PASO 2.4.9
// INICIO PASO 2.4.9 — Documentar POST y activar el filtro.
// app.MapPost("/api/v1/ordenes", async (AceriaDbContext db, CrearOrdenRequest request) =>
// {
//     var orden = new Orden { Id = Guid.NewGuid(), FechaCreacion = DateTime.UtcNow, Cliente = request.Cliente, Material = request.Material, Cantidad = request.Cantidad };
//     db.Ordenes.Add(orden);
//     await db.SaveChangesAsync();
//     return Results.Created($"/api/v1/ordenes/{orden.Id}", orden);
// })
//     .WithName("CrearOrden").WithSummary("Crea una orden").WithTags("Ordenes")
//     .Produces<Orden>(StatusCodes.Status201Created)
//     .AddEndpointFilter<ValidationFilter<CrearOrdenRequest>>()
//     .ProducesValidationProblem(StatusCodes.Status400BadRequest);
// FIN PASO 2.4.9

// RETO 1.1: descomentar este bloque completo para activar GET por id.
// app.MapGet("/api/v1/ordenes/{id:guid}", async (Guid id, AceriaDbContext db) =>
// {
//     var orden = await db.Ordenes.AsNoTracking().FirstOrDefaultAsync(o => o.Id == id);
//     return orden is not null ? Results.Ok(orden) : Results.NotFound();
// });

app.Run();

// INICIO PASO 2.4.9 — Habilitar pruebas WebApplicationFactory.
// public partial class Program { }
// FIN PASO 2.4.9
