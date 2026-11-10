# Punto 4.5 — Inyección de dependencias

## Objetivo
Comprender la inyección de dependencias y añadir al proyecto las clases de validación de registros del contenedor. Cerrar el módulo 4 con el resumen del estado del proyecto.

La práctica conecta además el patrón con los puertos, adaptadores y pruebas de integración que aparecen en este manual.

## Estado del proyecto
- Solución `AceriaApp.sln` con 14 proyectos.
- Documento `docs/inyeccion-dependencias.md` con las reglas y el cierre del módulo 4.
- Clases `RegistroInyeccion`, `ValidadorInyeccionDependencias` y `CatalogoInyeccion` en `src/AceriaApp.Api/InyeccionDependencias/`.
- 10 tests nuevos de catálogo y 3 funcionales en `tests/AceriaApp.InyeccionDependencias.Tests`.
- Los tests acumulados suman 118 pruebas: 10 de catálogo nuevas y 3 funcionales nuevas en este punto.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio 2026.
2. Verificar que SQL Server Express está arrancado.
3. Configurar las conexiones SQL Server `AceriaApp` y `AceriaHexagonal` en el entorno local.
4. Ejecutar `dotnet run --project src/AceriaApp.Api/AceriaApp.Api.csproj --urls http://localhost:5000` desde la raíz de esta etapa.
5. Navegar a `http://localhost:5000/swagger`.
6. Ejecutar `dotnet test AceriaApp.sln` para verificar los tests.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/inyeccion-dependencias.md`.
- Carpeta `InyeccionDependencias` en el proyecto API con tres clases nuevas.
- Proyecto `tests/AceriaApp.InyeccionDependencias.Tests` con 10 tests de catálogo y 3 funcionales nuevos.
- Cierre del módulo 4 con el resumen del estado del proyecto.
- Se conserva intacta la carpeta del punto 4.4.

## Documentación
- [ADR-010](docs/ADR-010-capas-aplicacion.md) a [ADR-017](docs/ADR-017-patron-result.md) (heredados).
- [Inyección de dependencias](docs/inyeccion-dependencias.md).

## Verificación ejecutable

Los catálogos describen ejemplos de diseño. El comportamiento de las clases reales se comprueba además con los tests funcionales del punto. Ejecuta `dotnet test AceriaApp.sln -c Release` y exige cero fallos y cero omisiones.
