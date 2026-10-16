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
