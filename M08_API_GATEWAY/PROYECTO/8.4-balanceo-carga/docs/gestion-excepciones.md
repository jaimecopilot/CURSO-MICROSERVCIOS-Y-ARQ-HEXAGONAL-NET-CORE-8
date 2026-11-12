# Gestión de excepciones — Punto 7.3

## Definición

Conjunto de mecanismos que permiten controlar los errores que ocurren durante la ejecución.

## Excepciones esperadas y excepcionales

- Esperadas: patrón Result.
- Excepcionales: excepciones.

## Excepciones personalizadas

Heredan de `Exception` e incluyen información contextual del dominio.

## Manejador global

`UseExceptionHandler` y un `IExceptionHandler` centralizan los fallos inesperados antes de iniciar la respuesta. Si ya se han enviado cabeceras no pueden reescribirla. Una cancelación solicitada por el cliente no se traduce en error interno 500.

## Formato problem details

RFC 9457 define `type`, `title`, `status`, `detail` e `instance`; no obliga a incluir detalles internos. El ejercicio devuelve un título genérico y correlación, sin stack trace, mensajes de excepción ni credenciales.

## Traducción de excepciones a códigos HTTP

| Excepción | Código |
|-----------|--------|
| OrdenNoEncontradaException | 404 |
| ValidacionException | 400 |
| ConflictoException | 409 |
| InventarioNoDisponibleException | 503 |
| No reconocida | 500 |

## Excepciones y logging

Las excepciones se registran con el nivel adecuado antes de devolver la respuesta.

## Excepciones y patrón Result

Las excepciones esperadas se representan con Result. Las excepcionales se capturan en el manejador global.

## Buenas prácticas

1. No usar excepciones para el flujo normal.
2. Capturar solo las excepciones manejables.
3. No capturar excepciones genéricas sin propósito.
4. Registrar las excepciones con contexto.
5. Devolver respuestas uniformes.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Manejador global | UseExceptionHandler |
| Formato | Problem details |
| Excepciones esperadas | Result |
| Excepciones excepcionales | Manejador global |
| Registro | Serilog |
| Validación | Test de coherencia |
## Contrato del ejercicio

Los nombres de excepción del catálogo son ejemplos de clasificación. No obligan al dominio a lanzar excepciones para errores esperados: las rutas existentes conservan Result y sus 400/404/409/422, y la indisponibilidad sigue siendo 503. No todo 4xx merece un log de nivel Error; se decide según su naturaleza. La regla `RegistraError` del catálogo se exige a fallos 5xx, sin registrar contenido libre del fallo.

El endpoint de diagnóstico requiere entorno Development y una opción explícita. No existe en Production. Las pruebas diferencian el formato del error, la correlación, la cancelación, las respuestas ya iniciadas y la preservación de los estados de negocio.
