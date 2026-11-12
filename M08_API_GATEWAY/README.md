# M08 — Publicación mediante API Gateway

**Autor del curso: JAIME GALLO**

Este módulo añade un proceso YARP independiente delante de Producción e Inventario. Conserva los cuatro puntos del temario y sus catálogos de análisis, y los acompaña de pruebas HTTP reales, dos instancias de Inventario, salud activa y recuperación de destinos.

## Material docente

- [Teoría en PDF](TEORIA/M08_TEORIA.pdf) y [Markdown](TEORIA/M08_TEORIA.md): 40 bloques ampliados, ejemplos explicados línea por línea y 12 diagramas disponibles en SVG y PNG.
- [Prácticas en PDF](PRACTICAS/M08_PRACTICAS.pdf) y [Markdown](PRACTICAS/M08_PRACTICAS.md): 96 pasos, archivos completos, cuatro retos optativos resueltos y recorridos PowerShell con SQL Server LocalDB y RabbitMQ.
- [Cobertura y correcciones](COBERTURA_Y_CORRECCIONES.md): trazabilidad del temario y correcciones técnicas aplicadas.
- [Revisión editorial y E2E](REVISION_EDITORIAL_M08.md): edición optimizada (145 páginas de prácticas), pruebas Linux/Windows y alcance del cierre antes de integrar en `main`.

## Etapas acumulativas

Cada carpeta contiene una solución completa. La base es M07 7.4, con 403 pruebas; las etapas obligatorias mantienen los retos en copias separadas.

| Punto | Proyecto | Proyectos | Proyectos de pruebas | Pruebas esperadas |
|---|---|---:|---:|---:|
| 8.1 | [Introducción al patrón API Gateway](PROYECTO/8.1-introduccion-api-gateway) | 35 | 23 | 415 |
| 8.2 | [Configuración básica de YARP](PROYECTO/8.2-configuracion-basica-yarp) | 37 | 24 | 451 |
| 8.3 | [Enrutamiento de peticiones](PROYECTO/8.3-enrutamiento-peticiones) | 38 | 25 | 476 |
| 8.4 | [Balanceo de carga](PROYECTO/8.4-balanceo-carga) | 39 | 26 | 491 |

Los cuatro catálogos añaden 42 pruebas. El gateway añade otras 46 pruebas funcionales: 26 de configuración, 15 de enrutamiento y 5 de balanceo. Cada reto añade una prueba al acumulado de su etapa.

## Ejecución y comprobación

Se requiere el SDK .NET 8 compatible con el `global.json` heredado. El manual incluye la configuración de SQL Server Express/LocalDB, RabbitMQ y las cinco terminales del recorrido completo. Los puertos docentes son 5100 para Gateway, 5105 para Producción y 5106/5107 para Inventario.

Desde la raíz del repositorio:

```powershell
python .github/scripts/m08_e2e_desde_practicas.py --no-tests --out .qa/m08-reconstruccion.json
dotnet run --project tools/M08ValidationHost -c Release -- python .github/scripts/m08_validar.py
```

El primer comando reconstruye el código y declara `SIN_TESTS`. El segundo necesita Docker, crea infraestructura real y comprueba las etapas, los retos y el tráfico entre procesos. La automatización añade una ejecución Windows LocalDB independiente y genera ambos PDF. Los informes incluyen revisión Git, resultados por proyecto y hashes para contrastar el código ejecutado con el publicado.

## Evidencias de cierre

- [Reconstrucción y pruebas por etapa](M08_E2E_RESULTADOS.json).
- [SQL Server y RabbitMQ](M08_SQLSERVER_RESULTADOS.json).
- [HTTP real a través del gateway](M08_HTTP_RESULTADOS.json).
- [Windows LocalDB](M08_WINDOWS_RESULTADOS.json).
- [Cobertura y geometría de los PDF](REPORTE_PDF_M08.json).
- [Comprobación automatizada de la revisión](CIERRE_AUTOMATIZADO.md).

La publicación exige que todos los trabajos de CI terminen correctamente y que sus certificados correspondan a la misma revisión. La revisión visual de las páginas y el cierre editorial se documentan antes de integrar el módulo en `main`.
