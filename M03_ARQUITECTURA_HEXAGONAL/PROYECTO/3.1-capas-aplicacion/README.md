# Punto 3.1 — Estructura del módulo 3 y del punto 3.1

**Curso:** Microservicios y arquitectura hexagonal con ASP.NET Core 8  
**Código de referencia:** AceriaApp, en continuidad con M02 2.4.

## Objetivo

el documento de capas de la aplicación es el artefacto de `docs` específico del punto 3.1. No modifica los trece documentos existentes del punto 2.4.

## Estado verificado del punto

- 3 proyectos en la solución `AceriaApp.sln` al finalizar este punto; la fuente histórica contaba otros proyectos que no existen en el repositorio actual.
- 23 pruebas xUnit acumuladas previstas (incluyendo las 16 de M02 y las nuevas del módulo 3).
- Clases del catálogo `Capas` en `src/AceriaApp.Api/Capas`.
- Documentación `docs/capas-aplicacion.md` y decisión `docs/ADR-010-capas-aplicacion.md`.
- Los endpoints REST del módulo 2 se conservan sin cambios funcionales.

## Cómo ejecutarlo

1. Abrir el archivo `AceriaApp.sln` de esta carpeta en Visual Studio, con SDK .NET 8.
2. Ejecutar `dotnet restore AceriaApp.sln` y después `dotnet build AceriaApp.sln -c Release`.
3. Ejecutar `dotnet test AceriaApp.sln -c Release --no-build`. La suite M03 se construye por adición desde M02.
4. La aplicación principal utiliza SQL Server Express LocalDB; los tests HTTP conectan proveedores InMemory independientes.
5. En 3.4, los endpoints hexagonales reales están en `/api/v1/hexagonal/ordenes` y utilizan un repositorio EF Core a través de un puerto de aplicación.

## Qué se ha añadido

la clase `Capa` modela una capa con su nombre y las capas de las que puede depender. Es la unidad de información del validador de la regla de dependencia.

## Nota de trazabilidad

El laboratorio `../../PRACTICAS/M03_PRACTICAS.md` es la fuente ejecutable de las incorporaciones. La copia íntegra histórica está en `../../FUENTE/M03_3.1_ORIGINAL.md`.
