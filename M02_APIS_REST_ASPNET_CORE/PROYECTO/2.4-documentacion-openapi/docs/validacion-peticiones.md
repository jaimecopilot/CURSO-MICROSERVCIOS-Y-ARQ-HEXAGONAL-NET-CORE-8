# Validación de peticiones — 2.3
## Sintaxis
El JSON malformado o un tipo no convertible impide el enlace. Nullable Reference Types no convierte por sí solo una propiedad string en requisito de runtime para Minimal API.
## Reglas semánticas
FluentValidation comprueba Cliente, Material y Cantidad en CrearOrdenRequest.
## Negocio
Las comprobaciones de stock, existencia de cliente y concurrencia pertenecen a aplicación/dominio y no se implementan en esta práctica.
## Integración
La extensión AddValidacion registra validadores y ValidationFilter<T> construye ValidationProblem. Registrar el validador no activa por sí solo el filtro: hay que asociarlo a endpoints compatibles.
## Códigos
Se establece la convención 400 para datos de entrada inválidos, y 422 para determinadas reglas semánticas de dominio cuando el contrato lo requiera; no es una obligación universal de HTTP.
