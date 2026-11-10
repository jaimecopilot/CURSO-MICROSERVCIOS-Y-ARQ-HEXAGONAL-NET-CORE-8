<!-- Documento de trabajo M03. Adaptación a AceriaApp.Api desde la fuente original íntegra en FUENTE. -->
# Capas de la aplicación — Punto 3.1

## Capas

1. Presentación.
2. Aplicación.
3. Dominio.
4. Infraestructura.

## Capa de dominio

Contiene entidades, value objects, agregados y reglas de negocio. No depende de ninguna otra capa.

## Capa de aplicación

Contiene casos de uso y orquestación. Depende del dominio. Define interfaces que la infraestructura implementa.

## Capa de infraestructura

Contiene implementaciones concretas: repositorios, clientes HTTP, publicadores de eventos. Depende de las interfaces definidas en las capas interiores.

## Capa de presentación

Contiene endpoints y controladores. Traduce entre el protocolo y los casos de uso. Depende de la aplicación.

## Regla de dependencia

Las dependencias se dirigen hacia el interior:

- Presentación → Aplicación → Dominio.
- Infraestructura → Aplicación → Dominio.
- Dominio no depende de nadie.

## Inversión de dependencias

Las interfaces se definen en las capas interiores y se implementan en las exteriores. El contenedor de dependencias inyecta la implementación.

## Arquitectura hexagonal

Núcleo central con dominio y aplicación, rodeado de puertos y adaptadores. Un mismo puerto puede tener varios adaptadores.

## Aplicación al proyecto del curso

| Capa | Contenido |
|------|-----------|
| Dominio | Entidades y reglas de negocio |
| Aplicación | Casos de uso e interfaces de repositorio |
| Infraestructura | Implementaciones de repositorio y EF Core |
| Presentación | Endpoints de Minimal API |

## Corrección de compatibilidad con el repositorio vigente

La implementación de partida no es `AceriaApp.Monolito.Api`, sino la Minimal API del proyecto `M02_APIS_REST_ASPNET_CORE/PROYECTO/2.4-documentacion-openapi`. Los ejemplos de esta ficha describen conceptos de diseño; su implementación real se incorpora al código en 3.3 y 3.4, con puertos de aplicación e infraestructura SQL Server. No se considera registrado un adaptador solo por mencionarlo en un catálogo.
