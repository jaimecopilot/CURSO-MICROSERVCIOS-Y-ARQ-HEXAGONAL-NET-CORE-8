# ADR-033: Enrutamiento de peticiones

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado YARP como gateway. Es necesario definir las reglas de enrutamiento y las transformaciones aplicadas a las peticiones.

## Decisión
Se documenta la selección de endpoints de ASP.NET Core: primero el menor `Order`, después la especificidad cuando Order coincide. Los órdenes negativos son válidos y la posición en el objeto JSON no establece la prioridad. Los recursos de Inventario y sus alias permiten GET y HEAD. Los alias `/inventario/api/v1/materiales/{**resto}` y `/inventario/api/v1/planificaciones/{**resto}` usan Order -10 y transformaciones en su orden declarado: eliminar solo `/inventario`, fijar `X-Canal: Gateway` y fijar `canal=gateway` mediante `QueryValueParameter`. No se elimina `/api/v1`. `QueryRouteParameter` obtiene un valor de ruta; `QueryValueParameter` usa un literal con Set o Append. Set en una cabecera también asigna un literal, no genera valores dinámicos. La correlación validada procede del middleware de M07 y se propaga por código. Los tests Kestrel comprueban coincidencia, métodos y transformaciones; el catálogo mantiene reglas pedagógicas propias.

## Alternativas consideradas
- Confiar en la posición de las rutas en JSON: descartado porque no es el criterio de prioridad de endpoints. Usar el mismo Order puede ser válido si la especificidad permite una selección no ambigua.
- Transformaciones en cada servicio: descartado por duplicación.
- Enrutamiento por host: descartado por simplicidad del proyecto.

## Consecuencias
- Positivas: enrutamiento predecible, transformaciones centralizadas, coherencia.
- Negativas: la configuración requiere mantener el orden de las rutas.
- Mitigación: la validación automática y las buenas prácticas documentadas.

## Alcance comprobable de esta etapa

Orden >= 0 y las transformaciones obligatorias son reglas del catálogo, no requisitos generales de YARP. No se publica un comodín global ni el diagnóstico interno. Copiar una cabecera arbitraria a la consulta requeriría una transformación personalizada. Aceptado registra la decisión; la ejecución y sus evidencias deben comprobarse por separado.

El directorio anterior se conserva intacto. Las copias del punto actual incluyen los cambios completos indicados en el manual.
