# Curso Arquitectura Hexagonal y Microservicios Avanzados

Curso teórico-práctico de **30 horas** dirigido a desarrolladores .NET con conocimientos de C# y ASP.NET Core.

## Objetivos

- Comprender los fundamentos de una arquitectura basada en microservicios y su aplicación en entornos empresariales.
- Diseñar e implementar microservicios utilizando ASP.NET Core y Arquitectura Hexagonal.
- Aplicar patrones de diseño y arquitectura como Repository, Unit of Work, Mediator y CQRS para desarrollar aplicaciones desacopladas y mantenibles.
- Implementar mecanismos básicos de comunicación entre servicios, resiliencia y publicación mediante un API Gateway.

## Temario

1. Introducción a los microservicios.
2. Desarrollo de APIs REST con ASP.NET Core.
3. Arquitectura Hexagonal.
4. Patrones de arquitectura.
5. Introducción a DDD y CQRS.
6. Comunicación entre microservicios.
7. Observabilidad y resiliencia.
8. Publicación mediante API Gateway.

## Organización del repositorio

Cada módulo se organiza en las carpetas `TEORIA/`, `PRACTICAS/` y `PROYECTO/`. Las carpetas docentes se incorporan con sus respectivos Markdown y PDF; los proyectos son estados reproducibles de AceriaApp por punto del temario.

### Módulo 1

- [Proyecto AceriaApp — puntos 1.1 a 1.5](M01_INTRODUCCION_MICROSERVICIOS/PROYECTO/)
- Cada punto conserva `AceriaApp.sln`, `src/`, `tests/` y `docs/`.
- Referencia de código: .NET 8, EF Core 8, SQL Server Express y xUnit.
- Los retos de cada punto están identificados mediante comentarios para descomentarlos.

### Módulo 2 — Desarrollo de APIs REST con ASP.NET Core

- [Teoría del módulo 2](M02_APIS_REST_ASPNET_CORE/TEORIA/M02_TEORIA.md) · [PDF](M02_APIS_REST_ASPNET_CORE/TEORIA/M02_TEORIA.pdf)
- [Prácticas guiadas del módulo 2](M02_APIS_REST_ASPNET_CORE/PRACTICAS/M02_PRACTICAS.md) · [PDF](M02_APIS_REST_ASPNET_CORE/PRACTICAS/M02_PRACTICAS.pdf)
- [Cuatro proyectos Minimal API progresivos (2.1–2.4)](M02_APIS_REST_ASPNET_CORE/PROYECTO/), .NET 8, EF Core 8 y SQL Server Express LocalDB.
