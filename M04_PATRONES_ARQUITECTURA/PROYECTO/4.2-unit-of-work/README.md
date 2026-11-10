# Punto 4.2 — Unit of Work

## Objetivo
Comprender el patrón Unit of Work y añadir al proyecto las clases de validación de unidades de trabajo.

La práctica conecta además el patrón con los puertos, adaptadores y pruebas de integración que aparecen en este manual.

## Estado del proyecto
- Solución `AceriaApp.sln` con 11 proyectos.
- Documento `docs/patron-unit-of-work.md` con las responsabilidades y las prohibiciones.
- Clases `UnidadDeTrabajo`, `ValidadorUnidadesDeTrabajo` y `CatalogoUnidadesDeTrabajo` en `src/AceriaApp.Api/UnitOfWork/`.
- 11 tests nuevos de catálogo y 4 funcionales en `tests/AceriaApp.UnitOfWork.Tests`.
- Los tests acumulados suman 77 pruebas: 11 de catálogo nuevas y 4 funcionales nuevas en este punto.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio 2026.
2. Verificar que SQL Server Express está arrancado.
3. Configurar las conexiones SQL Server `AceriaApp` y `AceriaHexagonal` en el entorno local.
4. Ejecutar `dotnet run --project src/AceriaApp.Api/AceriaApp.Api.csproj --urls http://localhost:5000` desde la raíz de esta etapa.
5. Navegar a `http://localhost:5000/swagger`.
6. Ejecutar `dotnet test AceriaApp.sln` para verificar los tests.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/patron-unit-of-work.md`.
- Carpeta `UnitOfWork` en el proyecto API con tres clases nuevas.
- Proyecto `tests/AceriaApp.UnitOfWork.Tests` con 11 tests de catálogo y 4 funcionales nuevos.
- Se conserva intacta la carpeta del punto 4.1.

## Documentación
- [ADR-010](docs/ADR-010-capas-aplicacion.md) a [ADR-014](docs/ADR-014-patron-repository.md) (heredados).
- [Patrón Unit of Work](docs/patron-unit-of-work.md).

## Verificación ejecutable

Los catálogos describen ejemplos de diseño. El comportamiento de las clases reales se comprueba además con los tests funcionales del punto. Ejecuta `dotnet test AceriaApp.sln -c Release` y exige cero fallos y cero omisiones.
