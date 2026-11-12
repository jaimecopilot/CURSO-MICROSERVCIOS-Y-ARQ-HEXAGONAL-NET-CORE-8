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

### Módulo 3 — Arquitectura hexagonal

- [Teoría](M03_ARQUITECTURA_HEXAGONAL/TEORIA/M03_TEORIA.md) · [PDF](M03_ARQUITECTURA_HEXAGONAL/TEORIA/M03_TEORIA.pdf).
- [Prácticas guiadas](M03_ARQUITECTURA_HEXAGONAL/PRACTICAS/M03_PRACTICAS.md) · [PDF](M03_ARQUITECTURA_HEXAGONAL/PRACTICAS/M03_PRACTICAS.pdf).
- [Proyectos y validación](M03_ARQUITECTURA_HEXAGONAL/README.md): cuatro etapas progresivas, 3.1–3.4.

### Módulo 4 — Patrones de arquitectura

- [Teoría](M04_PATRONES_ARQUITECTURA/TEORIA/M04_TEORIA.md) · [PDF](M04_PATRONES_ARQUITECTURA/TEORIA/M04_TEORIA.pdf).
- [Prácticas guiadas](M04_PATRONES_ARQUITECTURA/PRACTICAS/M04_PRACTICAS.md) · [PDF](M04_PATRONES_ARQUITECTURA/PRACTICAS/M04_PRACTICAS.pdf).
- [Proyectos y validación](M04_PATRONES_ARQUITECTURA/README.md): cinco etapas progresivas, 4.1–4.5.

### Módulo 5 — Introducción a DDD y CQRS

- [Teoría](M05_DDD_CQRS/TEORIA/M05_TEORIA.md) · [PDF](M05_DDD_CQRS/TEORIA/M05_TEORIA.pdf).
- [Prácticas guiadas](M05_DDD_CQRS/PRACTICAS/M05_PRACTICAS.md) · [PDF](M05_DDD_CQRS/PRACTICAS/M05_PRACTICAS.pdf).
- [Proyectos y validación](M05_DDD_CQRS/README.md): cinco etapas progresivas, 5.1–5.5.

### Módulo 6 — Comunicación entre microservicios

- [Teoría](M06_COMUNICACION_MICROSERVICIOS/TEORIA/M06_TEORIA.md) · [PDF](M06_COMUNICACION_MICROSERVICIOS/TEORIA/M06_TEORIA.pdf).
- [Prácticas guiadas](M06_COMUNICACION_MICROSERVICIOS/PRACTICAS/M06_PRACTICAS.md) · [PDF](M06_COMUNICACION_MICROSERVICIOS/PRACTICAS/M06_PRACTICAS.pdf).
- [Proyectos y validación](M06_COMUNICACION_MICROSERVICIOS/README.md): tres etapas progresivas, 6.1–6.3, con HTTP real, RabbitMQ y outbox/inbox SQL Server.

### Módulo 7 — Observabilidad y resiliencia

- [Teoría](M07_OBSERVABILIDAD_RESILIENCIA/TEORIA/M07_TEORIA.md) · [PDF](M07_OBSERVABILIDAD_RESILIENCIA/TEORIA/M07_TEORIA.pdf).
- [Prácticas guiadas](M07_OBSERVABILIDAD_RESILIENCIA/PRACTICAS/M07_PRACTICAS.md) · [PDF](M07_OBSERVABILIDAD_RESILIENCIA/PRACTICAS/M07_PRACTICAS.pdf).
- [Proyectos y validación](M07_OBSERVABILIDAD_RESILIENCIA/README.md): cuatro etapas progresivas, 7.1–7.4, con correlación JSON, salud SQL/AMQP, ProblemDetails y resiliencia HTTP mediante Polly v8.

### Módulo 8 — Publicación mediante API Gateway

- [Teoría](M08_API_GATEWAY/TEORIA/M08_TEORIA.md) · [PDF](M08_API_GATEWAY/TEORIA/M08_TEORIA.pdf).
- [Prácticas guiadas](M08_API_GATEWAY/PRACTICAS/M08_PRACTICAS.md) · [PDF](M08_API_GATEWAY/PRACTICAS/M08_PRACTICAS.pdf): 96 pasos, 145 páginas revisadas y cuatro retos optativos.
- [Proyectos y validación](M08_API_GATEWAY/README.md): cuatro etapas 8.1–8.4, gateway independiente con YARP, enrutamiento, transformaciones, balanceo, salud y recuperación de destinos, con SQL Server Express y RabbitMQ reales.
- [Informe de cierre automatizado](M08_API_GATEWAY/CIERRE_AUTOMATIZADO.md) y [revisión editorial](M08_API_GATEWAY/REVISION_EDITORIAL_M08.md). La publicación definitiva se verifica mediante la automatización correspondiente al commit de `main`.
