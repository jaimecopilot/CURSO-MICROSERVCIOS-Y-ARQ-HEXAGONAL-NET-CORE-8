# Revisión visual de los PDF de M02 y M03

Fecha: 2026-11-11. Revisión de solo lectura de los cuatro PDF regenerados en el entorno local. No se han modificado los PDF, sus Markdown ni los generadores durante esta revisión.

## Alcance y método

Se renderizaron y se inspeccionaron visualmente **las 253 páginas** mediante **31 hojas de contacto**. Cada miniatura conserva la página completa, con 400 píxeles de ancho, en hojas de 1260 × 1860 píxeles y hasta nueve páginas por hoja. Esta revisión global permite detectar distribución anómala, páginas vacías, colisiones grandes, desbordamiento de tablas y figuras cortadas; no equivale a leer íntegramente cada página al tamaño de impresión.

Además, se renderizaron y se inspeccionaron **33 páginas completas a 144 ppp**, aproximadamente 1191 × 1684 píxeles por página A4. Estas ampliaciones cubren los cambios SQL Server/Testcontainers, los tres diagramas nuevos relacionados con dichos cambios y muestras de explicaciones de código de los ocho puntos de M02 y M03.

Se utilizó PyMuPDF (`fitz`) para el renderizado y `view_image` para observar las imágenes. Las imágenes y el manifiesto de esta sesión están en `.qa/pdf-m02-m03/`; son evidencia temporal de revisión, no entregables del curso. El manifiesto distingue las hojas de contacto de las ampliaciones. La extracción textual auxiliar y la búsqueda de marcas editoriales se usaron como complemento; no sustituyen la inspección visual.

## Páginas efectivamente inspeccionadas

La numeración es la página física del PDF, empezando en 1.

| Documento | Inspección completa en hojas de contacto | Páginas ampliadas a 144 ppp |
|---|---|---|
| M02 prácticas | 1–64, ocho hojas | 14, 15, 16, 17, 18, 19, 25, 39, 51 |
| M02 teoría | 1–46, seis hojas | 7, 11, 12, 13, 14, 16, 26, 38 |
| M03 prácticas | 1–84, diez hojas | 1, 18, 38, 60, 75, 76, 77, 83 |
| M03 teoría | 1–59, siete hojas | 3, 19, 25, 33, 44, 56, 57, 58 |

Se observaron todas las hojas identificadas por `*_contact_*`. Las ampliaciones corresponden a los archivos `*_pNNN_144dpi.png`. No se afirma una lectura ampliada de las otras 220 páginas.

## Comprobaciones de los cambios de persistencia

| Ubicación | Evidencia visual observada | Resultado |
|---|---|---|
| M02 teoría 11 | Diagrama de imagen, Docker Engine, contenedor, proceso de pruebas y puertos; título, leyenda y párrafos circundantes | Cajas, textos y flechas completos; sin cruces sobre etiquetas ni recortes |
| M02 teoría 12 | Fragmento `MsSqlBuilder`, seis explicaciones de líneas, puertos y alternativa de entorno | Texto y código legibles; jerarquía y separación coherentes |
| M02 teoría 13 | Diagrama de `ACERIA_TEST_SQLSERVER` y aislamiento por caso; ejemplo PowerShell y sus explicaciones | Etiqueta larga contenida; conexiones claras; código ajustado al ancho sin salir del recuadro |
| M02 teoría 14 | Registro `UseSqlServer`, explicación de tres líneas y tabla del ciclo de prueba | Tabla completa; texto de celdas contenido, sin superposición |
| M02 prácticas 14–17 | Instalación de Testcontainers, `ApiFactory`, proyecto de tests, `SqlServerPruebas.cs`, conexión y limpieza | Bloques continuados entre páginas, legibles y dentro de sus fondos; instrucciones, rutas y explicación del aislamiento visibles |
| M02 prácticas 18–19 | `GetTests`, comprobación del proveedor y caso práctico de CI | Código completo visible en la ampliación de 18; explicación y encabezados legibles |
| M03 prácticas 1 | Requisitos Docker/Testcontainers, herencia del helper y tabla de pruebas acumuladas | Tabla sin pérdida de filas ni desbordamientos; requisitos y nombres de archivo contenidos |
| M03 prácticas 75–77 | `HexagonalFactory`, los dos contextos SQL Server, limpieza, tests HTTP y lectura del aislamiento | Continuidad de los bloques visible; no hay líneas ocultas por pie de página ni recortes laterales |
| M03 teoría 25, 56 | Explicaciones del adaptador y los dos modos de prueba | Terminología y nombres largos caben; espaciado regular |
| M03 teoría 57 | Diagrama puerto/adaptador/proveedor/motor y tabla de responsabilidades | Flecha discontinua, rótulos y recorrido separados; tabla legible y completa |
| M03 teoría 58 | Código de las dos bases, seis explicaciones y tabla de evidencias | Código y explicaciones claramente diferenciados; tabla contenida y enlaces visibles |

