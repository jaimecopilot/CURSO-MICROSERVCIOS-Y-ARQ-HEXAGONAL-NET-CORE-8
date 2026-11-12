# Retry y Circuit Breaker mediante Polly — Punto 7.4

## Resiliencia

Capacidad de limitar el impacto de fallos y recuperarse cuando las condiciones lo permiten. No garantiza disponibilidad ni convierte una operación fallida en éxito.

## Patrones de resiliencia

- Retry: reintenta operaciones fallidas.
- CircuitBreaker: corta el flujo cuando el destino falla.
- Timeout: limita el tiempo de espera.
- Bulkhead: aísla recursos por operación.

## Retry

- Se aplica a fallos transitorios.
- Intervalo fijo o exponencial.
- Requiere idempotencia en las operaciones.

## Circuit Breaker

Estados: cerrado, abierto y semiabierto.

## Combinación de patrones

    // Orden exterior → interior del handler de resiliencia:
    // timeout total → retry → circuit breaker → timeout de intento.
    // Cada reintento atraviesa el mismo circuito y queda dentro del presupuesto total.

## Polly

Polly v8 ofrece pipelines de resiliencia. La integración HTTP del ejercicio usa `Microsoft.Extensions.Http.Resilience` y `AddResilienceHandler`; no mezcla la API v7 `Policy.WrapAsync`/`AddPolicyHandler` con la API v8.

## Configuración de políticas

    var retry = new HttpRetryStrategyOptions
    {
        MaxRetryAttempts = 2,
        Delay = TimeSpan.FromMilliseconds(200),
        BackoffType = DelayBackoffType.Exponential,
        UseJitter = true
    };
    var circuit = new HttpCircuitBreakerStrategyOptions
    {
        MinimumThroughput = 4,
        FailureRatio = 0.5,
        SamplingDuration = TimeSpan.FromSeconds(10),
        BreakDuration = TimeSpan.FromSeconds(5)
    };

## Fallback

Solo devuelve una alternativa si el negocio la ha aprobado y puede distinguirse de un dato actual. En esta consulta no se inventa stock ni se devuelve éxito ficticio: circuito abierto o presupuesto agotado se traducen en indisponibilidad.

## Buenas prácticas

1. Timeout en todas las llamadas externas.
2. Retry solo en operaciones idempotentes.
3. Circuit breaker en destinos que fallan.
4. Registrar reintentos y aperturas.
5. Ajustar parámetros al contexto.

## Cierre del módulo 7

El proyecto AceriaApp dispone de:

- Logging estructurado con Serilog.
- Health checks separados en liveness y readiness.
- Gestión de excepciones con problem details.
- Retry, circuit breaker y timeout con Polly.
- 403 pruebas acumuladas en 34 proyectos, con 22 proyectos de tests y 42 documentos en `docs`.
- Treinta puntos completados (1.1 a 1.5, 2.1 a 2.4, 3.1 a 3.4, 4.1 a 4.5, 5.1 a 5.5, 6.1 a 6.3 y 7.1 a 7.4).

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Cliente HTTP | Políticas de retry, circuit breaker y timeout |
| Parámetros | Ajustados por destino |
| Registro | Reintentos y aperturas |
| Validación | Test de coherencia |
## Contrato del ejercicio

El presupuesto total es de 6 segundos y cada intento tiene 1 segundo. Hay como máximo dos reintentos además del intento inicial. Los fallos elegibles son HTTP 408/429/5xx, transporte y timeout del intento. No se reintentan 400/401/403/404, cancelación del usuario ni métodos mutantes. El circuito se comparte por cliente/destino; no se crea para cada llamada.

`MinimoDeMuestras` representa el mínimo de llamadas observado, no un número de fallos consecutivos. La apertura combina ese mínimo con la proporción de fallos dentro de la ventana. Los valores 5 y 3 del catálogo son ejemplos de mínimos para dos destinos; la configuración HTTP ejecutable usa 4. Las cinco entradas del catálogo conservan sus dos retries, dos circuit breakers y un timeout; sus ocho reintentos declarados no son los intentos de una petición ni la política del outbox de M6.

`OperacionIdempotente` expresa una condición del contrato, no implementa idempotencia. El verificador rechaza un retry que no la declare y exige límites y registro. Las pruebas funcionales observan intentos, cancelación, apertura y recuperación del circuito real de Polly.
