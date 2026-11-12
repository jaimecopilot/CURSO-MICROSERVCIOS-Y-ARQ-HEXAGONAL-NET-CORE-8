# Revisión editorial controlada de M08

**Rama de ensayo:** `revision/editorial-m08-20261112`.
**Base técnica:** `desarrollo/m08-api-gateway`, commit `5bde1a9a4e211b4816b797be182d558e1505bd63`, con los E2E y PDFs certificados tras `ed0d9166`.
**Objetivo:** eliminar glosas redundantes sin modificar código, instrucciones ejecutables, retos ni comprobaciones.

## Comparación del manual de prácticas

| Medida | Antes | Versión editorial |
|---|---:|---:|
| Palabras (separadas por espacios) | 109.770 | 42.145 |
| Explicaciones individuales de líneas | 3.785 | 360 |
| Entradas redundantes suprimidas | — | 3.425 |
| Reducción de palabras | — | 61,6 % |
| Pasos guiados | 96 | 96 |
| Bloques de código íntegros | 96 | 96 |
| Marcadores M08_CODIGO | 66 | 66 |
| Marcadores M08_RETO | 12 | 12 |

## Alcance y justificación

1. La única supresión de contenido ha afectado a explicaciones numeradas repetidas **con el mismo significado dentro de cada punto**. Se conserva la primera aparición por punto y todas las explicaciones únicas. La frase introductoria sobre las glosas se ha actualizado para describir este criterio.
2. Se han conservado sin modificación todos los bloques de código, las rutas de proyecto, los comentarios de extracción de archivos, las 96 instrucciones estructuradas, los procedimientos guiados y las verificaciones.
3. Los encabezados sin anotaciones se han retirado. Los demás se presentan como `Lectura selectiva`, sin prometer que hay una glosa por cada línea.
4. **Huella Git del contrato código + marcadores:** `b4b1a4da0787fd175cf4f6625ce5be6548a7deca`. Es la SHA-1 de un objeto Git `blob` con el contenido concatenado de los 96 fences Markdown y los 78 marcadores, separados mediante el esquema documentado en `.github/tests/test_m08_editorial.py`. Es idéntica antes/después de la intervención y se comprueba en pruebas automatizadas.
5. La teoría (incluidas sus 12 ilustraciones SVG/PNG) y las versiones de M01–M07 no se han editado.

## Validación técnica y editorial

**Cierre editorial y técnico de M08 (12/11/2026): PASS en rama de desarrollo.**

- [CI editorial 43237110128](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43237110128): **SUCCESS** en Linux, SQL Server Express real, RabbitMQ, HTTP YARP, Windows/LocalDB, PDF y publicación.
- [CI integrada de desarrollo 43248689157](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43248689157): **SUCCESS** para los tres artefactos y el cierre automático, ejecutado después de fusionar la corrección editorial.
- **Manual vigente:** prácticas de **145 páginas** y **42.145 palabras**, teoría de **51 páginas** con 12 diagramas. **360** citas de línea verificadas y **1.914** bloques de PDF cotejados; sin bloques omitidos, páginas vacías ni desbordamientos.
- **Trazabilidad:** 96 pasos, 96 bloques de código y 78 marcadores intactos; regresión mediante huella Git `b4b1a4da0787fd175cf4f6625ce5be6548a7deca`.
- **Pruebas acumuladas por etapa:** 415, 451, 476 y **491**; retos optativos aislados 416, 452, 477, 492; la evaluación de fiabilidad incluye destinos caídos y reincorporados.
- **Inspección visual:** revisión selectiva de portada, instrucciones, código largo, tablas, capturas de páginas intermedias y cierre documentada en la PR #10.

Esta aprobación corresponde a la rama de desarrollo; tras integrar en `main`, la cadena M06→M07→M08 debe recertificarse sobre el commit final, pues el M07 heredado puede haber cambiado de revisión.

## Criterio para extender a M07 y M06

No copiar reglas de poda automáticamente sin examinar los patrones de cada módulo. La simplificación debe respetar las decisiones técnicas específicas y los contratos de reconstrucción, y cada módulo debe tener un CI propio de punta a punta.
