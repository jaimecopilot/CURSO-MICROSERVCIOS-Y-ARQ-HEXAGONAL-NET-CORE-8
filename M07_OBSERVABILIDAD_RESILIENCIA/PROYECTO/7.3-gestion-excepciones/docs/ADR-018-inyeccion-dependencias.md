# ADR-018: Inyección de dependencias y cierre del módulo 4

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado los patrones Repository, Unit of Work, Mediator y Result. Es necesario definir cómo se componen los servicios en el contenedor de dependencias y cerrar el módulo 4.

## Decisión
Se adopta el contenedor de ASP.NET Core. `AddServiciosHexagonales(configuration)` registra el contexto SQL Server heredado y `AddPatronesOrdenes()` agrupa registros explícitos de `IOrdenTrabajoRepositorio`, `IUnitOfWork`, los casos de uso y el pipeline. Los manejadores se descubren por sus interfaces con `RegisterServicesFromAssemblyContaining`. Los componentes que comparten `HexagonalDbContext` tienen ciclo Scoped; MediatR también se configura con ese ciclo. Tres pruebas verifican la identidad dentro del ámbito, el aislamiento entre ámbitos, el flujo completo y el rechazo de una dependencia Scoped capturada por un Singleton. El catálogo de cinco registros sigue siendo un ejercicio de diseño y no afirma que exista un publicador RabbitMQ en la aplicación.

## Alternativas consideradas
- Uso de un contenedor externo: descartado por simplicidad del proyecto.
- Registro directo en `Program.cs`: descartado por crecimiento del archivo.
- Uso de Service Locator: descartado por acoplamiento.

## Consecuencias
- Positivas: composición declarativa, ciclo de vida gestionado, servicios testeables.
- Negativas: el contenedor añade indirección en la resolución.
- Mitigación: validación automática y uso consistente del patrón.
