# M01 — Cierre de la corrección pedagógica y validación técnica

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS  
**Módulo:** M01 — Introducción a los microservicios  
**Autor:** JAIME GALLO  
**Rama:** `version-corregida`  
**Fecha de validación:** 13 de noviembre de 2026  
**Estado:** CIERRE TÉCNICO VERIFICADO. La aprobación editorial final del autor es una decisión independiente.

## 1. Material de prácticas

- Manual revisado: `PRACTICAS/M01_PRACTICAS.md`.
- PDF sincronizado: `PRACTICAS/M01_PRACTICAS.pdf`, 86 páginas.
- Cinco puntos conservados: 1.1 a 1.5.
- 120 pasos y 52 fragmentos de código conservados.
- Sustituidas 25 explicaciones mecánicas de código por explicaciones funcionales. Se corrigieron introducciones, contradicciones entre «crear» y «comprobar» elementos ya preparados, y afirmaciones impropias sobre el alcance de indicadores de arquitectura.
- Cabecera `ARQUITECTURA HEXAGONAL Y MICROSERVICIOS / PRÁCTICAS MÓDULO 1 / JAIME GALLO` validada en las 86 páginas.
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
