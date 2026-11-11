# ADR-027: Logging

## Estado

Aceptado.

## Contexto

AceriaApp continúa la etapa anterior y necesita observar y limitar fallos distribuidos. Se conservan los contratos del dominio, SQL Server, RabbitMQ y outbox/inbox de M6. Los catálogos de análisis y la implementación funcional aportan evidencias diferentes y complementarias.

## Decisión

Integrar Serilog.AspNetCore 8.0.3 con consola JSON, propiedades estructuradas y nivel por entorno. Validar y propagar X-Correlation-ID. Registrar servicio, identificadores y resumen de petición sin cuerpos, query strings ni cabeceras de autenticación. El catálogo valida la política declarada y las pruebas funcionales observan eventos reales.

## Alternativas consideradas

- Mantener solo los catálogos: descartado porque los indicadores no prueban el comportamiento del proceso.
- Duplicar los componentes en Producción e Inventario: descartado; la biblioteca AceriaApp.Observabilidad comparte la integración ASP.NET sin acoplar el dominio.
- Introducir servicios de observabilidad externos: fuera del alcance del módulo; la consola JSON permite inspeccionar resultados reales.

## Consecuencias

- Positivas: comportamiento uniforme, contratos explícitos y fallos reproducibles.
- Negativas: deben mantenerse límites, configuración, políticas y pruebas de integración.
- Mitigación: conservar pruebas heredadas, validar errores y cancelación, y separar señales operativas de los datos sensibles.
