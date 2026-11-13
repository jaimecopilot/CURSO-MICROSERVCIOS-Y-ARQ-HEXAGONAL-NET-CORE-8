# M03 — Informe de revisión pedagógica y validación técnica

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS  
**Módulo:** M03 — Arquitectura hexagonal con ASP.NET Core 8  
**Autor:** JAIME GALLO  
**Rama:** `version-corregida`  
**Fecha:** 13 de noviembre de 2026  
**Estado:** CIERRE TÉCNICO DE ESTA REVISIÓN. La aceptación editorial definitiva corresponde al autor.

## Revisión de las prácticas

- Se revisaron los puntos 3.1, 3.2, 3.3 y 3.4, con **24 pasos en cada uno** (96 en total).
- Se sustituyeron los 96 encabezamientos de aprendizaje mecánicos por una secuencia explicativa situada junto a cada procedimiento.
- Se añadieron introducciones narrativas a cada punto y explicaciones técnicas detalladas de conceptos clave: dependencias, puertos y adaptadores, separación de proyectos y composición de ASP.NET Core.
- Se conservan intactos los **69 bloques originales de código**, sus referencias de archivo y las instrucciones de ejecución.
- PDF `PRACTICAS/M03_PRACTICAS.pdf`: **78 páginas**, con las tres líneas de cabecera verificadas en todas ellas.

## Pruebas reales de Windows con SQL Server Express

Los cuatro snapshots se compilaron y probaron en `windows-2022` con .NET 8, EF Core SQL Server y una instancia SQL Server 2022 Express real. Para evitar la limitación de rutas de bibliotecas nativas, cada proyecto se copió a una ruta de trabajo corta.

| Etapa | xUnit aprobadas | xUnit fallidas | Compilación |
|---|---:|---:|---|
| 3.1 Capas | 23 | 0 | Release OK |
| 3.2 Puertos y adaptadores | 31 | 0 | Release OK |
| 3.3 Separación física de capas | 38 | 0 | Release OK |
| 3.4 Implementación ASP.NET Core | 50 | 0 | Release OK |
| **Total de ejecuciones sobre los cuatro snapshots** | **142** | **0** | **Todas correctas** |

La etapa 3.4 incorpora **50 pruebas en su estado final**; el total 142 es el acumulado de ejecuciones de las cuatro etapas, no 142 pruebas diferentes.

## Integración HTTP y persistencia real

Sobre el snapshot final 3.4 se ejecutaron peticiones al adaptador HTTP hexagonal:

1. `GET /api/v1/hexagonal/ordenes` respondió HTTP 200.
2. `POST /api/v1/hexagonal/ordenes` respondió HTTP 201 con cabecera Location.
3. `GET /api/v1/hexagonal/ordenes/{id}` recuperó la orden persistida en SQL Server.
4. Entrada inválida: HTTP 400, sin confundirla con validación industrial.
5. Cantidad superior a la capacidad docente: HTTP 422.
6. `/swagger/v1/swagger.json`: HTTP 200.

## Trazabilidad y límites

El auditor valida los 96 identificadores de paso y la existencia de archivos de destino para los **57 marcadores `M03_CODIGO`** con su tipo de operación declarado (crear, reemplazar o insertar). Se han conservado los 69 bloques de código, sin alterar los contratos de los proyectos.

**Alcance de evidencia:** esta ejecución prueba las cuatro soluciones de referencia y el recorrido final mediante HTTP y SQL Server; también comprueba rutas marcadas y continuidad editorial. No sustituye la reconstrucción manual completa de cada archivo desde la práctica ni un ensayo separado de todas las acciones gráficas de Visual Studio. Las pruebas de catálogo y de integración acreditan capacidades diferentes. Los retos optativos quedan fuera del recuento.

## Evidencia y reproducibilidad

- [GitHub Actions — Windows SQL Server, M02 y M03](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43470830650).
- Validador: `tools/validar_practicas_m02_m03.py`.
- Workflow: `.github/workflows/m02-m03-windows-e2e.yml`.
- Regeneración del PDF: `.github/workflows/rebuild-corrected-theory-pdfs.yml`.
- Cabeceras: `tools/pdf_running_headers.py`.

**Conclusión:** M03 queda cerrado técnicamente para esta pasada de corrección de redacción en `version-corregida`. No se modifica el código de `PROYECTO` ni se fusionan los cambios en `main`.
