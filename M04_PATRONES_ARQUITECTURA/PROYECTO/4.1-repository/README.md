# Punto 4.1 — Repository

## Objetivo
Comprender el patrón Repository y añadir al proyecto las clases de validación de repositorios.

La práctica conecta además el patrón con los puertos, adaptadores y pruebas de integración que aparecen en este manual.

## Estado del proyecto
- Solución `AceriaApp.sln` con 10 proyectos.
- Documento `docs/patron-repository.md` con las responsabilidades y las prohibiciones.
- Clases `Repositorio`, `ValidadorRepositorios` y `CatalogoRepositorios` en `src/AceriaApp.Api/Repository/`.
- 8 tests nuevos de catálogo y 4 funcionales en `tests/AceriaApp.Repository.Tests`.
- Los tests acumulados suman 62 pruebas: 8 de catálogo nuevas y 4 funcionales nuevas en este punto.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio 2026.
2. Verificar que SQL Server Express está arrancado.
3. Configurar las conexiones SQL Server `AceriaApp` y `AceriaHexagonal` en el entorno local.
4. Ejecutar `dotnet run --project src/AceriaApp.Api/AceriaApp.Api.csproj --urls http://localhost:5000` desde la raíz de esta etapa.
5. Navegar a `http://localhost:5000/swagger`.
6. Ejecutar `dotnet test AceriaApp.sln` para verificar los tests.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/patron-repository.md`.
- Carpeta `Repository` en el proyecto API con tres clases nuevas.
- Proyecto `tests/AceriaApp.Repository.Tests` con 8 tests de catálogo y 4 funcionales nuevos.
- Se conserva intacta la carpeta del punto 3.4.

## Documentación
- [ADR-010](docs/ADR-010-capas-aplicacion.md) a [ADR-013](docs/ADR-013-implementacion-aspnet-core.md) (heredados).
- [Patrón Repository](docs/patron-repository.md).

## Verificación ejecutable

Los catálogos describen ejemplos de diseño. El comportamiento de las clases reales se comprueba además con los tests funcionales del punto. Ejecuta `dotnet test AceriaApp.sln -c Release` y exige cero fallos y cero omisiones.
