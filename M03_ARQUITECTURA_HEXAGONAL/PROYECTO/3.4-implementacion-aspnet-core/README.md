# Punto 3.4 — Carpeta del punto 3.4 a partir del punto 3.3

**Curso:** Microservicios y arquitectura hexagonal con ASP.NET Core 8  
**Código de referencia:** AceriaApp, en continuidad con M02 2.4.

## Objetivo

el documento de implementación en ASP.NET Core es el artefacto de `docs` específico del punto 3.4. Incluye el cierre del módulo 3 con el resumen del estado del proyecto. No modifica los dieciséis documentos existentes del punto 3.3.

## Estado verificado del punto

- 9 proyectos en la solución `AceriaApp.sln` al finalizar este punto.
- 50 pruebas xUnit acumuladas previstas (incluyendo las 16 de M02 y las nuevas del módulo 3).
- Clases del catálogo `Implementacion` en `src/AceriaApp.Api/Implementacion`.
- Documentación `docs/implementacion-aspnet-core.md` y decisión `docs/ADR-013-implementacion-aspnet-core.md`.
- Los endpoints REST del módulo 2 se conservan sin cambios funcionales.

## Cómo ejecutarlo

1. Abrir el archivo `AceriaApp.sln` de esta carpeta en Visual Studio, con SDK .NET 8.
2. Ejecutar `dotnet restore AceriaApp.sln` y después `dotnet build AceriaApp.sln -c Release`.
3. Ejecutar `dotnet test AceriaApp.sln -c Release --no-build`. La suite M03 se construye por adición desde M02.
4. La aplicación principal utiliza SQL Server Express LocalDB; los tests HTTP mantienen SQL Server y crean bases exclusivas independientes mediante `BaseSqlServer.Crear()`.
5. En 3.4, los endpoints hexagonales reales están en `/api/v1/hexagonal/ordenes` y utilizan un repositorio EF Core a través de un puerto de aplicación.

## Qué se ha añadido

la clase `RegistroServicio` modela un registro del contenedor de dependencias con el puerto, la implementación, el ciclo y si es adaptador de salida. Es la unidad de información del validador.
