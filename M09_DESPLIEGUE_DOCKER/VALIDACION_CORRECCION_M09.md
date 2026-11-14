# M09 — Estado de la corrección editorial y técnica de las prácticas

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS  
**Módulo:** M09 — Despliegue integral Docker Desktop para Windows  
**Autor:** JAIME GALLO  
**Rama:** `version-corregida`  
**Fecha:** 14 de noviembre de 2026  
**Estado:** CORRECCIÓN EDITORIAL, VALIDACIÓN ESTÁTICA Y E2E INTEGRAL EN CI LINUX COMPLETADOS; **PRUEBA EN DOCKER DESKTOP PARA WINDOWS PENDIENTE**. Aprobación editorial final a cargo del autor.

## Alcance aplicado

Se ha reescrito el manual M09 para convertir las explicaciones en un recorrido docente continuo, sin fórmulas repetitivas ni párrafos de relleno. Se conservan el módulo exclusivamente práctico, sus tres escenarios (Windows+LocalDB, APIs Windows+RabbitMQ Docker y despliegue integral Docker), las seis unidades de Compose, los contratos HTTP, el código C# de M08 y los 16 pasos de la práctica.

Se han reparado además instrucciones concretas que podían inducir errores de ejecución:

- Paso 9.2: no se repite el cambio de directorio hacia M09 si el alumno ya está dentro de `PROYECTO`.
- Paso 9.6: no se sobrescribe un `.env` personalizado con el archivo de ejemplo; solo se copia si no existe.
- Pasos 9.13–9.15: los sondeos de recuperación contemplan conexiones transitorias y vuelven a comprobar la disponibilidad de YARP, RabbitMQ y las APIs.
- Paso 9.16: `detener`, `bajar` y la operación destructiva `limpiar -ConfirmarBorradoDatos` aparecen en bloques separados, con consecuencias explícitas.

Los archivos de Docker y PowerShell del proyecto se mantienen como referentes; en esta intervención **no se ha modificado el código C# de M08** ni se ha fusionado la revisión con `main`.

## Evidencias automáticas

| Comprobación | Resultado | Fuente |
|---|---|---|
| PDF generado desde Markdown corregido | PASS | GitHub Actions, PDF M09 |
| Páginas y cabeceras exigidas | **17/17** | «ARQUITECTURA HEXAGONAL Y MICROSERVICIOS», «PRÁCTICAS MÓDULO 9», «JAIME GALLO» |
| Conservación de pasos | 16/16 | Pasos 9.1 a 9.16 presentes en Markdown y PDF |
| Bloques PowerShell del manual | **28/28** sin errores de sintaxis | Parseo con PowerShell 7 en runner Windows |
| Servicios Compose | 6/6 localizados y explicados | sqlserver, rabbitmq, inventario-1, inventario-2, produccion, gateway |
| Acciones del script | 6/6 localizadas | preparar, levantar, verificar, detener, bajar, limpiar |
| Código fuente reutilizado | Ruta M08/8.4 presente | `M08_API_GATEWAY/PROYECTO/8.4-balanceo-carga` |
| Script de despliegue | Sin errores de sintaxis PowerShell | Parseo estático en runner Windows |
| Despliegue real en CI Linux | **PASS: seis contenedores, SQL, RabbitMQ, YARP, orden, evento y persistencia** | GitHub Actions Linux, no certifica Docker Desktop Windows |
| Fallo/recuperación en CI Linux | **PASS: Inventario 2, YARP, RabbitMQ y nueva proyección** | Ensayo de resiliencia adicional en Docker Linux |

- [PDF M09 actualizado y validado, 17 páginas y 16 pasos](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43574189683).
- [Validación Windows de sintaxis y correspondencia con infraestructura, tres scripts](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43574189740).
- [Auditoría de los 17 PDF actualizados, 1.220 páginas y sincronización del procedimiento Windows](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43574610999).

## E2E integral reproducido en contenedores Linux

La ejecución [M09 Docker Compose integral E2E — Linux CI](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43520238826) ha finalizado con **SUCCESS**. Usa el código .NET real de M08 y el mismo `Dockerfile.Servicio`, `compose.fullstack.yml` y `EJECUTAR_DOCKER_WINDOWS.ps1`. El runner Linux invoca el script con `-PermitirLinuxEnCI`, que habilita esta comprobación técnica pero **no certifica Windows**.

