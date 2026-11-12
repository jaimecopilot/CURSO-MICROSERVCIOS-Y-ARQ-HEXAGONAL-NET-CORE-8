namespace AceriaApp.Api.Capas;

public class ValidadorReglaDependencia
{
    private readonly Dictionary<string, IReadOnlyList<string>> _reglas;

    public ValidadorReglaDependencia(Dictionary<string, IReadOnlyList<string>> reglas)
    {
        _reglas = reglas;
    }

    public ResultadoDependencia Validar(string capaOrigen, string capaDestino)
    {
        var errores = new List<string>();

        if (!_reglas.ContainsKey(capaOrigen))
        {
            errores.Add($"Capa origen desconocida: '{capaOrigen}'.");
            return new ResultadoDependencia(false, errores);
        }

        if (!_reglas[capaOrigen].Contains(capaDestino))
        {
            errores.Add($"La capa '{capaOrigen}' no puede depender de '{capaDestino}'.");
        }

        return new ResultadoDependencia(errores.Count == 0, errores);
    }
}

public record ResultadoDependencia(bool EsValida, IReadOnlyList<string> Errores);
