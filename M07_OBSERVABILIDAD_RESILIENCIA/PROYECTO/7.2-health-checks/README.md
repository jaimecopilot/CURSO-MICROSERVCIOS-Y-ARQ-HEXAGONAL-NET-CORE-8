# Punto 7.2 — Health Checks

## Objetivo

Completar el catálogo y su validación, distinguirlo de los adaptadores ejecutables y conservar la base anterior.

## Estado del proyecto

- Solución `AceriaApp.sln`: 32 proyectos, 20 proyectos de tests y 331 pruebas acumuladas.
- 13 pruebas nuevas de análisis en `tests/AceriaApp.HealthChecks.Tests`.
- Tipos `HealthCheck`, `ValidadorHealthChecks` y `CatalogoHealthChecks` en `src/AceriaApp.Api/HealthChecks`.
- Los catálogos no configuran logging, probes, manejadores ni políticas HTTP.

## Cómo ejecutarlo

1. Abre `AceriaApp.sln` en Visual Studio con soporte .NET 8.
2. Configura SQL Server Express o LocalDB y la conexión de pruebas `ACERIA_TEST_SQLSERVER`; conserva el helper `tests/Compartido/SqlServerPruebas.cs`.
3. Ejecuta `dotnet restore AceriaApp.sln` y `dotnet build AceriaApp.sln -c Release`.
4. Ejecuta `dotnet test AceriaApp.sln -c Release --no-build --no-restore` con los servicios requeridos por la integración funcional disponibles.
5. Sigue el manual M07 para iniciar los adaptadores y observar logs, salud, errores y recuperación HTTP.

## Qué se ha añadido respecto al punto anterior

El catálogo del punto, su proyecto de pruebas, `docs/health-checks.md` y el ADR-028. Los bloques funcionales se aplican progresivamente y el paso 16 completa el registro y la compilación del punto. Se conservan los documentos y pruebas heredados.

## Documentación

- [Tema del punto](docs/health-checks.md).
- [ADR-028](docs/ADR-028-health-checks.md).
- Los 36 documentos anteriores, incluidos los ADR-010 a ADR-027, permanecen disponibles en `docs`.
