# Punto 5.4 — Separación entre Commands y Queries

## Objetivo
Comprender el patrón CQRS y añadir al proyecto las clases de validación de la separación entre comandos y consultas.

Despachar comandos y consultas con MediatR y devolver proyecciones DTO sin seguimiento.

## Estado del proyecto
- Solución `AceriaApp.sln` con 21 proyectos.
- Documento `docs/commands-queries.md` con la definición y las reglas.
- Clases `MensajeCqrs`, `ValidadorCqrs` y `CatalogoCqrs` en `src/AceriaApp.Api/Cqrs/`.
- 12 tests de catálogo y 6 funcionales nuevos en `tests/AceriaApp.Cqrs.Tests`.
- Los tests acumulados suman 190 pruebas.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio con soporte de .NET 8.
2. Configurar SQL Server para los adaptadores heredados; las pruebas proporcionan su persistencia de prueba.
3. Configurar las conexiones `AceriaApp`, `AceriaHexagonal` y `AceriaProduccion` en el entorno local si se ejecuta la API con SQL Server.
4. Ejecutar `dotnet run --project src/AceriaApp.Api/AceriaApp.Api.csproj --urls http://localhost:5000` desde la raíz de la etapa.
5. Navegar a `http://localhost:5000/swagger`.
6. Ejecutar `dotnet test AceriaApp.sln` para verificar los tests.

El perfil de lanzamiento heredado activa `Development`. En ese entorno, si `SkipDatabaseInitialization` es falso, la API inicializa la base de Producción mediante `EnsureCreatedAsync`; no requiere datos iniciales. Configura `ConnectionStrings:AceriaProduccion` para tu SQL Server antes del arranque.

Para probar el nuevo flujo, envía `POST /api/v1/produccion/ordenes` con `{"cliente":"Axia","material":"Acero","cantidad":200}`, sigue su cabecera `Location` y envía los comandos `POST /{id}/planificar` y `POST /{id}/finalizar` bajo la ruta de órdenes.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/commands-queries.md`.
- Carpeta `Cqrs` en el proyecto API con tres clases nuevas.
- Proyecto `tests/AceriaApp.Cqrs.Tests` con 12 tests de catálogo y 6 funcionales nuevos.
- Se conserva intacta la carpeta del punto 5.3.

- Despachar comandos y consultas con MediatR y devolver proyecciones DTO sin seguimiento. Los bloques completos están en el paso 16 del manual.

## Documentación
- [ADR-010](docs/ADR-010-capas-aplicacion.md) a [ADR-021](docs/ADR-021-casos-uso.md) (heredados).
- [Separación entre Commands y Queries](docs/commands-queries.md).

## Verificación ejecutable

El catálogo describe ejemplos de diseño y sus indicadores; no inspecciona automáticamente las clases reales. Los archivos funcionales del paso 16 y sus tests comprueban el comportamiento ejecutable. Ejecuta `dotnet test AceriaApp.sln -c Release` y exige cero fallos y cero omisiones.
