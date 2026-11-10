using System.Collections.Generic;
using System.Linq;
namespace AceriaApp.Api.Repository;

public class ValidadorRepositorios
{
    public ResultadoRepositorios Validar(IEnumerable<Repositorio> repositorios)
    {
        var errores = new List<string>();
        var lista = repositorios.ToList();

        if (lista.Count == 0)
        {
            errores.Add("No hay repositorios declarados.");
        }

        foreach (var repositorio in lista)
        {
            if (string.IsNullOrWhiteSpace(repositorio.Nombre))
            {
                errores.Add("Un repositorio no declara el nombre.");
            }

            if (string.IsNullOrWhiteSpace(repositorio.Entidad))
            {
                errores.Add($"El repositorio '{repositorio.Nombre}' no declara la entidad.");
            }

            if (repositorio.NumeroDeMetodos < 1)
            {
                errores.Add($"El repositorio '{repositorio.Nombre}' no declara métodos.");
            }

            if (repositorio.TieneReglasDeNegocio)
            {
                errores.Add($"El repositorio '{repositorio.Nombre}' contiene reglas de negocio.");
            }

            if (repositorio.GestionaTransacciones)
            {
                errores.Add($"El repositorio '{repositorio.Nombre}' gestiona transacciones.");
            }
        }

        return new ResultadoRepositorios(errores.Count == 0, errores);
    }
}

public record ResultadoRepositorios(bool EsValido, IReadOnlyList<string> Errores);
