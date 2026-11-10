# Punto 5.1 — Conceptos básicos de Domain-Driven Design

## Objetivo
Comprender los conceptos básicos de Domain-Driven Design y añadir al proyecto las clases de validación de contextos delimitados.

Construir la frontera y las transiciones del contexto Producción.

## Estado del proyecto
- Solución `AceriaApp.sln` con 16 proyectos.
- Documento `docs/conceptos-ddd.md` con la definición y los contextos.
- Clases `ContextoDelimitado`, `ValidadorContextos` y `CatalogoContextos` en `src/AceriaApp.Api/Ddd/`.
- 11 tests de catálogo y 5 funcionales nuevos en `tests/AceriaApp.Ddd.Tests`.
- Los tests acumulados suman 134 pruebas.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio con soporte de .NET 8.
2. Configurar SQL Server para los adaptadores heredados; las pruebas proporcionan su persistencia de prueba.
3. Configurar las conexiones `AceriaApp` y `AceriaHexagonal` en el entorno local si se ejecuta la API con SQL Server.
4. Ejecutar `dotnet run --project src/AceriaApp.Api/AceriaApp.Api.csproj --urls http://localhost:5000` desde la raíz de la etapa.
5. Navegar a `http://localhost:5000/swagger`.
6. Ejecutar `dotnet test AceriaApp.sln` para verificar los tests.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/conceptos-ddd.md`.
- Carpeta `Ddd` en el proyecto API con tres clases nuevas.
- Proyecto `tests/AceriaApp.Ddd.Tests` con 11 tests de catálogo y 5 funcionales nuevos.
- Se conserva intacta la carpeta del punto 4.5.

- Construir la frontera y las transiciones del contexto Producción. Los bloques completos están en el paso 16 del manual.

## Documentación
- [ADR-010](docs/ADR-010-capas-aplicacion.md) a [ADR-018](docs/ADR-018-inyeccion-dependencias.md) (heredados).
- [Conceptos básicos de DDD](docs/conceptos-ddd.md).

## Verificación ejecutable

El catálogo describe ejemplos de diseño y sus indicadores; no inspecciona automáticamente las clases reales. Los archivos funcionales del paso 16 y sus tests comprueban el comportamiento ejecutable. Ejecuta `dotnet test AceriaApp.sln -c Release` y exige cero fallos y cero omisiones.
