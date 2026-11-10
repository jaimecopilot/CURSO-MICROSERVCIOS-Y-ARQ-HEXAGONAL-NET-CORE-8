# Punto 5.3 — Casos de uso

## Objetivo
Comprender los casos de uso como expresión de las operaciones del dominio y añadir al proyecto las clases de validación de casos de uso.

Conectar los casos de uso de Producción con sus puertos, persistencia y API.

## Estado del proyecto
- Solución `AceriaApp.sln` con 20 proyectos.
- Documento `docs/casos-uso.md` con la definición y las reglas.
- Clases `CasoDeUso`, `ValidadorCasosDeUso` y `CatalogoCasosDeUso` en `src/AceriaApp.Api/CasosDeUso/`.
- 12 tests de catálogo y 7 funcionales nuevos en `tests/AceriaApp.CasosDeUso.Tests`.
- Los tests acumulados suman 172 pruebas.

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
- Documento `docs/casos-uso.md`.
- Carpeta `CasosDeUso` en el proyecto API con tres clases nuevas.
- Proyecto `tests/AceriaApp.CasosDeUso.Tests` con 12 tests de catálogo y 7 funcionales nuevos.
- Se conserva intacta la carpeta del punto 5.2.

- Conectar los casos de uso de Producción con sus puertos, persistencia y API. Los bloques completos están en el paso 16 del manual.

## Documentación
- [ADR-010](docs/ADR-010-capas-aplicacion.md) a [ADR-020](docs/ADR-020-entidades-value-objects.md) (heredados).
- [Casos de uso](docs/casos-uso.md).

## Verificación ejecutable

El catálogo describe ejemplos de diseño y sus indicadores; no inspecciona automáticamente las clases reales. Los archivos funcionales del paso 16 y sus tests comprueban el comportamiento ejecutable. Ejecuta `dotnet test AceriaApp.sln -c Release` y exige cero fallos y cero omisiones.
