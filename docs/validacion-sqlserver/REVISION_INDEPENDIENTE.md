# Revisión independiente de la corrección SQL Server M02–M05

Fecha: 11/11/2026. Base de revisión: `41d37cb84f258dcfef7ad1e94b45571cbdcc76b8`; cambios del árbol de trabajo, todavía sin commit. Revisión de solo lectura, salvo este informe. No se ejecutaron SQL Server ni Windows en esta revisión.

## Hallazgos

### P1 — El cierre no vincula Windows al código reconstruido que publica

Rutas: `.github/scripts/comprobar_localdb_http.py:81`, `.github/scripts/cerrar_validacion_sqlserver.py:15–21`, `.github/workflows/sqlserver-modulos.yml:22–96`.

En la versión inspeccionada, Windows compila los proyectos del checkout; la matriz Linux reconstruye los proyectos desde los manuales y sus artefactos sustituyen esos proyectos al cerrar. El informe Windows guarda el commit, pero no los hashes del código ejecutado. El cierre compara el manifiesto final únicamente con el informe Linux. Que ambos informes mencionen el mismo commit no demuestra que Windows haya ejecutado los archivos resultantes de la reconstrucción. Un cambio de manual que modifique el programa o su configuración, manteniendo un snapshot anterior que aún supera el HTTP, permite cerrar y publicar como validado en Windows un proyecto diferente.

Además, cada módulo Linux empieza desde el snapshot del módulo anterior del checkout: `m03_e2e_desde_practicas.py:243–250`, `m04_e2e_desde_practicas.py:217` y `m05_e2e_desde_practicas.py:230–241`. Los cuatro jobs no consumen las reconstrucciones de sus predecesores ni el cierre coteja esa continuidad. La coherencia de la cadena M02→M05 puede perderse si un manual anterior cambia y los snapshots heredados todavía no están sincronizados.

Corrección necesaria: reconstruir las bases anteriores para cada validación, ejecutar Windows sobre la misma reconstrucción, registrar un manifiesto de sus archivos ejecutables/configuración y cotejarlo contra el resultado Linux antes de publicar. Debe existir una contraprueba que rechace manifiestos distintos.

Estado: comunicado al coordinador; este confirmó que está preparando esa corrección. No se da por resuelto hasta revisar el código actualizado.

### P2 — La publicación de M02 conserva archivos ejecutables que nunca se probaron

Rutas: `.github/scripts/e2e_laboratorio_m02.py:80–86`, `.github/scripts/validar_sqlserver.py:84`.

La reconstrucción se prueba en un directorio temporal limpio, pero `publish` copia encima del destino sin eliminar archivos ausentes de la reconstrucción. Si se retira o renombra un `.cs`, un proyecto o un archivo de configuración del manual, su versión anterior permanece en `PROYECTO`. El manifiesto se calcula después de esta superposición, de modo que también firma y empaqueta ese archivo no probado. Puede cambiar la compilación o el comportamiento del proyecto entregado aunque el proyecto temporal haya pasado.

Corrección necesaria: reemplazar exactamente las carpetas y archivos ejecutables por la reconstrucción, conservando únicamente materiales editoriales explícitos, o rechazar cualquier archivo ejecutable sobrante antes de firmar. Añadir una comprobación con un archivo obsoleto en el destino.

Estado: comunicado al coordinador; pendiente de comprobar la corrección.

## Comprobaciones de revisión satisfechas

- Los 18 helpers `SqlServerPruebas.cs` tienen el mismo SHA-256. Generan nombres propios `AceriaTest_<GUID>`, fuerzan `master` para crear/eliminar y no extraen el nombre de la base de la conexión externa. La limpieza se dirige a esa base; no se detectó borrado de bases ajenas.
- No se encontraron `UseSqlite`, `UseInMemoryDatabase`, dependencias EF SQLite/InMemory ni `Skip =` en C#/csproj de los proyectos M02–M05.
- La creación SQL propaga el fallo de conexión; no se detectó sustitución silenciosa de proveedor. El host inicia Express mediante Testcontainers y propaga el código de salida del proceso hijo.
- La prueba de rollback M04 divide los comandos mediante `MaxBatchSize(1)`, provoca el fallo después del primer INSERT y compara `WhenNeeded` con el control `Never` desde otro contexto. La contraprueba exige una fila cuando no hay transacción y cero con transacción; evita que un fallo anterior a cualquier escritura simule rollback.
- Las factorías M02/M03 aíslan sus contextos; M03 utiliza bases separadas para los modelos heredado y hexagonal. Producción M05 usa SQL Server y sus pruebas leen persistencia con contextos independientes.
- Los contadores de etapas exigen todas las pruebas aprobadas; M04/M05 inspeccionan resultados TRX y sus contadores. Los retos M03–M05 se ejecutan en copias aisladas. M02 marca explícitamente sus propuestas abiertas como `MANUAL_NO_EJECUTADO`, fuera del contador de pruebas aprobadas.
- Windows usa un proceso HTTP real y verifica escritura, validación, conflicto, reinicio y recuperación del estado; M05 comprueba también las líneas y el total del agregado. Los nombres admitidos por la limpieza LocalDB están restringidos al prefijo aislado y sufijos previstos.
- El cierre exige las dos plataformas, el job documental y nueve artefactos; contrasta el commit y los hashes de proyectos Linux y de Markdown/PDF. Las automatizaciones anteriores M02–M05 delegan en el workflow común.
- La sintaxis de todos los scripts Python se comprobó con `ast.parse`, sin generar archivos auxiliares. Los informes locales M02/M03 reconstruidos que se inspeccionaron declaran `SIN_TESTS`, no un PASS SQL ficticio.

## Criterios todavía no acreditados

Esta revisión estática no acredita el resultado de las 18 etapas sobre SQL Server Express real, las ejecuciones LocalDB/HTTP de Windows, la eliminación efectiva de todas las bases ni los ocho PDF finales. Deben aportarse las ejecuciones remotas y sus artefactos de la revisión corregida. Tampoco se acredita aquí la revisión visual del PDF ni el cierre de M6. No se identificó otro fallo de ejecución concreto en el código SQL inspeccionado; ello no reemplaza esas ejecuciones.

## Verificación posterior de las correcciones — 11/11/2026

Esta sección documenta la comprobación del coordinador sobre el código corregido y la evidencia de CI; no reescribe ni convierte la revisión inicial en una segunda revisión independiente.

- **P1 resuelto.** `reconstruct_through` reconstruye desde M02 todas las bases necesarias. Windows llama a esa misma reconstrucción antes de compilar y ejecutar; `source_manifest` registra C#, proyectos y configuración normalizando los saltos de línea. El cierre contrasta su igualdad con el manifiesto Linux de la etapa final. Las contrapruebas de código antiguo y archivo omitido pasan. La copia Windows en una ruta corta preserva este manifiesto y excluye binarios anteriores. Los cuatro jobs Windows y los cuatro jobs SQL pasaron en CI 42986550628.
- **P2 resuelto.** `publish` reemplaza la etapa completa y solo conserva README editorial cuando no viene en la reconstrucción. La regresión introduce `.cs`, proyectos, configuración y targets obsoletos, comprueba su desaparición y verifica idempotencia. Pasó de nuevo junto a los otros once controles.
- La revisión visual y el contraste íntegro de los PDF publicados se documentan en `REVISION_FINAL.md`. El cierre automatizado volvió a verificar satisfactoriamente los hashes sobre los artefactos recuperados de GitHub.
