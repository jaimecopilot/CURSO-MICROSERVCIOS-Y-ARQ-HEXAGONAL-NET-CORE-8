# Comunicación síncrona mediante HTTP — Punto 6.1

## Definición

Una interacción síncrona requiere recibir el resultado del destino para completar el paso del proceso. En .NET, `await` permite esperar sin bloquear un hilo; no elimina la dependencia temporal entre servicios.

## HTTP

HTTP expresa métodos, recursos, cabeceras, cuerpos y estados. No toda respuesta no exitosa significa ausencia: 404, 400 y 503 requieren tratamientos distintos. HTTP/1.1 y HTTP/2 utilizan TCP; HTTP/3 utiliza QUIC sobre UDP.

## Clientes tipados

Una clase encapsula la dirección, serialización y traducción de respuestas del servicio remoto. `IHttpClientFactory` gestiona los manejadores reutilizados; el cliente se registra con `AddHttpClient`.

## Configuración

Define URL base, timeout, cancelación y contratos de datos. Obtén las direcciones de la configuración del entorno y escapa los segmentos que proceden del usuario. Un cliente tipado no debe ocultar errores de transporte como un resultado de negocio inexistente.

## Acoplamiento temporal

La disponibilidad y latencia del destino forman parte del comportamiento observado por el solicitante. La asincronía de una tarea .NET no convierte HTTP en mensajería.

## Riesgos

Latencia acumulada, saturación, respuestas tardías, indisponibilidad y fallos en cascada. Incluso tras un timeout, el destino podría haber completado una escritura.

## Mitigación

Configura timeout, cancelación y límites de concurrencia. Usa reintentos acotados solo cuando la operación y el contrato permitan repetirla. No reintentes POST o PATCH a ciegas: requiere una clave de idempotencia aplicada de forma durable por el servidor. Un indicador del catálogo no implementa esa garantía. Un circuit breaker limita llamadas durante una incidencia; no repara el servicio remoto. Un valor alternativo solo sirve cuando el negocio lo acepta explícitamente.

## Consistencia

HTTP no proporciona una transacción atómica entre bases de servicios. Consultar stock no lo reserva. Una operación distribuida necesita una política explícita de reserva, compensación o reconciliación.

## Cuándo usarlo

Favorece HTTP cuando el flujo necesita el resultado actual, existe un contrato de latencia y el acoplamiento es aceptable. Una lectura también puede usar una proyección asíncrona si admite datos retrasados; la elección se toma por interacción.

## Aplicación al curso

`LlamadaSincrona`, `CatalogoLlamadas` y `ValidadorComunicacionSincrona` describen tres consultas GET entre nombres de servicios. Sus pruebas comprueban datos del análisis: no abren sockets ni prueban `HttpClient`, reintentos o circuit breakers. La implementación funcional separada comprueba tráfico HTTP y sus fallos controlados.
