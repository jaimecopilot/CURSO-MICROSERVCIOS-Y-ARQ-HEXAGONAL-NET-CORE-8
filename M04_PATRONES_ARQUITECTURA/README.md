# M04 — Patrones de arquitectura

**Autor del curso: JAIME GALLO · Proyecto acumulativo AceriaApp (.NET 8)**

## Material del módulo

- **[Teoría en Markdown](TEORIA/M04_TEORIA.md)** y **[PDF](TEORIA/M04_TEORIA.pdf)**: conceptos, explicaciones y figuras.
- **[Prácticas guiadas en Markdown](PRACTICAS/M04_PRACTICAS.md)** y **[PDF](PRACTICAS/M04_PRACTICAS.pdf)**: pasos, ejemplos de código, comprobaciones y retos.
- **[Proyectos de referencia](PROYECTO/)**: una solución completa por etapa, con código, tests y documentación necesaria.

## Etapas

- **04.1** — [`4.1-repository`](PROYECTO/4.1-repository/)
- **04.2** — [`4.2-unit-of-work`](PROYECTO/4.2-unit-of-work/)
- **04.3** — [`4.3-mediator`](PROYECTO/4.3-mediator/)
- **04.4** — [`4.4-result-pattern`](PROYECTO/4.4-result-pattern/)
- **04.5** — [`4.5-inyeccion-dependencias`](PROYECTO/4.5-inyeccion-dependencias/)

El recuento acumulado previsto de pruebas por etapa es **62, 77, 90, 105 y 118**. Sirve como orientación para contrastar la ejecución real: no equivale por sí solo a tener las pruebas aprobadas.

## Trabajar en Windows

En Windows, utiliza **SQL Server Express LocalDB**. Las pruebas de integración necesitan SQL Server real: configura `ACERIA_TEST_SQLSERVER` para apuntar a `master` con permisos de crear y eliminar bases, o utiliza la opción Docker Desktop/Testcontainers explicada en las prácticas. No se sustituye SQL Server por SQLite/InMemory.

**Orden recomendado:** teoría → práctica en tu carpeta de trabajo → compilación y tests → contraste con `PROYECTO/`. Nunca comiences copiando la solución final que estás intentando construir. Las carpetas de `PROYECTO/` incluyen los archivos de código y pruebas necesarios para ejecutar cada etapa.

El laboratorio [Docker Desktop para Windows](../PRACTICA_TRANSVERSAL_DOCKER_WINDOWS/README.md) complementa las prácticas y detalla el despliegue de infraestructura y del sistema completo, sin reemplazar el recorrido de este módulo.
