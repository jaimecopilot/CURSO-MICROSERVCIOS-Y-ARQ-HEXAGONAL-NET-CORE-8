using Microsoft.EntityFrameworkCore;
namespace AceriaApp.Inventario.Api;
public sealed class Existencia
{
    public string Material { get; set; } = "";
    public int Stock { get; set; }
}
public sealed class InventarioDbContext(DbContextOptions<InventarioDbContext> opciones) : DbContext(opciones)
{
    public DbSet<Existencia> Existencias => Set<Existencia>();
    public DbSet<PlanificacionRecibida> Planificaciones => Set<PlanificacionRecibida>();
    protected override void OnModelCreating(ModelBuilder model)
    {
        model.Entity<PlanificacionRecibida>().HasKey(x => x.EventoId);
        model.Entity<PlanificacionRecibida>().HasIndex(x => x.OrdenId).IsUnique();
        model.Entity<PlanificacionRecibida>().Property(x => x.HuellaContenido).HasMaxLength(64);
        model.Entity<Existencia>().HasKey(x => x.Material);
        model.Entity<Existencia>().Property(x => x.Material).HasMaxLength(100);
    }
}
