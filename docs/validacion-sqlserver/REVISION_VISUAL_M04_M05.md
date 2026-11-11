# Revisión visual de los PDF M04 y M05

Fecha: 2026-11-11. Revisión local mediante PyMuPDF (`fitz`) y visualización real de los PNG/JPG renderizados. La numeración indicada es la página física del PDF, empezando en 1.

## Alcance y método

Se inspeccionaron visualmente las **417 páginas de la primera versión**: M04 teoría 65, M04 prácticas 141, M05 teoría 65 y M05 prácticas 146. Se usaron 19 hojas de contacto, de hasta 24 páginas cada una, con miniaturas renderizadas a 32,4 dpi. Esta revisión global busca páginas vacías, contenido cortado, solapes evidentes, cambios de densidad, continuidad de tablas y posición de figuras; no permite certificar cada carácter pequeño.

Se ampliaron y leyeron visualmente **74 páginas completas a 108 dpi** de esa versión, seleccionadas por los cambios de SQL Server, rollback, Testcontainers, BaseSqlServer, unidad de trabajo, pruebas y explicación del código. Se añadió un recorte a 216 dpi del conector «responde» de M04 teoría p. 2. Las tablas nuevas y los diagramas de rollback y CQRS se revisaron a página completa.

Después de corregir la separación de las listas de objetivos, se inspeccionaron las **67 páginas de M05 teoría regenerado** en tres hojas de contacto nuevas y diez páginas completas a 108 dpi. También se comprobó M04 teoría p. 2 regenerada a 108 dpi y su conector a 216 dpi, cerrando V02. El total de ampliaciones completas observadas es 85 (74 iniciales, diez de M05 y una de M04 tras las correcciones). La nueva versión total de los cuatro documentos tiene 419 páginas. El alcance no es una lectura palabra por palabra de las 419 páginas a máxima resolución: combina cobertura visual global y ampliación dirigida. No se ejecutaron aquí pruebas .NET ni se sustituyó la verificación automatizada de texto y límites realizada por el proceso principal.

Evidencia local:

- `.qa/pdf-m04-m05/inventory.json`: inventario, huellas iniciales, páginas y selección inicial.
- `.qa/pdf-m04-m05/*-contact-*.jpg`: las 19 hojas de contacto iniciales.
- `.qa/pdf-m04-m05/*-108dpi.png`: las 74 ampliaciones iniciales.
- `.qa/pdf-m04-m05/M04_TEORIA-p002-connector-216dpi.png`: detalle del defecto inicial del conector.
- `.qa/pdf-m04-m05/after/`: nueva paginación y ampliaciones de M05 teoría.

## Documentos y huellas de la versión inspeccionada

| Documento | Páginas iniciales | SHA-256 inicial |
| --- | ---: | --- |
| `M04_PATRONES_ARQUITECTURA/TEORIA/M04_TEORIA.pdf` | 65 | `6f360f640d619212dc99e5c979eaa04df41232034eef4890128736841c1ad52d` |
| `M04_PATRONES_ARQUITECTURA/PRACTICAS/M04_PRACTICAS.pdf` | 141 | `591bf8c44f01dd4ca769836331a936406352f6f5db815a536f13d0ae5abb5e51` |
| `M05_DDD_CQRS/TEORIA/M05_TEORIA.pdf` | 65 | `ef9ead04834a88526d331904f566b18da4aff49654f2df3dbdcc96b04e1021ab` |
| `M05_DDD_CQRS/PRACTICAS/M05_PRACTICAS.pdf` | 146 | `9d94abad7c78328a4f7c05988f2cf3878e654477b0a24c945dc629d4cf4e6d7e` |

M05 teoría, tras la corrección de listas: **67 páginas**, SHA-256 `7b42a23dc6e6c61540da25eb4d09b67474c9a190dc46d3fab5ce2814a3fa9946`.

M04 teoría, tras la corrección de la etiqueta: **65 páginas**, SHA-256 `1163e152f4de17ddee57e39e3300560a43b7edb4203d21ccdcf622a1db5f4536`. Las dos prácticas conservan las huellas iniciales.

## Páginas ampliadas

| PDF | Páginas inspeccionadas a 108 dpi en la versión inicial |
| --- | --- |
| M04 teoría | 2, 16, 20, 21, 25, 26, 27, 28, 39, 48, 62 |
| M04 prácticas | 1, 14, 15, 16, 38, 40, 41, 42, 43, 44, 45, 71, 72, 73, 74, 103, 104, 106, 130, 131, 132, 133 |
| M05 teoría | 2, 14, 26, 29, 32, 39, 40, 41, 52, 53, 54, 55, 64 |
| M05 prácticas | 1, 2, 15, 16, 18, 40, 42, 45, 71, 72, 73, 76, 77, 78, 79, 80, 103, 104, 106, 107, 108, 109, 131, 132, 134, 135, 137, 138 |

