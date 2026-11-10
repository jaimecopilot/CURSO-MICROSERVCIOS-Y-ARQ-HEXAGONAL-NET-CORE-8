# ADR-012: Separación física entre dominio, aplicación e infraestructura

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado la arquitectura hexagonal con puertos y adaptadores. Es necesario decidir si la separación entre capas se realiza de forma lógica o física.

## Decisión
Se adopta la separación física: cada capa se agrupa en un proyecto independiente. El proyecto de dominio no referencia ningún otro proyecto. El proyecto de aplicación referencia el dominio. El proyecto de infraestructura referencia la aplicación y el dominio. El proyecto de presentación referencia la aplicación y la infraestructura. La separación se valida con un test que comprueba las referencias.

## Alternativas consideradas
- Separación lógica en carpetas: descartado por permitir violaciones invisibles.
- Un único proyecto para todas las capas: descartado por romper la regla de dependencia.

## Consecuencias
- Positivas: el compilador impide las violaciones, las dependencias son visibles, los tests referencian solo lo necesario.
- Negativas: la configuración de referencias requiere disciplina.
- Mitigación: validación automática con el validador.

## Adaptación técnica verificada del curso (M03)

Se parte de la API real y probada de M02, se conservan sus endpoints y se añaden reglas de dependencia verificadas en código. Los proyectos de Dominio, Aplicación e Infraestructura deben obedecer la dirección de referencias; en 3.4 se expone un nuevo adaptador HTTP funcional. El catálogo original se preserva sin atribuirle implementaciones que todavía no existen.
