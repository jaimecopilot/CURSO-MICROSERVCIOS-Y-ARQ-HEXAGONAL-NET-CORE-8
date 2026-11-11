# Cierre de la corrección SQL Server antes de M6

Fecha: 11 de noviembre de 2026. Resultado: **CERRADO en el alcance documentado**. Las tareas 01–13 del plan están completadas. M6 puede comenzar desde el proyecto final de M05 corregido.

## Revisiones y evidencia

- Base del trabajo: `41d37cb84f258dcfef7ad1e94b45571cbdcc76b8`.
- Código y manuales ejecutados en CI: `54709859d231c8607ba0761a28f442fda285fd58`.
- Artefactos publicados por CI: `7fe7da90bab1d8e3ca6d45fc9395828b919b7555`.
- [Ejecución conjunta 42986550628](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/42986550628): diez jobs terminados en SUCCESS, incluidos cuatro SQL Server, cuatro Windows, PDF y publicación condicionada.
- El commit de cierre solo añade o actualiza evidencia documental; conserva íntegros los proyectos, Markdown docentes, PDF, scripts y workflows comprobados. La integración en main se efectúa por avance directo desde la base conocida, sin alterar el árbol probado.

## Resultado por módulo

| Módulo | Etapas reconstruidas desde las prácticas | Pruebas aprobadas por etapa | Retos programados aprobados | Bases SQL aisladas verificadas | Windows LocalDB con reinicio HTTP |
|---|---:|---|---:|---:|---|
| M02 | 4 | 3, 7, 12, 16 | No aplica: propuestas abiertas manuales | 38 | PASS |
| M03 | 4 | 23, 31, 38, 50 | 4 | 144 | PASS |
| M04 | 5 | 62, 77, 90, 105, 118 | 5 | 342 | PASS |
| M05 | 5 | 134, 153, 172, 190, 208 | 5 | 486 | PASS |

Son 18 etapas obligatorias, 14 retos programados y 1.010 aperturas de bases aisladas documentadas. Los recuentos de pruebas son acumulativos por etapa; no deben sumarse como pruebas distintas. M03/M04/M05 acreditan respectivamente 27/52/60 compilaciones intermedias.

Los cuatro informes SQL registran proveedor Microsoft.EntityFrameworkCore.SqlServer, edición Express, versión real y bases AceriaTest_ aisladas. Testcontainers inicia SQL Server; no existe sustitución por SQLite o InMemory. Los tests de dominio puro conservan su independencia de infraestructura. La prueba de rollback de M04 compara la transacción con un control sin transacción después de una primera escritura efectiva.

Windows reconstruye el código desde los manuales y ejecuta las API finales en LocalDB. Comprueba creación, lectura, validación, recurso inexistente, conflicto, cierre/reapertura del proceso y recuperación del estado persistido. M05 verifica asimismo líneas y cantidad total del agregado de Producción. Los cuatro informes acreditan limpieza de sus bases temporales.

## Trazabilidad y regresiones del cierre

Sobre los artefactos recuperados de GitHub se volvió a ejecutar `.github/scripts/cerrar_validacion_sqlserver.py` con la identidad original de CI. Resultado PASS: coincidencia del Markdown, manifiestos de proyectos, identidad del código Windows/Linux y hashes de los ocho PDF. No se hizo una nueva ejecución local de SQL Server ni Windows: esos resultados proceden de los jobs remotos citados.

`python -m unittest discover -s .github/tests -v`: **12/12 PASS**. Incluyen rechazo de evidencia sin motor real, proveedor SQLite, etapas sin ejecutar, retos fallidos, versiones ausentes, código Windows distinto, normalización de rutas y publicación con archivos obsoletos. Los hallazgos P1 y P2 de la revisión independiente inicial quedan resueltos con código, regresiones y ejecución remota; véase la adenda en REVISION_INDEPENDIENTE.md.

## Materiales y PDF

La teoría incorpora la explicación de Docker, imagen, contenedor, puertos, Testcontainers y aislamiento, junto con diagramas SVG/PNG. Las prácticas contienen requisitos e instrucciones reproducibles. Se mantienen las explicaciones de código separadas y no se introduce una carpeta FUENTE ni referencias editoriales de procedencia en las prácticas.

| Documento | Teoría, páginas | Prácticas, páginas |
|---|---:|---:|
| M02 | 46 | 64 |
| M03 | 59 | 84 |
| M04 | 65 | 141 |
| M05 | 67 | 146 |

Los ocho documentos suman **672 páginas**. La revisión visual previa combinó hojas de contacto de todas las páginas y ampliaciones dirigidas; su alcance exacto consta en REVISION_VISUAL_M02_M03.md y REVISION_VISUAL_M04_M05.md. Las 672 páginas de los PDF publicados se renderizaron a 72 dpi RGB y se compararon píxel a píxel con las versiones locales revisadas: **cero páginas diferentes**. COMPARACION_PDF_PUBLICADOS.json conserva los hashes de ambas versiones. La igualdad visual no exige que el binario PDF sea idéntico, pues puede variar su metadato.

## Alcance y observaciones no bloqueantes

- M01 no fue modificado; conserva la evidencia SQL Server Docker 1.1–1.5 y Windows LocalDB 1.1/1.5 de la ejecución 42862047382. No se afirma haber repetido M01 en esta corrección.
- Los cuatro retos de M02 son propuestas abiertas para el alumno y figuran como MANUAL_NO_EJECUTADO. No se cuentan como retos ejecutados ni se inventa una solución que el manual no proporciona. El recorrido obligatorio completo de M02 sí está reconstruido y probado con SQL Server.
- Los clics de Visual Studio no se automatizan. Windows acredita el código y las operaciones HTTP documentadas, no cada acción de la interfaz del IDE.
- Mejoras menores de paginación conservadas: un record corto de M02 teoría continúa de la página 25 a la 26; el cierre de M03 prácticas ocupa una última página breve. No hay pérdida de contenido.
- La inspección visual global y las ampliaciones dirigidas no equivalen a una lectura ampliada manual de cada carácter de las 672 páginas.

No queda una comprobación técnica obligatoria pendiente de esta corrección.
