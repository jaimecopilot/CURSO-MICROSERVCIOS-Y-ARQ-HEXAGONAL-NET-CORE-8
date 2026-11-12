# M07 — Optimización editorial de prácticas (revisión controlada)

**Base:** `main`, commit `16a1a0783e14eaf1c4cdb07f25a13d6719f286d2`.  
**Rama:** `revision/editorial-m07-20261112`.

| Métrica | Antes | Después |
|---|---:|---:|
| Palabras del Markdown | 88.808 | 47.160 |
| Explicaciones de líneas | 2.662 | 233 |
| Explicaciones reiteradas retiradas | — | 2.429 |
| Reducción del volumen | — | 46,9 % |
| Pasos guiados | 96 | 96 |
| Bloques de código | 137 | 137 |
| Marcadores de generación M07 | 105 | 105 |

La intervención solo elimina repeticiones de glosas numeradas **dentro de cada punto**. Conserva la primera explicación equivalente, todas las anotaciones singulares, el contenido ejecutable completo, las rutas y todas las instrucciones de trabajo. Los títulos que ya no preceden anotaciones se retiran. Las comprobaciones y diagnósticos de cada paso permanecen.

**Huella Git del código y marcadores antes y después:** `ad6fd926a43501ed5fd03b6668c63965d7a20ec1`. Una prueba `test_m07_editorial.py` comprueba el contrato de bloques y marcadores y los 96 pasos.

**Cierre editorial y técnico (12/11/2026): PASS para esta edición.** La [ejecución 43238328603](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43238328603) certifica SQL Server Express real, RabbitMQ, E2E Linux, Windows/LocalDB, cuatro retos y PDF. Prácticas vigentes: **174 páginas**, 47.160 palabras, 233 citas numeradas, 1.952 bloques PDF cotejados, sin páginas vacías ni desbordamientos. La inspección visual selectiva figura en la PR #9; las antiguas actas visuales están identificadas como históricas. La continuidad acumulada en `main` se recertifica después del cierre de M06.
