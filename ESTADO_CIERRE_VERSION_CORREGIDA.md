# Estado de cierre de la versión corregida del curso

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS (.NET 8)  
**Rama:** `version-corregida` (independiente de `main`)  
**Autor:** JAIME GALLO  
**Corte de auditoría:** 14 de noviembre de 2026

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
- Conectados los validadores Windows de M03–M08 al modo `--reconstruir-incremental`, incluyendo el primer punto construido desde el último proyecto del módulo precedente. M02 dispone ya del reconstructor específico `tools/reconstruir_m02_incremental.py`, que obtiene sus cuatro etapas desde cero mediante los fragmentos del Markdown; las pruebas xUnit/SQL/HTTP Windows sobre las cuatro etapas reconstruidas han superado la ejecución [43520054081](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43520054081): 3, 7, 12 y 16 pruebas respectivamente, 0 fallos; integración SQL/HTTP final correcta.
- Creada auditoría PDF reproducible y muestras visuales en `tools/validar_publicacion_pdf.py`: **17 PDF, 1.220 páginas, 1.220 cabeceras**, sin páginas sin cuerpo ni bloques detectados fuera de página. La inspección visual completa sigue pendiente, pero la auditoría más reciente también comprueba que el PDF M09 contiene los comandos de certificación y resiliencia añadidos.
- Corregidos los números de páginas desactualizados en los informes M01 y M03.

## 3. Matriz de reconstrucción

| Módulo | Revisión editorial | Reconstrucción desde práctica | E2E sobre código |
|---|---|---|---|
| M01 | Material corregido, aprobación del autor pendiente | **5/5 etapas reconstruidas desde carpeta vacía**, código del manual, generación de migración EF, 64 pruebas xUnit acumuladas | **PASS Windows 2022/SQL Express/HTTP**, 1, 9, 13, 18 y 23 xUnit por etapa |
| M02 | Material corregido, aprobación pendiente | **4/4 etapas construidas desde carpeta vacía**, sin divergencias de código; README descriptivo aparte | **PASS Windows/SQL/HTTP** sobre código reconstruido: 3/3, 7/7, 12/12, 16/16 y recorrido HTTP final |
| M03 | Corregido, aprobación pendiente | 3 transiciones materializadas: 43 archivos de texto + 3 soluciones semánticas | E2E sobre etapas reconstruidas Windows/SQL PASS |
| M04 | Corregido, aprobación pendiente | 4 transiciones: 61 archivos + 4 soluciones | E2E reconstruido en Windows/SQL: consultar la última ejecución |
| M05 | Corregido, aprobación pendiente | 4 transiciones: 68 archivos + 4 soluciones | E2E reconstruido en Windows/SQL: consultar la última ejecución |
| M06 | Corregido, aprobación pendiente | 2 transiciones: 50 archivos + 2 soluciones | E2E reconstruido Windows/SQL/RabbitMQ: consultar la última ejecución |
| M07 | Corregido, aprobación pendiente | 3 transiciones: 50 archivos + 3 soluciones | E2E reconstruido Windows/SQL/RabbitMQ: consultar la última ejecución |
| M08 | Corregido, aprobación pendiente | 3 transiciones: 38 archivos + 3 soluciones | E2E reconstruido Windows/SQL/RabbitMQ: consultar la última ejecución |
| M09 | Prácticas corregidas, aprobación pendiente; **17 páginas PDF** | Seis contenedores, E2E integral y resiliencia validados en Docker Linux CI; certificador Windows real preparado con informe JSON | **PASS Docker CI Linux**; **Docker Desktop en Windows 10/11 pendiente de ejecutar** |

**Alcance:** M02–M08 son 29 puntos construidos acumulativamente desde M02.1 vacío. El resultado está contrastado con el código entregado y la solución .sln por membresía. Esta prueba de reconstrucción de archivos no ejecuta necesariamente cada una de las acciones gráficas del alumno ni equivale por sí sola al E2E integrado de todos los servicios.

## 4. Cierre técnico de M01 y M02

