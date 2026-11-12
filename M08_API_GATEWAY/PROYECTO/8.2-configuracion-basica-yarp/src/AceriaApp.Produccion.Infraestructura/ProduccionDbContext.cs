using AceriaApp.Produccion.Dominio;
using Microsoft.EntityFrameworkCore;
namespace AceriaApp.Produccion.Infraestructura;
public sealed class ProduccionDbContext(DbContextOptions<ProduccionDbContext> opciones) : DbContext(opciones)
{
    public DbSet<OrdenProduccion> Ordenes => Set<OrdenProduccion>();
    public DbSet<MensajeSalida> MensajesSalida => Set<MensajeSalida>();
    protected override void OnModelCreating(ModelBuilder model)
    {
        var salida = model.Entity<MensajeSalida>();
        salida.ToTable("MensajesSalida");
        salida.HasKey(x => x.Id);
        salida.HasIndex(x => x.OrdenId).IsUnique();
        salida.Property(x => x.Contenido).IsRequired();
        var orden = model.Entity<OrdenProduccion>();
        orden.Property(x => x.Revision).IsConcurrencyToken();
        orden.ToTable("OrdenesProduccion");
        orden.HasKey(o => o.Id);
        orden.Property(o => o.Id).ValueGeneratedNever();
        orden.Property(o => o.Cliente).HasMaxLength(100).IsRequired();
        orden.Property(o => o.Estado).HasConversion<string>().HasMaxLength(20);
        orden.Ignore(o => o.CantidadTotal);
        orden.Ignore(o => o.Cantidad);
        orden.Ignore(o => o.Material);
        orden.HasMany(o => o.Lineas).WithOne().HasForeignKey("OrdenId").IsRequired().OnDelete(DeleteBehavior.Cascade);
        orden.Navigation(o => o.Lineas).HasField("_lineas").UsePropertyAccessMode(PropertyAccessMode.Field);
        var linea = model.Entity<LineaDeOrden>();
        linea.ToTable("LineasProduccion");
        linea.HasKey(l => l.Id);
        linea.Property(l => l.Id).ValueGeneratedNever();
        linea.Property(l => l.Material).HasConversion(v => v.Valor, v => new NombreMaterial(v)).HasMaxLength(100).IsRequired();
        linea.Property(l => l.Cantidad).HasConversion(v => v.Valor, v => new CantidadProduccion(v));
    }
}
