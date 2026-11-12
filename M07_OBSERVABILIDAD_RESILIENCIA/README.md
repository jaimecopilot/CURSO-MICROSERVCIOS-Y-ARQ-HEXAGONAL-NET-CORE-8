# M07 — Observabilidad y resiliencia

**Autor del curso: JAIME GALLO · Proyecto acumulativo AceriaApp (.NET 8)**

## Material del módulo

- **[Teoría en Markdown](TEORIA/M07_TEORIA.md)** y **[PDF](TEORIA/M07_TEORIA.pdf)**: conceptos, explicaciones y figuras.
- **[Prácticas guiadas en Markdown](PRACTICAS/M07_PRACTICAS.md)** y **[PDF](PRACTICAS/M07_PRACTICAS.pdf)**: pasos, ejemplos de código, comprobaciones y retos.
- **[Proyectos de referencia](PROYECTO/)**: una solución completa por etapa, con código, tests y documentación necesaria.

## Etapas

- **07.1** — [`7.1-logging`](PROYECTO/7.1-logging/)
- **07.2** — [`7.2-health-checks`](PROYECTO/7.2-health-checks/)
- **07.3** — [`7.3-gestion-excepciones`](PROYECTO/7.3-gestion-excepciones/)
- **07.4** — [`7.4-retry-circuit-breaker-polly`](PROYECTO/7.4-retry-circuit-breaker-polly/)

El recuento acumulado previsto de pruebas por etapa es **309, 331, 353 y 403**. Sirve como orientación para contrastar la ejecución real: no equivale por sí solo a tener las pruebas aprobadas.

## Trabajar en Windows

Continúa el trabajo de M06. Las prácticas explican cómo arrancar RabbitMQ con Docker Desktop, comprobar `/health/live` y `/health/ready`, diagnosticar fallos y recuperar el servicio; la API sigue funcionando en Windows.

**Orden recomendado:** teoría → práctica en tu carpeta de trabajo → compilación y tests → contraste con `PROYECTO/`. Nunca comiences copiando la solución final que estás intentando construir. Las carpetas de `PROYECTO/` incluyen los archivos de código y pruebas necesarios para ejecutar cada etapa.

El laboratorio [Docker Desktop para Windows](../PRACTICA_TRANSVERSAL_DOCKER_WINDOWS/README.md) complementa las prácticas y detalla el despliegue de infraestructura y del sistema completo, sin reemplazar el recorrido de este módulo.
