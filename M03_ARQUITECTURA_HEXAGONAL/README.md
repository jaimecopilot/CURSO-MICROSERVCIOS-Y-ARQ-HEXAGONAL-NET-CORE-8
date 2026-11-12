# M03 — Arquitectura hexagonal

**Autor del curso: JAIME GALLO · Proyecto acumulativo AceriaApp (.NET 8)**

## Material del módulo

- **[Teoría en Markdown](TEORIA/M03_TEORIA.md)** y **[PDF](TEORIA/M03_TEORIA.pdf)**: conceptos, explicaciones y figuras.
- **[Prácticas guiadas en Markdown](PRACTICAS/M03_PRACTICAS.md)** y **[PDF](PRACTICAS/M03_PRACTICAS.pdf)**: pasos, ejemplos de código, comprobaciones y retos.
- **[Proyectos de referencia](PROYECTO/)**: una solución completa por etapa, con código, tests y documentación necesaria.

## Etapas

- **03.1** — [`3.1-capas-aplicacion`](PROYECTO/3.1-capas-aplicacion/)
- **03.2** — [`3.2-puertos-adaptadores`](PROYECTO/3.2-puertos-adaptadores/)
- **03.3** — [`3.3-separacion-capas`](PROYECTO/3.3-separacion-capas/)
- **03.4** — [`3.4-implementacion-aspnet-core`](PROYECTO/3.4-implementacion-aspnet-core/)

El recuento acumulado previsto de pruebas por etapa es **23, 31, 38 y 50**. Sirve como orientación para contrastar la ejecución real: no equivale por sí solo a tener las pruebas aprobadas.

## Trabajar en Windows

En Windows, utiliza **SQL Server Express LocalDB**. Las pruebas de integración necesitan SQL Server real: configura `ACERIA_TEST_SQLSERVER` para apuntar a `master` con permisos de crear y eliminar bases, o utiliza la opción Docker Desktop/Testcontainers explicada en las prácticas. No se sustituye SQL Server por SQLite/InMemory.

**Orden recomendado:** teoría → práctica en tu carpeta de trabajo → compilación y tests → contraste con `PROYECTO/`. Nunca comiences copiando la solución final que estás intentando construir. Las carpetas de `PROYECTO/` incluyen los archivos de código y pruebas necesarios para ejecutar cada etapa.

El laboratorio [Docker Desktop para Windows](../PRACTICA_TRANSVERSAL_DOCKER_WINDOWS/README.md) complementa las prácticas y detalla el despliegue de infraestructura y del sistema completo, sin reemplazar el recorrido de este módulo.
