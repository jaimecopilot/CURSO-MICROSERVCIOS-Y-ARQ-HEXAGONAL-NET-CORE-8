# ADR-010: Organización por capas y regla de dependencia

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha cerrado el módulo 2 con una API REST documentada. Es necesario reorganizar el código en capas para preparar la evolución hacia arquitectura hexagonal.

## Decisión
Se adopta la organización por capas: presentación, aplicación, dominio e infraestructura. La regla de dependencia se aplica de forma estricta: las dependencias se dirigen hacia el interior. La inversión de dependencias permite que la aplicación dependa de interfaces y que la infraestructura las implemente. La validación de la regla se realiza con un validador automático.

## Alternativas consideradas
- Mantener la organización plana: descartado por dificultad de evolución.
- Aplicar solo la separación de dominio: descartado por incompleto.
- Usar capas apiladas sin inversión de dependencias: descartado por acoplamiento.

## Consecuencias
- Positivas: separación de responsabilidades, testabilidad, mantenibilidad.
- Negativas: la organización requiere disciplina en la aplicación de la regla.
- Mitigación: validación automática de la regla con el validador.

## Aplicación en AceriaApp

Se parte de la API real y probada de M02, se conservan sus endpoints y se añaden reglas de dependencia verificadas en código. Los proyectos de Dominio, Aplicación e Infraestructura deben obedecer la dirección de referencias; en 3.4 se expone un nuevo adaptador HTTP funcional. El catálogo describe las relaciones arquitectónicas; cada implementación se comprueba en su proyecto correspondiente.
