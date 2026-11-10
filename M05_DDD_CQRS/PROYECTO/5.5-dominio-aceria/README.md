# Punto 5.5 — Aplicación al dominio de la acería

## Objetivo
Aplicar los conceptos de DDD y CQRS al dominio de la acería y añadir al proyecto las clases de validación del modelo del dominio. Cerrar el módulo 5 con el resumen del estado del proyecto.

Completar por HTTP el flujo de órdenes y la incorporación de líneas con sus invariantes.

## Estado del proyecto
- Solución `AceriaApp.sln` con 22 proyectos.
- Documento `docs/aplicacion-dominio-aceria.md` con los contextos, los agregados y el cierre del módulo 5.
- Clases `ElementoAceria`, `ValidadorDominioAceria` y `CatalogoAceria` en `src/AceriaApp.Api/DominioAceria/`.
- 10 tests de catálogo y 8 funcionales nuevos en `tests/AceriaApp.DominioAceria.Tests`.
- Los tests acumulados suman 208 pruebas.

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
- Documento `docs/aplicacion-dominio-aceria.md`.
- Carpeta `DominioAceria` en el proyecto API con tres clases nuevas.
- Proyecto `tests/AceriaApp.DominioAceria.Tests` con 10 tests de catálogo y 8 funcionales nuevos.
- Cierre del módulo 5 con el resumen del estado del proyecto.
- Se conserva intacta la carpeta del punto 5.4.

- Completar por HTTP el flujo de órdenes y la incorporación de líneas con sus invariantes. Los bloques completos están en el paso 16 del manual.

Mientras la orden siga en Borrador, `POST /api/v1/produccion/ordenes/{id}/lineas` con `{"material":"Acero inoxidable","cantidad":100}` añade una línea antes de planificar.

## Documentación
- [ADR-010](docs/ADR-010-capas-aplicacion.md) a [ADR-022](docs/ADR-022-commands-queries.md) (heredados).
- [Aplicación al dominio de la acería](docs/aplicacion-dominio-aceria.md).

## Verificación ejecutable

El catálogo describe ejemplos de diseño y sus indicadores; no inspecciona automáticamente las clases reales. Los archivos funcionales del paso 16 y sus tests comprueban el comportamiento ejecutable. Ejecuta `dotnet test AceriaApp.sln -c Release` y exige cero fallos y cero omisiones.
