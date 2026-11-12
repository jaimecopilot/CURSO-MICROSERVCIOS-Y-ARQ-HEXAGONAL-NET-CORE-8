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

Esta revisión **no se considera publicable** hasta contar con:
- una nueva ejecución correcta de CI sobre esta rama para Linux SQL Server/RabbitMQ + YARP E2E + Windows LocalDB;
- nuevos PDF y sus informes de páginas, geometría y cobertura;
- evidencias con hashes de la revisión exacta;
- inspección visual/manual de una muestra representativa de páginas y comparación pedagógica.

Las pruebas automatizadas acreditan la equivalencia del código ejecutable; no sustituyen la revisión editorial de calidad o claridad por un docente.

## Criterio para extender a M07 y M06

No copiar reglas de poda automáticamente sin examinar los patrones de cada módulo. La simplificación debe respetar las decisiones técnicas específicas y los contratos de reconstrucción, y cada módulo debe tener un CI propio de punta a punta.
