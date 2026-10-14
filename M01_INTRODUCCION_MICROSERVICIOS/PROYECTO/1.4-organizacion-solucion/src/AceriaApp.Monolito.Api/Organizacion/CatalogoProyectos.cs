// INICIO PASO 1.4.9 — SELECCIONAR EL BLOQUE COMENTADO Y DESCOMENTAR (Ctrl+K, Ctrl+U).
// using System.Linq;
// namespace AceriaApp.Monolito.Api.Organizacion;
//
// // PASO 1.4.9: filtrar nombres de proyectos.
// public class CatalogoProyectos
// {
//     private readonly List<string> _nombres;
//     public CatalogoProyectos(List<string> nombres) { _nombres = nombres; }
//     public IEnumerable<string> ProyectosValidos(ValidadorConvencionNombres validador) =>
//         _nombres.Where(n => validador.Validar(n).EsValido);
//     public IEnumerable<string> ProyectosInvalidos(ValidadorConvencionNombres validador) =>
//         _nombres.Where(n => !validador.Validar(n).EsValido);
//
//     // RETO 1.4: descomentar este bloque y el record al final del archivo.
//     // public ResumenProyectos Resumen(ValidadorConvencionNombres validador)
//     // {
//     //     var validos = _nombres.Count(n => validador.Validar(n).EsValido);
//     //     var invalidos = _nombres.Count - validos;
//     //     var total = _nombres.Count;
//     //     var porcentaje = total == 0 ? 0 : (double)validos / total * 100;
//     //     return new ResumenProyectos(validos, invalidos, porcentaje);
//     // }
// }
// // public record ResumenProyectos(int Validos, int Invalidos, double PorcentajeValidez);
// FIN PASO 1.4.9
