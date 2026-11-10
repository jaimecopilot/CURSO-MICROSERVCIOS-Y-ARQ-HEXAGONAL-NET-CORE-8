# ADR-016: Adopción del patrón Mediator con MediatR

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado los patrones Repository y Unit of Work. Es necesario desacoplar los adaptadores de entrada de los casos de uso.

## Decisión
Se adopta MediatR 12.4.1 en la capa de aplicación. `CrearOrdenCommand` y `ObtenerOrdenQuery` son records que implementan `IRequest<T>` y sus manejadores implementan `IRequestHandler<TRequest,TResponse>`. Los endpoints envían ambos mediante `ISender.Send`; los manejadores delegan en `OrdenesTransaccionales`. `AddMediatR` descubre los manejadores del ensamblado de aplicación y registra `LoggingBehavior`. Este pipeline observa el inicio y el fin y respeta la cancelación. Los contratos `INotification` e `INotificationHandler` se estudian como variante; este flujo no publica notificaciones ni incluye un pipeline de FluentValidation.

## Alternativas consideradas
- Inyección directa de los servicios de aplicación en los adaptadores: descartado por acoplamiento.
- Uso de un bus de mensajes externo: descartado por simplicidad del proyecto.

## Consecuencias
- Positivas: bajo acoplamiento, adaptadores simples, un único punto de entrada.
- Negativas: la indirección del mediador puede dificultar el seguimiento.
- Mitigación: la validación automática y el registro claro de los manejadores.
