# Corrección SQL Server antes de M6

Autorización: el usuario solicitó ejecutar todas las correcciones sin nuevas preguntas el 11/11/2026.
Base: 41d37cb84f258dcfef7ad1e94b45571cbdcc76b8. Rama: correccion/sqlserver-m02-m05-20261111.

## Criterio obligatorio
Aplicación y pruebas de integración usan SQL Server real. No se admite éxito con SQLite/InMemory ni pruebas omitidas. Pruebas de dominio puro no requieren BD. M6 no empieza hasta completar evidencias.

## Tareas y estado
- [x] 01 Matriz inicial: M1 SQL Server real (CI 42862047382); M2/M3 InMemory; M4/M5 SQLite más heredadas. Aplicaciones M1–M5 configuradas SQL Server.
- [x] 02 Entorno SQL Server Express/Testcontainers, bases aisladas, fallo obligatorio y limpieza.
- [x] 03 M02 cuatro etapas: API y persistencia SQL Server.
- [x] 04 M03 cuatro etapas: puertos/adaptadores y API SQL Server.
- [x] 05 M04 cinco etapas: Repository, Unit of Work y rollback SQL Server.
- [x] 06 M05 cinco etapas: dominio, casos de uso, CQRS, API y persistencia SQL Server.
- [x] 07 Teoría Docker/Testcontainers y diagramas.
- [x] 08 Prácticas reproducibles, sin referencias editoriales al material de partida.
- [x] 09 CI obligatorio SQL Server, registros y evidencias.
- [x] 10 Reconstrucción de las 18 etapas desde prácticas, pruebas y retos.
- [x] 11 Windows LocalDB: cuatro proyectos finales, inicialización y HTTP.
- [x] 12 PDF regenerados y revisión visual.
- [x] 13 Informe de cierre, commits y ejecuciones verificadas.

## Decisiones de ejecución
- Se trabaja en un clon aislado y rama de corrección; no se modifica M6.
- Una utilidad C# autocontenida se introduce en el manual M02 y se hereda. No se añade una dependencia oculta fuera de cada solución.
- Cada prueba dispone de una base AceriaTest_<GUID>. Una conexión externa permite CI/LocalDB; sin ella Testcontainers inicia Express en Docker. Nunca se cambia de proveedor silenciosamente.
- Imagen reproducible: mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04; Testcontainers.MsSql 3.10.0; SQL Express. Las versiones de EF existentes se conservan.
- Las comprobaciones SQL reales se ejecutarán en GitHub Actions: este entorno no dispone de Docker ni Windows. La compilación y revisión documental se hacen también localmente.
- La evidencia antigua se conserva como historial; los informes nuevos deben identificar proveedor y revisión comprobada.

## Registro
11/11/2026: clon recuperado, base verificada; ejecución iniciada. Revisión paralela separada de M02/M03, M04/M05 y teoría; integración, CI y cierre a cargo del coordinador.

Revisión independiente: se detectaron y corrigieron dos riesgos de falso cierre: vínculo del código comprobado en Windows con el publicado y eliminación de ejecutables obsoletos en la publicación de M02. Se añaden pruebas de regresión que fallaron antes de la corrección. Evidencia SQL/Windows sigue pendiente hasta CI.



11/11/2026: las 13 tareas están cerradas. CI 42986550628 terminó en SUCCESS sobre 54709859d231c8607ba0761a28f442fda285fd58. El commit 7fe7da90bab1d8e3ca6d45fc9395828b919b7555 contiene los artefactos de esa ejecución. Se verificaron sus manifiestos, las 18 etapas y 14 retos programados, los cuatro recorridos Windows y las 672 páginas renderizadas (idénticas a la revisión local). Los 12 controles de regresión del cierre vuelven a pasar. Véase REVISION_FINAL.md para alcance y observaciones menores. M6 queda habilitado; no se ha desarrollado como parte de esta corrección.

Comprobaciones automáticas completadas en https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/42989271274; las tareas 12 y 13 requieren además revisión visual y revisión final documentadas.


Verificación complementaria del cierre antes de publicar M06: los ocho PDF regenerados en `aa7319c2c799b78710d4435aaca8ef4857da34cf` se compararon con la entrega revisada `7fe7da90bab1d8e3ca6d45fc9395828b919b7555`. Las 672 páginas son idénticas píxel a píxel a 72 dpi; los contenidos de código y Markdown no variaron en esa regeneración. Las 13 tareas del cierre SQL Server siguen completadas. M06 ya dispone de su propia evidencia y revisión final en `M06_COMUNICACION_MICROSERVICIOS/REVISION_FINAL.md`.

Comprobaciones automáticas completadas en https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43248558074; las tareas 12 y 13 requieren además revisión visual y revisión final documentadas.

Comprobaciones automáticas completadas en https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43251643708; las tareas 12 y 13 requieren además revisión visual y revisión final documentadas.

Comprobaciones automáticas completadas en https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43254244146; las tareas 12 y 13 requieren además revisión visual y revisión final documentadas.