M05 teoría regenerado: **2, 14, 30, 42, 53, 54, 55, 56, 66 y 67**. Se verificaron de nuevo las cinco listas de objetivos, el estudio CQRS con su tabla y diagrama, y el cierre del documento.

## Hallazgos y correcciones

### V01. Listas de objetivos de M05 teoría fusionadas con el párrafo anterior

**Estado: corregido y verificado en el PDF regenerado.**

En la versión inicial, los cinco puntos mostraban «Módulo 5», «Objetivos de aprendizaje» y los primeros cinco objetivos en un párrafo corrido con guiones internos. Solo el sexto objetivo aparecía como viñeta. Se confirmó visualmente en pp. **2, 14, 29, 41 y 55**. No había texto recortado, pero la jerarquía y la facilidad de lectura eran peores que en M04.

Causa encontrada en `M05_DDD_CQRS/TEORIA/M05_TEORIA.md`: faltaban separaciones de párrafo antes del rótulo y antes del inicio de la lista; una línea vacía previa al sexto objetivo hacía que solo este último se reconociese como lista.

Con autorización del coordinador, se añadieron separaciones tras «Módulo» y tras «Objetivos de aprendizaje», y se dejó el sexto objetivo consecutivo a los otros cinco. No se cambió ninguna palabra: la comparación del texto antes/después eliminando espacios resultó idéntica. No se modificaron otros apartados.

Resultado visual confirmado en el nuevo PDF, pp. **2, 14, 30, 42 y 56**: rótulos separados, seis viñetas por punto, márgenes y separación legibles. La paginación pasó de 65 a 67 páginas. Se volvieron a revisar las 67 páginas en hojas de contacto para comprobar el efecto de la repaginación; no se observaron páginas vacías, colisiones ni tablas partidas por una fila.

### V02. Etiqueta «responde» parcialmente cubierta por los nodos del mapa general M04

**Estado: SVG, PNG y página 2 del PDF regenerado corregidos y verificados.**

En M04 teoría p. **2**, el conector de MediatR a Result tiene un hueco de 55 unidades SVG entre nodos. El fondo de la etiqueta medía 72,8 unidades. Como los nodos se pintaban después, se superponían a la etiqueta situada a la misma altura. El recorte a 216 dpi confirmó la pérdida parcial de la primera letra y el contacto con el borde derecho.

Corrección autorizada y limitada a:

- `M04_PATRONES_ARQUITECTURA/GRAFICOS/patrones_arquitectura.svg`.
- `M04_PATRONES_ARQUITECTURA/GRAFICOS/patrones_arquitectura.png`.
- `.github/scripts/m04_crear_figuras.py`, para que la regeneración conserve la corrección.

Se mantuvieron texto, tamaño, color, nodos y flechas. Solo se desplazaron verticalmente la etiqueta y su fondo, de `y=255/238` a `y=178/161`, al espacio libre encima del hueco. El generador incorpora una coordenada opcional `label_y`, utilizada únicamente por esa arista. Se ejecutaron los helpers y la sección del mapa general sin ejecutar el bucle de las otras figuras.

Se compararon las huellas de todos los SVG y PNG de M04 antes/después: solo cambiaron los dos archivos del mapa general. El PNG completo regenerado se abrió y se comprobó que «responde» es visible y no se superpone a los nodos. No se ha modificado ninguna otra figura ni PDF desde este subproceso. Después de la regeneración por el proceso principal, se abrió la página 2 del PDF nuevo a 108 dpi y un recorte a 216 dpi: la palabra «responde» se ve completa y queda separada de ambos nodos. La página conserva el mismo reparto de texto y figura. Una comparación estructural del SVG contra su versión anterior confirmó únicamente dos atributos `y` diferentes (texto y fondo).

## Observaciones de maquetación

### M04 teoría

- Cobertura global: pp. 1–65, tres hojas de contacto. Numeración, márgenes, separación de bloques y fondos de código consistentes.
- Pp. 16, 20–21: la distinción entre preparar, confirmar y revertir se ve completa. El diagrama de transacción conserva sus dos salidas y sus etiquetas; las explicaciones por líneas se leen sin colisiones.
- Pp. 25–28: el estudio de atomicidad conserva títulos, párrafos y tabla. La tabla de p. 26 contiene sus cuatro técnicas completas, sin texto que cruce las celdas. El diagrama de p. 27 muestra la primera escritura, el fallo posterior, el caso transaccional, el control negativo y el lector independiente; sus flechas y textos están íntegros. El extracto y sus siete explicaciones no se cortan.
- Pp. 39, 48 y 62: diagramas de pipeline, traducción HTTP y ámbitos de DI legibles. Los bloques de código largos continúan entre páginas dentro del ancho disponible.
- P. 65 es una página breve de documentación técnica; contiene texto y numeración, no es una página vacía.

### M04 prácticas

