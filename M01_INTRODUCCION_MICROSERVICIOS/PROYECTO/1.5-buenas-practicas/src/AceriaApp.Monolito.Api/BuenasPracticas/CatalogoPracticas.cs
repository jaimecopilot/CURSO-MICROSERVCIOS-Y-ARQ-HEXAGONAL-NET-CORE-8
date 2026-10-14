// INICIO PASO 1.5.9 — SELECCIONAR EL BLOQUE COMENTADO Y DESCOMENTAR (Ctrl+K, Ctrl+U).
// using System.Collections.Generic;
// using System.Linq;
// namespace AceriaApp.Monolito.Api.BuenasPracticas;
//
// // PASO 1.5.9: filtrar prácticas declaradas.
// public class CatalogoPracticas
// {
//     private readonly List<Practica> _practicas;
//
//     public CatalogoPracticas(List<Practica> practicas)
//     {
//         _practicas = practicas;
//     }
//
//     public IEnumerable<Practica> PracticasAplicadas() =>
//         _practicas.Where(p => p.EstaAplicada);
//
//     public IEnumerable<Practica> PracticasPendientes() =>
//         _practicas.Where(p => !p.EstaAplicada);
//
//     // RETO 1.5: descomentar el método junto con el record y el test opcional.
//     // public ResumenPracticas Resumen()
//     // {
//     //     var aplicadas = _practicas.Count(p => p.EstaAplicada);
//     //     var pendientes = _practicas.Count - aplicadas;
//     //     var total = _practicas.Count;
//     //     var porcentaje = total == 0 ? 0 : (double)aplicadas / total * 100;
//     //     return new ResumenPracticas(aplicadas, pendientes, porcentaje);
//     // }
// }
// // RETO 1.5: descomentar para habilitar el método Resumen().
// // public record ResumenPracticas(int Aplicadas, int Pendientes, double PorcentajeAplicacion);
// FIN PASO 1.5.9
