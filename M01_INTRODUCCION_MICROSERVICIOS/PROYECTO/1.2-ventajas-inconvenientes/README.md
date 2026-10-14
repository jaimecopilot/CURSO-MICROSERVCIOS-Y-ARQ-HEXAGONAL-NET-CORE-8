# Punto 1.2 — Ventajas e inconvenientes

## Objetivo
Analizar las ventajas e inconvenientes de monolito y microservicios con un marco explícito de cuatro dimensiones y añadir al proyecto las métricas de acoplamiento.

## Estado del proyecto
- Solución `AceriaApp.sln` con tres proyectos: `AceriaApp.Monolito.Api`, `AceriaApp.Monolito.Tests` y `AceriaApp.Metricas.Tests`.
- Documento `docs/analisis-ventajas-inconvenientes.md` con el análisis comparativo.
- Clases `MetricasAcoplamiento`, `MetricasServicio` y `AnalizadorMonolito` en `src/AceriaApp.Monolito.Api/Metricas/`.
- Ocho tests nuevos en `tests/AceriaApp.Metricas.Tests`.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio 2026.
2. Verificar que SQL Server Express está arrancado.
3. Ejecutar `dotnet ef database update` en `src\AceriaApp.Monolito.Api`.
4. Ejecutar `dotnet run` en `src\AceriaApp.Monolito.Api`.
5. Navegar a la URL `/swagger` en el puerto comunicado por el servidor.
6. Ejecutar `dotnet test AceriaApp.sln` para verificar los tests.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/analisis-ventajas-inconvenientes.md`.
- Carpeta `Metricas` en el proyecto monolítico con tres clases nuevas.
- Proyecto `tests/AceriaApp.Metricas.Tests` con ocho tests nuevos.
- Los archivos de código heredados del punto 1.1 no se han modificado.

## Documentación
- [ADR-001](docs/ADR-001-monolito-vs-microservicios.md)
- [Análisis de ventajas e inconvenientes](docs/analisis-ventajas-inconvenientes.md)

## Código progresivo del punto 1.2

Esta solución hereda **completado** el código del punto anterior. Los archivos nuevos del punto 1.2 están comentados inicialmente para que los actives según los pasos de las prácticas. No se altera el código heredado.

- **Paso 1.2.8:** `src/AceriaApp.Monolito.Api/Metricas/AnalizadorMonolito.cs`
- **Paso 1.2.6:** `src/AceriaApp.Monolito.Api/Metricas/MetricasAcoplamiento.cs`
- **Paso 1.2.7:** `src/AceriaApp.Monolito.Api/Metricas/MetricasServicio.cs`
- **Paso 1.2.15:** `tests/AceriaApp.Metricas.Tests/AnalizadorMonolitoTests.cs`
- **Paso 1.2.13:** `tests/AceriaApp.Metricas.Tests/MetricasAcoplamientoTests.cs`
- **Paso 1.2.14:** `tests/AceriaApp.Metricas.Tests/MetricasServicioTests.cs`

En Visual Studio, abre cada archivo cuando lo indique la práctica, selecciona **exclusivamente las líneas del bloque comentado** entre `INICIO PASO` y `FIN PASO`, y pulsa `Ctrl+K, Ctrl+U`. Primero se activan las clases de producción y después sus pruebas. El código que se obtiene coincide con la solución completa utilizada en las verificaciones.
