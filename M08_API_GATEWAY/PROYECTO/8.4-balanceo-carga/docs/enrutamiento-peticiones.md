# Enrutamiento de peticiones — Punto 8.3

## Proceso de coincidencia

YARP utiliza el enrutamiento de endpoints de ASP.NET Core para seleccionar una ruta que satisfaga sus condiciones. Primero interviene el valor de `Order`: los valores menores tienen prioridad, incluidos los negativos. Entre rutas con el mismo `Order`, interviene la especificidad del patrón. La posición de una entrada en el objeto JSON no establece su prioridad; deben evitarse coincidencias ambiguas.

## Patrones de ruta

Sintaxis de ASP.NET Core. Segmentos literales, parámetros, comodines y restricciones.

    {
      "Match": {
        "Path": "/api/v1/ordenes/{id:guid}",
        "Methods": [ "GET" ]
      }
    }


## Precedencia

Un `Order` menor prevalece sobre uno mayor antes de comparar la especificidad. Con el mismo `Order`, un patrón específico tiene mayor precedencia que otro más general. En el alias de Inventario se utiliza `Order: -10`; no hay una restricción general de YARP que obligue a usar órdenes no negativos.

## Transformaciones de ruta

- `PathRemovePrefix`: elimina un prefijo.
- `PathSet`: establece una ruta fija.
- `PathPattern`: aplica un patrón.

## Transformaciones de cabecera

- `RequestHeader` con `Set` o `Append`: fija o añade un valor de cabecera de petición. Para eliminarla se utiliza `RequestHeaderRemove`.
- `ResponseHeader` con `Set` o `Append`: fija o añade un valor de cabecera de respuesta. Para eliminarla se utiliza `ResponseHeaderRemove`.
- `Set` en estas transformaciones asigna un literal. Por ejemplo, `Set: generated` enviaría el texto generated; no genera un identificador. La correlación dinámica se obtiene del middleware de M07 y se propaga mediante código.

## Transformaciones de consulta

- `QueryRouteParameter`: establece el nombre del parámetro de consulta; su `Set` o `Append` indica el nombre del valor de ruta del que se toma el dato.
- `QueryValueParameter`: establece el nombre del parámetro de consulta; su `Set` o `Append` contiene un valor literal. En el alias se utiliza `QueryValueParameter: canal` con `Set: gateway`.
- Copiar dinámicamente un valor arbitrario de cabecera a la consulta requeriría una transformación personalizada; no se configura mediante una transformación integrada con un nombre inventado.

## Orden de aplicación

Las transformaciones de petición se aplican en el orden declarado dentro de `Transforms`; no existe una reordenación automática por categorías de ruta, cabecera y consulta. El alias docente declara:

1. `PathRemovePrefix: /inventario`.
2. `RequestHeader: X-Canal` con `Set: Gateway`.
3. `QueryValueParameter: canal` con `Set: gateway`.

Así, `/inventario/api/v1/materiales/Acero` se reenvía como `/api/v1/materiales/Acero`, conservando `/api/v1`. El proxy añade X-Canal: Gateway y fija canal=gateway; no elimina el prefijo de versión del backend.

## Enrutamiento por cabecera

La ruta se selecciona según el valor de una cabecera declarada en `Match.Headers`.

## Buenas prácticas

1. Documentar primero `Order` y después la especificidad; no confiar en el orden de escritura del JSON.
2. Restricciones en los parámetros.
3. Transformaciones solo cuando son necesarias.
4. Documentar el orden de las rutas.
5. Validar con un test.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Orden de rutas | Order menor antes; especificidad cuando Order coincide |
| Transformaciones ruta | Eliminar solo /inventario en los dos alias publicados |
| Transformaciones cabecera | X-Canal: Gateway; correlación validada por middleware y propagada por código |
| Transformaciones consulta | canal=gateway mediante QueryValueParameter y Set literal |
| Métodos | GET y HEAD en materiales, planificaciones y sus alias; las escrituras a esas rutas se rechazan |
| Validación | Tests del catálogo y peticiones Kestrel sobre coincidencia, métodos y transformaciones |

## Alcance comprobable de esta etapa

La restricción Orden >= 0 del validador de catálogo y sus transformaciones obligatorias son reglas del ejercicio de análisis, no del contrato general de YARP. El gateway utiliza rutas con Order negativo y otras sin transformaciones. Las rutas públicas no incluyen un comodín global: los endpoints internos de diagnóstico no se exponen por el alias. Las reglas de negocio permanecen en Producción e Inventario.

El directorio anterior se conserva intacto. Las copias del punto actual incluyen los cambios completos indicados en el manual.
