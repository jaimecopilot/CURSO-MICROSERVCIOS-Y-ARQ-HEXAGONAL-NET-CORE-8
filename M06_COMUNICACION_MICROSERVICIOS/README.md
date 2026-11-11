# Módulo 6 — Comunicación entre microservicios con .NET 8

**Curso JAIME GALLO · AceriaApp**

- [Teoría](TEORIA/M06_TEORIA.md) · [PDF](TEORIA/M06_TEORIA.pdf): 30 bloques, 30 ampliaciones y 10 diagramas SVG/PNG.
- [Prácticas](PRACTICAS/M06_PRACTICAS.md) · [PDF](PRACTICAS/M06_PRACTICAS.pdf): 72 pasos y 3 retos resueltos, con los archivos completos.
- [Proyectos acumulativos](PROYECTO):tres etapas desde M05 5.5 corregido y probado con SQL Server.
- [Evidencia de reconstrucción](M06_E2E_RESULTADOS.json), [SQL Server y broker](M06_SQLSERVER_RESULTADOS.json), [dos procesos HTTP](M06_HTTP_RESULTADOS.json), [Windows/LocalDB](M06_WINDOWS_RESULTADOS.json).

| Punto | Comportamiento ejecutable | Etapa |
|---|---|---|
| 6.1 | Cliente tipado HTTP entre Producción e Inventario, contratos y fallos diferenciados | [6.1](PROYECTO/6.1-comunicacion-sincrona-http) |
| 6.2 | Planificación y outbox atómicos, RabbitMQ real e inbox/proyección SQL idempotente | [6.2](PROYECTO/6.2-comunicacion-asincrona-eventos) |
| 6.3 | Consulta de disponibilidad informativa, planificación local y propagación eventual | [6.3](PROYECTO/6.3-cuando-usar-cada-enfoque) |

El alumno mantiene LocalDB en Windows. Docker ejecuta RabbitMQ mediante el Compose incluido y Testcontainers permite ejecutar las pruebas con SQL Server Express y RabbitMQ en instancias temporales. No existe sustitución de SQL Server por SQLite/InMemory. Las credenciales Compose son de práctica local; los puertos están ligados a 127.0.0.1.

Los catálogos de análisis no equivalen a tráfico de red. Las comprobaciones funcionales incluyen SQL Server, un broker RabbitMQ real y un recorrido entre dos procesos Kestrel. Windows verifica ambos procesos con LocalDB y persistencia tras reiniciar; la mensajería se ejecuta y se prueba en Linux con Docker.

## Arranque del laboratorio

Consulta los apartados «Entorno para las comunicaciones reales» y «Arranque de los dos procesos» de las prácticas. Las dos API escuchan en 5105 y 5106. Los workers están desactivados por defecto: desde 6.2 se habilitan con `Comunicacion__WorkersActivos=true` en ambas terminales. Cada etapa dispone de bases y topología propias.

El endpoint integrado es `POST /api/v 1/comunicacion/ordenes/{id}/planificar`. La ruta de planificación local de M5 permanece como ejercicio independiente y no publica eventos. La consulta de stock es informativa: no reserva material ni constituye una transacción distribuida. La proyección de Inventario registra la planificación; no descuenta stock ni genera facturas.

## Reproducir la validación

Desde la raíz del repositorio, con .NET 8, Python y Docker:

```bash
dotnet run --project tools/M06ValidationHost -c Release -- python .github/scripts/m 06_validar.py
python .github/scripts/m 06_crear_figuras.py
python .github/scripts/m 06_generar_pdf.py
```

El E2E parte exclusivamente de M05 y del Markdown de prácticas. Compila estados intermedios, ejecuta todas las pruebas acumuladas y reconstruye los tres retos en copias separadas. El modo `--no-tests` produce un informe `SIN_TESTS`; no se utiliza como evidencia de ejecución. Los pasos manuales de Visual Studio no se simulan.

El publicador conserva pendientes durante una caída del broker. Confirmación del broker, commit SQL y ACK son garantías distintas. Pueden existir duplicados; la recepción durable evita repetir el efecto de un evento ya registrado y rechaza una identidad con otro contenido. Los contratos incompatibles se envían a una cola de errores para inspección. BasicGet y el reintento periódico son mecanismos didácticos: el módulo no presenta este laboratorio como un despliegue de producción de alta carga.
