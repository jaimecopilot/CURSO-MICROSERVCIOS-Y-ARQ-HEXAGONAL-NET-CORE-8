# Punto 1.1 — Arquitectura monolítica vs. microservicios

## Objetivo
Comprender las diferencias entre monolito y microservicios y crear la estructura inicial del proyecto AceriaApp.

## Estado del proyecto
- Solución `AceriaApp.sln` con dos proyectos: `AceriaApp.Monolito.Api` y `AceriaApp.Monolito.Tests`.
- API Minimal con endpoints `GET /api/v1/ordenes` y `POST /api/v1/ordenes`.
- Persistencia con EF Core 8.0.0 y SQL Server Express (`AceriaDb`).
- Documentación OpenAPI con Swagger.
- Un test unitario de la entidad `Orden`.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio 2026.
2. Verificar que SQL Server Express está arrancado.
3. Ejecutar `dotnet ef database update` en `src\AceriaApp.Monolito.Api`.
4. Ejecutar `dotnet run` en `src\AceriaApp.Monolito.Api`.
5. Navegar a la URL `/swagger` en el puerto comunicado por el servidor.

## Qué se ha añadido respecto al punto anterior
Este es el primer punto del curso. No hay punto anterior.

## Documentación
- [ADR-001](docs/ADR-001-monolito-vs-microservicios.md)

## Código progresivo de este punto

El proyecto incluye el esqueleto ASP.NET Core de `Program.cs`. En los pasos **1.1.11**, **1.1.12** y **1.1.13**, descomenta los bloques identificados en `Orden.cs`, `AceriaDbContext.cs` y `Program.cs`, por ese orden. En el paso **1.1.17**, descomenta la prueba `OrdenTests.cs`. Compila en los puntos indicados de la práctica. El bloque de **RETO 1.1** de `Program.cs` permanece comentado hasta el reto.

Selecciona solo el bloque comentado de cada paso en Visual Studio y aplica `Ctrl+K, Ctrl+U`. Para `Program.cs`, no descomentes el bloque de reto al finalizar el paso 1.1.13.
