# Módulo 2 — Desarrollo de APIs REST con ASP.NET Core 8

**Autor: JAIME GALLO**

El módulo desarrolla una **Minimal API real de AceriaApp** desde el diseño del contrato REST hasta la validación y documentación de sus endpoints. Cada apartado dispone de teoría, práctica guiada y un estado ejecutable de la aplicación.

## Material del alumno

- [Teoría completa del módulo](TEORIA/M02_TEORIA.md) · [PDF](TEORIA/M02_TEORIA.pdf)
- [Prácticas guiadas del módulo](PRACTICAS/M02_PRACTICAS.md) · [PDF](PRACTICAS/M02_PRACTICAS.pdf)

## Proyectos del módulo

| Punto | Contenido | Solución |
|---|---|---|
| [2.1](PROYECTO/2.1-diseno-apis-rest/) | Recursos, DTO, EF Core, SQL Server Express LocalDB y primeros endpoints GET | `PROYECTO/2.1-diseno-apis-rest/src/AceriaApp.Api/AceriaApp.Api.csproj` |
| [2.2](PROYECTO/2.2-recursos-verbos-codigos/) | Verbos HTTP, POST y operaciones sobre recursos | `PROYECTO/2.2-recursos-verbos-codigos/src/AceriaApp.Api/AceriaApp.Api.csproj` |
| [2.3](PROYECTO/2.3-validacion-peticiones/) | FluentValidation, reglas de negocio y problem details | `PROYECTO/2.3-validacion-peticiones/src/AceriaApp.Api/AceriaApp.Api.csproj` |
| [2.4](PROYECTO/2.4-documentacion-openapi/) | OpenAPI/Swagger y comprobaciones del contrato publicado | `PROYECTO/2.4-documentacion-openapi/src/AceriaApp.Api/AceriaApp.Api.csproj` |

Los proyectos son **cuatro estados independientes y progresivos**: 2.2 continúa 2.1; 2.3 continúa 2.2; 2.4 completa el recorrido.

## Entorno de trabajo

- Visual Studio con soporte para ASP.NET Core y el **SDK .NET 8**.
- **EF Core 8 y SQL Server Express LocalDB** en Windows.
- xUnit y herramientas HTTP de Visual Studio para comprobar las respuestas.
- Cada proyecto contiene sus instrucciones de ejecución.

## Recorrido sugerido

Lee la explicación del punto en [TEORÍA](TEORIA/M02_TEORIA.md), ejecuta el apartado equivalente de [PRÁCTICAS](PRACTICAS/M02_PRACTICAS.md) y contrasta el comportamiento con la solución correspondiente. En las prácticas se explica cómo crear los archivos, escribir el código, enviar peticiones y comprobar su resultado.

El número de tests depende del **estado del proyecto de este recorrido Minimal API**: 3 pruebas en 2.1; 7 en 2.2; 12 en 2.3; y 16 en 2.4. Son los tests de las soluciones de este módulo.

> Para abrir cada etapa en Visual Studio, utiliza su archivo `.csproj`. Cada etapa contiene la API en `src/AceriaApp.Api/` y sus tests en `tests/AceriaApp.Api.Tests/`.
