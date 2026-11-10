namespace AceriaApp.Api.PuertosAdaptadores;

public class ValidadorPuertosAdaptadores
{
    private readonly List<Puerto> _puertos;
    private readonly List<Adaptador> _adaptadores;

    public ValidadorPuertosAdaptadores(List<Puerto> puertos, List<Adaptador> adaptadores)
    {
        _puertos = puertos;
        _adaptadores = adaptadores;
    }

    public ResultadoValidacionHexagonal Validar()
    {
        var errores = new List<string>();

        foreach (var puerto in _puertos)
        {
            if (puerto.Tipo != "Entrada" && puerto.Tipo != "Salida")
            {
                errores.Add($"Tipo de puerto no válido: '{puerto.Tipo}'.");
            }

            if (puerto.Capa != "Aplicacion")
            {
                errores.Add($"El puerto '{puerto.Nombre}' no está en la capa de aplicación.");
            }
        }

        foreach (var adaptador in _adaptadores)
        {
            var puerto = _puertos.FirstOrDefault(p => p.Nombre == adaptador.PuertoImplementado);
            if (puerto is null)
            {
                errores.Add($"El adaptador '{adaptador.Nombre}' implementa un puerto desconocido: '{adaptador.PuertoImplementado}'.");
                continue;
            }

            if (puerto.Tipo == "Entrada" && adaptador.Capa != "Presentacion")
            {
                errores.Add($"El adaptador de entrada '{adaptador.Nombre}' no está en la capa de presentación.");
            }

            if (puerto.Tipo == "Salida" && adaptador.Capa != "Infraestructura")
            {
                errores.Add($"El adaptador de salida '{adaptador.Nombre}' no está en la capa de infraestructura.");
            }
        }

        return new ResultadoValidacionHexagonal(errores.Count == 0, errores);
    }
}

public record ResultadoValidacionHexagonal(bool EsValida, IReadOnlyList<string> Errores);
