# AceriaApp — Curso de Microservicios con .NET 8

Repositorio del curso formativo de 30 horas sobre microservicios con .NET 8, organizado en 8 módulos y 34 puntos.

## Estructura del repositorio

- `modulo-1-introduccion-microservicios/`: 5 puntos (1.1 a 1.5).
- `modulo-2-apis-rest-aspnet-core/`: 4 puntos (2.1 a 2.4).
- `modulo-3-arquitectura-hexagonal/`: 4 puntos (3.1 a 3.4).
- `modulo-4-patrones-arquitectura/`: 5 puntos (4.1 a 4.5).
- `modulo-5-ddd-cqrs/`: 5 puntos (5.1 a 5.5).
- `modulo-6-comunicacion-microservicios/`: 3 puntos (6.1 a 6.3).
- `modulo-7-observabilidad-resiliencia/`: 4 puntos (7.1 a 7.4).
- `modulo-8-api-gateway/`: 4 puntos (8.1 a 8.4).

Cada punto contiene:

- `README.md`: objetivo del punto, estado del proyecto, cómo ejecutarlo y qué se ha añadido respecto al punto anterior.
- `AceriaApp.sln`: solución completa con todos los proyectos generados hasta ese punto.
- `src/`: código fuente de todos los proyectos.
- `tests/`: tests generados hasta ese punto.
- `docs/`: ADRs, diagramas UML y documentación generada.

## Requisitos

- .NET 8 SDK (LTS).
- Visual Studio 2026 Community.
- SQL Server Express.
- Docker Desktop (para tests de integración con Testcontainers).

## Cadena de conexión

`Server=.\SQLEXPRESS;Database=AceriaDb;Trusted_Connection=True;TrustServerCertificate=True`

## Cómo ejecutar cualquier punto

1. Abrir la carpeta del punto en Visual Studio 2026.
2. Abrir `AceriaApp.sln`.
3. Verificar que SQL Server Express está arrancado.
4. Ejecutar `dotnet ef database update` en el proyecto de API correspondiente.
5. Ejecutar `dotnet run` en el proyecto de API.
6. Navegar a la URL de Swagger que indique la salida de `dotnet run`.