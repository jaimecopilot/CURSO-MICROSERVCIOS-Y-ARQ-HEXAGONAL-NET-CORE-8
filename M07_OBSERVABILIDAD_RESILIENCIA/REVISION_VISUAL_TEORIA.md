# Revisión visual de teoría — M07

**Resultado:** revisión visual y comprobaciones documentales satisfactorias para la versión de teoría identificada por los hashes de este informe. Esta revisión no sustituye las pruebas ejecutables ni acredita un despliegue productivo.

## Documentos revisados

- `TEORIA/M07_TEORIA.md`: 19.523 palabras, cuarenta bloques y cuarenta ampliaciones aplicadas a AceriaApp.
- `TEORIA/M07_TEORIA.pdf`: 51 páginas A4.
- Doce diagramas en `TEORIA/IMAGENES`: tres por punto, cada uno con versión SVG vectorial y PNG de 1220 × 760 píxeles.

## Método

La versión final de cincuenta y una páginas se renderizó a 72 dpi y se inspeccionó completa mediante nueve hojas de contacto. Se abrieron además las páginas 11, 35 y 49 individualmente para comprobar la figura de selección de datos, el inicio del código y las cabeceras. La fase anterior de revisión había examinado las doce figuras en un contacto y ampliado el diagrama del circuito; en la versión final se volvió a abrir la figura de datos, cuyo pie se había actualizado para delimitar el alcance del logging.

Se compararon los cuarenta títulos de bloque con los cuatro puntos originales: coinciden en orden y contenido. Se comprobó el XML y el título accesible de las doce figuras SVG y las dimensiones de sus correspondientes PNG. La página 51 contiene la bibliografía y presenta menor densidad de contenido, sin ser una página vacía. Las figuras y sus interpretaciones permanecen juntas.

| Comprobación | Resultado |
|---|---|
| Bloques teóricos | 40; diez por punto y en el orden original |
| Ampliaciones didácticas | 40; una por bloque, con cuatro apartados aplicados |
| Diagramas únicos referenciados | 12; tres por punto |
| Pares SVG/PNG | 12; XML válido, título accesible y dimensiones correctas |
| Explicaciones en viñetas separadas | 272 |
| Citas Línea N contra línea física del ejemplo | 272 verificadas; las líneas vacías cuentan en la posición |
| Bloques HTML presentes en PDF | 776 de 776 |
| Bloques omitidos | 0 |
| Páginas vacías | 0 |
| Palabras fuera de página | 0 |
| Objetivos de aprendizaje | Listas separadas y agrupadas con la cabecera del punto |
| Tablas, ejemplos y diagramas | Sin recortes ni superposiciones observadas |
| Figuras e interpretación | Se mantienen agrupadas |

## Correcciones y sincronización técnica

Se corrigieron seis niveles de logging frente a la enumeración que decía cinco; se mantienen propiedades estructuradas y la correlación validada de 1–64 caracteres ASCII. Los nuevos eventos propios de M7 —resumen HTTP, excepciones y callbacks de Polly— evitan registrar datos de clientes, URLs completas y excepciones libres. Esta comprobación no constituye una auditoría del logging heredado de workers M6 o EF. CamposHttpSeguros elimina RequestPath después de FromLogContext; Response.OnStarting conserva X-Correlation-ID incluso si el manejador limpia la respuesta de error. Se distingue la correlación de una implementación completa de tracing y la consola JSON de una garantía de conservación de auditoría.

La teoría diferencia live, ready y startup; la caída de una dependencia no se presenta como causa de reinicio del proceso. El ejemplo de rutas usa filtros distintos, y se explica el límite de IsOpen frente a una comprobación AMQP real. Disponibilidad de sonda, disponibilidad funcional y progreso del outbox son conceptos separados. Se aclara que Docker HEALTHCHECK marca salud y no reinicia por sí solo.

Los contratos de implementación se cotejaron con las decisiones finales de observabilidad: Observabilidad:NivelMinimo, Information predeterminado y Warning en Production; live sin checks externos; ready con tres comprobaciones SQL en Producción y una en Inventario, más RabbitMQ si los workers están activos; Degraded y Unhealthy traducidos a 503. Las respuestas de salud excluyen descripciones y excepciones internas.

Se usa IExceptionHandler de ASP.NET Core 8 y se actualiza ProblemDetails a RFC 9457. Se preservan los códigos de Result, la indisponibilidad 503, cancelación y respuesta iniciada. El estado 499 sin cuerpo se explica como convención local para una petición cancelada, no como un estado HTTP estándar ni como garantía de entrega al cliente desconectado. El error 500 mantiene título público genérico, traceId y correlationId, con salida JSON coherente cuando Accept no selecciona el escritor habitual.

Polly utiliza API v8: dos reintentos, demora base de 200 ms exponencial con jitter, circuito con cuatro muestras y ratio 0,5 en diez segundos, apertura de cinco segundos, timeout de intento de un segundo y total de seis. Se explican SelectPipelineByAuthority, el cuerpo HTTP dentro del presupuesto, cancelación cooperativa, Retry-After, ausencia de reintentos mutantes y la diferencia entre indisponibilidad y stock cero. Los ejemplos anteriores de Policy/WrapAsync se identifican como API antigua y no se usan como implementación. No se desarrolla M8 ni se promete una duración fija de laboratorio.

## Reproducción

```bash
python .github/scripts/m07_crear_figuras.py
python .github/scripts/m07_generar_pdf.py --solo TEORIA
```

El generador de figuras requiere CairoSVG y Cairo. El PDF utiliza Markdown o Mistune, BeautifulSoup, WeasyPrint y PyMuPDF. El generador valida cuarenta bloques, cuarenta ampliaciones y doce figuras en teoría; para prácticas valida noventa y seis pasos y cuatro retos. `--solo PRACTICAS` genera únicamente el manual; sin la opción se procesan ambos documentos.

## Identidad de los archivos revisados

- SHA-256 Markdown: `18c1554b25528c4d9a67c8710bddd6e06d87cea3893d2041d5a85a103fcdb653`.
- SHA-256 PDF: `139d8480f663b6fe977eb0092cc9e97e472bc6144dcde61a2fa967f849854433`.

El informe automático de cobertura y geometría queda en `REPORTE_PDF_M07.json`. La revisión visual del manual se documenta por separado en REVISION_VISUAL_PRACTICAS.md. Este informe identifica los archivos locales revisados; la equivalencia con el artefacto final de CI requiere comparar sus huellas tras descargarlo.

## Cotejo con la publicación de CI

La ejecución integral [43013439346](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43013439346) generó el PDF publicado con SHA-256 `cce0367c06a74ad739340362e492865ddc63eb35e8a1a190764af02ea100eb9f`. Sus 51 páginas coinciden píxel a píxel a 86,4 dpi con el PDF local identificado en este informe. No se observaron diferencias visuales. El resultado y ambas huellas están en COTEJO_PDF_CI.json.
