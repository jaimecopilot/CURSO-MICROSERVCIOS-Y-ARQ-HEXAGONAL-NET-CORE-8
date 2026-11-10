# ADR-015: Adopción del patrón Unit of Work

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado el patrón Repository. Es necesario coordinar las operaciones de varios repositorios en una única transacción.

## Decisión
Se adopta un contrato mínimo `IUnitOfWork` con `CommitAsync`. La implementación `EfUnitOfWork` delega en un único `SaveChangesAsync` de `HexagonalDbContext`. El nuevo `OrdenTrabajoRepositorio` prepara cambios sin confirmarlos y comparte contexto con la unidad de trabajo. EF Core utiliza su transacción automática relacional cuando el lote lo requiere: una prueba provoca el fallo después de un INSERT y comprueba la reversión; el control sin transacción deja una fila. No se publica un método Rollback en este contrato. Los cambios no confirmados se descartan al desechar el contexto; una reversión tras un fallo de persistencia la resuelve la transacción del proveedor. El repositorio heredado de M03 conserva su comportamiento para los endpoints anteriores.

## Alternativas consideradas
- Gestión de transacciones en cada repositorio: descartado por duplicación.
- Uso directo del `DbContext` desde la aplicación: descartado por acoplamiento.
- Sin unidad de trabajo: descartado por riesgo de cambios parciales.

## Consecuencias
- Positivas: atomicidad, desacoplamiento de transacciones, coordinación de repositorios.
- Negativas: la unidad de trabajo añade una capa de indirección.
- Mitigación: la interfaz se limita a las operaciones necesarias.

## Variantes del catálogo y del contrato ejecutable

El catálogo de diseño de este punto incluye unidades que declaran confirmación y reversión explícitas. Sus dos registros y el resumen de seis repositorios son datos del ejercicio de validación. La implementación ejecutable utiliza `IUnitOfWork.CommitAsync` y `EfUnitOfWork`, con un repositorio para las órdenes; la prueba del lote coordina dos entidades y la transacción pertenece al contexto. Una unidad de trabajo puede coordinar varios repositorios que compartan ese contexto, pero este punto no implementa repositorios ficticios de inventario o clientes.
