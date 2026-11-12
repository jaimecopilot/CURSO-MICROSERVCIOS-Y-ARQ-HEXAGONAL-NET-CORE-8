# ADR-030: Retry y Circuit Breaker mediante Polly

## Estado

Aceptado.

## Contexto

AceriaApp continúa la etapa anterior y necesita observar y limitar fallos distribuidos. Se conservan los contratos del dominio, SQL Server, RabbitMQ y outbox/inbox de M6. Los catálogos de análisis y la implementación funcional aportan evidencias diferentes y complementarias.

## Decisión

Usar Polly v8 mediante Microsoft.Extensions.Http.Resilience solo en las consultas GET a Inventario. Aplicar timeout total 6 s, dos reintentos de 200 ms exponenciales con jitter, circuito de mínimo cuatro muestras y proporción 0,5 en diez segundos, apertura cinco segundos, y timeout de intento un segundo. No repetir métodos mutantes ni estados permanentes ni cancelación del usuario. Conservar el circuito por cliente/destino y traducir agotamiento a indisponibilidad.

## Alternativas consideradas

- Mantener solo los catálogos: descartado porque los indicadores no prueban el comportamiento del proceso.
- Duplicar los componentes en Producción e Inventario: descartado; la biblioteca AceriaApp.Observabilidad comparte la integración ASP.NET sin acoplar el dominio.
- Introducir servicios de observabilidad externos: fuera del alcance del módulo; la consola JSON permite inspeccionar resultados reales.

## Consecuencias

- Positivas: comportamiento uniforme, contratos explícitos y fallos reproducibles.
- Negativas: deben mantenerse límites, configuración, políticas y pruebas de integración.
- Mitigación: conservar pruebas heredadas, validar errores y cancelación, y separar señales operativas de los datos sensibles.
