# ADR-011: Puertos y adaptadores

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado la organización por capas y la regla de dependencia. Es necesario definir los puertos y adaptadores que conectan el núcleo con el exterior.

## Decisión
Se adopta la arquitectura hexagonal con puertos de entrada y de salida. Los puertos se definen en la capa de aplicación. Los adaptadores de entrada se sitúan en la capa de presentación. Los adaptadores de salida se sitúan en la capa de infraestructura. La inversión de dependencias se aplica con el contenedor de dependencias. La validación de la coherencia se realiza con un validador automático.

## Alternativas consideradas
- Acoplar el núcleo a los adaptadores: descartado por violar la regla de dependencia.
- Definir un solo tipo de puerto: descartado por pérdida de información.
- Validar manualmente la coherencia: descartado por falta de trazabilidad.

## Consecuencias
- Positivas: núcleo independiente, adaptadores intercambiables, validación automática.
- Negativas: la definición de puertos requiere disciplina.
- Mitigación: validación automática con el validador.

## Aplicación en AceriaApp

Se parte de la API real y probada de M02, se conservan sus endpoints y se añaden reglas de dependencia verificadas en código. Los proyectos de Dominio, Aplicación e Infraestructura deben obedecer la dirección de referencias; en 3.4 se expone un nuevo adaptador HTTP funcional. El catálogo describe las relaciones arquitectónicas; cada implementación se comprueba en su proyecto correspondiente.
