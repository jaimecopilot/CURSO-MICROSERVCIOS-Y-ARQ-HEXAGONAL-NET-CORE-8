# Punto 1.4 — Organización de una solución basada en microservicios

## Objetivo
Comprender cómo se organiza una solución basada en microservicios y añadir al proyecto las clases de validación de convenciones de nombres.

## Estado del proyecto
- Solución `AceriaApp.sln` con cinco proyectos: `AceriaApp.Monolito.Api`, `AceriaApp.Monolito.Tests`, `AceriaApp.Metricas.Tests`, `AceriaApp.Diseno.Tests` y `AceriaApp.Organizacion.Tests`.
- Documento `docs/organizacion-solucion.md` con las tres decisiones de organización y las convenciones.
- Clases `ConvencionNombres`, `ValidadorConvencionNombres` y `CatalogoProyectos` en `src/AceriaApp.Monolito.Api/Organizacion/`.
- Cinco tests nuevos en `tests/AceriaApp.Organizacion.Tests`.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio 2026.
2. Verificar que SQL Server Express está arrancado.
3. Ejecutar `dotnet ef database update` en `src\AceriaApp.Monolito.Api`.
4. Ejecutar `dotnet run` en `src\AceriaApp.Monolito.Api`.
5. Navegar a `/swagger` en el puerto indicado por la API.
6. Ejecutar `dotnet test AceriaApp.sln`.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/organizacion-solucion.md`.
- Carpeta `Organizacion` en el proyecto monolítico con tres clases nuevas.
- Proyecto `tests/AceriaApp.Organizacion.Tests` con cinco tests nuevos.
- No se ha modificado ningún archivo de código heredado del punto 1.3.

## Documentación
- [ADR-001](docs/ADR-001-monolito-vs-microservicios.md)
- [ADR-002](docs/ADR-002-metricas-acoplamiento.md)
- [ADR-003](docs/ADR-003-principios-diseno.md)
- [Análisis de ventajas e inconvenientes](docs/analisis-ventajas-inconvenientes.md)
- [Principios de diseño](docs/principios-diseno.md)
- [Organización de la solución](docs/organizacion-solucion.md)

## Código progresivo del punto 1.4

Esta solución hereda **completado** el código del punto anterior. Los archivos nuevos del punto 1.4 están comentados inicialmente para que los actives según los pasos de las prácticas. No se altera el código heredado.

- **Paso 1.4.9:** `src/AceriaApp.Monolito.Api/Organizacion/CatalogoProyectos.cs`
- **Paso 1.4.6:** `src/AceriaApp.Monolito.Api/Organizacion/ConvencionNombres.cs`
- **Paso 1.4.7:** `src/AceriaApp.Monolito.Api/Organizacion/ValidadorConvencionNombres.cs`
- **Paso 1.4.15:** `tests/AceriaApp.Organizacion.Tests/CatalogoProyectosTests.cs`
- **Paso 1.4.14:** `tests/AceriaApp.Organizacion.Tests/ValidadorConvencionNombresTests.cs`

En Visual Studio, abre cada archivo cuando lo indique la práctica, selecciona **exclusivamente las líneas del bloque comentado** entre `INICIO PASO` y `FIN PASO`, y pulsa `Ctrl+K, Ctrl+U`. Primero se activan las clases de producción y después sus pruebas. El código que se obtiene coincide con la solución completa utilizada en las verificaciones.
