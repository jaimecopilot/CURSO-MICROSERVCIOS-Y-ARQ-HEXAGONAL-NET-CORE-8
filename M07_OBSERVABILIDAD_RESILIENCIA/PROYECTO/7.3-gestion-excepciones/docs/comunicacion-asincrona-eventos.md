# Comunicación asíncrona basada en eventos — Punto 6.2

## Definición

El emisor publica un hecho y no espera al procesamiento de cada consumidor para terminar su operación. La aceptación por el broker y la finalización del trabajo del consumidor son momentos diferentes.

## Evento

Describe un hecho pasado y contiene identificador estable, versión, instante y datos suficientes para interpretarlo. Un evento de dominio pertenece al modelo local; un evento de integración es un contrato público entre fronteras. No se publican directamente entidades de dominio.

## Publicadores, consumidores y broker

El publicador conoce el contrato y el broker; no necesita enumerar todos los consumidores. RabbitMQ enruta mensajes según exchanges, colas y bindings. Que un catálogo declare consumidores no crea ninguna cola ni suscripción.

## Desacoplamiento temporal

Una cola puede retener mensajes durante una caída del consumidor, según su durabilidad y política de expiración. El broker sigue siendo una dependencia y debe estar disponible cuando el productor intenta publicar o habrá que diferir el envío.

## Consistencia eventual

Los estados de los servicios pueden diferir mientras se procesan mensajes. Define qué operación está pendiente, cómo se consulta su avance y cómo se resuelven fallos permanentes. Eventual no significa un plazo garantizado.

## Entrega e idempotencia

La entrega al menos una vez puede producir duplicados. El consumidor identifica el mensaje y registra de forma durable su efecto antes de confirmar la entrega. Un ACK prematuro puede perder trabajo. Una confirmación del publicador indica aceptación del broker, no éxito de todos los consumidores.

## Reintentos y mensajes fallidos

Acota los reintentos y su demora; separa fallos transitorios de contratos inválidos. Usa una cola de fallidos y un procedimiento de inspección o reproceso. La política del catálogo exige que los eventos de integración del ejercicio declaren estas decisiones; no pretende imponerlas a todos los eventos de dominio.

## Transacción y publicación

Guardar datos y publicar son dos operaciones. El patrón outbox registra el cambio y la intención de publicación en una transacción local. Un despachador vuelve a publicar pendientes; el consumidor debe seguir tolerando duplicados.

## Aplicación al curso

`Evento`, `CatalogoEventos` y `ValidadorComunicacionAsincrona` validan cuatro contratos de integración y seis suscripciones declaradas. No representan seis servicios distintos ni demuestran conexión con RabbitMQ. Los eventos locales de dominio pueden existir sin suscriptores remotos y sin políticas de entrega de un broker.

## Correspondencia ejecutable

La implementación funcional de mensajería debe comprobar publicación, consumo, persistencia del efecto e idempotencia. Los tests del catálogo solo demuestran coherencia de sus entradas; no sustituyen esa comprobación.
