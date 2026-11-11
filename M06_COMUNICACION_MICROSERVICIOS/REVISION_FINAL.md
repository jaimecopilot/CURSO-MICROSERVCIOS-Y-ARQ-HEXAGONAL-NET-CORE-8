# Cierre de M06 — Comunicación entre microservicios

**Resultado: completado y verificado.** Revisión ejecutable comprobada: `4236caf93137ad72bb5009ba2916be1c0a29ddbc`.

[GitHub Actions](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/42998626042) ejecutó SQL Server Express, RabbitMQ, el recorrido HTTP entre dos procesos, Windows/LocalDB y generación de PDF. Los informes de la entrega conservan los hashes de manual, proyectos y documentos comprobados.

| Comprobación | Evidencia |
|---|---|
| Reconstrucción exclusivamente desde M05 y el manual | 72 pasos, 92 operaciones y 63 archivos distintos |
| Compilaciones intermedias | 36 superadas |
| Etapas 6.1 / 6.2 / 6.3 | 232 / 264 / 283 pruebas superadas |
| Retos 6.1 / 6.2 / 6.3 en copias independientes | 233 / 265 / 284 pruebas acumuladas superadas |
| Solución final | 29 proyectos, incluidos 18 proyectos de pruebas |
| SQL Server real | 436 bases aisladas verificadas, proveedor y edición contrastados |
| RabbitMQ real | Publicación, entrega, reintento, duplicados y cola de errores |
| HTTP entre procesos | 200, 202, 404, 409 y 503; persistencia tras reiniciar |
| Windows | LocalDB, dos procesos HTTP y persistencia confirmados |
| Controles Python | 31 pruebas superadas |
| Teoría | 41 páginas, 30 bloques, 30 ampliaciones y 10 diagramas SVG/PNG |
| Prácticas | 146 páginas, 3 retos resueltos y 941 explicaciones de líneas verificadas |
| PDF publicados | 187 páginas cotejadas con la revisión visual; ninguna diferencia de píxeles a 72 dpi |

## Hallazgos resueltos

La revisión independiente detectó que una línea añadida desde una lectura antigua podía guardarse después de planificar. La raíz ahora mantiene una revisión común a las mutaciones de líneas y estado. EF comprueba esa revisión y el conflicto se traduce a HTTP 409. Las pruebas SQL verifican ambos órdenes de confirmación y la igualdad entre las cantidades de la orden persistida y del evento.

Se añadió una prueba conjunta con SQL Server y RabbitMQ que provoca un fallo SQL después de confirmar la publicación y antes de marcar el outbox. El reintento publica el mismo EventoId; dos entregas producen una sola proyección durable, con identidad, cantidad y huella comprobadas.

El primer cierre detectó un informe Windows escrito con la codificación del sistema. La regresión reprodujo el fallo de lectura en UTF-8; la escritura explícita en UTF-8 lo corrigió. La ejecución definitiva verifica el recorrido completo de nuevo.

Se corrigieron referencias al paso de implementación, explicaciones de confirms/commit/ack y un salto de página excesivo en listados largos. Ambos informes de revisión visual identifican los PDF publicados.

## Base heredada y alcance

M01–M05 permanecen idénticos a la base `aa7319c2c799b78710d4435aaca8ef4857da34cf`. La regeneración automática previa de M02–M05 se cotejó con la revisión anterior: sus 672 páginas son visualmente idénticas. M6 hereda exactamente M05 5.5 y adapta únicamente sus propias copias acumulativas.

El módulo ejecuta comunicaciones reales. La consulta de stock es informativa; no reserva ni descuenta existencias. El 202 acredita la planificación local y la actualización de Inventario es eventual. El outbox admite reenvíos y el receptor evita repetir el efecto. BasicGet y los reintentos periódicos son decisiones didácticas explícitas.

No quedan incidencias bloqueantes conocidas en el alcance acordado. Los archivos de diagnóstico transitorios y las herramientas de autoría no son necesarios para que el alumno reconstruya el proyecto desde el manual.
