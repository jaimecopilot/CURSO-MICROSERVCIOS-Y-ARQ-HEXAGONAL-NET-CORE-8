using AceriaApp.Api.Modelo;
using Microsoft.EntityFrameworkCore;

namespace AceriaApp.Api.Datos;

public sealed class AceriaDbContext(
    DbContextOptions<AceriaDbContext> options) : DbContext(options)
{
    public DbSet<Orden> Ordenes => Set<Orden>();
// Dentro de AceriaDbContext, antes de su última llave:
protected override void OnModelCreating(ModelBuilder b)
{
    var e = b.Entity<Orden>();
    e.HasKey(x => x.Id);
    e.Property(x => x.Cliente).HasMaxLength(100).IsRequired();
    e.Property(x => x.Material).HasMaxLength(100).IsRequired();
    e.Property(x => x.Estado).HasMaxLength(24).IsRequired();
}

}
