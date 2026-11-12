# Aplicación al dominio de la acería — Punto 5.5

## Dominio

El análisis del dominio distingue Producción, Aprovisionamiento, Clientes y Facturación. El catálogo de elementos de este punto contiene diez ejemplos de los tres primeros; Facturación se menciona como posible frontera, sin elementos implementados en este ejercicio.

## Contexto de producción en el análisis

- Entidades: OrdenProduccion, LineaProduccion, ProductoTerminado.
- Value objects: Cantidad, Peso, Temperatura.
- Invariantes: cantidad mínima, temperatura de fusión, secuencia.

## Contexto de aprovisionamiento en el análisis

- Entidades: OrdenCompra, Proveedor, Material.
- Value objects: Cantidad, Precio, FechaEntrega.
- Invariantes: cantidad mínima, plazo, condiciones de pago.

## Contexto de clientes en el análisis

- Entidades: Cliente, Contacto.
- Value objects: Direccion, Telefono, Correo.
- Invariantes: razón social, identificador fiscal, dirección completa.

## Agregados del catálogo

- OrdenProduccion: raíz OrdenProduccion con LineaProduccion.
- OrdenCompra: raíz OrdenCompra con LineaCompra.
- Cliente: raíz Cliente con Contacto.

## Lenguaje ubicuo

- Producción: orden de producción, colada, producto terminado.
- Aprovisionamiento: orden de compra, proveedor, materia prima.
- Clientes: cliente, contacto, dirección fiscal.

## Casos de uso del análisis

- Producción: crear orden, asignar material, iniciar colada, finalizar producto.
- Aprovisionamiento: crear orden de compra, recibir material, registrar proveedor.
- Clientes: registrar cliente, actualizar contacto, consultar historial.

## Commands y queries del análisis

- Commands producción: CrearOrdenProduccionCommand, AsignarMaterialCommand.
- Queries producción: ObtenerOrdenProduccionQuery, ListarOrdenesProduccionQuery.
- Commands aprovisionamiento: CrearOrdenCompraCommand, RecibirMaterialCommand.
- Queries aprovisionamiento: ObtenerOrdenCompraQuery, ListarProveedoresQuery.

## Cierre del módulo 5

El proyecto AceriaApp dispone de:

- Conceptos básicos de DDD: contextos delimitados, lenguaje ubicuo y subdominios.
- Contexto Producción ejecutable con entidades y value objects que mantienen invariantes.
- Casos de uso de Producción con `ResultadoProduccion<T>` y unidad de trabajo.
- Separación entre commands y queries.
- Catálogo de análisis de tres contextos y flujo ejecutable del contexto Producción.
- 208 pruebas acumuladas en 22 proyectos, de los cuales 15 son proyectos de tests.
- Veintitrés puntos completados (1.1 a 1.5, 2.1 a 2.4, 3.1 a 3.4, 4.1 a 4.5 y 5.1 a 5.5).

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Contexto implementado | Producción |
| Agregado implementado | OrdenProduccion con LineaDeOrden |
| Casos de uso implementados | Crear, obtener, planificar, finalizar y añadir líneas |
| Commands ejecutables | Crear, planificar, finalizar y agregar línea en Producción |
| Queries ejecutables | Obtener y listar DTO de Producción |

## Alcance implementado y evidencia

Las listas de entidades, agregados y mensajes de los apartados de análisis describen alternativas de modelado. El código del paso 16 implementa el contexto Producción y no proporciona un caso de uso de recibir material ni de registrar clientes. El catálogo usa el nombre LineaProduccion; la entidad hija ejecutable es `LineaDeOrden`. El agregado permite añadir líneas conforme a su estado y capacidad. La API expone el flujo bajo `/api/v1/produccion/ordenes`; las pruebas siguen las respuestas HTTP y comprueban la lectura del estado persistido.
