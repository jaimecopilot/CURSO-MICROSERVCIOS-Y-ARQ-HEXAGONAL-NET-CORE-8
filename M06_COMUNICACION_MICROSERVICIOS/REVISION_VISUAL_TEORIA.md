# Revisión visual de teoría — M06

**Resultado:** revisión visual y comprobaciones documentales satisfactorias para el PDF de teoría generado. Esta revisión no sustituye la ejecución de las prácticas ni acredita prestaciones de un despliegue productivo.

## Documentos revisados

- `TEORIA/M06_TEORIA.md`: 16,140 palabras, 30 bloques y 30 ampliaciones didácticas.
- `TEORIA/M06_TEORIA.pdf`: 41 páginas A4.
- `GRAFICOS/comunicacion_microservicios.svg` y su PNG: mapa general.
- Nueve diagramas de detalle en `TEORIA/IMAGENES`, tres por punto; cada SVG tiene un PNG de 1220 × 760 píxeles.

## Método y resultados

Se inspeccionaron las 41 páginas renderizadas en seis hojas de contacto. Se revisaron además a mayor resolución las páginas 6, 20, 25, 38 y 41, que contienen el cliente HTTP, publicación RabbitMQ, diagrama de inbox, matriz de decisión y tabla de rutas/bibliografía. Se inspeccionaron los diez diagramas en una hoja de contacto y se verificó el diagrama de inbox después de su última corrección.

| Comprobación | Resultado |
|---|---|
| Bloques teóricos | 30; diez por cada punto |
| Ampliaciones | 30; una por bloque, con cuatro apartados aplicados |
| Diagramas únicos referenciados | 10; un mapa y nueve detalles |
| Pares SVG/PNG | 10; SVG XML válido, título accesible y PNG con dimensiones esperadas |
| Explicaciones en viñetas separadas | 184 |
| Referencias Línea N contra línea física del ejemplo | 184 verificadas, incluidas posiciones de líneas vacías |
| Bloques HTML presentes en PDF | 579 de 579 |
| Bloques omitidos | 0 |
| Páginas vacías | 0 |
| Palabras fuera del área de página | 0 |
| Tablas, diagramas y pies | Sin recortes ni superposición observados |
| Cabeceras de punto y objetivos | Agrupados para evitar un título separado de sus objetivos |
| Fragmentos de código que caben en una página | Se mantienen unidos para evitar llaves huérfanas |

## Ajustes realizados durante la revisión

Se acortaron etiquetas de conectores para que no rozaran las tarjetas. Los diagramas tienen fondo opaco, texto vectorial y versiones PNG consistentes. La tarjeta de inbox distingue tratamiento de errores de formato/versión y fallos técnicos. El PDF mantiene cada figura con su interpretación, evita dividir innecesariamente bloques de código y conserva la numeración física de los ejemplos.

La revisión técnica del texto distingue `await` de bloqueo de hilo, HTTP/3 sobre QUIC, 404 frente a 500, disposición de respuestas, cancelación, observación frente a reserva, confirms frente a ack y efecto idempotente local frente a una promesa global de entrega exactamente una vez. También corrige Saga, Event Sourcing y la matriz de decisión.

## Alcance pendiente de comprobación conjunta

Las rutas, `OrdenPlanificadaV1`, `Version = 1`, outbox, inbox, huella del payload, DLQ y sondeo didáctico con `BasicGetAsync` se alinearon con el contrato de implementación del módulo. La integración final debe cotejar esta descripción con las prácticas terminadas y su evidencia ejecutada. No se ha renderizado ni revisado el PDF de prácticas en este encargo parcial.

## Reproducción

```bash
python .github/scripts/m06_crear_figuras.py
python .github/scripts/m06_generar_pdf.py --solo TEORIA
```

Las dependencias del generador de figuras son CairoSVG y su soporte Cairo. El generador PDF utiliza Markdown o Mistune, BeautifulSoup, WeasyPrint y PyMuPDF. `--solo PRACTICAS` permite renderizar la otra entrega cuando su contenido esté completo; sin `--solo` se validan ambos documentos.

## Identidad de los archivos revisados

- SHA-256 Markdown: `10345b233ba407d83c635332c837300f087a4657b38e0464a1bb7740f1e5506e`.
- SHA-256 PDF: `5042740a8db5944dc0229bf01fc652aed4cc6abd0e6dd8c73a82a48fd069ef87`.

El informe automático de cobertura y geometría queda en `REPORTE_PDF_M06.json`.
