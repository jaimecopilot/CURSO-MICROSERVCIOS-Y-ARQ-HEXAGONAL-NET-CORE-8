# Punto 3.3 — Carpeta del punto 3.3 a partir del punto 3.2

**Curso:** Microservicios y arquitectura hexagonal con ASP.NET Core 8  
**Código de referencia:** AceriaApp, en continuidad con M02 2.4.

## Objetivo

el documento de separación de capas es el artefacto de `docs` específico del punto 3.3. No modifica los quince documentos existentes del punto 3.2.

## Estado verificado del punto

- 8 proyectos en la solución `AceriaApp.sln` al finalizar este punto.
- 38 pruebas xUnit acumuladas previstas (incluyendo las 16 de M02 y las nuevas del módulo 3).
- Clases del catálogo `SeparacionCapas` en `src/AceriaApp.Api/SeparacionCapas`.
- Documentación `docs/separacion-capas.md` y decisión `docs/ADR-012-separacion-capas.md`.
- Los endpoints REST del módulo 2 se conservan sin cambios funcionales.

## Cómo ejecutarlo

1. Abrir el archivo `AceriaApp.sln` de esta carpeta en Visual Studio, con SDK .NET 8.
2. Ejecutar `dotnet restore AceriaApp.sln` y después `dotnet build AceriaApp.sln -c Release`.
3. Ejecutar `dotnet test AceriaApp.sln -c Release --no-build`. La suite M03 se construye por adición desde M02.
4. La aplicación principal utiliza SQL Server Express LocalDB; los tests HTTP mantienen SQL Server y crean bases exclusivas independientes mediante `BaseSqlServer.Crear()`.
5. En 3.4, los endpoints hexagonales reales están en `/api/v1/hexagonal/ordenes` y utilizan un repositorio EF Core a través de un puerto de aplicación.

## Qué se ha añadido

la clase `Proyecto` modela un proyecto con su nombre, capa y lista de referencias. Es la unidad de información del validador de separación.
