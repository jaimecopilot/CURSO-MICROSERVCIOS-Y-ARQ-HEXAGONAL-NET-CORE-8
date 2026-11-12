namespace AceriaApp.Comunicacion.Aplicacion;
public sealed class FlujoPlanificacion(IPlanificadorIntegrado planificador, IClienteInventario inventario)
{
    public async Task<EstadoPlanificacion> EjecutarAsync(Guid id, CancellationToken ct)
    {
        ct.ThrowIfCancellationRequested();
        var lineas = await planificador.ObtenerLineasAsync(id, ct);
        if (lineas is null) return EstadoPlanificacion.NoExiste;
        foreach (var grupo in lineas.GroupBy(x => x.Material, StringComparer.OrdinalIgnoreCase))
        {
            var material = await inventario.ObtenerAsync(grupo.Key, ct);
            if (material is null || material.Stock < grupo.Sum(x => x.Cantidad)) return EstadoPlanificacion.SinDisponibilidad;
        }
        // Esta lectura es informativa: otro proceso puede cambiar el stock. No es una reserva.
        return await planificador.PlanificarAsync(id, ct);
    }
}
