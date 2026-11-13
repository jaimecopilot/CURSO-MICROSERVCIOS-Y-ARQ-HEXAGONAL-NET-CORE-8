# M09 — Estado de la corrección editorial y técnica de las prácticas

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS  
**Módulo:** M09 — Despliegue integral Docker Desktop para Windows  
**Autor:** JAIME GALLO  
**Rama:** `version-corregida`  
**Fecha:** 13 de noviembre de 2026  
**Estado:** CORRECCIÓN EDITORIAL Y VERIFICACIÓN ESTÁTICA CERRADAS; **PRUEBA E2E REAL EN DOCKER DESKTOP PARA WINDOWS PENDIENTE**. Aprobación editorial final a cargo del autor.

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
| Páginas y cabeceras exigidas | 16/16 | «ARQUITECTURA HEXAGONAL Y MICROSERVICIOS», «PRÁCTICAS MÓDULO 9», «JAIME GALLO» |
| Conservación de pasos | 16/16 | Pasos 9.1 a 9.16 presentes en Markdown y PDF |
| Bloques PowerShell del manual | 27/27 sin errores de sintaxis | Parseo con PowerShell 7 en runner Windows |
| Servicios Compose | 6/6 localizados y explicados | sqlserver, rabbitmq, inventario-1, inventario-2, produccion, gateway |
| Acciones del script | 6/6 localizadas | preparar, levantar, verificar, detener, bajar, limpiar |
| Código fuente reutilizado | Ruta M08/8.4 presente | `M08_API_GATEWAY/PROYECTO/8.4-balanceo-carga` |
| Script de despliegue | Sin errores de sintaxis PowerShell | Parseo estático en runner Windows |

- [PDF M09 generado y validado](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43509870226).
- [Validación Windows de sintaxis y correspondencia con infraestructura](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43510540166).

## Alcance que **no** certifican estas evidencias

El runner Windows empleado aquí **parsea** todos los bloques PowerShell y comprueba la correspondencia con Compose y el script, pero no ejecuta Docker Desktop. La validación del PDF comprueba texto, cabeceras, paginación y renderización básica, pero no equivale a una inspección humana de cada página ni a una ejecución completa de laboratorio desde un proyecto vacío.

Para afirmar que el despliegue integral funciona sobre un equipo Windows real se debe ejecutar en Docker Desktop + WSL 2:

1. `.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion preparar`
2. `.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion levantar`
3. `.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion verificar`

Hay que conservar el archivo `.qa/docker-windows-e2e.json` con `resultado=PASS`, las respuestas HTTP que acrediten orden y proyección, el balanceo mediante `X-Instancia` y la recuperación tras reinicio. Esta prueba **sigue pendiente**, sin atribuir un PASS de Linux o de sintaxis PowerShell al entorno físico Windows.

## Criterio de cierre

La redacción M09, el documento PDF con cabecera en cada página y la validación estructural/sintáctica están preparados para revisión editorial por el autor. La certificación final de ejecución en Docker Desktop para Windows solo se cerrará al disponer de la evidencia E2E descrita.
