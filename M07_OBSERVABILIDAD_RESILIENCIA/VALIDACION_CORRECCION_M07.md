# M07 — Cierre técnico de las prácticas corregidas

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS  
**Módulo:** M07 — Observabilidad y resiliencia  
**Autor:** JAIME GALLO  
**Rama:** version-corregida  
**Fecha:** 13 de noviembre de 2026  
**Estado:** CIERRE TÉCNICO DE ESTA REVISIÓN; la aprobación editorial definitiva corresponde al autor.

## Revisión pedagógica

Las prácticas conservan los 96 pasos originales, sus 137 bloques de código completos y 93 marcadores de archivo y modo de operación. Los pasos han sido reescritos con una explicación conectada a su propósito funcional; se han eliminado las introducciones formularias y las glosas repetitivas por número de línea, sin perder instrucciones técnicas ni fragmentos de código.

El PDF corregido contiene **144 páginas** y la cabecera del curso, PRÁCTICAS MÓDULO 7 y el autor figura en todas las páginas (144/144). El Markdown y el PDF están sincronizados.

## Pruebas ejecutadas en Windows

Los snapshots de todas las etapas se copiaron a directorios temporales cortos, se compilaron en Release con .NET 8 y se ejecutaron mediante xUnit. Los tests utilizan SQL Server 2022 Express real y RabbitMQ real disponible en el runner Windows.

| Etapa | Pruebas correctas | Fallidas | Proyectos de pruebas |
|---|---:|---:|---:|
| 7.1 — Logging | 309 | 0 | 19 |
| 7.2 — Health Checks | 331 | 0 | 20 |
| 7.3 — Gestión de excepciones | 353 | 0 | 21 |
| 7.4 — Retry y Circuit Breaker | 403 | 0 | 22 |
| **Acumulado de ejecuciones** | **1396** | **0** | — |

El snapshot final contiene **403 pruebas**, no 1396 casos independientes; el acumulado repite los tests heredados entre etapas.

## Comprobaciones funcionales

La suite incluye logging y correlación, comprobaciones de vida y preparación, tratamiento de excepciones y pruebas de resiliencia con Polly. Los escenarios de retry, cancelación, timeout y circuit breaker se ejercitan con fallos controlados, mientras el conjunto acumulado mantiene las pruebas de SQL Server y RabbitMQ.

**Paridad de contenido:** 73 destinos: 73 equivalentes normalizados; 0 divergencias. La auditoría verificó los destinos de todos los marcadores de este módulo y comparó el último bloque de referencia de cada archivo con su contenido resultante.

## Alcance y limitaciones

- Los ensayos son reales en Windows y utilizan dependencias efectivas, pero prueban los proyectos canónicos de referencia. No reproducen automáticamente cada clic de Visual Studio ni todos los cambios manuales del alumno desde un proyecto vacío.
- Se utilizan bases de datos aisladas y topologías de mensajería temporales para evitar interferencias entre pruebas. La batería no pretende certificar una instalación productiva, ni autenticación y despliegues completos de todos los servicios.
- El runner Windows utiliza RabbitMQ nativo 4.3.5; los manuales siguen enseñando Docker Desktop con la imagen didáctica 4.1.5. Las pruebas acreditan el protocolo y la integración, no la instalación del entorno Docker Desktop de cada alumno.
- Los retos optativos no forman parte del conteo de pruebas. La revisión final de estilo por el autor sigue siendo una decisión independiente.

## Evidencias reproducibles

- [Ejecución Windows — tres módulos, SQL y RabbitMQ](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43492441952).
- [Generación y cabeceras PDF de M06-M08](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43491606429).
- [Auditoría adicional de paridad de código](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43493682718).
- Validador: tools/validar_practicas_m06_m08_windows.py.
- Workflow Windows: .github/workflows/m06-m08-practicas-windows-e2e.yml.
- Generador PDF: .github/workflows/rebuild-corrected-m06-m08-practicas.yml.

**Conclusión:** M07 cerrado técnicamente para la revisión de prácticas en version-corregida. No se han modificado las teorías, los proyectos de referencia ni la rama main.
