# Punto 7.3 — Gestión de excepciones

## Objetivo

Completar el catálogo y su validación, distinguirlo de los adaptadores ejecutables y conservar la base anterior.

## Estado del proyecto

- Solución `AceriaApp.sln`: 33 proyectos, 21 proyectos de tests y 353 pruebas acumuladas.
- 13 pruebas nuevas de análisis en `tests/AceriaApp.GestionExcepciones.Tests`.
- Tipos `ManejadorExcepcion`, `ValidadorGestionExcepciones` y `CatalogoExcepciones` en `src/AceriaApp.Api/GestionExcepciones`.
- Los catálogos no configuran logging, probes, manejadores ni políticas HTTP.

## Cómo ejecutarlo

1. Abre `AceriaApp.sln` en Visual Studio con soporte .NET 8.
2. Configura SQL Server Express o LocalDB y la conexión de pruebas `ACERIA_TEST_SQLSERVER`; conserva el helper `tests/Compartido/SqlServerPruebas.cs`.
3. Ejecuta `dotnet restore AceriaApp.sln` y `dotnet build AceriaApp.sln -c Release`.
4. Ejecuta `dotnet test AceriaApp.sln -c Release --no-build --no-restore` con los servicios requeridos por la integración funcional disponibles.
5. Sigue el manual M07 para iniciar los adaptadores y observar logs, salud, errores y recuperación HTTP.

## Qué se ha añadido respecto al punto anterior

El catálogo del punto, su proyecto de pruebas, `docs/gestion-excepciones.md` y el ADR-029. Los bloques funcionales se aplican progresivamente y el paso 16 completa el registro y la compilación del punto. Se conservan los documentos y pruebas heredados.

## Documentación

- [Tema del punto](docs/gestion-excepciones.md).
- [ADR-029](docs/ADR-029-gestion-excepciones.md).
- Los 38 documentos anteriores, incluidos los ADR-010 a ADR-028, permanecen disponibles en `docs`.
