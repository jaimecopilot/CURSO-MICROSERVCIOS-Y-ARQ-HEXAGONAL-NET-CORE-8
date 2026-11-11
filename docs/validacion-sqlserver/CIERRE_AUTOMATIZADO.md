# Validación SQL Server M02–M05

Resultado automatizado: **PASS**. Revisión comprobada: `54709859d231c8607ba0761a28f442fda285fd58`.

Ejecución: https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/42986550628

| Módulo | Etapas reconstruidas | Pruebas por etapa | Bases SQL verificadas | Windows LocalDB y reinicio HTTP |
|---|---:|---|---:|---|
| M02 | 4 | 3, 7, 12, 16 | 38 | PASS |
| M03 | 4 | 23, 31, 38, 50 | 144 | PASS |
| M04 | 5 | 62, 77, 90, 105, 118 | 342 | PASS |
| M05 | 5 | 134, 153, 172, 190, 208 | 486 | PASS |

Las pruebas de integración utilizaron SQL Server Express real iniciado con Testcontainers. Cada prueba dispone de una base aislada. Las pruebas de dominio puro conservan su independencia de infraestructura. Windows comprueba los cuatro proyectos finales, peticiones HTTP, validación, conflictos y conservación de los datos después de reiniciar el proceso.

Los retos programados de M03, M04 y M05 se ejecutan aisladamente. M02 contiene propuestas abiertas de ampliación manual; su informe las identifica como MANUAL_NO_EJECUTADO y no las cuenta como pruebas aprobadas.

M01 conserva la evidencia SQL Server Docker 1.1–1.5 y LocalDB Windows 1.1/1.5 de la ejecución 42862047382; no se modificó su código.

Los ocho PDF fueron regenerados desde sus Markdown; se comprobaron cobertura íntegra de texto y límites de página. La revisión visual y la revisión independiente del cambio se registran en REVISION_FINAL.md antes de integrar en main.
