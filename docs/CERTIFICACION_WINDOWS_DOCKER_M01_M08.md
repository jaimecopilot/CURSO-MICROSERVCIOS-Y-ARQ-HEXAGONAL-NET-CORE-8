# Certificación del curso M01–M08: Windows, SQL Server, RabbitMQ y Docker

**Fecha de corte:** 12/11/2026. **Estado:** revisión técnica, no fusionado en main. **M09 excluido** hasta evaluación y aprobación del usuario.

## Objeto de esta auditoría

Asegurar, por cada módulo, que las prácticas permiten construir las etapas .NET 8 y ejecutar sus pruebas con un equipo **Windows**; cuando utilizan Docker, deben explicar **qué imagen o servicio ejecutan, para qué sirve, cómo levantarlo en Docker Desktop para Windows y cómo comprobar su funcionamiento**. Los resultados se apoyan en las ejecuciones de GitHub Actions y no deben deducirse del texto de los manuales.

**No confundir las tres certificaciones:**
- **A. Windows + SQL Server LocalDB y RabbitMQ nativo:** runner Windows 2022 con tests acumulativos y retos, sin Docker Desktop.
- **B. Docker Linux fullstack:** SQL Express, RabbitMQ, dos inventarios, Producción y YARP con tests HTTP, outbox/inbox y recuperación. Esta prueba es funcional, pero el anfitrión es Linux.
- **C. Docker Desktop + WSL2 sobre Windows físico:** ejecución completa del mismo Compose en el equipo Windows. **Todavía requiere comprobación física**; A y B no la sustituyen.

## Matriz técnica por módulo

| Módulo | Etapas del módulo | Batería acumulada de tests por etapa | Necesidad de Docker | Qué se despliega o consume | Manuales Docker existentes |
|---|---|---|---|---|---|
| M01 | 1.1–1.5 | 24 pasos por punto; SQL/HTTP/reto | Ninguna | API .NET 8 y SQL Server LocalDB en Windows | No aplicable |
| M02 | 2.1–2.4 | 3, 7, 12, 16 | Opcional | Testcontainers.MsSql para pruebas EF Core, o LocalDB sin Docker | Sección de preparación Docker Desktop + Testcontainers |
| M03 | 3.1–3.4 | 23, 31, 38, 50 | Opcional | Testcontainers.MsSql para HTTP/integración, o LocalDB | Sección de preparación Docker Desktop + Testcontainers |
| M04 | 4.1–4.5 | 62, 77, 90, 105, 118 | Opcional | Testcontainers.MsSql o LocalDB | Sección de preparación Docker Desktop + Testcontainers |
| M05 | 5.1–5.5 | 134, 153, 172, 190, 208 | Opcional | Testcontainers.MsSql o LocalDB | Sección de preparación Docker Desktop + Testcontainers |
| M06 | 6.1–6.3 | 232, 264, 283 | Sí para broker de laboratorio | Docker Compose RabbitMQ; las APIs Producción/Inventario ejecutan dotnet run en Windows | Comandos Compose, puertos, AMQP, credenciales y health; alternativa Testcontainers SQL |
| M07 | 7.1–7.4 | 309, 331, 353, 403 | Sí para broker de laboratorio | RabbitMQ heredado de M06; observabilidad y resiliencia de las APIs Windows | Compose, pruebas de caída y recuperación, health checks |
| M08 | 8.1–8.4 | 415, 451, 476, 491 | Sí para broker de laboratorio | RabbitMQ heredado y YARP en Windows, Producción + 2 Inventarios | Compose, rutas YARP, puertos, evento y persistencia |

El *curso base* no necesita desplegar todas las APIs en Docker para ejecutar M06–M08: la infraestructura Docker usada en esas prácticas se limita a RabbitMQ (más el SQL de tests con Testcontainers opcional). La **práctica transversal** incorpora el despliegue fullstack en Docker sin alterar los 34 puntos existentes.

