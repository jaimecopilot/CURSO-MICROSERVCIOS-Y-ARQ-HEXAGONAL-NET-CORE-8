# ADR-003: Aplicación de principios de diseño a los límites de servicio

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado un monolito modular y ha definido métricas de acoplamiento. Es necesario aplicar principios de diseño explícitos para decidir los límites entre módulos y preparar la extracción futura de microservicios.

## Decisión
Se adoptan ocho principios: responsabilidad única, ocultación de información, acoplamiento débil y cohesión fuerte, límite del contexto, autonomía, contrato explícito, tolerancia al fallo y evolución independiente. Se implementa un validador automático que audita los límites de servicio del monolito.

## Alternativas consideradas
- Aplicar los principios sin validación automática: descartado por falta de trazabilidad.
- Aplicar solo algunos principios: descartado por incoherencia.

## Consecuencias
- Positivas: decisiones trazables, auditoría automática, preparación para la extracción.
- Negativas: el validador puede requerir ajuste de umbrales.
- Mitigación: revisar los umbrales al final de cada módulo.
