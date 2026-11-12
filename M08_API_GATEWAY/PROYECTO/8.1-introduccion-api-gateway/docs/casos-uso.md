# Casos de uso — Punto 5.3

## Definición

Operación del sistema que expresa una intención del negocio. Puede exponerse como método de un servicio de aplicación o como manejador de una solicitud; el contrato refleja su intención.

## Relación con comando

El caso de uso puede invocarse directamente por su contrato. En 5.3 la API invoca los casos de uso; los mensajes y manejadores MediatR del contexto Producción se incorporan en 5.4.

## Orquestación

El caso de uso orquesta entidades, value objects, repositorios y unidad de trabajo. Mantiene la política de aplicación y delega las invariantes en el dominio; no reproduce las reglas internas del agregado.

## Coordinación de repositorios

1. Recuperar entidades con repositorios.
2. Modificar entidades del dominio.
3. Persistir cambios con repositorios.
4. Confirmar transacción con la unidad de trabajo.
5. Devolver el resultado.

## Casos de uso de escritura y de lectura

- Escritura: modifican el estado, requieren unidad de trabajo.
- Lectura: no modifican el estado, pueden usar proyecciones.

## Casos de uso y puertos de entrada

Cada puerto agrupa los casos de uso de una misma capacidad de negocio.

## Casos de uso y adaptadores de entrada

La API llama los casos de uso mediante inyección de dependencias. Un mediador es una opción de despacho que se incorpora en el siguiente punto.

## Validación

- Sintáctica: contrato de la petición.
- Aplicación: comprobaciones de entrada y traducción de errores esperados; no se incorpora FluentValidation a este flujo.
- Negocio: invariantes del dominio.

## Transacciones

El caso de uso decide cuándo confirmar los cambios del contexto de persistencia mediante la unidad de trabajo. Una operación de lectura no confirma cambios. No se promete atomicidad entre contextos distintos ni servicios externos.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Aplicación ejecutable | Casos de uso de crear, obtener, planificar y finalizar órdenes de producción |
| Adaptador de entrada | Endpoints bajo /api/v1/produccion/ordenes |
| Resultados | `ResultadoProduccion<T>` |
| Coordinación | IOrdenProduccionRepositorio e IProduccionUnitOfWork |
| Validación | Test de coherencia |

## Alcance del catálogo

`CatalogoCasosDeUso` contiene ejemplos CrearOrden, CancelarOrden, ObtenerOrden y ListarOrdenes. Sus indicadores son datos pedagógicos; no constituyen un inventario de métodos implementados en Producción. En este punto se ejecutan crear, obtener, planificar y finalizar una orden. El nuevo contexto tiene su propia persistencia y no comparte entidades con el flujo hexagonal heredado. Los tests funcionales comprueban el orden de las operaciones y la persistencia desde otro contexto de prueba.
