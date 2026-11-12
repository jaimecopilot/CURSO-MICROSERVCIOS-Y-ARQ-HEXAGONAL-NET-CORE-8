using System.Net;
using System.Net.Http.Json;
using AceriaApp.Comunicacion.Contratos;
using AceriaApp.Inventario.Api;
using AceriaApp.PruebasSqlServer;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Xunit;
namespace AceriaApp.ComunicacionSincrona.Tests;
public class InventarioSqlTests
{
    private sealed class Factory : WebApplicationFactory<InventarioProgram>
    {
        private readonly BaseSqlServer bd=BaseSqlServer.Crear();
        public Factory()
        {
            using var db=Nuevo();db.Database.EnsureCreated();
            db.Existencias.Add(new Existencia{Material="Acero",Stock=80});db.SaveChanges();
        }
        public InventarioDbContext Nuevo()=>new(new DbContextOptionsBuilder<InventarioDbContext>().UseSqlServer(bd.ConnectionString).Options);
        protected override void ConfigureWebHost(IWebHostBuilder builder)
        {
            builder.UseEnvironment("Development");builder.UseSetting("SkipDatabaseInitialization","true");
            builder.ConfigureTestServices(s=>{s.RemoveAll<DbContextOptions<InventarioDbContext>>();s.AddDbContext<InventarioDbContext>(o=>o.UseSqlServer(bd.ConnectionString));});
        }
        protected override void Dispose(bool disposing){base.Dispose(disposing);if(disposing)bd.Dispose();}
    }
    [Fact]
    public async Task API_devuelve_datos_persistidos_con_SQLServer()
    {using var f=new Factory();using var http=f.CreateClient();var r=await http.GetFromJsonAsync<MaterialDto>("/api/v1/materiales/Acero");Assert.Equal(80,r!.Stock);using var db=f.Nuevo();Assert.Equal("Microsoft.EntityFrameworkCore.SqlServer",db.Database.ProviderName);}
    [Fact]
    public async Task API_devuelve_404_para_material_ausente()
    {using var f=new Factory();using var http=f.CreateClient();Assert.Equal(HttpStatusCode.NotFound,(await http.GetAsync("/api/v1/materiales/NoExiste")).StatusCode);}
    [Fact]
    public async Task Stock_se_recupera_desde_otro_contexto_SQL()
    {using var f=new Factory();using(var db=f.Nuevo()){(await db.Existencias.SingleAsync()).Stock=70;await db.SaveChangesAsync();}using var otro=f.Nuevo();Assert.Equal(70,(await otro.Existencias.SingleAsync()).Stock);}
}
