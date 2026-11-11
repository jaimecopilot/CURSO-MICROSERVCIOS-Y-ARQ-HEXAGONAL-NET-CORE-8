# Módulo 7 — Observabilidad y resiliencia con .NET 8

**Curso JAIME GALLO · AceriaApp**

Cuatro etapas acumulativas desde M06 6.3: logs y correlación, salud, excepciones y resiliencia HTTP mediante Polly v8. El cierre exige ejecución real de SQL Server, RabbitMQ y Windows/LocalDB, revisión de los PDF y coincidencia de hashes.

- [Teoría](TEORIA/M07_TEORIA.md) · [PDF](TEORIA/M07_TEORIA.pdf): 40 bloques, 40 ampliaciones y 12 diagramas SVG/PNG.
- [Prácticas](PRACTICAS/M07_PRACTICAS.md) · [PDF](PRACTICAS/M07_PRACTICAS.pdf): 96 pasos, cuatro retos resueltos y cuatro recorridos ejecutables con PowerShell 7.
- [Proyectos](PROYECTO): copias independientes de cada etapa; el código completo aparece en el manual.

| Punto | Comportamiento | Proyectos | Pruebas esperadas |
|---|---|---:|---:|
| [7.1 Logging](PROYECTO/7.1-logging) | JSON, correlación validada y propagada entre API | 31 | 309 |
| [7.2 Salud](PROYECTO/7.2-health-checks) | Liveness y readiness con SQL/AMQP reales | 32 | 331 |
| [7.3 Excepciones](PROYECTO/7.3-gestion-excepciones) | ProblemDetails seguro y diagnóstico limitado a Development | 33 | 353 |
| [7.4 Polly](PROYECTO/7.4-retry-circuit-breaker-polly) | Retry acotado, circuito compartido y recuperación observable | 34 | 403 |

La base conserva las 283 pruebas de M6. M7 añade 56 de catálogos y 64 funcionales; los cuatro retos se ejecutan aparte y añaden una prueba a su etapa. Los catálogos son análisis, no sustituyen la ejecución de middleware, conexiones o políticas reales.

## Arranque y comprobación

Dentro de cada etapa, sigue «Recorrido funcional 7.x» de las prácticas: Producción escucha en 5105 e Inventario en 5106. Se utiliza SQL Server Express/LocalDB; el recorrido de salud habilita RabbitMQ con el Compose heredado. Cada etapa utiliza bases propias. Los workers están desactivados por defecto.

Desde la raíz del repositorio, con .NET 8, Python y Docker, el host crea SQL Server Express y RabbitMQ temporales, reconstruye las cuatro etapas y ejecuta las pruebas:

```bash
dotnet run --project tools/M07ValidationHost -c Release -- python .github/scripts/m07_validar.py
```

Para reconstruir sin afirmar que se han ejecutado pruebas:

```bash
python .github/scripts/m07_e2e_desde_practicas.py --no-tests --out .qa/m07-reconstruccion.json
```

El resultado de ese comando es `SIN_TESTS`. La validación completa exige 403 pruebas en la etapa final, cero omisiones, los cuatro retos y el recorrido entre procesos. Las pruebas temporales de Polly usan un reloj virtual y transporte controlado; el recorrido HTTP acredita caída y recuperación de Inventario real sin reiniciar Producción.

## Alcance de las garantías

La minimización de datos corresponde a los eventos propios de M7: resumen HTTP, manejador de excepciones y callbacks Polly. Se elimina también RequestPath de los scopes automáticos. Los logs heredados de workers y EF no se presentan como auditados ni exentos de información interna.

Readiness confirma acceso a las dependencias, no que todos los mensajes estén procesados. El presupuesto HTTP es de seis segundos, con un segundo por intento y hasta dos reintentos solo para lecturas admitidas. La respuesta de indisponibilidad no inventa stock y la consulta GET no reserva material. El módulo conserva la semántica outbox/inbox y de planificación de M6.
