# ADR-017: Adopción del patrón Result

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado los patrones Repository, Unit of Work y Mediator. Es necesario definir cómo se representan los errores en los casos de uso.

## Decisión
Se adopta `AceriaApp.Hexagonal.Aplicacion.Patrones.Result<T>` para los errores esperados del nuevo flujo. `OrdenesConResultado` valida las entradas y devuelve `Exito` o `Fallo` con `Error` tipado; los errores de infraestructura y de programación siguen propagándose como excepciones. Los manejadores de MediatR conservan el resultado explícito y `PatronesOrdenesEndpoints` lo traduce a 201 con Location, 200, 400, 404 o 409 y Problem Details. `LoggingBehavior` permanece como pipeline de observación; no se incorpora un comportamiento de FluentValidation. El tipo básico `AceriaApp.Api.ResultPattern.Result<T>` se mantiene para el ejercicio de catálogo y sus pruebas. Siete pruebas funcionales verifican las fábricas, las ramas del resultado y las respuestas HTTP con persistencia real de prueba.

## Alternativas consideradas
- Uso exclusivo de excepciones: descartado por coste y falta de expresividad.
- Uso de códigos de error numéricos: descartado por menor legibilidad.
- Uso de una jerarquía de excepciones personalizadas: descartado por mezclar errores esperados y excepcionales.

## Consecuencias
- Positivas: errores explícitos, contrato de respuesta verificable, flujo de errores controlado.
- Negativas: la estructura del resultado añade código adicional.
- Mitigación: la validación automática y el uso consistente del patrón.
