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

**Cierre:** esta rama requiere regeneración de PDF, comprobación de sus páginas y verificación Linux SQL Server/RabbitMQ, HTTP y Windows LocalDB antes de dar por aprobada la corrección. Las antiguas actas de revisión visual corresponden a la edición previa, no son evidencia de la nueva maquetación.
