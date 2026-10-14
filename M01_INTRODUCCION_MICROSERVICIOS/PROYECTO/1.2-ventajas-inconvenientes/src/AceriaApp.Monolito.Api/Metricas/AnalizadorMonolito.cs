// INICIO PASO 1.2.8 — SELECCIONAR EL BLOQUE COMENTADO Y DESCOMENTAR (Ctrl+K, Ctrl+U).
// using System.Linq;
// namespace AceriaApp.Monolito.Api.Metricas;
//
// // PASO 1.2.8: agregar indicadores y filtrar candidatos.
// public class AnalizadorMonolito
// {
//     private readonly List<MetricasServicio> _servicios;
//
//     public AnalizadorMonolito(List<MetricasServicio> servicios)
//     {
//         _servicios = servicios;
//     }
//
//     public MetricasAcoplamiento CalcularAcoplamientoGlobal()
//     {
//         var numeroDeProyectos = _servicios.Count;
//         var numeroDeReferencias = _servicios.Sum(s => s.NumeroDeDependenciasExternas);
//         var numeroDeTablasCompartidas = _servicios.Sum(s => s.NumeroDeTablas);
//         return new MetricasAcoplamiento
//         {
//             NumeroDeProyectos = numeroDeProyectos,
//             NumeroDeReferenciasEntreProyectos = numeroDeReferencias,
//             NumeroDeTablasCompartidas = numeroDeTablasCompartidas
//         };
//     }
//
//     public IEnumerable<MetricasServicio> ServiciosCandidatosAExtraccion() =>
//         _servicios.Where(s => s.EsCandidatoAExtraccion());
//
//     // RETO 1.2: descomentar para seleccionar el servicio con menor índice.
//     // public MetricasServicio? ServicioMenosAcoplado()
//     // {
//     //     if (_servicios.Count == 0) return null;
//     //     return _servicios.OrderBy(s => s.IndiceDeComplejidad())
//     //                      .ThenBy(s => s.Nombre).First();
//     // }
// }
// FIN PASO 1.2.8
