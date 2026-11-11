# Patrón Result — Punto 4.4

## Definición

Patrón que representa el resultado de una operación como un valor explícito en lugar de como una excepción.

## Errores esperados y excepcionales

- Errores esperados: Result.
- Errores excepcionales: excepción.

## Estructura

- `IsSuccess`: indicador del tipo básico que se estudia y prueba en `AceriaApp.Api.ResultPattern`. En el contrato ejecutable de aplicación se denomina `EsExito`.
- `Value`: valor del tipo básico. El contrato ejecutable utiliza `Valor` y rechaza leerlo en un fallo.
- `Error`: información del error; el contrato ejecutable incorpora `Codigo`, `Descripcion` y `Tipo`, y rechaza leerlo en un éxito.

## Variantes

- `Result<T>`: valor de éxito y mensaje de error.
- `Result<T, TError>`: valor de éxito y tipo de error específico.
- `Result`: sin valor de éxito.
- `Result<T>` con lista de errores.

## Result Pattern en los casos de uso

Los casos de uso devuelven `Result<T>` en lugar de lanzar excepciones para errores esperados.

## Result Pattern en los adaptadores de entrada

Los adaptadores traducen el resultado en respuestas HTTP.

## Composición de resultados

Las variantes más completas pueden ofrecer `Map`, `Bind` y `Match`. El contrato construido en este punto utiliza comprobaciones explícitas de `EsExito`; no expone esos tres métodos.

## Result Pattern y validación

La validación de esta ruta se realiza en `OrdenesConResultado`, que devuelve un error de categoría `Validacion` antes de preparar escrituras. Integrar FluentValidation en un pipeline es otra variante; el comportamiento registrado aquí es `LoggingBehavior`.

## Cuándo usar el patrón

- Errores esperados: sí.
- Operaciones frecuentes: sí.
- Firma explícita: sí.
- Errores excepcionales: no.
- Operación sin fallo esperado: no.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Caso de uso ejecutable | OrdenesConResultado devuelve `Result<OrdenHexagonal>` |
| Errores esperados | `Result<OrdenHexagonal>.Fallo` con Error tipado |
| Éxito | `Result<OrdenHexagonal>.Exito` |
| Adaptadores entrada | Traducen el resultado a HTTP |
| Validación ejecutable | OrdenesConResultado; 400 antes de persistir |
| Validación del patrón | Test de coherencia |

## Correspondencia con el código ejecutable

El catálogo de este punto describe reglas de diseño y contiene ejemplos de contratos. Sus nombres no implican servicios registrados. La implementación utiliza los proyectos `AceriaApp.Hexagonal.Aplicacion`, `AceriaApp.Hexagonal.Dominio` y `AceriaApp.Hexagonal.Infraestructura`, compuestos desde `AceriaApp.Api`. Comprueba los archivos y los tests funcionales que incorpora el paso de compilación de este punto.
