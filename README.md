# Curso de arquitectura hexagonal y microservicios con .NET 8

**Material para alumnos · M01–M08 (teoría, prácticas y proyecto) + M09 (despliegue Docker) · AceriaApp**

Esta edición contiene solo lo necesario para estudiar los **ocho módulos de arquitectura y el laboratorio práctico M09**, realizar las prácticas y ejecutar sus proyectos de referencia en Windows. Los registros internos de revisión, generación y certificación del curso se conservan fuera de esta edición.

## Cómo estudiar

1. Abre la **teoría** del módulo en Markdown o PDF; utiliza los diagramas y las imágenes incluidos.
2. Sigue las **prácticas guiadas** en su orden: crea los archivos, incorpora el código y realiza cada verificación con Visual Studio o PowerShell.
3. Utiliza **PROYECTO/** para comparar tu resultado **después** de completar una etapa. Cada subcarpeta representa un estado final independiente de AceriaApp; no copies la solución terminada al iniciar el ejercicio.
4. Ejecuta los tests de la etapa con `dotnet test AceriaApp.sln -c Release` desde la carpeta que contiene esa solución, una vez preparadas sus dependencias SQL/RabbitMQ.

**Continuidad de los proyectos.** M01 es un laboratorio introductorio independiente. M02.1 comienza deliberadamente con un proyecto ASP.NET Core Empty creado desde cero; no se copia el código del monolito de M01. Desde M02.1 hasta M08.4 las prácticas evolucionan AceriaApp acumulativamente. La reconstrucción automatizada de esas **29 etapas consecutivas** está documentada en `ESTADO_CIERRE_VERSION_CORREGIDA.md`; esto acredita la paridad del código, pero no significa que se hayan automatizado todos los clics de Visual Studio. M09 despliega en Docker el código final de M08 sin reprogramar sus APIs.

## Módulos

| Módulo | Contenido | Material |
|---|---|---|
| M01 | Introducción a los microservicios | [Abrir](./M01_INTRODUCCION_MICROSERVICIOS/README.md) |
| M02 | APIs REST con ASP.NET Core 8 | [Abrir](./M02_APIS_REST_ASPNET_CORE/README.md) |
| M03 | Arquitectura hexagonal | [Abrir](./M03_ARQUITECTURA_HEXAGONAL/README.md) |
| M04 | Patrones de arquitectura | [Abrir](./M04_PATRONES_ARQUITECTURA/README.md) |
| M05 | Introducción a DDD y CQRS | [Abrir](./M05_DDD_CQRS/README.md) |
| M06 | Comunicación entre microservicios | [Abrir](./M06_COMUNICACION_MICROSERVICIOS/README.md) |
| M07 | Observabilidad y resiliencia | [Abrir](./M07_OBSERVABILIDAD_RESILIENCIA/README.md) |
| M08 | Publicación mediante API Gateway | [Abrir](./M08_API_GATEWAY/README.md) |
| M09 | Práctica: despliegue integral en Docker | [Abrir](./M09_DESPLIEGUE_DOCKER/README.md) |

M01–M08 incluyen `TEORIA/`, `PRACTICAS/`, `PROYECTO/` y `README.md`, con los gráficos necesarios para sus explicaciones. M09 es **solo práctico**, por lo que incluye `PRACTICAS/`, `PROYECTO/` y su README, pero no teoría adicional ni nuevas APIs C#.

## Preparar Windows

- **.NET SDK 8**, Visual Studio con desarrollo ASP.NET Core y PowerShell 7.
- **SQL Server Express LocalDB** para las APIs y pruebas locales en Windows. Los tests pueden utilizar una conexión SQL Server real mediante `ACERIA_TEST_SQLSERVER`.
- **Docker Desktop con motor WSL 2 y contenedores Linux** solo cuando lo exija la práctica: opcional para SQL Server de pruebas con Testcontainers en M02–M05; necesario para RabbitMQ en los recorridos de M06–M08.
- Las instrucciones específicas de cada etapa y los comandos de configuración están en su `PRACTICAS/Mxx_PRACTICAS.md`.

## M09 — Despliegue integral Docker Desktop en Windows

[M09 — Prácticas y proyecto Docker](./M09_DESPLIEGUE_DOCKER/README.md): instalación, comprobaciones, SQL Server Express, RabbitMQ, Dockerfiles, Compose, PowerShell, seis contenedores y AceriaApp con YARP. **Es el módulo 9 y es exclusivamente práctico**.

Los ejemplos de contraseña y puertos son solo para un laboratorio local; no se deben reutilizar en producción.
