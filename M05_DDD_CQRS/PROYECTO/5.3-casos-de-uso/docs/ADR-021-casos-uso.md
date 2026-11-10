# ADR-021: Casos de uso

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado DDD y ha definido entidades y value objects. Es necesario definir cómo se expresan las operaciones del dominio y cómo se coordinan los elementos del modelo.

## Decisión
Se implementan casos de uso de Producción para crear, obtener, planificar y finalizar una orden. `AceriaApp.Produccion.Aplicacion` depende del dominio y declara `IOrdenProduccionRepositorio`, `IProduccionUnitOfWork` y `ResultadoProduccion<T>`. `AceriaApp.Produccion.Infraestructura` implementa la persistencia mediante `ProduccionDbContext`. La API traduce el resultado a HTTP y compone las dependencias. Los casos de uso orquestan la carga del agregado, sus operaciones y la confirmación; el agregado conserva las invariantes. Las pruebas sustituyen la persistencia o utilizan SQLite para comprobar el comportamiento relacional. MediatR se añade a este contexto en 5.4; los manejadores anteriores de M04 permanecen independientes.

## Alternativas consideradas
- Servicios de aplicación sin casos de uso explícitos: descartado por falta de intención.
- Representar todos los errores esperados mediante excepciones: se prefiere un resultado explícito para distinguirlos de fallos técnicos.
- Invocar EF Core directamente desde aplicación: se prefiere el puerto de unidad de trabajo para desacoplar la confirmación. La atomicidad la aporta el adaptador transaccional, no la interfaz por sí sola.

## Consecuencias
- Positivas: operaciones explícitas, coordinación clara, errores explícitos.
- Negativas: los contratos y adaptadores añaden archivos y decisiones de composición.
- Mitigación: la validación automática y la convención de nombres.

## Alcance del catálogo

`CatalogoCasosDeUso` contiene ejemplos CrearOrden, CancelarOrden, ObtenerOrden y ListarOrdenes. Sus indicadores son datos pedagógicos; no constituyen un inventario de métodos implementados en Producción. En este punto se ejecutan crear, obtener, planificar y finalizar una orden. El nuevo contexto tiene su propia persistencia y no comparte entidades con el flujo hexagonal heredado. Los tests funcionales comprueban el orden de las operaciones y la persistencia desde otro contexto de prueba.
