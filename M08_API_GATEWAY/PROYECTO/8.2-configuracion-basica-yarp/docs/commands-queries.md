# Separación entre Commands y Queries — Punto 5.4

## CQRS

Patrón arquitectónico que separa las operaciones de escritura de las operaciones de lectura.

## Commands

- Expresan una intención de cambio.
- Solicitan cambios; la entrega exactamente una vez no está garantizada por CQRS.
- Su idempotencia depende del contrato y de su implementación; deben decidir cómo tratar duplicados.

## Queries

- Expresan una solicitud de información.
- Son idempotentes.
- No modifican el estado.

## Separación de modelos

- Modelo de escritura: entidades, value objects, invariantes.
- Modelo de lectura: proyecciones, DTOs, vistas.

## Beneficios

- Separación de responsabilidades.
- Optimización por modelo.
- Escalabilidad independiente.
- Evolución independiente.

## Costes

- Complejidad adicional.
- Consistencia eventual cuando las proyecciones se actualizan de forma asíncrona; no es obligatoria en CQRS.
- Duplicación de conceptos.
- Sincronización entre modelos.

## CQRS con un único modelo de datos

La separación distingue contratos de escritura y proyecciones de lectura. Pueden usar una misma base de datos; no se requiere duplicar el almacenamiento.

## CQRS con dos modelos de datos

El modelo de escritura y el de lectura usan bases de datos distintas. La propagación se realiza con eventos.

## Cuándo aplicar CQRS

- Lecturas complejas: sí.
- Alto volumen de lectura: sí.
- Requisitos distintos: sí.
- CRUD simple: no.
- Consistencia fuerte: compatible con una base de datos compartida y proyección síncrona.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Commands ejecutables | Crear, planificar y finalizar órdenes de Producción |
| Queries ejecutables | Obtener y listar proyecciones de órdenes de Producción |
| Manejadores | Separados por tipo |
| Base de datos de Producción | Única para escritura y lectura, sin sincronización asíncrona |
| Validación | Test de coherencia |

## Correspondencia ejecutable

Los nombres de `CatalogoCqrs` son ejemplos de análisis y no registran manejadores. `DevuelveResult` es una convención del laboratorio, no un requisito universal de CQRS: una consulta puede devolver directamente un DTO y un comando puede expresar el resultado con otro contrato. El flujo de Producción dispone de sus propios mensajes de crear, planificar, finalizar, obtener y listar. Los comandos trabajan sobre el agregado mediante los casos de uso; las consultas construyen una proyección DTO sin seguimiento de EF Core. La unidad de trabajo no se usa para confirmar una consulta. Los registros MediatR del contexto conservan el flujo heredado de M04.