## Evidencias automáticas verificables

- SQL real + E2E en Linux sobre el código integrado de M06: [ejecución 43256618514](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43256618514), SUCCESS.
- M07: [ejecución 43260520555](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43260520555), SUCCESS.
- M08: [ejecución 43268192055](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43268192055), SUCCESS.
- M01–M08 Windows 2022, LocalDB y RabbitMQ nativo cuando procede: [ejecución 43276348330](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43276348330). En el último corte **PASS M01–M07; M08 en curso**.
- Fullstack con Docker real en Linux: [ejecución 43276348308](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43276348308), **SUCCESS** (SQL Express + RabbitMQ + Gateway + Producción + 2 Inventarios, HTTP/outbox/inbox/persistencia).
- PDF de los manuales M02–M08 y de la práctica Docker: [ejecución 43280531243](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43280531243), SUCCESS. El PDF transversal incorpora 16 ejercicios, 11 páginas, cero páginas vacías y cero desbordamientos según su reporte de preflight.

## Práctica Docker transversal: entregables

Ubicación: [PRACTICA_TRANSVERSAL_DOCKER_WINDOWS](../PRACTICA_TRANSVERSAL_DOCKER_WINDOWS/).

- `PRACTICAS_DOCKER_WINDOWS.md` y `.pdf`: procedimientos guiados para Windows/WSL2, Testcontainers SQL, RabbitMQ Compose y despliegue fullstack.
- `docker/Dockerfile.Servicio`: imagen de build SDK .NET 8 y publicación en runtime ASP.NET 8.
- `docker/compose.fullstack.yml`: SQL Server Express, RabbitMQ y cuatro procesos .NET (Producción, Inventario x2, Gateway YARP).
- `EJECUTAR_DOCKER_WINDOWS.ps1`: arranque, diagnóstico de salud, tráfico HTTP real, outbox/inbox, persistencia tras reinicio y limpieza consciente de volúmenes.
- `.env.example`: solo credenciales de laboratorio; `.env` real ignorado.
- `generar_pdf.py` y `REPORTE_PDF_DOCKER.json`: sincronización editorial con comprobaciones de A4.

## Criterios antes de aprobar el curso

1. Todas las entradas de la matriz M01–M08 deben mostrar PASS del E2E Windows con tests SQL y retos; no basta `--no-tests` o simplemente compilar.
2. El Markdown de prácticas y su PDF deben coincidir, conservar el código y los marcadores de reconstrucción y carecer de páginas en blanco o desbordamientos.
3. M02–M05 deben conservar la vía LocalDB sin Docker y la vía Testcontainers con Docker Desktop; M06–M08 deben tener instrucciones locales concretas de RabbitMQ, comprobación del broker y consumo desde las APIs.
4. La certificación **Windows+Docker Desktop** necesita un equipo Windows real. Desde PowerShell 7, con Docker Desktop abierto y contenedores Linux:
   - Copiar `PRACTICA_TRANSVERSAL_DOCKER_WINDOWS/.env.example` a `.env` y sustituir contraseña.
   - Ejecutar `.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion preparar`.
   - Ejecutar `.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion levantar`.
   - Guardar `.qa/docker-windows-e2e.json` y comprobar `resultado=PASS` y anfitrión Windows.
   - Completar los ejercicios de fallo/recuperación manuales del documento.
5. No fusionar la PR final ni comenzar M09 hasta que el usuario revise y valide la entrega. **Una prueba Linux SUCCESS no equivale a prueba Docker Desktop Windows SUCCESS**.

## Regla de continuidad

Si se interrumpe la conversación, consultar primero la [PR #15](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/pull/15), luego las ejecuciones citadas y esta matriz. No regenerar M01–M08 desde cero. El código y la documentación ya publicados en `main` se preservan; los cambios nuevos permanecen en la rama de revisión hasta su certificación.
