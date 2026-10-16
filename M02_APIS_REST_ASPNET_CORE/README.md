# Módulo 2 — Desarrollo de APIs REST con ASP.NET Core

Este módulo desarrolla el contrato HTTP de AceriaApp a partir de las soluciones del módulo 1. El alumno trabaja con .NET 8, EF Core 8, SQL Server Express y Visual Studio.

## Material docente

- **Teoría:** [leer Markdown](TEORIA/M02_TEORIA.md) · [abrir PDF](TEORIA/M02_TEORIA.pdf).
- **Prácticas:** [seguir Markdown](PRACTICAS/M02_PRACTICAS.md) · [abrir PDF](PRACTICAS/M02_PRACTICAS.pdf).

## Proyectos para realizar los ejercicios

| Punto | Solución independiente | Tests acumulados |
|:--|:--|--:|
| 2.1 — Diseño de APIs REST | [2.1-diseno-apis-rest](PROYECTO/2.1-diseno-apis-rest/) | 31 |
| 2.2 — Recursos, verbos y códigos | [2.2-recursos-verbos-codigos](PROYECTO/2.2-recursos-verbos-codigos/) | 36 |
| 2.3 — Validación de peticiones | [2.3-validacion-peticiones](PROYECTO/2.3-validacion-peticiones/) | 42 |
| 2.4 — Documentación OpenAPI | [2.4-documentacion-openapi](PROYECTO/2.4-documentacion-openapi/) | 51 |

Los cuatro proyectos son **estados acumulativos independientes**. Cada carpeta contiene su propia solución `AceriaApp.sln`, código fuente, pruebas, documentación y README. Se empieza por 2.1 y se avanza en orden.

## Uso de cada proyecto

1. Abrir el archivo `AceriaApp.sln` de la carpeta del punto correspondiente.
2. Restaurar paquetes NuGet y comprobar el entorno de SQL Server Express.
3. Seguir los pasos de `PRACTICAS/M02_PRACTICAS.md`; el código nuevo de cada paso aparece identificado para poder activarlo progresivamente.
4. Compilar con `dotnet build AceriaApp.sln` y ejecutar las pruebas con `dotnet test AceriaApp.sln`.
5. Utilizar el README del proyecto elegido para revisar los archivos nuevos y las instrucciones particulares.

Los recuentos de pruebas anteriores corresponden a los estados completos básicos; los retos opcionales añaden pruebas adicionales.