Los diagramas nuevos ampliados son los de M02 teoría 11 y 13 y M03 teoría 57. Se comprobó la legibilidad visual de sus etiquetas y la ausencia de colisiones; esta revisión no sustituye la verificación semántica ni la ejecución de los ejemplos.

## Muestras de explicación de código por punto

| Punto | Muestra de teoría ampliada | Muestra de prácticas ampliada | Observación |
|---|---|---|---|
| 2.1 | 7 y 12–14 | 14–19 | Bloques diferenciados, viñetas legibles, explicación del aislamiento bien separada |
| 2.2 | 16 | 25 | Record y sus líneas explicadas; instrucciones y explicación del PUT legibles |
| 2.3 | 26 | 39 | Explicaciones del contrato y filtro legibles; se registra abajo una mejora de paginación del record |
| 2.4 | 38 | 51 | YAML y explicación por líneas; código de configuración con fondo y márgenes consistentes |
| 3.1 | 3 | 18 | Explicaciones con nombres de línea en negrita; continuaciones largas conservan sangría de lista |
| 3.2 | 19 | 38 | Código del puerto y adaptador, resumen y test; viñetas sin solapamientos |
| 3.3 | 33 | 60 | Árbol de proyectos, explicación de sus líneas, resumen y test legibles |
| 3.4 | 44 | 83 | Registro DI y explicación; resumen y test con separación coherente |

Los bloques largos se fragmentan entre páginas y algunas instrucciones largas se ajustan visualmente a más de una línea. En las ampliaciones inspeccionadas no se han encontrado caracteres recortados ni texto superpuesto al borde del bloque. No se ha comprobado mediante esta revisión la fidelidad del pegado desde el PDF al editor.

## Hallazgos

No se detectaron colisiones de texto, recortes laterales, figuras amputadas, páginas completamente en blanco ni tablas con contenido perdido en el recorrido visual global. Las tablas examinadas en detalle conservan sus bordes y el contenido de sus celdas. La tabla de catálogo de M02 teoría 22–23 continúa con encabezado repetido, según la hoja de contacto.

Se registran dos **mejoras menores de paginación**, sin pérdida de contenido:

1. **M02 teoría 25–26:** el record corto `CrearOrdenRequest` empieza al final de 25 y deja `int Cantidad);` como primera línea de 26. La continuidad se observó en la hoja de contacto y el fragmento de 26 se amplió. Sería más cómodo mantener este bloque corto en una sola página.
2. **M03 prácticas 83–84:** el cierre «Resultado verificable y cierre del punto 3.4» queda solo al inicio de la última página 84, con mucho espacio libre debajo. Se observó en la hoja de contacto; la página no está vacía. Agrupar el cierre con el contenido precedente podría mejorar la economía de paginación.

Las últimas páginas de M02 teoría y M03 teoría también tienen espacio libre propio del cierre del documento; no se consideraron páginas en blanco ni evidencia de contenido omitido. No se han aplicado correcciones, por tratarse de una revisión de solo lectura.

## Referencias editoriales en prácticas

En la observación de las páginas ampliadas no aparecieron rótulos de procedencia editorial. Una búsqueda complementaria sobre el texto de las **148 páginas de prácticas** no encontró las marcas `fuente` como palabra, `editorial`, `documento original`, `manual original`, `Gemini`, `ChatGPT`, `adaptado` como palabra ni `extraído` como palabra.

Las menciones «Archivo de trabajo», «Archivo completo», «Referencia de código» y «Código final de referencia» observadas describen archivos y etapas del proyecto que el alumno debe utilizar. No son atribuciones editoriales a un documento fuente. La búsqueda tiene un vocabulario explícito y no certifica la ausencia de toda formulación posible de procedencia.

## Identificación exacta de los PDF revisados

| Ruta desde la raíz del repositorio | Páginas | SHA-256 |
|---|---:|---|
| `M02_APIS_REST_ASPNET_CORE/PRACTICAS/M02_PRACTICAS.pdf` | 64 | `c957d5249813bcd194ec398a6c990ffb3715b894c17307c2f0adc85fffb0121e` |
| `M02_APIS_REST_ASPNET_CORE/TEORIA/M02_TEORIA.pdf` | 46 | `af01f43c02ffd98ecb3f32b3fdcf83c57c8e92836f1e9296cf3055065ef79b06` |
| `M03_ARQUITECTURA_HEXAGONAL/PRACTICAS/M03_PRACTICAS.pdf` | 84 | `0592a2ebb0fd51d13ccdae11cc2f4ebb8c7b25706d719a74a9a51741be7c4719` |
| `M03_ARQUITECTURA_HEXAGONAL/TEORIA/M03_TEORIA.pdf` | 59 | `0242778884b66cffb57ab6ab256e7d9628d67a0e7fc2c9a719b599fab150ef4e` |

Estos son los PDF locales inspeccionados. El contraste con los PDF producidos por CI queda fuera de esta sesión de revisión: debe compararse su versión final y, si cambian la composición o la paginación, volver a observar las páginas correspondientes. La inspección visual tampoco acredita que se haya ejecutado SQL Server, Docker o Visual Studio.
