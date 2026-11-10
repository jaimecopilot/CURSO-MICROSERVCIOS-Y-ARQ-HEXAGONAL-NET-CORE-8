# Punto 5.2 — Entidades y Value Objects

## Objetivo
Comprender las entidades y los value objects como elementos tácticos del modelo del dominio y añadir al proyecto las clases de validación del modelo.

Añadir valores inmutables, identidad y líneas encapsuladas al agregado de Producción.

## Estado del proyecto
- Solución `AceriaApp.sln` con 17 proyectos.
- Documento `docs/entidades-value-objects.md` con la definición y las reglas.
- Clases `ElementoModelo`, `ValidadorModeloDominio` y `CatalogoModelo` en `src/AceriaApp.Api/ModeloDominio/`.
- 12 tests de catálogo y 7 funcionales nuevos en `tests/AceriaApp.ModeloDominio.Tests`.
- Los tests acumulados suman 153 pruebas.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio con soporte de .NET 8.
2. Configurar SQL Server para los adaptadores heredados; las pruebas proporcionan su persistencia de prueba.
3. Configurar las conexiones `AceriaApp` y `AceriaHexagonal` en el entorno local si se ejecuta la API con SQL Server.
4. Ejecutar `dotnet run --project src/AceriaApp.Api/AceriaApp.Api.csproj --urls http://localhost:5000` desde la raíz de la etapa.
5. Navegar a `http://localhost:5000/swagger`.
6. Ejecutar `dotnet test AceriaApp.sln` para verificar los tests.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/entidades-value-objects.md`.
- Carpeta `ModeloDominio` en el proyecto API con tres clases nuevas.
- Proyecto `tests/AceriaApp.ModeloDominio.Tests` con 12 tests de catálogo y 7 funcionales nuevos.
- Se conserva intacta la carpeta del punto 5.1.

- Añadir valores inmutables, identidad y líneas encapsuladas al agregado de Producción. Los bloques completos están en el paso 16 del manual.

## Documentación
- [ADR-010](docs/ADR-010-capas-aplicacion.md) a [ADR-019](docs/ADR-019-conceptos-ddd.md) (heredados).
- [Entidades y Value Objects](docs/entidades-value-objects.md).

## Verificación ejecutable

El catálogo describe ejemplos de diseño y sus indicadores; no inspecciona automáticamente las clases reales. Los archivos funcionales del paso 16 y sus tests comprueban el comportamiento ejecutable. Ejecuta `dotnet test AceriaApp.sln -c Release` y exige cero fallos y cero omisiones.
