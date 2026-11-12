# ADR-029: Gestión de excepciones

## Estado

Aceptado.

## Contexto

AceriaApp continúa la etapa anterior y necesita observar y limitar fallos distribuidos. Se conservan los contratos del dominio, SQL Server, RabbitMQ y outbox/inbox de M6. Los catálogos de análisis y la implementación funcional aportan evidencias diferentes y complementarias.

## Decisión

Centralizar fallos inesperados mediante IExceptionHandler, UseExceptionHandler y ProblemDetails de ASP.NET Core 8 conforme a RFC 9457. Conservar Result y los estados 400/404/409/422/503. No transformar cancelación en 500 ni reescribir una respuesta iniciada. El diagnóstico controlado solo existe en Development con una opción activada.

## Alternativas consideradas

- Mantener solo los catálogos: descartado porque los indicadores no prueban el comportamiento del proceso.
- Duplicar los componentes en Producción e Inventario: descartado; la biblioteca AceriaApp.Observabilidad comparte la integración ASP.NET sin acoplar el dominio.
- Introducir servicios de observabilidad externos: fuera del alcance del módulo; la consola JSON permite inspeccionar resultados reales.

## Consecuencias

- Positivas: comportamiento uniforme, contratos explícitos y fallos reproducibles.
- Negativas: deben mantenerse límites, configuración, políticas y pruebas de integración.
- Mitigación: conservar pruebas heredadas, validar errores y cancelación, y separar señales operativas de los datos sensibles.
