# Revisión visual de teoría — M06

**Resultado:** revisión visual y comprobaciones documentales satisfactorias para el PDF de teoría generado. Esta revisión no sustituye la ejecución de las prácticas ni acredita prestaciones de un despliegue productivo.

## Documentos revisados

- `TEORIA/M06_TEORIA.md`: 16.168 palabras, 30 bloques y 30 ampliaciones didácticas.
- `TEORIA/M06_TEORIA.pdf`: 41 páginas A4.
- `GRAFICOS/comunicacion_microservicios.svg` y su PNG: mapa general.
- Nueve diagramas de detalle en `TEORIA/IMAGENES`, tres por punto; cada SVG tiene un PNG de 1220 × 760 píxeles.

## Método y resultados

Se inspeccionaron las 41 páginas renderizadas en seis hojas de contacto durante la revisión inicial y se repitió la revisión completa de la versión final en cuatro contactos. Se revisaron además a mayor resolución las páginas 6, 20, 25, 38 y 41, que contienen el cliente HTTP, publicación RabbitMQ, diagrama de inbox, matriz de decisión y tabla de rutas/bibliografía. Se inspeccionaron los diez diagramas en una hoja de contacto y se verificó el diagrama de inbox después de su última corrección.

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

## Comprobación conjunta final

Las rutas, `OrdenPlanificadaV1`, `Version = 1`, outbox, inbox, huella del payload, DLQ y sondeo didáctico con `BasicGetAsync` se cotejaron con las prácticas integradas. Se corrigió la ruta de partida a `M05_DDD_CQRS/PROYECTO/5.5-dominio-aceria` y se alinearon tipo y clave de enrutamiento con `orden.planificada.v1`. El ejemplo de transporte identifica `MessageId` como metadato opcional; el receptor implementado deduplica por `EventoId` del JSON. Se ampliaron las páginas finales 1, 19 y 20 para revisar estas correcciones.

El PDF de prácticas se ha revisado por separado en `REVISION_VISUAL_PRACTICAS.md`. La comprobación documental distingue los ejemplos conceptuales de las capacidades implementadas; la ejecución de las pruebas y del recorrido entre procesos conserva su evidencia técnica independiente.

## Reproducción

```bash
python .github/scripts/m06_crear_figuras.py
python .github/scripts/m06_generar_pdf.py --solo TEORIA
```

Las dependencias del generador de figuras son CairoSVG y su soporte Cairo. El generador PDF utiliza Markdown o Mistune, BeautifulSoup, WeasyPrint y PyMuPDF. `--solo PRACTICAS` renderiza únicamente el manual; sin `--solo` se validan ambos documentos.

## Identidad de los archivos revisados

- SHA-256 Markdown: `490836081f31be85e6a929befccd3f832c1b94756720d8295482a0aa62a11ceb`.
- SHA-256 PDF: `e2d2db90ff8bce8763472ed2b72f466069b9f8aac054bc79da3126ea7c892a05`.

El informe automático de cobertura y geometría queda en `REPORTE_PDF_M06.json`.
