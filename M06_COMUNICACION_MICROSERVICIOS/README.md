# M06 — Comunicación entre microservicios

**Autor del curso: JAIME GALLO · Proyecto acumulativo AceriaApp (.NET 8)**

## Material del módulo

- **[Teoría en Markdown](TEORIA/M06_TEORIA.md)** y **[PDF](TEORIA/M06_TEORIA.pdf)**: conceptos, explicaciones y figuras.
- **[Prácticas guiadas en Markdown](PRACTICAS/M06_PRACTICAS.md)** y **[PDF](PRACTICAS/M06_PRACTICAS.pdf)**: pasos, ejemplos de código, comprobaciones y retos.
- **[Proyectos de referencia](PROYECTO/)**: una solución completa por etapa, con código, tests y documentación necesaria.

## Etapas

- **06.1** — [`6.1-comunicacion-sincrona-http`](PROYECTO/6.1-comunicacion-sincrona-http/)
- **06.2** — [`6.2-comunicacion-asincrona-eventos`](PROYECTO/6.2-comunicacion-asincrona-eventos/)
- **06.3** — [`6.3-cuando-usar-cada-enfoque`](PROYECTO/6.3-cuando-usar-cada-enfoque/)

El recuento acumulado previsto de pruebas por etapa es **232, 264 y 283**. Sirve como orientación para contrastar la ejecución real: no equivale por sí solo a tener las pruebas aprobadas.

## Trabajar en Windows

Aquí aparece RabbitMQ: `compose.yml` se crea en la práctica 6.1 y las etapas posteriores lo heredan. El broker funciona en Docker Desktop; los procesos de Producción e Inventario se ejecutan con `dotnet run` en Windows. Sigue el manual para configurar puertos, credenciales, bases SQL y trabajadores outbox/inbox.

**Orden recomendado:** teoría → práctica en tu carpeta de trabajo → compilación y tests → contraste con `PROYECTO/`. Nunca comiences copiando la solución final que estás intentando construir. Las carpetas de `PROYECTO/` incluyen los archivos de código y pruebas necesarios para ejecutar cada etapa.

El laboratorio [Docker Desktop para Windows](../PRACTICA_TRANSVERSAL_DOCKER_WINDOWS/README.md) complementa las prácticas y detalla el despliegue de infraestructura y del sistema completo, sin reemplazar el recorrido de este módulo.
