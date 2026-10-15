namespace AceriaApp.Monolito.Api.DisenoRest;
public class UriRest
{
    public string Version { get; init; } = "v1";
    public string Recurso { get; init; } = string.Empty;
    public string? Identificador { get; init; }
    public string? SubRecurso { get; init; }
    public string Construir()
    {
        var partes = new List<string> { "api", Version, Recurso };
        if (!string.IsNullOrWhiteSpace(Identificador)) partes.Add(Identificador);
        if (!string.IsNullOrWhiteSpace(SubRecurso)) partes.Add(SubRecurso);
        return "/" + string.Join("/", partes);
    }
}
