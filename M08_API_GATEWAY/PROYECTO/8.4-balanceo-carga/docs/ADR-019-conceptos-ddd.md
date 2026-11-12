# ADR-019: Adopción de Domain-Driven Design

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha cerrado el módulo 4 con los patrones de arquitectura. Es necesario definir cómo se organiza el dominio del negocio y cómo se alinean los límites de los servicios con los límites del negocio.

## Decisión
Se adopta DDD con fronteras explícitas de modelo. El catálogo de análisis describe Producción, Aprovisionamiento, Clientes e Identidad y valida sus indicadores. La implementación comienza únicamente con el contexto Producción en `AceriaApp.Produccion.Dominio`: `OrdenProduccion` usa el lenguaje del negocio y protege las transiciones Borrador, Planificada y Finalizada. El dominio no depende de EF Core, HTTP ni de los proyectos hexagonales heredados. Los otros contextos continúan siendo ejemplos de análisis; no se implementan aquí servicios autónomos para ellos. Las pruebas funcionales ejecutan el modelo propio y comprueban la frontera del ensamblado.

## Alternativas consideradas
- Organización exclusivamente por capas técnicas sin fronteras de dominio: descartada porque mezcla modelos del negocio.
- Modelo único para todo el dominio: descartado por mezclar significados.
- Sin lenguaje ubicuo: descartado por dificultar la comunicación.

## Consecuencias
- Positivas: alineación con el negocio, lenguaje compartido, límites claros.
- Negativas: requiere inversión inicial y colaboración continua.
- Mitigación: la validación automática y la revisión periódica de los contextos.

## Correspondencia ejecutable

`ContextoDelimitado`, `CatalogoContextos` y `ValidadorContextos` representan datos del ejercicio. Sus indicadores no prueban la arquitectura por sí solos. El contexto implementado es Producción, con `OrdenProduccion` en un proyecto independiente y transiciones controladas. Las pruebas funcionales comprueban construcción, reglas y frontera de dependencias. La relación entre contextos no requiere compartir las entidades del modelo.