**M01:** nuevo reconstructor `tools/reconstruir_m01_desde_cero.py` crea las cinco etapas desde una carpeta vacía utilizando bloques del manual, solución y proyectos generados con SDK .NET 8 fijado; genera una migración EF Core desde el modelo y realiza compilación, xUnit y E2E SQL/HTTP en Windows. **PASS 5/5, 64 ejecuciones xUnit acumuladas**. [Evidencia reproducible](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43573679482). No afirma haber simulado todos los clics de Visual Studio; es una validación adicional al esqueleto de alumno previsto.

### Cierre de la antigua brecha de M02

Se ha creado `tools/reconstruir_m02_incremental.py`. El reconstructor utiliza el Markdown de prácticas y sus fragmentos de C#, XML, HTTP y JSON para crear primero M02.1 desde una **carpeta vacía**, y después M02.2, M02.3 y M02.4 a partir de la etapa reconstruida anterior. Su resultado ha sido comparado con todos los archivos de código de los cuatro snapshots canónicos: **4/4 PASS, 0 diferencias de código**. No utiliza el código de la etapa final para fabricar los archivos.

Los `README.md` descriptivos quedan excluidos de esta comparación automática y requieren lectura editorial separada. La batería Windows SQL/HTTP sobre el código reconstruido se ejecutó con resultado **PASS** en las cuatro etapas. Sigue pendiente evaluar manualmente las acciones gráficas de Visual Studio y aprobar el texto editorial de manera definitiva.

[Reconstrucción M02 desde vacío](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43519740684).

## 5. Evidencias

- [M01 reconstrucción desde vacío 5/5 en Windows SQL Express y 64 xUnit acumuladas, PASS](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43573679482).
- [M02 creado desde cero 4/4](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43519740684).
- [M02 Windows SQL/HTTP sobre reconstrucción real, PASS](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43520054081).
- [M09 Docker integral Linux CI, PASS (no certifica Windows)](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43520238826).
- [M09 Docker Linux CI con caída y recuperación de Inventario 2 y RabbitMQ, PASS](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43521475426).
- [Cadena íntegra M02.1–M08.4, 29/29](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43519922250).
- [Reconstrucción 19/19 interna de M03–M08](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43515823932).
- [Reconstrucción 6/6 de los límites M02→M03 hasta M07→M08](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43517914444).
- [Reconstrucción acumulativa de 25 etapas, consultar resultado](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43518461160).
- [M03 reconstrucción + Windows SQL/HTTP](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516047019).
- [M04–M05 reconstrucción + Windows SQL/HTTP](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516053548).
- [M06–M08 reconstrucción + Windows SQL/RabbitMQ](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43516060673).
- [Auditoría PDF actualizada, 17 documentos y 1.220 páginas, y sincronía M09 Markdown/PDF](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43574610999).
- [Sintaxis PowerShell y estructura M09](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43510540166).

## 6. Pendientes para publicación definitiva

1. **Ninguna reconstrucción de código M01–M08 pendiente**: M01 reconstruido de vacío 5/5 con xUnit y SQL/HTTP en Windows; M02–M08 encadenados 29/29 desde M02.1 vacío y comprobados con baterías Windows sobre código reconstruido. Las acciones de interfaz gráfica de Visual Studio y retos opcionales no están automatizados.
2. Certificar M09 físicamente en **Windows 10/11 compatible, PowerShell 7 y Docker Desktop + WSL 2**, para lo que se ha preparado `M09_DESPLIEGUE_DOCKER/PROYECTO/CERTIFICAR_DOCKER_DESKTOP_WINDOWS.ps1` y el workflow manual `.github/workflows/m09-certificacion-windows-desktop.yml`. Se necesita una máquina Windows Desktop real con Docker Desktop activo, manualmente o mediante runner self-hosted con etiqueta `docker-desktop-wsl2`; el runner `windows-2022` es Windows Server y no sirve. La prueba Linux E2E ya pasó; **no existe todavía resultado PASS del Windows Desktop físico**.
3. Completar la inspección editorial de los pasos de alumno y los `README.md` descriptivos; validar las instrucciones gráficas que no cubren las pruebas automatizadas.
4. Revisión humana de los PDF, especialmente la presentación de código y las muestras de las **1.220 páginas**.
5. Aprobación editorial del autor y decisión de publicación/fusión a `main`.

**Importante:** Este archivo es un estado trazable, no un certificado prematuro de finalización. La rama `main` no se modifica.
