namespace AceriaApp.Api.Implementacion;

public class ValidadorRegistroServicios
{
    private static readonly string[] CiclosPermitidos = { "Transient", "Scoped", "Singleton" };

    public ResultadoRegistro Validar(IEnumerable<RegistroServicio> registros)
    {
        var errores = new List<string>();
        var lista = registros.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay registros declarados.");
        }

        foreach (var registro in lista)
        {
            if (string.IsNullOrWhiteSpace(registro.Puerto))
            {
                errores.Add("Un registro no declara el puerto.");
            }

            if (string.IsNullOrWhiteSpace(registro.Implementacion))
            {
                errores.Add($"El puerto '{registro.Puerto}' no declara implementación.");
            }

            if (!CiclosPermitidos.Contains(registro.Ciclo))
            {
                errores.Add($"Ciclo no permitido en el puerto '{registro.Puerto}': '{registro.Ciclo}'.");
            }

            if (registro.EsAdaptadorDeSalida && registro.Ciclo == "Transient")
            {
                errores.Add($"Un adaptador de salida no debería registrarse como Transient: '{registro.Puerto}'.");
            }
        }

        return new ResultadoRegistro(errores.Count == 0, errores);
    }
}

public record ResultadoRegistro(bool EsValido, IReadOnlyList<string> Errores);
