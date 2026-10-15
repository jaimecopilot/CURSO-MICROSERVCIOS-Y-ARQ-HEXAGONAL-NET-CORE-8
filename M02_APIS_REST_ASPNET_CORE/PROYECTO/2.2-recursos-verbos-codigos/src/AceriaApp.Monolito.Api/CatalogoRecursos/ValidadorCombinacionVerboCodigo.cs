// INICIO PASO 2.2.7 — Activar el código de este paso con Ctrl+K, Ctrl+U.
// namespace AceriaApp.Monolito.Api.CatalogoRecursos;
// public class ValidadorCombinacionVerboCodigo
// {
//     private static readonly Dictionary<string,int[]> CodigosPorVerbo=new(StringComparer.OrdinalIgnoreCase)
//     {
//         ["GET"]=new[]{200,404}, ["POST"]=new[]{201,400,409,422},
//         ["PUT"]=new[]{200,204,400,404,409,422},
//         ["PATCH"]=new[]{200,204,400,404,409,422},
//         ["DELETE"]=new[]{204,404}
//     };
//     public ResultadoCombinacion Validar(CombinacionVerboCodigo combinacion)
//     {
//         var errores=new List<string>();
//         if(!CodigosPorVerbo.TryGetValue(combinacion.Verbo,out var codigos))
//         {
//             errores.Add($"Verbo no permitido: '{combinacion.Verbo}'.");
//             return new(false,errores);
//         }
//         if(!codigos.Contains(combinacion.Codigo))
//             errores.Add($"Código '{combinacion.Codigo}' no permitido para el verbo '{combinacion.Verbo}'.");
//         return new(errores.Count==0,errores);
//     }
// }
// public record ResultadoCombinacion(bool EsValida,IReadOnlyList<string> Errores);
// FIN PASO 2.2.7
