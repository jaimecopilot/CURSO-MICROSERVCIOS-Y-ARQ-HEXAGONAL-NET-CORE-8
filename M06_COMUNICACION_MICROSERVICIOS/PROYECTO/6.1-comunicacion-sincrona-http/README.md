# Punto 6.1 — Comunicación síncrona mediante HTTP

## Objetivo

Completar el catálogo y su validación, distinguirlo de los adaptadores ejecutables y conservar la base anterior.

## Estado del proyecto

- Solución `AceriaApp.sln`: 27 proyectos y 232 pruebas acumuladas.
- 13 pruebas nuevas de análisis en `tests/AceriaApp.ComunicacionSincrona.Tests`.
- Tipos `LlamadaSincrona`, `ValidadorComunicacionSincrona` y `CatalogoLlamadas` en `src/AceriaApp.Api/ComunicacionSincrona`.
- Los catálogos no demuestran tráfico HTTP ni entrega de mensajes.

## Cómo ejecutarlo

1. Abre `AceriaApp.sln` en Visual Studio con soporte .NET 8.
2. Configura SQL Server Express o LocalDB y la conexión de pruebas `ACERIA_TEST_SQLSERVER`; conserva el helper `tests/Compartido/SqlServerPruebas.cs`.
3. Ejecuta `dotnet restore AceriaApp.sln` y `dotnet build AceriaApp.sln -c Release`.
4. Ejecuta `dotnet test AceriaApp.sln -c Release --no-build --no-restore` con los servicios requeridos por la integración funcional disponibles.
5. Sigue el manual M06 para iniciar los adaptadores y observar cada recorrido de comunicación.

## Qué se ha añadido respecto al punto anterior

El catálogo del punto, su proyecto de pruebas, `docs/comunicacion-sincrona-http.md` y el ADR-024. Los bloques funcionales de los pasos 5 a 15 completan la integración del punto. Se conservan los documentos y pruebas heredados.

## Documentación

- [Tema del punto](docs/comunicacion-sincrona-http.md).
- [ADR-024](docs/ADR-024-comunicacion-sincrona-http.md).
- Los 28 documentos anteriores, incluidos los ADR-010 a ADR-023, permanecen disponibles en `docs`.
