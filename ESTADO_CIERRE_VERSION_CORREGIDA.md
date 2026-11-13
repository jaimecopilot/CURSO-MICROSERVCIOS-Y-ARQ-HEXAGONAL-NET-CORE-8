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
- También materializadas las **6/6 transiciones entre módulos** (M02→M03 hasta M07→M08), sin divergencias. Se han reconstruido sucesivamente **29/29 etapas M02.1–M08.4**, empezando M02.1 desde una carpeta vacía y reutilizando siempre el resultado generado en la etapa anterior. [Prueba acumulativa PASS](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43519922250).
- Conectados los validadores Windows de M03–M08 al modo `--reconstruir-incremental`, incluyendo el primer punto construido desde el último proyecto del módulo precedente. M02 dispone ya del reconstructor específico `tools/reconstruir_m02_incremental.py`, que obtiene sus cuatro etapas desde cero mediante los fragmentos del Markdown; las pruebas xUnit/SQL/HTTP Windows se han conectado a las copias reconstruidas y su ejecución más reciente debe verificarse.
- Creada auditoría PDF reproducible y muestras visuales en `tools/validar_publicacion_pdf.py`: **17 PDF, 1.219 páginas, 1.219 cabeceras**, sin páginas sin cuerpo ni bloques detectados fuera de página. La inspección visual completa sigue pendiente.
- Corregidos los números de páginas desactualizados en los informes M01 y M03.

## 3. Matriz de reconstrucción

| Módulo | Revisión editorial | Reconstrucción desde práctica | E2E sobre código |
|---|---|---|---|
| M01 | Material corregido, aprobación del autor pendiente | Activación y comprobación de bloques del primer módulo; no simula todos los clics | Windows SQL/HTTP PASS histórico |
| M02 | Material corregido, aprobación pendiente | **4/4 etapas construidas desde carpeta vacía**, sin divergencias de código; README descriptivo aparte | E2E sobre reconstrucción en Windows/SQL/HTTP: pendiente de resultado reciente; E2E de referencia PASS |
| M03 | Corregido, aprobación pendiente | 3 transiciones materializadas: 43 archivos de texto + 3 soluciones semánticas | E2E sobre etapas reconstruidas Windows/SQL PASS |
| M04 | Corregido, aprobación pendiente | 4 transiciones: 61 archivos + 4 soluciones | E2E reconstruido en Windows/SQL: consultar la última ejecución |
| M05 | Corregido, aprobación pendiente | 4 transiciones: 68 archivos + 4 soluciones | E2E reconstruido en Windows/SQL: consultar la última ejecución |
| M06 | Corregido, aprobación pendiente | 2 transiciones: 50 archivos + 2 soluciones | E2E reconstruido Windows/SQL/RabbitMQ: consultar la última ejecución |
| M07 | Corregido, aprobación pendiente | 3 transiciones: 50 archivos + 3 soluciones | E2E reconstruido Windows/SQL/RabbitMQ: consultar la última ejecución |
| M08 | Corregido, aprobación pendiente | 3 transiciones: 38 archivos + 3 soluciones | E2E reconstruido Windows/SQL/RabbitMQ: consultar la última ejecución |
| M09 | Prácticas corregidas, aprobación pendiente | Comandos PowerShell y seis servicios Compose validados en estructura/sintaxis | **Docker Desktop físico Windows pendiente** |

**Alcance:** M02–M08 son 29 puntos construidos acumulativamente desde M02.1 vacío. El resultado está contrastado con el código entregado y la solución .sln por membresía. Esta prueba de reconstrucción de archivos no ejecuta necesariamente cada una de las acciones gráficas del alumno ni equivale por sí sola al E2E integrado de todos los servicios.

## 4. Cierre de la antigua brecha de M02

Se ha creado `tools/reconstruir_m02_incremental.py`. El reconstructor utiliza el Markdown de prácticas y sus fragmentos de C#, XML, HTTP y JSON para crear primero M02.1 desde una **carpeta vacía**, y después M02.2, M02.3 y M02.4 a partir de la etapa reconstruida anterior. Su resultado ha sido comparado con todos los archivos de código de los cuatro snapshots canónicos: **4/4 PASS, 0 diferencias de código**. No utiliza el código de la etapa final para fabricar los archivos.

Los `README.md` descriptivos quedan excluidos de esta comparación automática y requieren lectura editorial separada. La siguiente evidencia es el E2E Windows SQL/HTTP del mismo material reconstruido, no de una copia canónica, además de la evaluación de la reproducibilidad pedagógica de cada instrucción de Visual Studio.

[Reconstrucción M02 desde vacío](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43519740684).

## 5. Evidencias

- [M02 creado desde cero 4/4](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43519740684).
- [Cadena íntegra M02.1–M08.4, 29/29](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43519922250).
- [Reconstrucción 19/19 interna de M03–M08](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43515823932).
- [Reconstrucción 6/6 de los límites M02→M03 hasta M07→M08](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43517914444).
- [Reconstrucción acumulativa de 25 etapas, consultar resultado](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43518461160).
- [M03 reconstrucción + Windows SQL/HTTP](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516047019).
- [M04–M05 reconstrucción + Windows SQL/HTTP](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516053548).
- [M06–M08 reconstrucción + Windows SQL/RabbitMQ](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516060673).
- [Auditoría PDF, 17 documentos y 1.219 páginas](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516616292).
- [Sintaxis PowerShell y estructura M09](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43510540166).

## 6. Pendientes para publicación definitiva

1. Verificar el resultado de xUnit/HTTP/SQL sobre M02 reconstruido y la última regresión Windows de continuidad M03–M08. La reconstrucción acumulativa **29/29** ya pasó.
2. Validar el laboratorio de M09 en Docker real (CI Linux es evidencia adicional, no Docker Desktop Windows) y ejecutar la práctica físicamente en Windows.
3. Completar comprobaciones editoriales de los pasos de alumno y `README.md` del material entregado.
4. Revisión humana de los PDF, especialmente la presentación de código y las muestras de las 1.219 páginas.
5. Aprobación editorial del autor y decisión de publicación/fusión a `main`.

**Importante:** Este archivo es un estado trazable, no un certificado prematuro de finalización. La rama `main` no se modifica.
