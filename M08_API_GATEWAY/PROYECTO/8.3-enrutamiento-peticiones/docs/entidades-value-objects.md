# Entidades y Value Objects — Punto 5.2

## Entidad

Objeto del dominio que se distingue por su identidad, no por sus atributos.

## Identidad

- Natural: número de bastidor, DNI, ISBN.
- Asignada: número de factura, código de pedido.
- Generada: Guid, ULID, Snowflake ID.

## Value object

Objeto del dominio que se compara por sus atributos, sin identidad propia. Es inmutable y se sustituye por otro valor cuando cambia el concepto representado.

## Comparación

| Aspecto | Entidad | Value object |
|---------|---------|--------------|
| Identidad | Propia | No tiene |
| Mutabilidad | Depende del modelo; no define la identidad | Inmutable |
| Ciclo de vida | Sí | No |
| Igualdad | Por identidad | Por atributos |

## Invariantes

Condiciones que deben mantenerse en todo estado observable. Se validan al construir el objeto y en cada operación que cambia su estado.

## Composición

Los value objects se componen para formar estructuras más complejas.

## Persistencia

- Entidades: clave primaria.
- Value objects: mapeados como parte de la entidad.

## Criterios de decisión

- Identidad → entidad.
- La mutabilidad puede aparecer en entidades, pero no las define.
- Ciclo de vida → entidad.
- Sin identidad → value object.
- Sin ciclo de vida → value object.

## Errores comunes

- Entidad para concepto sin identidad.
- Value object para concepto con identidad.
- Value object mutable.
- Rechazar una entidad solo por ser inmutable: la identidad determina su categoría.
- Invariantes sin validar.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Entidades ejecutables | OrdenProduccion y LineaDeOrden |
| Value objects ejecutables | NombreMaterial y CantidadProduccion |
| Identidad | Guid en las entidades |
| Inmutabilidad | Valores sin setters públicos y construcción controlada |
| Invariantes | Construcción, capacidad total y operaciones del agregado |
| Validación | Test de coherencia |

## Alcance del catálogo y del modelo

El catálogo conserva los ejemplos Orden, Material, Cliente, Dinero, Direccion y Cantidad para practicar la clasificación. No implica que esos seis tipos estén implementados como entidades o valores de Producción. `ValidadorModeloDominio` exige identidad para las entidades e inmutabilidad para los value objects; no rechaza una entidad por ser inmutable. El código ejecutable usa `OrdenProduccion`, `LineaDeOrden`, `NombreMaterial` y `CantidadProduccion`, cuya identidad, igualdad y capacidad se verifican con pruebas funcionales. La capacidad de 500 pertenece a este ejercicio y no representa una regla universal del sector.
