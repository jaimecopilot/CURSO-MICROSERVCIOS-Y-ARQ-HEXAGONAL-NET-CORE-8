# Revisión visual de prácticas — M07

**Resultado:** revisión visual satisfactoria de las 267 páginas del manual identificado por las huellas de este informe. No se modificó el contenido del manual durante la revisión ni fue necesario regenerar los PDF después de la generación final.

## Documento y cobertura

El manual contiene 88.808 palabras, 96 pasos guiados, cuatro retos resueltos y cuatro recorridos funcionales en PowerShell. Su comprobación editorial incluye 2.662 explicaciones de código con referencias a líneas físicas: las líneas vacías cuentan en la numeración y su explicación se conserva cuando está incluida en la fuente.

| Comprobación | Resultado |
|---|---|
| Páginas A4 | 267 |
| Pasos guiados | 96; 24 por punto y en orden |
| Retos de ampliación con solución | 4 |
| Recorridos funcionales | 4; puntos 7.1, 7.2, 7.3 y 7.4 |
| Referencias de línea física | 2.662 comprobadas |
| Bloques HTML presentes en el PDF | 4.402 de 4.402 |
| Bloques omitidos | 0 |
| Páginas vacías | 0 |
| Palabras fuera de página | 0 |
| Tablas, párrafos, código y pies de página | Sin recortes ni superposiciones observadas |

## Método y observaciones

Se renderizaron las 267 páginas a 72 dpi y se recorrieron todas mediante 23 hojas de contacto, con doce páginas por contacto salvo el último. Se inspeccionaron individualmente las páginas 13, 82, 109, 141, 202 y 241: correlación y OnStarting, registro de las sondas, ensayo de caída de dependencias, manejador de errores, canalización de resiliencia y recuperación del circuito desde PowerShell. Esta selección amplía la inspección general en los bloques funcionales de los cuatro puntos.

Las páginas 9, 16, 45, 54, 73, 77, 166 y 233 presentan espacio libre porque el bloque de código siguiente cabe completo en una página y se conserva unido. La página 189 cierra el punto 7.3 y el punto 7.4 empieza en la siguiente página. Estas páginas se revisaron en sus respectivos contactos: el espacio libre no procede de una omisión de texto. Los listados que superan una página fluyen entre páginas; se comprobó la continuidad visual y la cobertura textual completa. La última página, 267, contiene el cierre del reto y el resultado esperado del módulo.

El manual usa la tipografía y los márgenes del generador precedente del curso. Las rutas largas y las líneas de código se ajustan al ancho disponible. Una línea física del código puede ocupar varias líneas visuales del PDF; las referencias Línea N siguen contando la línea física original, incluidas las vacías. Esta distinción se valida automáticamente y no se recalcula a partir del salto visual de línea.

La revisión visual no sustituye la reconstrucción desde el manual ni las pruebas ejecutables de SQL, RabbitMQ, HTTP y resiliencia. Los resultados de esas comprobaciones se documentan en los informes de validación correspondientes.

## Reproducción

```bash
python .github/scripts/m07_generar_pdf.py --solo PRACTICAS
```

Sin la opción `--solo`, el generador procesa teoría y prácticas y escribe el informe conjunto `REPORTE_PDF_M07.json`. Valida los 96 pasos, las cuatro soluciones de reto, las citas de línea física, la cobertura completa del texto y la geometría de página antes de dar por generado cada archivo.

## Identidad de los archivos revisados

- SHA-256 Markdown: `e55780210e16e2affe1ca21f606ce4c3a8eba59d0ec66150027db7aae14a9bb9`.
- SHA-256 PDF: `c56f2c5a4d7e8d0af43660f1ca9bcec16037b787445924082559ad475807c4f0`.
- Tamaño PDF: 700.922 bytes.

Estas huellas corresponden a los archivos locales inspeccionados. El cotejo con el artefacto final de CI se debe realizar después de descargarlo; este informe no da por acreditada una equivalencia todavía no comprobada.

## Cotejo con la publicación de CI

La ejecución integral [43013439346](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43013439346) generó el PDF publicado con SHA-256 `18b5a4dfc8f952af3c2d165e73998be62b77bf43779ebe459fb928c825c3b688`. Sus 267 páginas coinciden píxel a píxel a 86,4 dpi con el PDF local identificado en este informe. No se observaron diferencias visuales. El resultado y ambas huellas están en COTEJO_PDF_CI.json.
