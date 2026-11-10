# Punto 4.4 — Result Pattern

## Objetivo
Comprender el patrón Result y añadir al proyecto las clases de validación de resultados.

La práctica conecta además el patrón con los puertos, adaptadores y pruebas de integración que aparecen en este manual.

## Estado del proyecto
- Solución `AceriaApp.sln` con 13 proyectos.
- Documento `docs/patron-result.md` con la definición y las reglas.
- Clases `Result<T>`, `ResultadoOperacion`, `ValidadorResultados` y `CatalogoResultados` en `src/AceriaApp.Api/ResultPattern/`.
- 8 tests nuevos de catálogo y 7 funcionales en `tests/AceriaApp.ResultPattern.Tests`.
- Los tests acumulados suman 105 pruebas: 8 de catálogo nuevas y 7 funcionales nuevas en este punto.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio 2026.
2. Verificar que SQL Server Express está arrancado.
3. Configurar las conexiones SQL Server `AceriaApp` y `AceriaHexagonal` en el entorno local.
4. Ejecutar `dotnet run --project src/AceriaApp.Api/AceriaApp.Api.csproj --urls http://localhost:5000` desde la raíz de esta etapa.
5. Navegar a `http://localhost:5000/swagger`.
6. Ejecutar `dotnet test AceriaApp.sln` para verificar los tests.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/patron-result.md`.
- Carpeta `ResultPattern` en el proyecto API con cuatro clases nuevas.
- Proyecto `tests/AceriaApp.ResultPattern.Tests` con 8 tests de catálogo y 7 funcionales nuevos.
- Se conserva intacta la carpeta del punto 4.3.

## Documentación
- [ADR-010](docs/ADR-010-capas-aplicacion.md) a [ADR-016](docs/ADR-016-patron-mediator.md) (heredados).
- [Patrón Result](docs/patron-result.md).

## Verificación ejecutable

Los catálogos describen ejemplos de diseño. El comportamiento de las clases reales se comprueba además con los tests funcionales del punto. Ejecuta `dotnet test AceriaApp.sln -c Release` y exige cero fallos y cero omisiones.
