// INICIO PASO 2.3.16 — Habilitar espacio de nombres Validacion.
// using AceriaApp.Monolito.Api.Validacion;
// FIN PASO 2.3.16
using AceriaApp.Monolito.Api.Dominio;
using AceriaApp.Monolito.Api.Infraestructura;
using Microsoft.EntityFrameworkCore;

// PASO 1.1.13 — Registro de EF Core y OpenAPI.
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<AceriaDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("AceriaDb")));
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
// INICIO PASO 2.3.16 — Registrar validadores desde la extensión.
// builder.Services.AddValidacion();
// FIN PASO 2.3.16

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// PASO 1.1.13 — Consultar las órdenes.
app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) =>
    await db.Ordenes.AsNoTracking().ToListAsync());

// PASO 1.1.13 — Crear una orden.
app.MapPost("/api/v1/ordenes", async (AceriaDbContext db, Orden orden) =>
{
    orden.Id = Guid.NewGuid();
    orden.FechaCreacion = DateTime.UtcNow;
    db.Ordenes.Add(orden);
    await db.SaveChangesAsync();
    return Results.Created($"/api/v1/ordenes/{orden.Id}", orden);
});

// RETO 1.1: descomentar este bloque completo para activar GET por id.
// app.MapGet("/api/v1/ordenes/{id:guid}", async (Guid id, AceriaDbContext db) =>
// {
//     var orden = await db.Ordenes.AsNoTracking().FirstOrDefaultAsync(o => o.Id == id);
//     return orden is not null ? Results.Ok(orden) : Results.NotFound();
// });

app.Run();
