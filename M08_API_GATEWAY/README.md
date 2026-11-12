# M08 — Publicación mediante API Gateway

**Autor del curso: JAIME GALLO · Proyecto acumulativo AceriaApp (.NET 8)**

## Material del módulo

- **[Teoría en Markdown](TEORIA/M08_TEORIA.md)** y **[PDF](TEORIA/M08_TEORIA.pdf)**: conceptos, explicaciones y figuras.
- **[Prácticas guiadas en Markdown](PRACTICAS/M08_PRACTICAS.md)** y **[PDF](PRACTICAS/M08_PRACTICAS.pdf)**: pasos, ejemplos de código, comprobaciones y retos.
- **[Proyectos de referencia](PROYECTO/)**: una solución completa por etapa, con código, tests y documentación necesaria.

## Etapas

- **08.1** — [`8.1-introduccion-api-gateway`](PROYECTO/8.1-introduccion-api-gateway/)
- **08.2** — [`8.2-configuracion-basica-yarp`](PROYECTO/8.2-configuracion-basica-yarp/)
- **08.3** — [`8.3-enrutamiento-peticiones`](PROYECTO/8.3-enrutamiento-peticiones/)
- **08.4** — [`8.4-balanceo-carga`](PROYECTO/8.4-balanceo-carga/)

El recuento acumulado previsto de pruebas por etapa es **415, 451, 476 y 491**. Sirve como orientación para contrastar la ejecución real: no equivale por sí solo a tener las pruebas aprobadas.

## Trabajar en Windows

YARP funciona como proceso .NET 8 en Windows delante de Producción y dos instancias de Inventario; RabbitMQ continúa en Docker Desktop. El recorrido 8.4 incluye preparación, peticiones HTTP, balanceo, eventos y persistencia. **Nota para alumnos:** los comandos de herramientas de autor `.github/scripts/` y `tools/M08ValidationHost` mencionados al final del manual pertenecen al entorno de certificación del profesorado y no están distribuidos aquí. Para comprobar tu proyecto, utiliza `dotnet build AceriaApp.sln`, `dotnet test AceriaApp.sln` y los recorridos de PowerShell explicados en las prácticas.

**Orden recomendado:** teoría → práctica en tu carpeta de trabajo → compilación y tests → contraste con `PROYECTO/`. Nunca comiences copiando la solución final que estás intentando construir. Las carpetas de `PROYECTO/` incluyen los archivos de código y pruebas necesarios para ejecutar cada etapa.

El laboratorio [Docker Desktop para Windows](../PRACTICA_TRANSVERSAL_DOCKER_WINDOWS/README.md) complementa las prácticas y detalla el despliegue de infraestructura y del sistema completo, sin reemplazar el recorrido de este módulo.
