namespace AceriaApp.Comunicacion.Contratos;
public sealed record LineaPlanificadaV1(string Material, int Cantidad);
public sealed record OrdenPlanificadaV1(Guid EventoId, Guid OrdenId, DateTimeOffset OcurridoEnUtc,
    IReadOnlyList<LineaPlanificadaV1> Lineas, int Version = 1)
{
    public void Validar()
    {
        if (Version != 1 || EventoId == Guid.Empty || OrdenId == Guid.Empty || OcurridoEnUtc == default ||
            Lineas is null || Lineas.Count == 0 || Lineas.Count > 500 ||
            Lineas.Any(x => x is null || string.IsNullOrWhiteSpace(x.Material) || x.Material.Length > 100 || x.Cantidad < 1 || x.Cantidad > 500) ||
            Lineas.Sum(x => (long)x.Cantidad) > 500)
            throw new InvalidDataException("Evento de planificación incompatible o inválido.");
    }
}
