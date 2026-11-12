# M01 — Introducción a los microservicios

**Autor del curso: JAIME GALLO · Proyecto acumulativo AceriaApp (.NET 8)**

## Material del módulo

- **[Teoría en Markdown](TEORIA/M01_TEORIA.md)** y **[PDF](TEORIA/M01_TEORIA.pdf)**: conceptos, explicaciones y figuras.
- **[Prácticas guiadas en Markdown](PRACTICAS/M01_PRACTICAS.md)** y **[PDF](PRACTICAS/M01_PRACTICAS.pdf)**: pasos, ejemplos de código, comprobaciones y retos.
- **[Proyectos de referencia](PROYECTO/)**: una solución completa por etapa, con código, tests y documentación necesaria.

## Etapas

- **01.1** — [`1.1-monolito-vs-microservicios`](PROYECTO/1.1-monolito-vs-microservicios/)
- **01.2** — [`1.2-ventajas-inconvenientes`](PROYECTO/1.2-ventajas-inconvenientes/)
- **01.3** — [`1.3-principios-diseno`](PROYECTO/1.3-principios-diseno/)
- **01.4** — [`1.4-organizacion-solucion`](PROYECTO/1.4-organizacion-solucion/)
- **01.5** — [`1.5-buenas-practicas`](PROYECTO/1.5-buenas-practicas/)

El recuento acumulado previsto de pruebas por etapa es **cinco puntos, 24 pasos por punto; pruebas SQL/HTTP y retos**. Sirve como orientación para contrastar la ejecución real: no equivale por sí solo a tener las pruebas aprobadas.

## Trabajar en Windows

La primera práctica construye los conceptos y la solución de partida. Cada carpeta conserva `AceriaApp.sln`, código fuente, tests y documentación didáctica. Consulta el apartado inicial del manual para preparar SQL Server Express LocalDB.

**Orden recomendado:** teoría → práctica en tu carpeta de trabajo → compilación y tests → contraste con `PROYECTO/`. Nunca comiences copiando la solución final que estás intentando construir. Las carpetas de `PROYECTO/` incluyen los archivos de código y pruebas necesarios para ejecutar cada etapa.

El laboratorio [Docker Desktop para Windows](../PRACTICA_TRANSVERSAL_DOCKER_WINDOWS/README.md) complementa las prácticas y detalla el despliegue de infraestructura y del sistema completo, sin reemplazar el recorrido de este módulo.
