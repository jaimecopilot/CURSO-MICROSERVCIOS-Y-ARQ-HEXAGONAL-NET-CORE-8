using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Monolito.Api.BuenasPracticas;

// PASO 1.5.7: verificación sobre prácticas DECLARADAS (no inspecciona código).
public class ValidadorBuenasPracticas
{
    private readonly IReadOnlyList<string> _categoriasPermitidas;

    public ValidadorBuenasPracticas(IReadOnlyList<string> categoriasPermitidas)
    {
        _categoriasPermitidas = categoriasPermitidas;
    }

    public ResultadoPracticas Validar(IEnumerable<Practica> practicas)
    {
        var errores = new List<string>();
        var lista = practicas.ToList();
        if (lista.Count == 0)
        {
            errores.Add("No se ha declarado ninguna práctica.");
        }
        foreach (var practica in lista)
        {
            if (!_categoriasPermitidas.Contains(practica.Categoria))
                errores.Add($"Categoría no permitida: '{practica.Categoria}'.");
            if (!practica.EstaAplicada)
                errores.Add($"Práctica no aplicada: '{practica.Codigo}'.");
        }
        return new ResultadoPracticas(errores.Count == 0, errores);
    }
}

public record ResultadoPracticas(bool EsValido, IReadOnlyList<string> Errores);
