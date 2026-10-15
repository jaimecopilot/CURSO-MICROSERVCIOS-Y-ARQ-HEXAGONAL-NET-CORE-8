# Punto 1.3 — Principios de diseño

## Objetivo
Comprender los principios de diseño que guían la descomposición de un sistema en servicios autónomos y añadir al proyecto las clases de validación de límites de servicio.

## Estado del proyecto
- Solución `AceriaApp.sln` con cuatro proyectos: `AceriaApp.Monolito.Api`, `AceriaApp.Monolito.Tests`, `AceriaApp.Metricas.Tests` y `AceriaApp.Diseno.Tests`.
- Documento `docs/principios-diseno.md` con los ocho principios y su aplicación al proyecto.
- Clases `LimiteServicio`, `ValidadorLimiteServicio` y `CatalogoLimites` en `src/AceriaApp.Monolito.Api/Diseno/`.
- Cuatro tests nuevos en `tests/AceriaApp.Diseno.Tests`.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio 2026.
2. Verificar que SQL Server Express está arrancado.
3. Ejecutar `dotnet ef database update` en `src\AceriaApp.Monolito.Api`.
4. Ejecutar `dotnet run` en `src\AceriaApp.Monolito.Api`.
5. Navegar a `/swagger` en el puerto mostrado por la API.
6. Ejecutar `dotnet test AceriaApp.sln` para verificar los tests.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/principios-diseno.md`.
- Carpeta `Diseno` en el proyecto monolítico con tres clases nuevas.
- Proyecto `tests/AceriaApp.Diseno.Tests` con cuatro tests nuevos.
- No se ha modificado ningún archivo de código heredado del punto 1.2.

## Documentación
- [ADR-001](docs/ADR-001-monolito-vs-microservicios.md)
- [ADR-002](docs/ADR-002-metricas-acoplamiento.md)
- [Análisis de ventajas e inconvenientes](docs/analisis-ventajas-inconvenientes.md)
- [Principios de diseño](docs/principios-diseno.md)

## Código progresivo del punto 1.3

Esta solución contiene **activo** el código del punto anterior. Los archivos nuevos del punto 1.3 están comentados inicialmente para que los actives según los pasos de las prácticas. No se altera el código heredado.

- **Paso 1.3.9:** `src/AceriaApp.Monolito.Api/Diseno/CatalogoLimites.cs`
- **Paso 1.3.6:** `src/AceriaApp.Monolito.Api/Diseno/LimiteServicio.cs`
- **Paso 1.3.7:** `src/AceriaApp.Monolito.Api/Diseno/ValidadorLimiteServicio.cs`
- **Paso 1.3.15:** `tests/AceriaApp.Diseno.Tests/CatalogoLimitesTests.cs`
- **Paso 1.3.14:** `tests/AceriaApp.Diseno.Tests/ValidadorLimiteServicioTests.cs`

En Visual Studio, abre cada archivo cuando lo indique la práctica, selecciona **exclusivamente las líneas del bloque comentado** entre `INICIO PASO` y `FIN PASO`, y pulsa `Ctrl+K, Ctrl+U`. Primero se activan las clases de producción y después sus pruebas. Después de activar un paso, guarda el archivo y compila cuando lo indique la práctica. Evita descomentar bloques posteriores antes de llegar a ellos.
