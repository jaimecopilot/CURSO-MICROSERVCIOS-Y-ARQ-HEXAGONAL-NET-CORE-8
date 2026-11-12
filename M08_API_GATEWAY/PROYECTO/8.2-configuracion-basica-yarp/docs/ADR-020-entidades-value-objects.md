# ADR-020: Entidades y Value Objects

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado Domain-Driven Design y ha definido contextos delimitados. Es necesario definir los elementos tácticos del modelo del dominio.

## Decisión
Se distingue identidad de igualdad por valor. `OrdenProduccion` y `LineaDeOrden` son entidades con identidad; `NombreMaterial` y `CantidadProduccion` son valores inmutables. La raíz controla las líneas, los cambios de estado y una capacidad total máxima de 500 unidades del ejercicio. Las invariantes se comprueban al construir y al cambiar estado. Ser mutable no es requisito universal de una entidad. El catálogo utiliza ejemplos de entidades mutables y valores inmutables; el validador comprueba identidad e invariantes sin exigir mutabilidad a las entidades. Las pruebas funcionales comprueban identidad, igualdad, validación y encapsulación del agregado.

## Alternativas consideradas
- Todo entidades: descartado por añadir identidad innecesaria.
- Todo value objects: descartado por no modelar el ciclo de vida.
- Modelo plano sin distinción: descartado por falta de expresividad.

## Consecuencias
- Positivas: modelo expresivo, validación clara, persistencia adecuada.
- Negativas: la distinción requiere análisis por cada concepto.
- Mitigación: la validación automática y la revisión del modelo.

## Alcance del catálogo y del modelo

El catálogo conserva los ejemplos Orden, Material, Cliente, Dinero, Direccion y Cantidad para practicar la clasificación. No implica que esos seis tipos estén implementados como entidades o valores de Producción. `ValidadorModeloDominio` exige identidad para las entidades e inmutabilidad para los value objects; no rechaza una entidad por ser inmutable. El código ejecutable usa `OrdenProduccion`, `LineaDeOrden`, `NombreMaterial` y `CantidadProduccion`, cuya identidad, igualdad y capacidad se verifican con pruebas funcionales. La capacidad de 500 pertenece a este ejercicio y no representa una regla universal del sector.
