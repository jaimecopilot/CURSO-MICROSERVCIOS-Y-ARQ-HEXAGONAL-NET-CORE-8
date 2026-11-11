namespace AceriaApp.Produccion.Dominio;
public sealed class ReglaProduccionException(string codigo, string mensaje) : Exception(mensaje)
{
    public string Codigo { get; } = codigo;
}
public enum EstadoOrdenProduccion { Borrador, Planificada, Finalizada }
