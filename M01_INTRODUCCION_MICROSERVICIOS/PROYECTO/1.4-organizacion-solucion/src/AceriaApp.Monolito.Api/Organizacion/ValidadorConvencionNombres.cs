// INICIO PASO 1.4.7 — SELECCIONAR EL BLOQUE COMENTADO Y DESCOMENTAR (Ctrl+K, Ctrl+U).
// using System.Collections.Generic;
// using System.Linq;
// namespace AceriaApp.Monolito.Api.Organizacion;
//
// // PASO 1.4.7: validar prefijo, cantidad de partes y tipo permitido.
// public class ValidadorConvencionNombres
// {
//     private readonly string _prefijo;
//     private readonly IReadOnlyList<string> _tiposPermitidos;
//     public ValidadorConvencionNombres(string prefijo, IReadOnlyList<string> tiposPermitidos)
//     {
//         _prefijo = prefijo;
//         _tiposPermitidos = tiposPermitidos;
//     }
//
//     public ResultadoConvencion Validar(string nombreProyecto)
//     {
//         var errores = new List<string>();
//         if (!nombreProyecto.StartsWith(_prefijo + ".", StringComparison.Ordinal))
//             errores.Add($"El proyecto no empieza por '{_prefijo}.'.");
//         var partes = nombreProyecto.Split('.');
//         if (partes.Length != 3)
//             errores.Add("El nombre no tiene el formato 'Prefijo.Componente.Tipo'.");
//         else if (!_tiposPermitidos.Contains(partes[2]))
//             errores.Add($"El tipo '{partes[2]}' no está permitido.");
//         return new ResultadoConvencion(errores.Count == 0, errores);
//     }
// }
// public record ResultadoConvencion(bool EsValido, IReadOnlyList<string> Errores);
// FIN PASO 1.4.7
