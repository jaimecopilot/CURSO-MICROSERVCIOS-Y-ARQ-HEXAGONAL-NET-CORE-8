using System.Net;
using AceriaApp.Pruebas.Gateway;
using Xunit;
using Microsoft.Extensions.DependencyInjection;
using Yarp.ReverseProxy;
using Yarp.ReverseProxy.Model;

namespace AceriaApp.Balanceo.Tests;

public sealed class GatewayBalanceoFuncionalTests
{
    // Detecta pérdida del middleware de balanceo o sustitución accidental de RoundRobin.
    [Fact]
    public async Task RoundRobin_alterna_los_dos_destinos_sanos()
    {
        await using var prueba = await GatewayPruebas.CrearAsync(segundaInstancia: true);
        var instancias = await LeerInstanciasAsync(prueba, 8);
        Assert.Equal(4, instancias.Count(x => x == "inventario-1"));
        Assert.Equal(4, instancias.Count(x => x == "inventario-2"));
        for (var i = 1; i < instancias.Count; i++) Assert.NotEqual(instancias[i - 1], instancias[i]);
        await GatewayPruebas.EsperarAsync(() => Task.FromResult(prueba.Inventario1.Sondeos > 0 && prueba.Inventario2!.Sondeos > 0), "No se observaron sondeos activos en ambos servidores.");
    }

    [Fact]
    public async Task Tras_caida_fisica_y_recuperacion_la_instancia_vuelve_al_reparto()
    {
        await using var prueba = await GatewayPruebas.CrearAsync(segundaInstancia: true);
        Assert.Contains("inventario-2", await LeerInstanciasAsync(prueba, 4));
        await prueba.Inventario2!.DetenerAsync();
        await EsperarSaludAsync(prueba, "inventario-2", DestinationHealth.Unhealthy);
        Assert.All(await LeerInstanciasAsync(prueba, 8), x => Assert.Equal("inventario-1", x));
        await prueba.ReiniciarInventario2Async();
        await EsperarSaludAsync(prueba, "inventario-2", DestinationHealth.Healthy);
        var recuperadas = await LeerInstanciasAsync(prueba, 8);
        Assert.Equal(4, recuperadas.Count(x => x == "inventario-2"));
    }

    [Fact]
    public async Task Todos_los_destinos_detenidos_dan_503_y_un_destino_recuperado_restaura_servicio()
    {
        await using var prueba = await GatewayPruebas.CrearAsync(segundaInstancia: true);
        await prueba.Inventario1.DetenerAsync();
        await prueba.Inventario2!.DetenerAsync();
        await EsperarSaludAsync(prueba, "inventario-1", DestinationHealth.Unhealthy);
        await EsperarSaludAsync(prueba, "inventario-2", DestinationHealth.Unhealthy);
        for (var i = 0; i < 4; i++)
        {
            using var respuesta = await prueba.Cliente.GetAsync("/api/v1/materiales/Acero");
            Assert.Equal(HttpStatusCode.ServiceUnavailable, respuesta.StatusCode);
        }
        await prueba.ReiniciarInventario2Async();
        await EsperarSaludAsync(prueba, "inventario-2", DestinationHealth.Healthy);
        Assert.All(await LeerInstanciasAsync(prueba, 4), x => Assert.Equal("inventario-2", x));
    }

    [Fact]
    public async Task Readiness_no_satisfactoria_excluye_un_servidor_que_sigue_escuchando()
    {
        await using var prueba = await GatewayPruebas.CrearAsync(segundaInstancia: true);
        prueba.Inventario2!.Listo = false;
        await EsperarSaludAsync(prueba, "inventario-2", DestinationHealth.Unhealthy);
        Assert.All(await LeerInstanciasAsync(prueba, 8), x => Assert.Equal("inventario-1", x));
        using (var directo = new HttpClient())
        using (var respuesta = await directo.GetAsync(prueba.Inventario2.Direccion + "/api/v1/materiales/Acero"))
            Assert.Equal(HttpStatusCode.OK, respuesta.StatusCode);
        prueba.Inventario2.Listo = true;
        await EsperarSaludAsync(prueba, "inventario-2", DestinationHealth.Healthy);
        Assert.Contains("inventario-2", await LeerInstanciasAsync(prueba, 4));
    }

    [Fact]
    public async Task Una_escritura_abortada_en_el_backend_no_se_reintenta()
    {
        await using var prueba = await GatewayPruebas.CrearAsync(segundaInstancia: true);
        using var respuesta = await prueba.Cliente.PostAsync("/api/v1/ordenes?abortar=true", new StringContent("{\"cantidad\":1}"));
        Assert.Equal(HttpStatusCode.BadGateway, respuesta.StatusCode);
        Assert.Equal(1, prueba.Produccion.Escrituras);
        Assert.Equal(0, prueba.Inventario1.Escrituras + prueba.Inventario2!.Escrituras);
    }

    private static async Task<List<string>> LeerInstanciasAsync(GatewayPruebas prueba, int cantidad)
    {
        var instancias = new List<string>();
        for (var i = 0; i < cantidad; i++)
        {
            using var respuesta = await prueba.Cliente.GetAsync("/api/v1/materiales/Acero");
            instancias.Add(respuesta.IsSuccessStatusCode ? Assert.Single(respuesta.Headers.GetValues("X-Instancia")) : $"HTTP-{(int)respuesta.StatusCode}");
        }
        return instancias;
    }

    private static Task EsperarSaludAsync(GatewayPruebas prueba, string destinoId, DestinationHealth salud) =>
        GatewayPruebas.EsperarAsync(() =>
        {
            var estado = prueba.Proxy.Services.GetRequiredService<IProxyStateLookup>();
            var coincide = estado.TryGetCluster("inventario-cluster", out var cluster) &&
                cluster.Destinations.TryGetValue(destinoId, out var destino) && destino.Health.Active == salud;
            return Task.FromResult(coincide);
        }, $"El destino {destinoId} no alcanzó el estado activo {salud}.");
}
