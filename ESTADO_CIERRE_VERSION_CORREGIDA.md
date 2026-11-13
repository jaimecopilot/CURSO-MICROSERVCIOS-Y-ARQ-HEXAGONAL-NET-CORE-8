# Estado de cierre de la versión corregida del curso

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS (.NET 8)  
**Rama:** `version-corregida` (independiente de `main`)  
**Autor:** JAIME GALLO  
**Corte de auditoría:** 13 de noviembre de 2026

## 1. Regla de cierre

El material solo estará cerrado cuando se cumplan separadamente:

1. **Fidelidad editorial:** teoría y prácticas revisadas y aprobadas por el autor.
2. **Trazabilidad:** cada operación de creación o modificación indicada en prácticas produce el archivo esperado; los cambios generados por herramientas (`dotnet sln add`) se comprueban por semántica.
3. **Ejecutabilidad:** compilación, pruebas xUnit e integración real de las etapas reconstruidas, con SQL Server/RabbitMQ en los módulos que correspondan.
4. **Docker Desktop Windows:** ejecución real de M09 en el entorno solicitado, con informe de evidencias; Linux no sustituye esta certificación.
5. **Publicación:** PDF y Markdown coherentes, maquetación revisada, edición para alumnos preparada y decisión expresa de integrar en `main`.

Un PASS de PDF, una compilación de referencia o la existencia de un marcador no sustituye los demás puntos.

## 2. Qué se ha ejecutado en esta pasada

- Reparados los disparadores de los workflows M04/M05 y la activación de M06/M08 cuando cambia código o manual.
- Corregida la auditoría de paridad M06/M08 para que **falle** si detecta discrepancias.
- Creado `tools/auditar_reconstruccion_practicas.py`: compara cambios entre etapas; aplica sólo operaciones que constan en el manual a una copia de la etapa anterior; registra proyectos nuevos con `dotnet sln add`; compara texto con el proyecto final y compara semánticamente las soluciones .sln. **No copia el destino para fabricar un PASS**.
- Materializadas y comprobadas **19/19 transiciones internas** de M03–M08: **310 archivos de texto** iguales con normalización inocua y **19 soluciones .sln** equivalentes por membresía, sobre **329 cambios**.
- También materializadas las **6/6 transiciones entre módulos** (M02→M03 hasta M07→M08), sin divergencias. Se ha preparado una reconstrucción acumulativa de **25 etapas consecutivas M03.1–M08.4** que utiliza el resultado construido en cada punto como origen del siguiente; debe consultarse su ejecución antes de certificarla.
- Conectados los validadores Windows de M03–M08 al modo `--reconstruir-incremental`, incluyendo el primer punto construido desde el último proyecto del módulo precedente. En M02 se conserva el E2E previo, pero no se habilita una falsa reconstrucción: faltan metadatos de operación.
- Creada auditoría PDF reproducible y muestras visuales en `tools/validar_publicacion_pdf.py`: **17 PDF, 1.219 páginas, 1.219 cabeceras**, sin páginas sin cuerpo ni bloques detectados fuera de página. La inspección visual completa sigue pendiente.
- Corregidos los números de páginas desactualizados en los informes M01 y M03.

## 3. Matriz de reconstrucción

