using System.Collections.Generic;
namespace AceriaApp.Monolito.Api.Diseno;

// PASO 1.3.7: validar reglas explícitas de diseño de servicios.
public class ValidadorLimiteServicio
{
    public ResultadoValidacion Validar(LimiteServicio limite)
    {
        var errores = new List<string>();
        if (string.IsNullOrWhiteSpace(limite.CapacidadDeNegocio))
            errores.Add("El servicio no declara una capacidad de negocio.");
        if (string.IsNullOrWhiteSpace(limite.ContextoDelimitado))
            errores.Add("El servicio no declara un contexto delimitado.");
        if (limite.NumeroDeConceptos > 3)
            errores.Add("El servicio maneja más de tres conceptos: cohesión baja.");
        if (limite.NumeroDeDependenciasSalientes > 3)
            errores.Add("El servicio depende de más de tres servicios: acoplamiento alto.");
        if (limite.ExponeEntidadesDeDominio)
            errores.Add("El servicio expone entidades de dominio: viola la ocultación.");
        if (limite.ComparteBaseDeDatos)
            errores.Add("El servicio comparte base de datos: viola la autonomía.");
        return new ResultadoValidacion(errores.Count == 0, errores);
    }
}
public record ResultadoValidacion(bool EsValido, IReadOnlyList<string> Errores);
