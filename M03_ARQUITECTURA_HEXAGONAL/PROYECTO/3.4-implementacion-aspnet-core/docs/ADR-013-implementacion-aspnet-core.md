# ADR-013: Implementación de la arquitectura hexagonal en ASP.NET Core

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado la separación física entre dominio, aplicación e infraestructura. Es necesario definir cómo se implementa la arquitectura hexagonal en ASP.NET Core y cómo se configura el contenedor de dependencias.

## Decisión
Los endpoints se agrupan por recurso en clases de extensión. Los repositorios se implementan como adaptadores de salida en la capa de infraestructura. Los servicios de aplicación se implementan como puertos de entrada. El contenedor de dependencias se configura con métodos de extensión por área. La configuración se valida con tests que verifican los registros y los ciclos de vida. Se adopta el ciclo Scoped para los adaptadores de base de datos y Singleton para los adaptadores sin estado.

## Alternativas consideradas
- Registro directo en Program.cs: descartado por crecimiento del archivo.
- Uso de un contenedor externo: descartado por simplicidad del proyecto.
- Ciclo Transient para todos los servicios: descartado por coste de instanciación.

## Consecuencias
- Positivas: configuración legible, validación automática, ciclos adecuados.
- Negativas: la configuración requiere disciplina en el registro.
- Mitigación: validación automática con el validador.

## Adaptación técnica verificada del curso (M03)

Se parte de la API real y probada de M02, se conservan sus endpoints y se añaden reglas de dependencia verificadas en código. Los proyectos de Dominio, Aplicación e Infraestructura deben obedecer la dirección de referencias; en 3.4 se expone un nuevo adaptador HTTP funcional. El catálogo original se preserva sin atribuirle implementaciones que todavía no existen.
