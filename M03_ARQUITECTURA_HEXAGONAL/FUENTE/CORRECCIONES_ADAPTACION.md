# Correcciones verificables al Módulo 3 original

Se han leído y conservado los cuatro puntos completos del ZIP y la revisión posterior de sus errores.

## Distinción esencial entre fuente original y versión implementable

La fuente antigua describe la solución hipotética `AceriaApp.Monolito.Api` y enumera hasta 15 proyectos heredados de un curso anterior. **Ese estado no existe** en la rama `main` aprobada: el punto real anterior es la Minimal API M02 2.4. Por tanto, los proyectos que se crean en M03 parten **del código actual que sí está en GitHub**. Los cuatro ejemplos de catálogo de la fuente (capas, puertos, separación, DI) se conservan íntegros en `FUENTE/` y se implementan como código y pruebas, pero no se hace pasar por verdadero que los proyectos de dominio o los servicios RabbitMQ estén registrados si son solo nombres de ejemplo.

## Errores conocidos en la validación original

La revisión original del 7 de octubre menciona: (1) «quince proyectos» en el README 3.4, cuando en aquella solución hipotética eran 14; (2) «setenta y cuatro pruebas» cuando la suma que la propia fuente ofrece es 81; (3) «catorce proyectos de tests» en lugar de proyectos totales; (4) «doce puntos completados» cuando 5 + 4 + 4 = 13; (5) una tabla de errores que describe incorrectamente un caso ya contemplado por el validador. La corrección se aplica en esta versión sin borrar el texto fuente.

## Recuentos actuales (no los históricos)

Base M02 2.4: 16 pruebas xUnit. Los cuatro ejercicios originales de M03 aportan 7, 8, 7 y 8 pruebas, respectivamente. El laboratorio actual incorpora cuatro pruebas HTTP adicionales de la implementación hexagonal real: **23 / 31 / 38 / 50 pruebas acumuladas**. Estos números son una expectativa que **solo se confirma cuando GitHub Actions completa el E2E**. No se deben copiar las cifras 58 / 66 / 73 / 81 del proyecto antiguo.

## Código real frente a catálogos conceptuales

- En 3.1 se programan reglas de dependencia entre capas; aún son comprobaciones descriptivas.
- En 3.2 se programan catálogos y se definen los puertos conceptual y técnicamente.
- En 3.3 se separan proyectos físicos reales: Dominio sin EF Core; Aplicación con `IOrdenRepositorio`; Infraestructura con `HexagonalDbContext` y `OrdenRepositorioSqlServer`.
- En 3.4 se conectan `OrdenesCasoUso`, el repositorio SQL Server y `HexagonalOrdenesEndpoints` por DI, con HTTP GET/POST/finalizar y pruebas E2E con InMemory.

Los endpoints originales de M02 **se preservan** para no romper el módulo aprobado. El nuevo adaptador está en `/api/v1/hexagonal/ordenes`. Su versión permite demostrar puertos y dependencias reales antes de considerar una futura sustitución de las rutas heredadas.

## Conservación íntegra

El texto original de teoría, práctica, reto, tablas de errores, documentación y código de cada punto permanece exactamente en `FUENTE/M03_3.N_ORIGINAL.md`, con SHA-256 en `MANIFIESTO_FUENTE.json`. La validación original está completa en `FUENTE/M03_VALIDACION_ORIGINAL.md`. Los materiales del alumno separan la teoría de la práctica; la tabla global repetitiva de errores no aparece en las versiones canónicas, siguiendo la misma corrección editorial aplicada a M01/M02, pero sí se conserva en la fuente original.
