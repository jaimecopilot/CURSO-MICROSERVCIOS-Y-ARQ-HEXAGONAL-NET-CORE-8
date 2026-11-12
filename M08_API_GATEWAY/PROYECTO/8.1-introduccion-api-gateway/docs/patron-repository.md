# Patrón Repository — Punto 4.1

## Definición

Abstracción que media entre la capa de dominio o aplicación y la capa de persistencia.

## Responsabilidades

- Recuperar entidades del almacenamiento.
- Añadir entidades al almacenamiento.
- Actualizar o eliminar entidades existentes.

## Lo que no debe hacer

- Contener reglas de negocio.
- Validar invariantes.
- Transformar entidades en DTOs.
- Ejecutar consultas complejas con múltiples JOINs.
- Gestionar transacciones de múltiples repositorios.

## Repositorio específico frente a genérico

- Específico: interfaz por entidad.
- Genérico: interfaz común para varias entidades.

## Repositorio y puertos de salida

La interfaz del repositorio es el puerto de salida de persistencia; la clase concreta es su adaptador de infraestructura.

## Repositorio y pruebas con dobles

Los repositorios se sustituyen por dobles en los tests de la aplicación. Este punto utiliza un repositorio en memoria para verificar el caso de uso sin EF Core y el adaptador relacional para comprobar persistencia.

## Repositorio y unidad de trabajo

El repositorio gestiona una entidad. La unidad de trabajo coordina varias.

## Cuándo usar el patrón

- Dominio complejo: sí.
- Varios repositorios: sí.
- Pruebas unitarias: sí.
- CRUD simple: no.
- Sin lógica de dominio: no.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Puerto ejecutable | IOrdenRepositorio, en la aplicación |
| Adaptador ejecutable | OrdenRepositorioSqlServer, en infraestructura |
| Operaciones ejecutables | ListarAsync, ObtenerAsync, AgregarAsync, GuardarAsync |
| Consultas complejas | Servicios específicos |
| Validación | Test de coherencia de repositorios |

## Correspondencia con el código ejecutable

El catálogo de este punto describe reglas de diseño y contiene ejemplos de contratos. Sus nombres no implican servicios registrados. La implementación utiliza los proyectos `AceriaApp.Hexagonal.Aplicacion`, `AceriaApp.Hexagonal.Dominio` y `AceriaApp.Hexagonal.Infraestructura`, compuestos desde `AceriaApp.Api`. Comprueba los archivos y los tests funcionales que incorpora el paso de compilación de este punto.
