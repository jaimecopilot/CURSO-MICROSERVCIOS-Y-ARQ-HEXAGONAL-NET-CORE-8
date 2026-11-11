# Revisión visual de prácticas — M06

**Resultado:** revisión visual y documental satisfactoria de la versión final. Se inspeccionaron las 146 páginas del PDF en trece hojas de contacto y se ampliaron quince páginas para revisar las partes de mayor densidad o modificadas durante el cierre.

## Documentos revisados

- `PRACTICAS/M06_PRACTICAS.md`: 46.190 palabras, 72 pasos y 92 operaciones de construcción.
- `PRACTICAS/M06_PRACTICAS.pdf`: 146 páginas A4.
- Tres retos optativos con código, explicaciones y comprobación, aplicables a copias independientes.

## Método y resultados

La revisión general abarcó todas las páginas y los tres puntos. Las ampliaciones finales se hicieron en las páginas 1, 63, 65, 66, 67, 68, 72, 78, 99, 100, 101, 104, 119, 140 y 146. Comprenden portada y recuentos, conflictos de concurrencia, versión de la raíz, persistencia SQL, transporte RabbitMQ, receptor idempotente, prueba de interrupción después de publicar, recorrido de dos procesos, flujo híbrido y cierre del último reto.

| Comprobación | Resultado |
|---|---|
| Primer título de la primera página | M06 — Prácticas integrales: comunicación entre microservicios con .NET 8 |
| Pasos obligatorios | 72; veinticuatro por punto, en orden |
| Operaciones de construcción | 92; distribución 32, 40 y 20 |
| Retos con solución y comprobación | 3 |
| Explicaciones en viñetas separadas | 941 |
| Referencias Línea N contra línea física | 941 de 941 verificadas |
| Líneas vacías explicadas | 140; incluidas en la verificación física |
| Bloques HTML presentes en PDF | 2346 de 2346 |
| Bloques omitidos | 0 |
| Páginas vacías | 0 |
| Palabras fuera del área de página | 0 |
| Tablas, código y numeración | Sin recortes, solapes ni caracteres ilegibles observados |
| Recuentos declarados de pruebas por etapa | 232, 264 y 283; consistentes en portada, pasos y cierre |
| Proyectos y documentos declarados por etapa | 27/30, 28/32 y 29/34 |

## Ajustes comprobados

Se eliminó la referencia obsoleta a concentrar la implementación funcional en el paso 16: el manual identifica los pasos de incorporación y reserva el paso 16 para compilar. Se corrigieron espacios entre prosa y códigos HTTP/cantidades.

Las explicaciones de `CreateChannelOptions` distinguen el canal con confirms de publicación del canal de consumo. La disposición de la conexión describe sustitución y cierre. Las explicaciones de `SaveChangesAsync` se contextualizan: estado y outbox en el planificador, marcado posterior a confirmación en el despachador, inbox/proyección en el receptor y preparación de datos en pruebas o arranque.

La versión `Revision` de la raíz se incrementa tras mutaciones de líneas y estado y se configura como token de concurrencia. Los archivos de dominio, aplicación y persistencia señalan el conflicto traducido a HTTP 409 y las operaciones de reemplazo correspondientes. Las descripciones distinguen las pruebas SQL de `OutboxInboxTests` de la prueba con broker real que publica, falla al marcar, reintenta y verifica un único efecto local en `RabbitMqTests`.

Se corrigió un salto excesivo antes de un archivo de código mayor que una página. El generador permite que los listados largos continúen desde el espacio disponible, mientras mantiene juntos los fragmentos cortos. La revisión final de todos los contactos confirma la continuidad de los listados y sus explicaciones; este ajuste redujo de 151 a 146 páginas sin omitir contenido. El PDF de teoría conserva el mismo hash tras este ajuste exclusivo de maquetación.

## Coherencia del recorrido

La consulta HTTP de disponibilidad se presenta como informativa. El manual no atribuye reserva ni descuento de stock a la planificación. La API de Producción conserva su frontera con Inventario, y la planificación integrada utiliza la ruta de comunicación. El 202 acredita aceptación local; la lectura de la proyección puede devolver 404 mientras el evento esté pendiente y 200 tras procesarlo.

Las secciones revisadas distinguen confirmación del broker, commit SQL y ack del consumidor. El receptor compara identidad y huella del contenido. Los errores incompatibles se dirigen a la cola de errores y los fallos técnicos permiten reintento. El sondeo `BasicGetAsync` se presenta como recurso didáctico. Las referencias Línea N corresponden al texto físico del bloque mostrado, aunque una línea larga se ajuste visualmente a varias líneas del PDF.

## Alcance de la revisión

Este informe acredita maquetación, cobertura y coherencia documental de las secciones revisadas. La ejecución de compilación, pruebas SQL Server/RabbitMQ y recorrido HTTP se comprueba mediante sus informes técnicos y CI; no se deduce de la apariencia del PDF. No quedan incidencias visuales conocidas en esta versión.

## Reproducción

```bash
python .github/scripts/m06_generar_pdf.py
```

El generador valida ambos Markdown, las explicaciones, la cobertura del PDF y la geometría de página. Las dependencias son Markdown o Mistune, BeautifulSoup, WeasyPrint y PyMuPDF.

## Identidad de los archivos revisados

- SHA-256 Markdown: `b27b9d3a438691168e8f54694aeb98e6db38432709134540a3c1a6448e7f7751`.
- SHA-256 PDF: `dc933176e0bb45c511e3c7bf9b1e4e5dfd152fbf9c0db45d4cb8e554283cde0b`.

El informe automático de ambos documentos queda en `REPORTE_PDF_M06.json`.
