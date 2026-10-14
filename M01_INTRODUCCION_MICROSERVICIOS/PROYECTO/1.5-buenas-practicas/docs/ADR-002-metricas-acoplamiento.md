# ADR-002: Métricas de acoplamiento para decidir la extracción de servicios

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado un monolito modular. Es necesario decidir qué funcionalidades son candidatas a extraerse como microservicios en módulos posteriores.

## Decisión
Se adoptan dos indicadores objetivos: el índice de acoplamiento entre proyectos y el índice de compartición de datos. Una funcionalidad es candidata a extracción si tiene como máximo una dependencia externa y como máximo tres tablas propias.

## Alternativas consideradas
- Decidir la extracción por criterio subjetivo: descartado por falta de trazabilidad.
- Extraer todas las funcionalidades a la vez: descartado por el coste operativo.

## Consecuencias
- Positivas: decisiones trazables, comparables y medibles.
- Negativas: los umbrales son iniciales y pueden requerir ajuste.
- Mitigación: revisar los umbrales al final de cada módulo.
