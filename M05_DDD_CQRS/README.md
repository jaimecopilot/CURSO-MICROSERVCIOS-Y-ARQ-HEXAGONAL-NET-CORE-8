# M05 — Introducción a DDD y CQRS

**Autor del curso: JAIME GALLO · Proyecto acumulativo AceriaApp (.NET 8)**

## Material del módulo

- **[Teoría en Markdown](TEORIA/M05_TEORIA.md)** y **[PDF](TEORIA/M05_TEORIA.pdf)**: conceptos, explicaciones y figuras.
- **[Prácticas guiadas en Markdown](PRACTICAS/M05_PRACTICAS.md)** y **[PDF](PRACTICAS/M05_PRACTICAS.pdf)**: pasos, ejemplos de código, comprobaciones y retos.
- **[Proyectos de referencia](PROYECTO/)**: una solución completa por etapa, con código, tests y documentación necesaria.

## Etapas

- **05.1** — [`5.1-conceptos-ddd`](PROYECTO/5.1-conceptos-ddd/)
- **05.2** — [`5.2-entidades-value-objects`](PROYECTO/5.2-entidades-value-objects/)
- **05.3** — [`5.3-casos-de-uso`](PROYECTO/5.3-casos-de-uso/)
- **05.4** — [`5.4-commands-queries`](PROYECTO/5.4-commands-queries/)
- **05.5** — [`5.5-dominio-aceria`](PROYECTO/5.5-dominio-aceria/)

El recuento acumulado previsto de pruebas por etapa es **134, 153, 172, 190 y 208**. Sirve como orientación para contrastar la ejecución real: no equivale por sí solo a tener las pruebas aprobadas.

## Trabajar en Windows

En Windows, utiliza **SQL Server Express LocalDB**. Las pruebas de integración necesitan SQL Server real: configura `ACERIA_TEST_SQLSERVER` para apuntar a `master` con permisos de crear y eliminar bases, o utiliza la opción Docker Desktop/Testcontainers explicada en las prácticas. No se sustituye SQL Server por SQLite/InMemory.

**Orden recomendado:** teoría → práctica en tu carpeta de trabajo → compilación y tests → contraste con `PROYECTO/`. Nunca comiences copiando la solución final que estás intentando construir. Las carpetas de `PROYECTO/` incluyen los archivos de código y pruebas necesarios para ejecutar cada etapa.

El laboratorio [Docker Desktop para Windows](../PRACTICA_TRANSVERSAL_DOCKER_WINDOWS/README.md) complementa las prácticas y detalla el despliegue de infraestructura y del sistema completo, sin reemplazar el recorrido de este módulo.
