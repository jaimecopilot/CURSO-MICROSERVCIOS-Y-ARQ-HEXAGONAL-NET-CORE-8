# Separación entre dominio, aplicación e infraestructura — Punto 3.3

## Formas de separación

- Lógica: carpetas dentro de un mismo proyecto.
- Física: proyectos independientes.

## Proyectos del sistema

| Proyecto | Contenido | Referencias |
|----------|-----------|-------------|
| AceriaApp.Hexagonal.Dominio | Entidades y reglas de negocio | Ninguna |
| AceriaApp.Hexagonal.Aplicacion | Puertos y servicios | Dominio |
| AceriaApp.Hexagonal.Infraestructura | Repositorios y adaptadores | Aplicación y Dominio |
| AceriaApp.Api | Endpoints y configuración | Aplicación e Infraestructura |

## Regla de dependencia en la separación física

- Dominio no referencia ningún proyecto del sistema.
- Aplicación referencia solo Dominio.
- Infraestructura referencia Aplicación y Dominio.
- Api referencia Aplicación e Infraestructura.

## Ventajas

- El compilador impide las violaciones de la regla.
- Las dependencias son visibles en el archivo `.csproj`.
- Los tests referencian solo los proyectos que necesitan.
- Las bibliotecas pueden reutilizarse en distintas aplicaciones.

## Contenedor de dependencias

La presentación registra las implementaciones de los puertos. El contenedor resuelve las dependencias en tiempo de ejecución.

## Aplicación al proyecto del curso

| Proyecto | Publicación |
|----------|-------------|
| Dominio | Biblioteca reutilizable |
| Aplicación | Biblioteca reutilizable |
| Infraestructura | Biblioteca reutilizable |
| Api | Aplicación ejecutable |

## Corrección de compatibilidad con el repositorio vigente

La implementación de partida no es `AceriaApp.Monolito.Api`, sino la Minimal API del proyecto `M02_APIS_REST_ASPNET_CORE/PROYECTO/2.4-documentacion-openapi`. Los ejemplos de esta ficha describen conceptos de diseño; su implementación real se incorpora al código en 3.3 y 3.4, con puertos de aplicación e infraestructura SQL Server. No se considera registrado un adaptador solo por mencionarlo en un catálogo.
