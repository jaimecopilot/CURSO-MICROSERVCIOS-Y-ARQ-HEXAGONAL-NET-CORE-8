# ADR-024: Comunicación síncrona mediante HTTP

## Estado

Aceptado.

## Contexto

AceriaApp continúa la etapa anterior y necesita razonar explícitamente sobre sus interacciones. La solución conserva los modelos y pruebas heredados; el catálogo nuevo es un ejercicio de análisis separado de los adaptadores de comunicación ejecutables.

## Decisión

Registrar las llamadas, validar destinos, métodos y timeout, y revisar la seguridad de los reintentos. No exigir reintentos para todas las operaciones: POST y PATCH necesitan un contrato de idempotencia antes de repetirse. El cliente HTTP y las pruebas de tráfico verifican por separado el comportamiento real.

## Alternativas consideradas

- Elegir un solo estilo para todo el sistema: descartado porque las interacciones tienen necesidades diferentes.
- Omitir los criterios de recuperación y consistencia: descartado porque deja ambiguos los fallos parciales.
- Considerar suficiente la validación del catálogo: descartado porque no comprueba la comunicación ejecutable.

## Consecuencias

- Positivas: decisiones explícitas, casos de rechazo reproducibles y trazabilidad por interacción.
- Negativas: mantener contratos, políticas y pruebas de comportamiento añade trabajo.
- Mitigación: distinguir pruebas de análisis y pruebas funcionales, mantener límites claros y revisar las decisiones con evidencia operativa.
