# M08 — Cierre técnico de las prácticas corregidas

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS  
**Módulo:** M08 — API Gateway mediante YARP  
**Autor:** JAIME GALLO  
**Rama:** version-corregida  
**Fecha:** 13 de noviembre de 2026  
**Estado:** CIERRE TÉCNICO DE ESTA REVISIÓN; la aprobación editorial definitiva corresponde al autor.

## Revisión pedagógica

Las prácticas conservan los 96 pasos originales, sus 96 bloques de código completos y 66 marcadores de archivo y modo de operación. Los pasos han sido reescritos con una explicación conectada a su propósito funcional; se han eliminado las introducciones formularias y las glosas repetitivas por número de línea, sin perder instrucciones técnicas ni fragmentos de código.

El PDF corregido contiene **118 páginas** y la cabecera del curso, PRÁCTICAS MÓDULO 8 y el autor figura en todas las páginas (118/118). El Markdown y el PDF están sincronizados.

## Pruebas ejecutadas en Windows

Los snapshots de todas las etapas se copiaron a directorios temporales cortos, se compilaron en Release con .NET 8 y se ejecutaron mediante xUnit. Los tests utilizan SQL Server 2022 Express real y RabbitMQ real disponible en el runner Windows.

| Etapa | Pruebas correctas | Fallidas | Proyectos de pruebas |
|---|---:|---:|---:|
| 8.1 — Introducción al gateway | 415 | 0 | 23 |
| 8.2 — Configuración de YARP | 451 | 0 | 24 |
| 8.3 — Enrutamiento de peticiones | 476 | 0 | 25 |
| 8.4 — Balanceo de carga | 491 | 0 | 26 |
| **Acumulado de ejecuciones** | **1833** | **0** | — |

El snapshot final contiene **491 pruebas**, no 1833 casos independientes; el acumulado repite los tests heredados entre etapas.

## Comprobaciones funcionales

Las pruebas funcionales de YARP ejercitan el reenvío HTTP, las transformaciones y el enrutamiento, el reparto RoundRobin entre destinos, la exclusión de servidores no preparados, la caída y recuperación de una instancia y la protección frente a reintentos de escrituras no idempotentes. La regresión incluye SQL Server y RabbitMQ reales.

**Paridad de contenido:** 47 destinos: 47 equivalentes normalizados; 0 divergencias. La auditoría verificó los destinos de todos los marcadores de este módulo y comparó el último bloque de referencia de cada archivo con su contenido resultante.

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

**Conclusión:** M08 cerrado técnicamente para la revisión de prácticas en version-corregida. No se han modificado las teorías, los proyectos de referencia ni la rama main.
