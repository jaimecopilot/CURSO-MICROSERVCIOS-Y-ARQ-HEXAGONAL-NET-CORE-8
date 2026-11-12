# M06 — Revisión editorial controlada

**Base:** `main` — `16a1a0783e14eaf1c4cdb07f25a13d6719f286d2`.  
**Rama:** `revision/editorial-m06-20261112`.

| Indicador | Antes | Después |
|---|---:|---:|
| Palabras de prácticas | 46.190 | 32.293 |
| Anotaciones numeradas de líneas | 941 | 173 |
| Comentarios repetidos retirados | — | 768 |
| Reducción | — | 30,1 % |
| Pasos ejecutables | 72 | 72 |
| Bloques íntegros de código | 114 | 114 |
| Marcadores de construcción de proyectos y retos | 101 | 101 |

Solo se han eliminado comentarios de línea con contenido repetido dentro de un mismo punto. Se conserva la primera aparición y cada anotación singular. No se alteran los ejemplos, pruebas, JSON, archivos, instrucciones HTTP, SQL Server, RabbitMQ, outbox/inbox ni retos.

El contrato exacto de código y marcadores tiene SHA-1 de objeto Git `9320c00ac908574bf541cf6c25dac7bee08367b5`, cotejado antes/después. Su regresión automatizada está en `.github/tests/test_m06_editorial.py`.

**Cierre editorial y técnico de la edición optimizada: PASS.** La [ejecución 43248017123](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43248017123) certificó después de la integración en `main` E2E real de SQL Server Express, RabbitMQ, dos procesos HTTP, Windows LocalDB y ambos PDF. Prácticas vigentes: **116 páginas**, 32.293 palabras, 173 citas verificadas, 1.552 bloques HTML cotejados, sin omisiones ni desbordamientos; la inspección visual selectiva se conserva en la PR #8. Las actas de 146 páginas quedan explícitamente identificadas como históricas. Se ejecutará una recertificación de continuidad tras la actualización de M02–M05 en `main`.