Se ha comprobado el arranque y la salud de SQL Server Express, RabbitMQ, Inventario 1, Inventario 2, Producción y YARP; GET de stock a través del gateway; distribución por `X-Instancia`; creación de orden SQL; segunda línea; planificación HTTP 202 y rechazo HTTP 409; proyección asíncrona de la orden recibida; y recuperación de la misma orden y evento tras reiniciar las APIs. La acción `levantar` y una repetición separada de `verificar` devolvieron ambas **PASS integral**. El workflow adjunta JSON de evidencias, estado y logs de los servicios sin publicar `.env`.

**Ampliación de resiliencia superada:** una ejecución posterior incorpora el script `VALIDAR_FALLOS_DOCKER_WINDOWS.ps1` y valida diez lecturas consecutivas por Inventario 1 tras detener Inventario 2, recuperación del balanceo al reactivarlo, degradación de readiness al detener RabbitMQ y retorno a salud después de recuperarlo. Después se repite el flujo integral de órdenes y eventos. [Ejecución Docker Linux completa con fallos y recuperación — PASS](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43521475426). Sus evidencias adicionales están en `.qa/docker-fallos-e2e.json` y `.qa/docker-windows-e2e.json`. No se afirma un ensayo de redelivery de mensajes creados *durante* la caída del broker ni una certificación física de Windows.

## Preparación adicional del cierre Windows

Los scripts del módulo son `EJECUTAR_DOCKER_WINDOWS.ps1`, `VALIDAR_FALLOS_DOCKER_WINDOWS.ps1` y `CERTIFICAR_DOCKER_DESKTOP_WINDOWS.ps1`. Se han sometido a un analizador sintáctico PowerShell en un runner Windows. Se ha añadido una prueba negativa que exige que el certificador **rechace Windows Server** de forma explícita y registre `resultado=FAIL`, sin falsos positivos. [GitHub Actions: verificación negativa Windows Server y sintaxis de los tres scripts — SUCCESS](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43574842983).

Esta verificación del preflight no equivale a ejecutar el laboratorio sobre Windows 10/11 con Docker Desktop.

## Alcance que **no** certifican estas evidencias

La auditoría PowerShell sobre Windows **parsea** todos los bloques y comprueba la correspondencia con Compose; el nuevo E2E ejecuta realmente Docker sobre **Linux CI**, pero todavía no ejecuta Docker Desktop sobre Windows. La validación del PDF comprueba texto, cabeceras, paginación y renderización básica, pero no equivale a una inspección humana de cada página ni a una ejecución completa de laboratorio desde un proyecto vacío.

El laboratorio ya cuenta con `PROYECTO/CERTIFICAR_DOCKER_DESKTOP_WINDOWS.ps1`, que verifica Windows 10/11 compatible, PowerShell 7, WSL 2, Docker Desktop en modo Linux, Compose y SDK .NET 8. Ejecuta los tres procedimientos (`preparar`, `levantar`, `verificar`), comprueba caída y recuperación de Inventario 2 y RabbitMQ y repite la integración después de recuperarlos. El script no acepta el modo `-PermitirLinuxEnCI` y no certifica Windows Server. Se ejecuta en **PowerShell 7 de Windows 10/11, dentro de `M09_DESPLIEGUE_DOCKER/PROYECTO`**:

```powershell
.\CERTIFICAR_DOCKER_DESKTOP_WINDOWS.ps1
```

También existe el workflow de disparo **manual** `.github/workflows/m09-certificacion-windows-desktop.yml`, que solo se puede ejecutar cuando haya un runner **self-hosted**, Windows 10/11 con Docker Desktop activo, etiquetado `docker-desktop-wsl2`. Los runners estándar `windows-2022` son Windows Server y no sirven para esa certificación. Se deben conservar los informes `.qa/certificacion-windows-docker-desktop.json`, `.qa/docker-windows-e2e.json` y `.qa/docker-fallos-e2e.json` con `resultado=PASS`. **Todavía no se dispone de esa evidencia física de Windows Desktop**. El PASS de Linux no se convierte en un PASS de Windows.

## Criterio de cierre

La redacción M09, el documento PDF con cabecera en cada página, la validación estructural/sintáctica y el E2E integral con pruebas de fallos sobre Linux están completados para revisión editorial por el autor. La certificación final de ejecución en Docker Desktop para Windows solo se cerrará al disponer de la evidencia E2E descrita.
