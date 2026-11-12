# ADR-022: Separación entre Commands y Queries

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado DDD y ha definido casos de uso. Es necesario separar las operaciones de escritura de las de lectura.

## Decisión
Se incorporan mensajes y manejadores MediatR 12.4.1 en `AceriaApp.Produccion.Aplicacion`. Los comandos delegan las escrituras en los casos de uso del contexto. Las consultas devuelven DTO mediante un puerto de lectura y una proyección `AsNoTracking` de infraestructura, sin exponer el agregado ni confirmar cambios. La API despacha mensajes con `ISender`. Lectura y escritura comparten la base de Producción; no existe replicación asíncrona ni requisito de consistencia eventual. Las pruebas verifican el despacho, la cancelación y la ausencia de escrituras o seguimiento en consultas. El catálogo mantiene sus cuatro mensajes demostrativos y se valida de forma separada.

## Alternativas consideradas
- Modelo único sin separación: descartado por falta de claridad.
- CQRS con dos bases de datos: descartado por complejidad prematura.
- CQRS con proyecciones actualizadas por eventos: aplazado; el contexto usa lectura y escritura sobre la misma base.

## Consecuencias
- Positivas: separación de responsabilidades, claridad, evolución independiente.
- Negativas: cada modelo requiere sus propios manejadores.
- Mitigación: la validación automática y la convención de nombres.

## Correspondencia ejecutable

Los nombres de `CatalogoCqrs` son ejemplos de análisis y no registran manejadores. `DevuelveResult` es una convención del laboratorio, no un requisito universal de CQRS: una consulta puede devolver directamente un DTO y un comando puede expresar el resultado con otro contrato. El flujo de Producción dispone de sus propios mensajes de crear, planificar, finalizar, obtener y listar. Los comandos trabajan sobre el agregado mediante los casos de uso; las consultas construyen una proyección DTO sin seguimiento de EF Core. La unidad de trabajo no se usa para confirmar una consulta. Los registros MediatR del contexto conservan el flujo heredado de M04.