- Cobertura global: pp. 1–141, seis hojas de contacto.
- P. 1: instrucciones SQL Server/LocalDB/Testcontainers y tabla de resultados legibles. Las cadenas largas se ajustan al ancho de la página.
- Punto 4.1, pp. 14–16: paquete Testcontainers, helper compartido, pruebas con BaseSqlServer y sus explicaciones por líneas están completos visualmente.
- Punto 4.2, pp. 38, 40–45: se distinguen el registro SQL Server, el contrato de trabajo, `IUnitOfWork`, `CommitAsync`, el repositorio que prepara cambios, y las pruebas de rollback. La explicación de p. 43 exige una escritura previa al fallo; pp. 44–45 contienen el control `WhenNeeded`/`Never`, el contador de INSERT y la lectura independiente. Los comentarios no se confunden con el código y se conservan los saltos de página.
- Punto 4.3, pp. 71–74: mensajes, pruebas MediatR, BaseSqlServer y explicación de la liberación de recursos quedan dentro del ancho útil.
- Punto 4.4, pp. 103–104 y 106: referencias Testcontainers, prueba HTTP y factoría SQL Server legibles, con sus comentarios por líneas.
- Punto 4.5, pp. 130–133: composición scoped y tests de aislamiento/validación del contenedor legibles. La cadena empleada para validar DI está explicada como configuración que no abre conexiones.
- P. 141 es una continuación breve del aprendizaje, con texto y numeración. No es una hoja vacía accidental.

### M05 teoría

- Se revisaron las 65 páginas iniciales y las 67 páginas posteriores a V01.
- En la versión inicial, pp. 26, 32, 39–40: diagramas y explicaciones de mapeo, commit y límites transaccionales legibles; no hay texto fuera de los paneles.
- Estudio CQRS: pp. 52–55 iniciales; pp. **53–56** tras V01. La figura de p. **54** final presenta command, agregado, confirmación, base SQL Server, query y DTO sin solapes. La tabla de p. **55** final conserva todas sus filas y columnas; el código continúa desde p. 54 con las explicaciones correspondientes.
- P. 64 inicial / 65 final: el recorrido vertical mantiene los nodos y las flechas dentro del marco.
- Las referencias finales ocupan pp. 66–67 después de la repaginación. La última página es breve y contiene dos entradas de una lista continuada; no se observa truncamiento ni página en blanco. Esta revisión no ha cambiado esa distribución editorial.

### M05 prácticas

- Cobertura global: pp. 1–146, siete hojas de contacto.
- Pp. 1–2: la tabla de resultados continúa con cabecera repetida; no se corta ninguna fila. Requisitos y configuración de SQL Server quedan dentro de los márgenes.
- Punto 5.1, pp. 15–16 y 18: dominio, estados y pruebas; explicación por líneas separada del código.
- Punto 5.2, pp. 40, 42 y 45: entidad hija, raíz, value objects y pruebas de invariantes; se conservan las viñetas y referencias a líneas.
- Punto 5.3, pp. 71–73 y 76–80: configuración SQL Server, puertos, unidad de trabajo, casos de uso, Testcontainers, pruebas y factoría compartida. Las cadenas largas se ajustan visualmente; no salen del fondo del código ni pisan el pie.
- Punto 5.4, pp. 103–104 y 106–109: puertos de lectura, handlers, registro del proveedor, pruebas CQRS, contador/estado de seguimiento y prohibición de guardado. Las explicaciones de BaseSqlServer y la comprobación del proveedor se ven completas.
- Punto 5.5, pp. 131–132, 134–135 y 137–138: mensajes, caso de uso, pruebas HTTP y cancelación. La lectura por líneas cubre los cambios del flujo; no se observan cortes ni superposición con títulos o pies.

## Referencias editoriales en las prácticas

No se observaron bibliografías, citas a libros ni referencias editoriales de fuente en las hojas de contacto ni en las páginas ampliadas de M04/M05 prácticas. Como comprobación complementaria, se extrajo el texto de las **287 páginas de prácticas** y se buscaron libros/bibliografía/editorial, Fowler, Evans, Vernon, «fuente editorial», «referencias bibliográficas» y URL HTTP/HTTPS.

No hubo coincidencias de los términos editoriales. Las diez URL encontradas eran instrucciones locales `http://localhost:5000/swagger`, cinco por documento; no remiten a fuentes editoriales. Este resultado corresponde a esa búsqueda explícita y a la inspección visual descrita, no a una afirmación de lectura manual exhaustiva de cada palabra.

## Dictamen limitado a esta revisión

M04 prácticas, M05 prácticas y M05 teoría corregido no presentan defectos visuales bloqueantes en el alcance inspeccionado. Los ejemplos ampliados y sus explicaciones por líneas son legibles; los diagramas nuevos de SQL Server/rollback/CQRS y las tablas nuevas se mantienen completos.

M04 teoría también queda sin defectos visuales bloqueantes observados tras comprobar la página 2 regenerada y cerrar V02. Las dos correcciones detectadas están documentadas con sus evidencias anteriores y posteriores. El dictamen se limita a la combinación de inspección global y ampliación dirigida descrita; no constituye una certificación de lectura manual exhaustiva ni de ejecución del código.
