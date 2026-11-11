# Punto 7.4 — Retry y Circuit Breaker mediante Polly

## Objetivo

Completar el catálogo y su validación, distinguirlo de los adaptadores ejecutables y conservar la base anterior.

## Estado del proyecto

- Solución `AceriaApp.sln`: 34 proyectos, 22 proyectos de tests y 403 pruebas acumuladas.
- 18 pruebas nuevas de análisis en `tests/AceriaApp.Resiliencia.Tests`.
- Tipos `PoliticaResiliencia`, `ValidadorResiliencia` y `CatalogoPoliticas` en `src/AceriaApp.Api/Resiliencia`.
- Los catálogos no configuran logging, probes, manejadores ni políticas HTTP.

## Cómo ejecutarlo

1. Abre `AceriaApp.sln` en Visual Studio con soporte .NET 8.
2. Configura SQL Server Express o LocalDB y la conexión de pruebas `ACERIA_TEST_SQLSERVER`; conserva el helper `tests/Compartido/SqlServerPruebas.cs`.
3. Ejecuta `dotnet restore AceriaApp.sln` y `dotnet build AceriaApp.sln -c Release`.
4. Ejecuta `dotnet test AceriaApp.sln -c Release --no-build --no-restore` con los servicios requeridos por la integración funcional disponibles.
5. Sigue el manual M07 para iniciar los adaptadores y observar logs, salud, errores y recuperación HTTP.

## Qué se ha añadido respecto al punto anterior

El catálogo del punto, su proyecto de pruebas, `docs/retry-circuit-breaker-polly.md` y el ADR-030. Los bloques funcionales se aplican progresivamente y el paso 17 completa el registro y la compilación del punto. Se conservan los documentos y pruebas heredados.

## Documentación

- [Tema del punto](docs/retry-circuit-breaker-polly.md).
- [ADR-030](docs/ADR-030-retry-circuit-breaker-polly.md).
- Los 40 documentos anteriores, incluidos los ADR-010 a ADR-029, permanecen disponibles en `docs`.
