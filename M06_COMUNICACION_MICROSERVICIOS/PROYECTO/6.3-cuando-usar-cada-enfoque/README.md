# Punto 6.3 — Cuándo utilizar cada enfoque

## Objetivo

Completar el catálogo y su validación, distinguirlo de los adaptadores ejecutables y conservar la base anterior.

## Estado del proyecto

- Solución `AceriaApp.sln`: 29 proyectos y 283 pruebas acumuladas.
- 12 pruebas nuevas de análisis en `tests/AceriaApp.Decisiones.Tests`.
- Tipos `DecisionComunicacion`, `ValidadorDecisiones` y `CatalogoDecisiones` en `src/AceriaApp.Api/Decisiones`.
- Los catálogos no demuestran tráfico HTTP ni entrega de mensajes.

## Cómo ejecutarlo

1. Abre `AceriaApp.sln` en Visual Studio con soporte .NET 8.
2. Configura SQL Server Express o LocalDB y la conexión de pruebas `ACERIA_TEST_SQLSERVER`; conserva el helper `tests/Compartido/SqlServerPruebas.cs`.
3. Ejecuta `dotnet restore AceriaApp.sln` y `dotnet build AceriaApp.sln -c Release`.
4. Ejecuta `dotnet test AceriaApp.sln -c Release --no-build --no-restore` con los servicios requeridos por la integración funcional disponibles.
5. Sigue el manual M06 para iniciar los adaptadores y observar cada recorrido de comunicación.

## Qué se ha añadido respecto al punto anterior

El catálogo del punto, su proyecto de pruebas, `docs/cuando-usar-cada-enfoque.md` y el ADR-026. Los bloques funcionales de los pasos 5 a 15 completan la integración del punto. Se conservan los documentos y pruebas heredados.

## Documentación

- [Tema del punto](docs/cuando-usar-cada-enfoque.md).
- [ADR-026](docs/ADR-026-cuando-usar-cada-enfoque.md).
- Los 32 documentos anteriores, incluidos los ADR-010 a ADR-025, permanecen disponibles en `docs`.
