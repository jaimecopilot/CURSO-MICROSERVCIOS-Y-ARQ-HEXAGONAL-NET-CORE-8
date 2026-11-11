# Patrón Unit of Work — Punto 4.2

## Definición

Abstracción que coordina las operaciones de varios repositorios en una única transacción.

## Responsabilidades

- Mantener el seguimiento de cambios.
- Coordinar la persistencia.
- Exponer la operación de confirmación.

## Lo que no debe hacer

- Contener reglas de negocio.
- Conocer entidades concretas.
- Transformar entidades en DTOs.
- Ejecutar consultas complejas.
- Gestionar la lógica de los repositorios.

## Relación con Repository

El repositorio gestiona una entidad. La unidad de trabajo coordina varios repositorios.

## EF Core como unidad de trabajo

El `DbContext` implementa el patrón Unit of Work con `SaveChanges` y `SaveChangesAsync`.

## Unidad de trabajo personalizada

Envuelve el `DbContext` y expone solo las operaciones necesarias para la aplicación.

## Transacciones distribuidas

La unidad de trabajo se limita a la transacción local. La transacción distribuida requiere patrones adicionales.

## Cuándo usar el patrón

- Operación con varias entidades: sí.
- Coordinación de repositorios: sí.
- Desacoplamiento de transacciones: sí.
- Operación con una entidad: un envoltorio adicional es opcional; resulta útil si se desea hacer explícito el punto de confirmación o sustituirlo en pruebas.
- Sin requisito de atomicidad: no.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Puerto de salida | IUnitOfWork |
| Adaptador de salida | EfUnitOfWork |
| Repositorio del nuevo flujo | OrdenTrabajoRepositorio prepara los cambios |
| Unidad de trabajo | Confirma los cambios |
| Validación | Test de coherencia |

## Correspondencia con el código ejecutable

El catálogo de este punto describe reglas de diseño y contiene ejemplos de contratos. Sus nombres no implican servicios registrados. La implementación utiliza los proyectos `AceriaApp.Hexagonal.Aplicacion`, `AceriaApp.Hexagonal.Dominio` y `AceriaApp.Hexagonal.Infraestructura`, compuestos desde `AceriaApp.Api`. Comprueba los archivos y los tests funcionales que incorpora el paso de compilación de este punto.


## Variantes del catálogo y del contrato ejecutable

El catálogo de diseño de este punto incluye unidades que declaran confirmación y reversión explícitas. Sus dos registros y el resumen de seis repositorios son datos del ejercicio de validación. La implementación ejecutable utiliza `IUnitOfWork.CommitAsync` y `EfUnitOfWork`, con un repositorio para las órdenes; la prueba del lote coordina dos entidades y la transacción pertenece al contexto. Una unidad de trabajo puede coordinar varios repositorios que compartan ese contexto, pero este punto no implementa repositorios ficticios de inventario o clientes.
