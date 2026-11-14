# M01 — Cierre de la corrección pedagógica y validación técnica

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS  
**Módulo:** M01 — Introducción a los microservicios  
**Autor:** JAIME GALLO  
**Rama:** `version-corregida`  
**Fecha de validación:** 13 de noviembre de 2026  
**Estado:** CIERRE TÉCNICO VERIFICADO. La aprobación editorial final del autor es una decisión independiente.

## 1. Material de prácticas

- Manual revisado: `PRACTICAS/M01_PRACTICAS.md`.
- PDF sincronizado: `PRACTICAS/M01_PRACTICAS.pdf`, **85 páginas actuales**.
- Cinco puntos conservados: 1.1 a 1.5.
- 120 pasos y 52 fragmentos de código conservados.
- Sustituidas 25 explicaciones mecánicas de código por explicaciones funcionales. Se corrigieron introducciones, contradicciones entre «crear» y «comprobar» elementos ya preparados, y afirmaciones impropias sobre el alcance de indicadores de arquitectura.
- Cabecera `ARQUITECTURA HEXAGONAL Y MICROSERVICIOS / PRÁCTICAS MÓDULO 1 / JAIME GALLO` validada en las **85 páginas del PDF actual**.
- Ningún archivo de `PROYECTO` fue alterado por la revisión; los ejemplos de código del manual se conservaron.

## 2. Reconstrucción en Windows

La reconstrucción se realizó en `windows-2022` con .NET 8. Cada etapa se copió en una carpeta independiente y se activaron sus bloques `INICIO PASO` / `FIN PASO`, manteniendo los retos opcionales comentados. En 1.1 se activaron las migraciones incluidas con extensión provisional `.cs.txt`.

| Etapa | Fragmentos de código activados | Pruebas xUnit correctas | Compilación |
|---|---:|---:|---|
| 1.1 — Monolito | 6 | 1/1 | Release OK |
| 1.2 — Métricas | 6 | 9/9 | Release OK |
| 1.3 — Diseño | 5 | 13/13 | Release OK |
| 1.4 — Organización | 5 | 18/18 | Release OK |
| 1.5 — Buenas prácticas | 5 | 23/23 | Release OK |

**Total:** 64 ejecuciones de pruebas correctas entre snapshots. Se ejecutaron dos pasadas satisfactorias: una de compilación/xUnit y otra seguida de la integración SQL/HTTP.

## 3. Integración real

Ambiente: Windows Server 2022; SQL Server **2022 Express**, instancia `SQLEXPRESS`; EF Core 8; ASP.NET Core 8.

En el snapshot final **1.5** se verificó:

1. Aplicación de migración `202610140001_Inicial` mediante `dotnet-ef` 8.0.0 a SQL Server Express.
2. `GET /api/v1/ordenes` devuelve HTTP 200 y colección JSON.
3. `POST /api/v1/ordenes` devuelve HTTP 201, datos de la orden y `Location`.
4. Una nueva consulta GET recupera la orden persistida.
5. `/swagger/v1/swagger.json` devuelve HTTP 200 y declara `/api/v1/ordenes`.
6. El entorno de pruebas limpia la base de datos creada para el recorrido.

## 4. Alcance de las comprobaciones

La comprobación es **real**, pero no autoriza afirmaciones más amplias que las pruebas efectuadas:

- La reconstrucción está automatizada a partir de los mismos bloques que el manual pide activar; no simula todas las interacciones gráficas del alumno en Visual Studio.
- Se ejecutó el E2E HTTP y SQL del snapshot final acumulado, no una sesión HTTP independiente por cada uno de los cinco snapshots.
- Los retos optativos no se activaron ni se incluyeron en el recuento de pruebas.
- Los catálogos y validadores de M01 demuestran las reglas que programan, pero no pueden decidir automáticamente la arquitectura de una empresa real.
- La correcta extracción de texto, cabecera y puntos del PDF está validada de manera automática; no se afirma una inspección visual humana de cada página.

## 5. Evidencia y repetibilidad

- [Ejecución Windows y SQL Express en GitHub Actions](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43457816017).
- Workflow: `.github/workflows/m01-windows-e2e.yml`.
- Validador: `tools/validar_m01_windows.py`.
- Generación del PDF: `.github/workflows/rebuild-corrected-theory-pdfs.yml`.
- Cabeceras: `tools/pdf_running_headers.py`.

**Conclusión:** M01 puede considerarse **cerrado técnicamente para esta revisión** en la rama `version-corregida`. No se ha fusionado con `main`. El autor mantiene la aprobación editorial y la publicación definitiva.

**Verificación editorial de paginación actual:** [auditoría de los 17 PDF y 1.219 páginas](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516616292). La prueba automatizada comprueba cabeceras, contenido extraíble y márgenes; la aprobación visual final sigue correspondiendo al autor.

## 6. Reconstrucción adicional desde un directorio vacío — 14 de noviembre de 2026

Se ha añadido `tools/reconstruir_m01_desde_cero.py`. A diferencia de la batería anterior de activación de bloques comentados, esta comprobación **no copia ninguno de los cinco proyectos canónicos**. Crea una solución `AceriaApp.sln`, metadatos mínimos `.csproj`, configuración reproducible y los archivos C# y Markdown tomados de los fragmentos identificados de las prácticas corregidas. Cada punto hereda el resultado generado por el anterior. El SDK se fija en **.NET 8**, aunque el runner tenga instalado también un SDK más reciente.

La migración inicial de EF Core se genera desde el modelo con `dotnet-ef` y se aplica a una nueva base SQL Server Express, en lugar de copiar los archivos de migración históricos. Por ello se comprueba el **comportamiento**, no la igualdad literal del nombre de la migración. También se contrastan los archivos C# de cada etapa y la lista de proyectos de la solución con los proyectos de referencia.

| Etapa | C# reconstruidos | Proyectos de la solución | xUnit |
|---|---:|---:|---:|
| 1.1 | 4 | 2 | 1/1 |
| 1.2 | 10 | 3 | 9/9 |
| 1.3 | 15 | 4 | 13/13 |
| 1.4 | 20 | 5 | 18/18 |
| 1.5 | 25 | 6 | 23/23 |

**Resultado: 5/5 etapas reconstruidas, compiladas y probadas, 64 ejecuciones acumuladas de xUnit sin fallos.** En el punto final se ejecutó un E2E Windows con SQL Server Express y migración real: GET 200, POST 201 con Location y persistencia verificable, y OpenAPI/Swagger 200.

- [GitHub Actions: M01 reconstruido desde cero en Windows y SQL Express — SUCCESS](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43573679482).
- Script: `tools/reconstruir_m01_desde_cero.py`.
- Workflow: `.github/workflows/m01-desde-cero-windows-e2e.yml`.

**Alcance:** El manual del alumno entrega expresamente una solución preparada, y esta reconstrucción desde vacío representa una comprobación **adicional**, no una modificación encubierta de ese itinerario. Los metadatos y la solución se generan de forma reproducible; los archivos fuente se obtienen del manual. No se simulan operaciones gráficas de Visual Studio ni se ejecutan los retos optativos. La aprobación de redacción y de presentación visual corresponde al autor.
