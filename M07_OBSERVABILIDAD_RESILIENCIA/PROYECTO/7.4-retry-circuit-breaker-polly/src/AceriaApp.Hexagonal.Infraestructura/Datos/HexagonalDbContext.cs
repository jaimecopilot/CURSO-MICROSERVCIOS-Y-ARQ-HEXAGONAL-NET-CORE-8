using AceriaApp.Hexagonal.Dominio;
using Microsoft.EntityFrameworkCore;

namespace AceriaApp.Hexagonal.Infraestructura.Datos;

public sealed class HexagonalDbContext(DbContextOptions<HexagonalDbContext> options) : DbContext(options)
{
    public DbSet<OrdenHexagonal> Ordenes => Set<OrdenHexagonal>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        var e = modelBuilder.Entity<OrdenHexagonal>();
        e.ToTable("OrdenesHexagonales");
        e.HasKey(o => o.Id);
        e.Property(o => o.Cliente).HasMaxLength(100).IsRequired();
        e.Property(o => o.Material).HasMaxLength(100).IsRequired();
        e.Property(o => o.Estado).HasMaxLength(24).IsRequired();
    }
}
