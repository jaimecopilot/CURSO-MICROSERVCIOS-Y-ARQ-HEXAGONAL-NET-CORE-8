using System;
using AceriaApp.Monolito.Api.Infraestructura;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace AceriaApp.Monolito.Api.Infraestructura.Migraciones;

// PASO 1.1.14 — Migración inicial de la tabla dbo.Ordenes.
[DbContext(typeof(AceriaDbContext))]
[Migration("202610140001_Inicial")]
public partial class Inicial : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Ordenes",
            columns: table => new
            {
                Id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                Cliente = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                Material = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                Cantidad = table.Column<int>(type: "int", nullable: false),
                FechaCreacion = table.Column<DateTime>(type: "datetime2", nullable: false)
            },
            constraints: table => table.PrimaryKey("PK_Ordenes", x => x.Id));
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable(name: "Ordenes");
    }
}
