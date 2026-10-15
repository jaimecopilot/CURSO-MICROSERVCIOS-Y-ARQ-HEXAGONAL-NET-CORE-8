using System;
using AceriaApp.Monolito.Api.Infraestructura;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Metadata;

#nullable disable

namespace AceriaApp.Monolito.Api.Infraestructura.Migraciones;

// PASO 1.1.14 — Estado del modelo después de la migración inicial.
[DbContext(typeof(AceriaDbContext))]
public partial class AceriaDbContextModelSnapshot : ModelSnapshot
{
    protected override void BuildModel(ModelBuilder modelBuilder)
    {
        modelBuilder.HasAnnotation("ProductVersion", "8.0.0")
            .HasAnnotation("Relational:MaxIdentifierLength", 128);

        modelBuilder.Entity("AceriaApp.Monolito.Api.Dominio.Orden", b =>
        {
            b.Property<Guid>("Id").HasColumnType("uniqueidentifier");
            b.Property<int>("Cantidad").HasColumnType("int");
            b.Property<string>("Cliente").IsRequired().HasMaxLength(100).HasColumnType("nvarchar(100)");
            b.Property<DateTime>("FechaCreacion").HasColumnType("datetime2");
            b.Property<string>("Material").IsRequired().HasMaxLength(100).HasColumnType("nvarchar(100)");
            b.HasKey("Id");
            b.ToTable("Ordenes");
        });
    }
}
