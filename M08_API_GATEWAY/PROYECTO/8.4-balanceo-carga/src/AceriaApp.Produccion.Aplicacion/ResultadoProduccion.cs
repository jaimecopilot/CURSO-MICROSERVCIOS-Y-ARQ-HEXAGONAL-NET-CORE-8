namespace AceriaApp.Produccion.Aplicacion;
public enum TipoErrorProduccion { Validacion, NoEncontrado, Conflicto }
public sealed record ErrorProduccion(string Codigo, string Mensaje, TipoErrorProduccion Tipo);
public sealed class ResultadoProduccion<T>
{
    private readonly T? valor;
    private readonly ErrorProduccion? error;
    public bool EsExito { get; }
    private ResultadoProduccion(T valor) { this.valor = valor; EsExito = true; }
    private ResultadoProduccion(ErrorProduccion error) { this.error = error; }
    public T Valor => EsExito ? valor! : throw new InvalidOperationException("Un fallo no contiene valor.");
    public ErrorProduccion Error => !EsExito ? error! : throw new InvalidOperationException("Un éxito no contiene error.");
    public static ResultadoProduccion<T> Exito(T valor)
    { ArgumentNullException.ThrowIfNull(valor); return new(valor); }
    public static ResultadoProduccion<T> Fallo(ErrorProduccion error)
    { ArgumentNullException.ThrowIfNull(error); return new(error); }
}
