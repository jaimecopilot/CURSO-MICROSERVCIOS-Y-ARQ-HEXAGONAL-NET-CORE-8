namespace AceriaApp.Hexagonal.Aplicacion.Patrones;

public enum TipoError { Validacion, NoEncontrado, Conflicto }

public sealed record Error
{
    public string Codigo { get; }
    public string Descripcion { get; }
    public TipoError Tipo { get; }
    public Error(string codigo, string descripcion, TipoError tipo)
    {
        if (string.IsNullOrWhiteSpace(codigo)) throw new ArgumentException("Código requerido.", nameof(codigo));
        if (string.IsNullOrWhiteSpace(descripcion)) throw new ArgumentException("Descripción requerida.", nameof(descripcion));
        if (!Enum.IsDefined(tipo)) throw new ArgumentOutOfRangeException(nameof(tipo));
        Codigo = codigo; Descripcion = descripcion; Tipo = tipo;
    }
}

/// <summary>Solo puede construirse un éxito con valor o un fallo con error.</summary>
public sealed class Result<T> where T : notnull
{
    private readonly T? valor;
    private readonly Error? error;
    public bool EsExito { get; }
    public T Valor => EsExito ? valor! : throw new InvalidOperationException("Un fallo no contiene valor.");
    public Error Error => !EsExito ? error! : throw new InvalidOperationException("Un éxito no contiene error.");
    private Result(T valor) { this.valor = valor; EsExito = true; }
    private Result(Error error) { this.error = error; EsExito = false; }
    public static Result<T> Exito(T valor)
    { ArgumentNullException.ThrowIfNull(valor); return new Result<T>(valor); }
    public static Result<T> Fallo(Error error)
    { ArgumentNullException.ThrowIfNull(error); return new Result<T>(error); }
}
