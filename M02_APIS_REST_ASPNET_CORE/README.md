# M02 — APIs REST con ASP.NET Core 8

**Autor del curso: JAIME GALLO · Proyecto acumulativo AceriaApp (.NET 8)**

## Material del módulo

- **[Teoría en Markdown](TEORIA/M02_TEORIA.md)** y **[PDF](TEORIA/M02_TEORIA.pdf)**: conceptos, explicaciones y figuras.
- **[Prácticas guiadas en Markdown](PRACTICAS/M02_PRACTICAS.md)** y **[PDF](PRACTICAS/M02_PRACTICAS.pdf)**: pasos, ejemplos de código, comprobaciones y retos.
- **[Proyectos de referencia](PROYECTO/)**: una solución completa por etapa, con código, tests y documentación necesaria.

## Etapas

- **02.1** — [`2.1-diseno-apis-rest`](PROYECTO/2.1-diseno-apis-rest/)
- **02.2** — [`2.2-recursos-verbos-codigos`](PROYECTO/2.2-recursos-verbos-codigos/)
- **02.3** — [`2.3-validacion-peticiones`](PROYECTO/2.3-validacion-peticiones/)
- **02.4** — [`2.4-documentacion-openapi`](PROYECTO/2.4-documentacion-openapi/)

El recuento acumulado previsto de pruebas por etapa es **3, 7, 12 y 16**. Sirve como orientación para contrastar la ejecución real: no equivale por sí solo a tener las pruebas aprobadas.

## Trabajar en Windows

En Windows, utiliza **SQL Server Express LocalDB**. Las pruebas de integración necesitan SQL Server real: configura `ACERIA_TEST_SQLSERVER` para apuntar a `master` con permisos de crear y eliminar bases, o utiliza la opción Docker Desktop/Testcontainers explicada en las prácticas. No se sustituye SQL Server por SQLite/InMemory.

**Orden recomendado:** teoría → práctica en tu carpeta de trabajo → compilación y tests → contraste con `PROYECTO/`. Nunca comiences copiando la solución final que estás intentando construir. Las carpetas de `PROYECTO/` incluyen los archivos de código y pruebas necesarios para ejecutar cada etapa.

El laboratorio [Docker Desktop para Windows](../PRACTICA_TRANSVERSAL_DOCKER_WINDOWS/README.md) complementa las prácticas y detalla el despliegue de infraestructura y del sistema completo, sin reemplazar el recorrido de este módulo.
