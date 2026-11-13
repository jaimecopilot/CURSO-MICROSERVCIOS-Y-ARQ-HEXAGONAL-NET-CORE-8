# M04 — Informe de corrección editorial y validación técnica

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS  
**Módulo:** M04 — Patrones de arquitectura  
**Autor:** JAIME GALLO  
**Rama:** `version-corregida`  
**Fecha:** 13 de noviembre de 2026  
**Estado:** CIERRE TÉCNICO DE ESTA PASADA; validación editorial del autor independiente.

## Corrección de prácticas

Se han revisado los puntos 4.1 a 4.5 (Repository, Unit of Work, Mediator, Result Pattern e inyección de dependencias), con 24 pasos por punto. Se han mantenido los **120 pasos**, los **136 bloques de código** y los **96 marcadores `M04_CODIGO`** con rutas, modos de inserción y orden de aplicación.

Los objetivos y justificaciones formulistas se han integrado en explicaciones sobre cómo operan los puertos, la persistencia SQL, MediatR, los resultados de aplicación y la composición de servicios. Las **282 glosas numeradas** de código, incluidas las de retos, se han transformado en comentarios explicativos sin alterar los bloques de código ni los fragmentos opcionales.

PDF: `PRACTICAS/M04_PRACTICAS.pdf`, **123 páginas** en la ejecución de generación corregida, con el encabezado `ARQUITECTURA HEXAGONAL Y MICROSERVICIOS / PRÁCTICAS MÓDULO 4 / JAIME GALLO` en cada página.

## Pruebas reproducidas en Windows y SQL Server Express

Los cinco snapshots fueron copiados a rutas de trabajo cortas sobre Windows Server 2022, compilados en Release y probados con `dotnet test`. El helper SQL compartido creó bases independientes en **SQL Server Express 2022**, utilizando el proveedor EF Core SQL Server real.

| Punto | Pruebas correctas | Pruebas fallidas |
|---|---:|---:|
| 4.1 Repository | 62 | 0 |
| 4.2 Unit of Work | 77 | 0 |
| 4.3 Mediator | 90 | 0 |
| 4.4 Result Pattern | 105 | 0 |
| 4.5 Inyección de dependencias | 118 | 0 |
| **Total de ejecuciones sobre snapshots** | **452** | **0** |

El estado final cuenta **118 pruebas**. La cifra 452 suma sus ejecuciones acumuladas y no significa que existan 452 casos distintos.

El recorrido E2E del snapshot 4.5 verificó sobre el endpoint `/api/v1/patrones/ordenes`:

- Crear orden: HTTP **201** y cabecera **Location**.
- Recuperar por ID: HTTP **200** con la misma entidad persistida.
- Consultar un ID desconocido: **404**.
- Finalizar: **200**; repetir la transición: conflicto **409**.
- Enviar datos inválidos: **400**.
- Obtener documento OpenAPI: **200**.

## Alcance y límites

El auditor confirma el orden de los 120 pasos y la existencia de archivos destino para los **96 marcadores explícitos**. Los proyectos de referencia se compilan y se someten a pruebas reales con SQL Express. No se ha reproducido manualmente la totalidad de acciones gráficas de Visual Studio ni reconstruido cada archivo desde una carpeta vacía siguiendo el texto del alumno; tampoco se han ejecutado los retos optativos. Los tests de catálogo acreditan sus reglas declaradas, no la implementación de un servicio remoto ajeno al recorrido.

## Evidencias

- [Ejecución de Windows con M04 y M05](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43485558931).
- `.github/workflows/m04-m05-windows-e2e.yml`
- `tools/validar_practicas_m04_m05.py`
- `.github/workflows/rebuild-corrected-theory-pdfs.yml`
- `tools/pdf_running_headers.py`

**Conclusión:** M04 supera el cierre técnico de la revisión en `version-corregida`. No se ha fusionado con `main` ni se han modificado los proyectos de referencia.
