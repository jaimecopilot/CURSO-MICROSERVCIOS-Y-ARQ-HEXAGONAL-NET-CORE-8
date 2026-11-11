# ADR-014: Adopción del patrón Repository

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha cerrado el módulo 3 con una arquitectura hexagonal completa. Es necesario definir la abstracción de acceso a datos que usará la capa de aplicación.

## Decisión
Se adopta el patrón Repository con repositorios específicos por entidad. El contrato ejecutable IOrdenRepositorio expone ListarAsync, ObtenerAsync, AgregarAsync y GuardarAsync. No contiene una operación Delete. El catálogo estudia ejemplos de repositorios con cinco o cuatro métodos; esas cantidades no se presentan como una inspección del contrato real. Los repositorios no contienen reglas de negocio, no validan invariantes, no transforman entidades en DTOs, no ejecutan consultas complejas y no gestionan transacciones. Las consultas complejas se delegan en servicios específicos. La coherencia de los ejemplos se valida con el catálogo y el contrato real se comprueba con cuatro pruebas funcionales: doble sin EF, capacidad, lectura desde otro contexto y persistencia de la transición.

## Alternativas consideradas
- Acceso directo a EF Core desde la aplicación: descartado por acoplar la aplicación a la tecnología.
- Repositorio genérico único: descartado por pérdida de expresividad.
- Sin repositorio, uso de DbContext directamente: descartado por dificultad de pruebas.

## Consecuencias
- Positivas: independencia de la tecnología, pruebas con dobles, separación de responsabilidades.
- Negativas: la interfaz del repositorio debe mantenerse simple.
- Mitigación: validación automática con el validador.
