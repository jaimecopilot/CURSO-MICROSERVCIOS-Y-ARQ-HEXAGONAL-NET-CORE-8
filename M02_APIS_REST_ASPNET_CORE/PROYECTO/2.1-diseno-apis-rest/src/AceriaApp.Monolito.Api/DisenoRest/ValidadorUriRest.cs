// INICIO PASO 2.1.8 — Activar el código de este paso con Ctrl+K, Ctrl+U.
// using System.Text.RegularExpressions;
// namespace AceriaApp.Monolito.Api.DisenoRest;
// public class ValidadorUriRest
// {
//     private static readonly HashSet<string> VerbosProhibidos = new(StringComparer.OrdinalIgnoreCase)
//         { "crear", "obtener", "listar", "actualizar", "eliminar", "get", "post", "put", "patch", "delete" };
//     public ResultadoUri Validar(string? uri)
//     {
//         var errores = new List<string>();
//         if (string.IsNullOrWhiteSpace(uri)) return new(false, new[] { "La URI es obligatoria." });
//         if (!uri.StartsWith("/api/", StringComparison.Ordinal)) errores.Add("La URI no empieza por '/api/'.");
//         var partes = uri.Split('?', 2)[0].Trim('/').Split('/');
//         if (partes.Length < 3 || !Regex.IsMatch(partes[1], @"^v[1-9]\d*$"))
//             errores.Add("La URI no incluye versión después de 'api'.");
//         if (partes.Length < 3 || string.IsNullOrWhiteSpace(partes[2]))
//             errores.Add("La URI no identifica un recurso.");
//         foreach (var parte in partes.Skip(2))
//             if (VerbosProhibidos.Contains(parte))
//                 errores.Add($"La URI contiene un verbo prohibido: '{parte}'.");
//         return new(errores.Count==0,errores);
//     }
// }
// public record ResultadoUri(bool EsValida, IReadOnlyList<string> Errores);
// FIN PASO 2.1.8