| Módulo | Revisión editorial | Reconstrucción desde práctica | E2E sobre código |
|---|---|---|---|
| M01 | Material corregido, aprobación del autor pendiente | Activación y comprobación de bloques del primer módulo; no simula todos los clics | Windows SQL/HTTP PASS histórico |
| M02 | Material corregido, aprobación pendiente | **Brecha**: sus operaciones están descritas en prosa/código, pero sólo 12 marcadores identifican rutas; la reconstrucción automática necesita codificar inserciones y reemplazos | E2E de proyectos de referencia Windows SQL/HTTP PASS |
| M03 | Corregido, aprobación pendiente | 3 transiciones materializadas: 43 archivos de texto + 3 soluciones semánticas | E2E sobre etapas reconstruidas Windows/SQL PASS |
| M04 | Corregido, aprobación pendiente | 4 transiciones: 61 archivos + 4 soluciones | E2E reconstruido en Windows/SQL: consultar la última ejecución |
| M05 | Corregido, aprobación pendiente | 4 transiciones: 68 archivos + 4 soluciones | E2E reconstruido en Windows/SQL: consultar la última ejecución |
| M06 | Corregido, aprobación pendiente | 2 transiciones: 50 archivos + 2 soluciones | E2E reconstruido Windows/SQL/RabbitMQ: consultar la última ejecución |
| M07 | Corregido, aprobación pendiente | 3 transiciones: 50 archivos + 3 soluciones | E2E reconstruido Windows/SQL/RabbitMQ: consultar la última ejecución |
| M08 | Corregido, aprobación pendiente | 3 transiciones: 38 archivos + 3 soluciones | E2E reconstruido Windows/SQL/RabbitMQ: consultar la última ejecución |
| M09 | Prácticas corregidas, aprobación pendiente | Comandos PowerShell y seis servicios Compose validados en estructura/sintaxis | **Docker Desktop físico Windows pendiente** |

**Límite de M03–M08:** las seis transiciones iniciales sí se han construido desde el final del módulo precedente. Las 19 transiciones internas y las seis transiciones modulares pasaron una prueba de materialización; la ejecución acumulativa de los 25 puntos en una misma cadena se debe confirmar por su workflow. No se replican los clics de Visual Studio.

## 4. Brecha precisa de M02

La auditoría incremental en M02 ha encontrado **16 modificaciones** respecto a etapas anteriores (2.2–2.4), repartidas en:
- **13 cambios sin operación de escritura identificada por marcador:** incluye `README.md`, `Program.cs`, validadores, contratos, pruebas y configuración de OpenAPI.
- **3 cambios con marcador de referencia**, pero sin semántica `crear/reemplazar/insertar` aplicable por el reconstructor.
- La primera muestra de `Program.cs` del punto 2.1 es intencionalmente un **esqueleto intermedio**, no el archivo final; no debe exigirse que coincida por sí sola con el snapshot 2.1.

**Acción requerida:** aprovechar los fragmentos que ya existen en el manual M02, asignarles operaciones explícitas con punto y ruta, resolver el orden de cambios de `Program.cs`, reconstruir 2.1–2.4 sin leer el código del destino y activar xUnit/SQL/HTTP sobre esas copias.

No se debe añadir un apéndice artificial de código final ni declarar la trazabilidad cerrada por mera coincidencia de rutas.

## 5. Evidencias

- [Reconstrucción 19/19 interna de M03–M08](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43515823932).
- [Reconstrucción 6/6 de los límites M02→M03 hasta M07→M08](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43517914444).
- [Reconstrucción acumulativa de 25 etapas, consultar resultado](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43518461160).
- [M03 reconstrucción + Windows SQL/HTTP](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516047019).
- [M04–M05 reconstrucción + Windows SQL/HTTP](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516053548).
- [M06–M08 reconstrucción + Windows SQL/RabbitMQ](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516060673).
- [Auditoría PDF, 17 documentos y 1.219 páginas](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516616292).
- [Sintaxis PowerShell y estructura M09](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43510540166).

## 6. Pendientes para publicación definitiva

1. Materialización íntegra de M02, especialmente Program.cs y cambios incrementales.
2. Certificación de la cadena completa de 25 pasos M03–M08 sobre resultados reconstruidos sucesivamente, empezando en M02 2.4; su workflow existe y la ejecución debe comprobarse.
3. E2E Windows/SQL/RabbitMQ de M03–M08 con la nueva reconstrucción del primer punto desde el módulo anterior; los E2E previos de las 19 transiciones internas resultaron satisfactorios.
4. Ensayo M09 con Docker Desktop sobre Windows real.
5. Revisión humana de la presentación de los PDF, especialmente las muestras y el cuerpo de cada módulo; verificación editorial final.
6. Decisión del autor sobre publicación y fusión a `main`.

**Importante:** Este archivo es un estado trazable, no un certificado prematuro de finalización. La rama `main` no se modifica.
