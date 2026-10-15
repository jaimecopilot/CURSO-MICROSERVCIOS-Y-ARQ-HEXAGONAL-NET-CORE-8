# Catálogo de recursos — 2.2
## Contrato
| Recurso | URI | Métodos previstos |
|---|---|---|
| Orden | /api/v1/ordenes | GET, POST |
| Orden | /api/v1/ordenes/{id} | GET, PUT, PATCH, DELETE |
| Línea | /api/v1/ordenes/{id}/lineas | GET, POST |
| Material | /api/v1/materiales | GET, POST |
## Semántica
GET es seguro e idempotente. PUT y DELETE son idempotentes, pero la respuesta de un reintento puede cambiar. PATCH puede ser idempotente dependiendo de la operación. Las tablas de resultados del ejercicio son un subconjunto didáctico, no un inventario exhaustivo de códigos HTTP permitidos.
## Errores
Problem Details se documenta según RFC 9457, sucesora de RFC 7807. No confundir metadatos declarados en OpenAPI con implementación de respuestas.
