# Punto 4.3 — Mediator (MediatR)

## Objetivo
Comprender el patrón Mediator y añadir al proyecto las clases de validación de mensajes MediatR.

La práctica conecta además el patrón con los puertos, adaptadores y pruebas de integración que aparecen en este manual.

## Estado del proyecto
- Solución `AceriaApp.sln` con 12 proyectos.
- Documento `docs/patron-mediator.md` con las definiciones y las reglas.
- Clases `Mensaje`, `ValidadorMensajes` y `CatalogoMensajes` en `src/AceriaApp.Api/Mediator/`.
- 10 tests nuevos de catálogo y 3 funcionales en `tests/AceriaApp.Mediator.Tests`.
- Los tests acumulados suman 90 pruebas: 10 de catálogo nuevas y 3 funcionales nuevas en este punto.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio 2026.
2. Verificar que SQL Server Express está arrancado.
3. Configurar las conexiones SQL Server `AceriaApp` y `AceriaHexagonal` en el entorno local.
4. Ejecutar `dotnet run --project src/AceriaApp.Api/AceriaApp.Api.csproj --urls http://localhost:5000` desde la raíz de esta etapa.
5. Navegar a `http://localhost:5000/swagger`.
6. Ejecutar `dotnet test AceriaApp.sln` para verificar los tests.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/patron-mediator.md`.
- Carpeta `Mediator` en el proyecto API con tres clases nuevas.
- Proyecto `tests/AceriaApp.Mediator.Tests` con 10 tests de catálogo y 3 funcionales nuevos.
- Se conserva intacta la carpeta del punto 4.2.

## Documentación
- [ADR-010](docs/ADR-010-capas-aplicacion.md) a [ADR-015](docs/ADR-015-patron-unit-of-work.md) (heredados).
- [Patrón Mediator](docs/patron-mediator.md).

## Verificación ejecutable

Los catálogos describen ejemplos de diseño. El comportamiento de las clases reales se comprueba además con los tests funcionales del punto. Ejecuta `dotnet test AceriaApp.sln -c Release` y exige cero fallos y cero omisiones.
