# Punto 7.1 — Logging

## Objetivo

Completar el catálogo y su validación, distinguirlo de los adaptadores ejecutables y conservar la base anterior.

## Estado del proyecto

- Solución `AceriaApp.sln`: 31 proyectos, 19 proyectos de tests y 309 pruebas acumuladas.
- 12 pruebas nuevas de análisis en `tests/AceriaApp.Logging.Tests`.
- Tipos `ConfiguracionLogging`, `ValidadorLogging` y `CatalogoLogging` en `src/AceriaApp.Api/Logging`.
- Los catálogos no configuran logging, probes, manejadores ni políticas HTTP.

## Cómo ejecutarlo

1. Abre `AceriaApp.sln` en Visual Studio con soporte .NET 8.
2. Configura SQL Server Express o LocalDB y la conexión de pruebas `ACERIA_TEST_SQLSERVER`; conserva el helper `tests/Compartido/SqlServerPruebas.cs`.
3. Ejecuta `dotnet restore AceriaApp.sln` y `dotnet build AceriaApp.sln -c Release`.
4. Ejecuta `dotnet test AceriaApp.sln -c Release --no-build --no-restore` con los servicios requeridos por la integración funcional disponibles.
5. Sigue el manual M07 para iniciar los adaptadores y observar logs, salud, errores y recuperación HTTP.

## Qué se ha añadido respecto al punto anterior

El catálogo del punto, su proyecto de pruebas, `docs/logging.md` y el ADR-027. Los bloques funcionales se aplican progresivamente y el paso 17 completa el registro y la compilación del punto. Se conservan los documentos y pruebas heredados.

## Documentación

- [Tema del punto](docs/logging.md).
- [ADR-027](docs/ADR-027-logging.md).
- Los 34 documentos anteriores, incluidos los ADR-010 a ADR-026, permanecen disponibles en `docs`.
