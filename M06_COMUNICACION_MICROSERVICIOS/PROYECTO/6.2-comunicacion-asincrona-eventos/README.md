# Punto 6.2 — Comunicación asíncrona basada en eventos

## Objetivo

Completar el catálogo y su validación, distinguirlo de los adaptadores ejecutables y conservar la base anterior.

## Estado del proyecto

- Solución `AceriaApp.sln`: 28 proyectos y 264 pruebas acumuladas.
- 13 pruebas nuevas de análisis en `tests/AceriaApp.ComunicacionAsincrona.Tests`.
- Tipos `Evento`, `ValidadorComunicacionAsincrona` y `CatalogoEventos` en `src/AceriaApp.Api/ComunicacionAsincrona`.
- Los catálogos no demuestran tráfico HTTP ni entrega de mensajes.

## Cómo ejecutarlo

1. Abre `AceriaApp.sln` en Visual Studio con soporte .NET 8.
2. Configura SQL Server Express o LocalDB y la conexión de pruebas `ACERIA_TEST_SQLSERVER`; conserva el helper `tests/Compartido/SqlServerPruebas.cs`.
3. Ejecuta `dotnet restore AceriaApp.sln` y `dotnet build AceriaApp.sln -c Release`.
4. Ejecuta `dotnet test AceriaApp.sln -c Release --no-build --no-restore` con los servicios requeridos por la integración funcional disponibles.
5. Sigue el manual M06 para iniciar los adaptadores y observar cada recorrido de comunicación.

## Qué se ha añadido respecto al punto anterior

El catálogo del punto, su proyecto de pruebas, `docs/comunicacion-asincrona-eventos.md` y el ADR-025. Los bloques funcionales de los pasos 5 a 15 completan la integración del punto. Se conservan los documentos y pruebas heredados.

## Documentación

- [Tema del punto](docs/comunicacion-asincrona-eventos.md).
- [ADR-025](docs/ADR-025-comunicacion-asincrona-eventos.md).
- Los 30 documentos anteriores, incluidos los ADR-010 a ADR-024, permanecen disponibles en `docs`.
