# Patrón Mediator — Punto 4.3

## Definición

Patrón que reduce el acoplamiento entre los componentes al centralizar la comunicación en un objeto mediador.

## Mediator en la capa de aplicación

Los adaptadores de entrada envían comandos y consultas al mediador. El mediador los distribuye al manejador correspondiente.

## Comandos

Mensajes que solicitan una acción que modifica el estado. Se nombran con un verbo en imperativo.

## Consultas

Mensajes que solicitan información sin modificar el estado. Se nombran con un sustantivo o con un verbo en forma interrogativa.

## Notificaciones

Mensajes que informan de un evento ocurrido. Se nombran con un sustantivo en pasado. Pueden tener varios manejadores.

## MediatR

Biblioteca de .NET que implementa el patrón Mediator. Ofrece `IRequest`, `IRequest<T>`, `INotification`, `IRequestHandler` e `INotificationHandler`.

## Envío de comandos y consultas

En MediatR 12.4.1 se utiliza `Send`, que ya devuelve una tarea y se espera con `await`. Los endpoints dependen de `ISender` para enviar comandos y consultas; no existe un método `SendAsync` en esta API.

## Publicación de notificaciones

MediatR 12.4.1 publica con `Publish`, que ya devuelve una tarea y se espera con `await`; no ofrece `PublishAsync`. Las notificaciones se estudian en el catálogo de este punto y no se implementa aquí un publicador de eventos de negocio.

## MediatR y validación

Un pipeline puede integrar FluentValidation como variante de diseño. El flujo ejecutable de este punto registra `LoggingBehavior`, que registra inicio y fin sin datos del cliente y comprueba cancelación; las comprobaciones de entrada permanecen en el endpoint y en el caso de uso. No se registra un pipeline de FluentValidation para esta ruta.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Comando ejecutable | CrearOrdenCommand |
| Consulta ejecutable | ObtenerOrdenQuery |
| Notificaciones | Ejemplos del catálogo; no se publican en este flujo |
| Manejadores | Implementan IRequestHandler |
| MediatR | Registrado con AddMediatR |
| Pipeline ejecutable | LoggingBehavior para observación y cancelación |

## Correspondencia con el código ejecutable

El catálogo de este punto describe reglas de diseño y contiene ejemplos de contratos. Sus nombres no implican servicios registrados. La implementación utiliza los proyectos `AceriaApp.Hexagonal.Aplicacion`, `AceriaApp.Hexagonal.Dominio` y `AceriaApp.Hexagonal.Infraestructura`, compuestos desde `AceriaApp.Api`. Comprueba los archivos y los tests funcionales que incorpora el paso de compilación de este punto.
