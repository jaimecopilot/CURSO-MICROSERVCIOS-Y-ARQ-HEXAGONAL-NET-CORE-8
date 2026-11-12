# Cuándo utilizar cada enfoque — Punto 6.3

## Decisión por interacción

Selecciona comunicación síncrona, asíncrona o una combinación según el resultado que necesita el caso de uso. Un mismo servicio puede utilizar los tres estilos en operaciones diferentes.

## Respuesta inmediata

HTTP facilita recibir una respuesta directa. La asincronía de `await` no cambia ese contrato. Una notificación asíncrona sin protocolo de respuesta no puede ofrecer el resultado inmediato del consumidor. Un acuse de recibo del broker no es el resultado de negocio.

## Consistencia

La necesidad de conocer el stock actual no hace atómica una reserva posterior. La consistencia eventual requiere estados pendientes y una forma de observar el avance. HTTP por sí solo tampoco coordina una transacción distribuida.

## Disponibilidad y fallos

HTTP depende de la disponibilidad simultánea del destinatario. Mensajería puede desacoplar el consumo si existe almacenamiento durable, pero añade dependencias operativas y retrasos. Documenta timeout, reintentos seguros, mensajes fallidos y recuperación.

## Volumen, frecuencia y latencia

Mide las tasas de llegada, capacidad del consumidor, tamaño del mensaje y latencia admitida. Una cola absorbe picos limitados; no resuelve una falta de capacidad permanente.

## Organización

Considera la autonomía de los equipos, la propiedad de los contratos, las versiones compatibles y la capacidad de operación del broker. Ningún estilo exige automáticamente un microservicio nuevo.

## Patrones híbridos

Combina consulta síncrona con notificación asíncrona cuando cada fase lo necesita. Describe el protocolo, sus estados y la autoridad de cada dato; un indicador booleano no implementa una saga.

## Matriz de decisión

| Necesidad | Opción a evaluar | Condición que hay que verificar |
|---|---|---|
| Resultado del destino durante la petición | HTTP | Timeout y tratamiento de indisponibilidad |
| Notificación de un hecho a varios interesados | Eventos | Contratos versionados y entrega durable |
| Escritura local y aviso remoto | Eventos con outbox | Transacción local e idempotencia |
| Consulta actual y trabajo posterior | Híbrida | Estado pendiente y consulta de avance |

## Decisiones del catálogo

Se describen dos interacciones síncronas, dos asíncronas y una híbrida. Una interacción síncrona sin necesidad de respuesta inmediata puede ser válida por simplicidad u operación; no se rechaza por ese único dato. El análisis asíncrono de este ejercicio requiere tolerancia eventual y no promete resultado inmediato del consumidor. La modalidad híbrida exige describir su patrón.

## Cierre del módulo

Los catálogos de llamadas, eventos y decisiones verifican datos de análisis. La integración funcional de HTTP y mensajería aporta pruebas separadas de comportamiento. Ni los nombres de servicios ni los booleanos del catálogo demuestran tráfico, colas, reintentos o transacciones distribuidas.
