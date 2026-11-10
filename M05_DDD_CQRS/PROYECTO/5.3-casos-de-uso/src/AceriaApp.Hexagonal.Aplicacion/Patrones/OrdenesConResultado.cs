using AceriaApp.Hexagonal.Dominio;
namespace AceriaApp.Hexagonal.Aplicacion.Patrones;

public sealed class OrdenesConResultado(IOrdenTrabajoRepositorio repositorio, IUnitOfWork trabajo)
{
    public async Task<Result<OrdenHexagonal>> CrearAsync(string cliente, string material, int cantidad, CancellationToken ct = default)
    {
        if (string.IsNullOrWhiteSpace(cliente) || string.IsNullOrWhiteSpace(material)
            || cliente.Trim().Length > 100 || material.Trim().Length > 100 || cantidad <= 0 || cantidad > 500)
            return Result<OrdenHexagonal>.Fallo(new Error("orden.validacion",
                "Cliente y material de 1 a 100 caracteres; cantidad entre 1 y 500.", TipoError.Validacion));
        var orden = new OrdenHexagonal(cliente, material, cantidad);
        await repositorio.AgregarAsync(orden, ct);
        await trabajo.CommitAsync(ct);
        return Result<OrdenHexagonal>.Exito(orden);
    }

    public async Task<Result<OrdenHexagonal>> ObtenerAsync(Guid id, CancellationToken ct = default)
    {
        var orden = await repositorio.ObtenerAsync(id, ct);
        return orden is null
            ? Result<OrdenHexagonal>.Fallo(new Error("orden.ausente", "No existe la orden.", TipoError.NoEncontrado))
            : Result<OrdenHexagonal>.Exito(orden);
    }

    public async Task<Result<OrdenHexagonal>> FinalizarAsync(Guid id, CancellationToken ct = default)
    {
        var resultado = await ObtenerAsync(id, ct);
        if (!resultado.EsExito) return resultado;
        var orden = resultado.Valor;
        if (orden.Estado == "Finalizada")
            return Result<OrdenHexagonal>.Fallo(new Error("orden.finalizada", "La orden ya está finalizada.", TipoError.Conflicto));
        orden.Finalizar();
        await trabajo.CommitAsync(ct);
        return Result<OrdenHexagonal>.Exito(orden);
    }
}
