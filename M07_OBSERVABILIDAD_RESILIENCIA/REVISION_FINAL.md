# M07 — Revisión final y cierre

**Resultado: PASS.** Módulo completo comprobado sobre la revisión `53286086bdc9de179af1329cf0b18d421415c71e`.

[Ejecución integral de GitHub Actions](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43013439346). Los tres trabajos de validación —Linux, Windows y PDF— y el publicador han terminado correctamente. El cierre documental posterior conserva exactamente el código y los PDF comprobados.

## Entrega

- Teoría: 51 páginas, 40 bloques originales, 40 ampliaciones aplicadas y 12 diagramas en SVG y PNG.
- Prácticas: 267 páginas, 96 pasos, 93 operaciones con archivos completos, cuatro retos resueltos y cuatro recorridos ejecutables con PowerShell 7.
- Cuatro soluciones acumulativas desde M06 6.3. Base de 29 proyectos y 283 pruebas; final de 34 proyectos y 403 pruebas.
- 56 pruebas nuevas de catálogos y 64 funcionales. Las pruebas temporales de Polly utilizan reloj virtual y transporte controlado; las comprobaciones entre procesos acreditan HTTP, SQL Server y RabbitMQ reales por separado.

| Etapa | Proyectos | Proyectos de tests | Documentos | Pruebas obligatorias | Pruebas con reto aislado |
|---|---:|---:|---:|---:|---:|
| 7.1 | 31 | 19 | 36 | 309 | 310 |
| 7.2 | 32 | 20 | 38 | 331 | 332 |
| 7.3 | 33 | 21 | 40 | 353 | 354 |
| 7.4 | 34 | 22 | 42 | 403 | 404 |

Los cuatro retos se ejecutaron en copias independientes sin alterar las etapas obligatorias. El E2E realizó 52 compilaciones intermedias y reconstruyó exclusivamente desde M06 y los bloques del Markdown; no copió una implementación final de M07. No hubo pruebas omitidas ni sustitución de SQL Server por un proveedor en memoria. Se acreditaron 622 bases de prueba con SQL Server Express real.

## Comportamiento acreditado

- Logs JSON y correlación validada compartida entre Producción e Inventario; sustitución de cabeceras inválidas y exclusión de ruta concreta, query, cuerpo y Authorization en eventos propios de M07.
- Liveness independiente de dependencias y readiness con consultas SQL y conexión AMQP autenticada. Caída real de RabbitMQ: live 200 y ready 503; recuperación: ready 200 sin reiniciar las API. Base SQL inexistente: readiness 503 sin alterar la instancia compartida.
- ProblemDetails 500 seguro en ambas API, con traceId y correlationId; diagnóstico ausente en Production aunque se active su indicador. Se conservan los errores esperados del dominio.
- Inventario real detenido: reintentos 7401, circuito abierto 7402 e indisponibilidad 503. Recuperación 7403 con el mismo proceso de Producción, sin stock ficticio.
- Planificación, líneas, outbox, RabbitMQ, inbox y proyección SQL; persistencia después de reiniciar. Windows repitió los recorridos HTTP con LocalDB; la mensajería se acreditó en Linux.

## Revisión independiente y correcciones

La revisión encontró dos defectos que se reprodujeron mediante regresiones antes de corregirlos: UseExceptionHandler borraba la cabecera X-Correlation-ID al generar 500, y los scopes ASP.NET añadían RequestPath con el valor concreto de la URL. OnStarting conserva la cabecera y un enriquecedor elimina RequestPath. Las dos regresiones fallaron primero y pasaron después, sin alterar los conteos de pruebas.

La primera ejecución integral aprobó las cuatro etapas y los retos, pero detectó una incidencia del host de pruebas: Docker reasignaba el puerto aleatorio de RabbitMQ durante stop/start y las API conservaban la URI inicial. [El diagnóstico con el mismo host](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43012897452) observó 32770 antes y 32771 después, con el broker activo. El host ahora selecciona un puerto libre y fija su enlace explícitamente. [La comprobación posterior](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43013368680) mantuvo 41703 y aprobó el recorrido Linux completo. La ejecución integral enlazada al inicio repitió después todo el cierre con el host corregido.

La revisión independiente del cambio no encontró problemas importantes. La compilación del host y la comprobación local de las 118 pruebas nuevas que no necesitan infraestructura externa finalizaron sin advertencias. Las 75 comprobaciones Python también pasaron.

## Revisión editorial y visual

Las 318 páginas se inspeccionaron visualmente mediante contactos y ampliaciones. Se validaron 2.934 citas contra líneas físicas de código y la cobertura de 5.178 bloques HTML: 776 de teoría y 4.402 de prácticas. No hay bloques omitidos, páginas vacías ni desbordamientos detectados.

El cotejo de los PDF generados en CI con los revisados localmente compara todas las páginas píxel a píxel a 86,4 dpi. Resultado: 318 de 318 idénticas. Las huellas binarias, que pueden diferir por detalles de generación, quedan registradas por separado en [COTEJO_PDF_CI.json](COTEJO_PDF_CI.json). Los informes visuales conservan la identidad local revisada y añaden la identidad publicada.

## Alcance y conservación

M01–M06 permanecen intactos respecto a `25b8745fea66592680d49d33adf1c027294e4411`. Los documentos y archivos de pruebas heredados se conservan también dentro de las copias M07.

La garantía de minimización de logs se limita a los eventos nuevos propios de M07. Los workers heredados y EF pueden registrar detalles internos y no se presentan como auditados globalmente. Readiness acredita acceso, no finalización de todas las entregas. El módulo no instala un backend de observabilidad ni reserva stock mediante la consulta GET.

## Evidencias

- [E2E y retos](M07_E2E_RESULTADOS.json).
- [SQL Server y hashes de proyectos](M07_SQLSERVER_RESULTADOS.json).
- [HTTP y RabbitMQ](M07_HTTP_RESULTADOS.json).
- [Windows/LocalDB](M07_WINDOWS_RESULTADOS.json).
- [Cobertura y huellas PDF](REPORTE_PDF_M07.json).
- [Revisión visual de teoría](REVISION_VISUAL_TEORIA.md) y [prácticas](REVISION_VISUAL_PRACTICAS.md).
- [Cierre automatizado](CIERRE_AUTOMATIZADO.md).
