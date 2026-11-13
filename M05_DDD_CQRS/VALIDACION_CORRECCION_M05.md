# M05 — Informe de corrección editorial y validación técnica

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS  
**Módulo:** M05 — Domain-Driven Design y CQRS  
**Autor:** JAIME GALLO  
**Rama:** `version-corregida`  
**Fecha:** 13 de noviembre de 2026  
**Estado:** CIERRE TÉCNICO DE ESTA PASADA; aprobación editorial final del autor independiente.

## Corrección pedagógica de las prácticas

Se han revisado los cinco puntos 5.1 a 5.5, con **24 pasos por punto** y **120 pasos en total**. El manual explica en prosa el diseño de contextos delimitados, el agregado de Producción, las invariantes, las entidades y value objects, los casos de uso, el puerto de repositorio y la separación CQRS. Se distingue la validez de un catálogo conceptual del comportamiento ejecutable de las clases y adaptadores.

Se conservan exactamente los **146 bloques de código originales**, con sus **106 marcadores `M05_CODIGO`** de paso, ruta y operación (crear, reemplazar o insertar). Las **294 glosas numeradas de líneas**, incluidas las de los retos, se han transformado en comentarios didácticos. El código de la raíz `OrdenProduccion` se acompaña ahora de una explicación desarrollada de la capacidad didáctica, las transiciones y la igualdad por identidad.

PDF: `PRACTICAS/M05_PRACTICAS.pdf`, **126 páginas** en la pasada de generación corregida, con la cabecera `ARQUITECTURA HEXAGONAL Y MICROSERVICIOS / PRÁCTICAS MÓDULO 5 / JAIME GALLO` verificada en cada página. La sincronización definitiva con el último cambio editorial se acredita por la ejecución final de generación.

## Pruebas reales con Windows y SQL Server Express

Los cinco snapshots se copiaron a rutas cortas del runner `windows-2022` para evitar limitaciones nativas de SQL Client, y se compilaron en Release. Los tests utilizaron el proveedor relacional EF Core SQL Server contra **SQL Server Express 2022**, con bases aisladas por prueba.

| Punto | Pruebas correctas | Fallidas |
|---|---:|---:|
| 5.1 Conceptos DDD | 134 | 0 |
| 5.2 Entidades y Value Objects | 153 | 0 |
| 5.3 Casos de uso | 172 | 0 |
| 5.4 Commands y Queries | 190 | 0 |
| 5.5 Dominio de la acería | 208 | 0 |
| **Total de ejecuciones acumuladas** | **857** | **0** |

El snapshot final contiene **208 pruebas**, no 857 casos distintos. La cifra acumulada refleja cinco ejecuciones de la solución a medida que crecen sus etapas.

## E2E funcional del contexto Producción

Sobre `/api/v1/produccion/ordenes` en la etapa 5.5 se comprobaron:

- Crear orden en SQL Server Express: **POST 201** y cabecera Location.
- Recuperarla por ID: **GET 200** con identidad y cliente persistidos.
- Buscar ID inexistente: **404**.
- Agregar línea a una orden en Borrador: **200**.
- Planificar: **200**; finalizar: **200**.
- Repetir la finalización: conflicto **409**.
- Crear con entrada inválida: **400**.
- Listar órdenes e incluir la creada: **200**.
- Documento OpenAPI: **200**.

## Alcance y trazabilidad

El auditor comprueba el orden de los **120 pasos** y verifica que los destinos de los **106 marcadores `M05_CODIGO`** existen en los snapshots. Los tests prueban las soluciones canónicas y los comportamientos SQL/HTTP del estado final; no equivalen a reconstruir manualmente todos los archivos siguiendo cada clic de Visual Studio ni incluyen los retos optativos. Los tests de catálogo demuestran las reglas declaradas, mientras los tests del dominio e integración acreditan invariantes y persistencia: son evidencias diferentes que no deben confundirse.

## Evidencias y reproducción

- [GitHub Actions de Windows — M04 y M05](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43485558931).
- Validador: `tools/validar_practicas_m04_m05.py`.
- Workflow: `.github/workflows/m04-m05-windows-e2e.yml`.
- Generación PDF: `.github/workflows/rebuild-corrected-theory-pdfs.yml`.
- Cabeceras: `tools/pdf_running_headers.py`.

**Conclusión:** M05 supera el cierre técnico de esta revisión editorial en `version-corregida`. No se han modificado los proyectos de referencia ni fusionado los cambios con `main`.
