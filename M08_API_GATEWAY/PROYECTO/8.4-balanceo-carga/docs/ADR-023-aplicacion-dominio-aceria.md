# ADR-023: Aplicación de DDD y CQRS al dominio de la acería

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado DDD, entidades, value objects, casos de uso y CQRS. Es necesario aplicar los conceptos al dominio concreto de la acería y cerrar el módulo 5.

## Decisión
Se cierra el módulo con un flujo ejecutable del contexto Producción. `OrdenProduccion` es la raíz y controla las instancias de `LineaDeOrden`, los valores `NombreMaterial` y `CantidadProduccion`, la capacidad total de 500 y las transiciones Borrador, Planificada y Finalizada. Un comando permite agregar líneas mediante el endpoint de la orden; la raíz rechaza cambios incompatibles con su estado. Los casos de uso coordinan repositorio y unidad de trabajo. Las consultas devuelven proyecciones DTO sobre la misma base de Producción. Las pruebas HTTP ejecutan el recorrido completo y verifican errores esperados, persistencia y aislamiento de lectura. Los catálogos describen también Aprovisionamiento y Clientes; no se implementan sus agregados ni servicios. Facturación e Identidad quedan como fronteras del análisis, fuera de este flujo.

## Alternativas consideradas
- Modelo único para todo el dominio: descartado por mezclar significados.
- Sin contexto núcleo: descartado por falta de foco.
- Sin CQRS en el dominio: descartado por falta de separación.

## Consecuencias
- Positivas: alineación con el negocio, modelo expresivo, separación clara.
- Negativas: la aplicación requiere análisis por contexto.
- Mitigación: la validación automática y la revisión del modelo.

## Alcance implementado y evidencia

Las listas de entidades, agregados y mensajes de los apartados de análisis describen alternativas de modelado. El código del paso 16 implementa el contexto Producción y no proporciona un caso de uso de recibir material ni de registrar clientes. El catálogo usa el nombre LineaProduccion; la entidad hija ejecutable es `LineaDeOrden`. El agregado permite añadir líneas conforme a su estado y capacidad. La API expone el flujo bajo `/api/v1/produccion/ordenes`; las pruebas siguen las respuestas HTTP y comprueban la lectura del estado persistido.
