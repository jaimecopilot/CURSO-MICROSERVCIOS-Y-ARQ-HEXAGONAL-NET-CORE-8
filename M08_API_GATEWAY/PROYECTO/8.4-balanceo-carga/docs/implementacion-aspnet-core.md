# Implementación en ASP.NET Core — Punto 3.4

## ASP.NET Core como adaptador de entrada

Los endpoints traducen entre HTTP y los puertos de entrada. No contienen reglas de negocio.

## ASP.NET Core como contenedor de dependencias

El contenedor registra las implementaciones de los puertos. Inyecta las implementaciones en los endpoints.

## Ciclos de vida

- Transient: nueva instancia en cada resolución.
- Scoped: una instancia por ámbito de petición.
- Singleton: una instancia por aplicación.

## Registro de adaptadores

| Adaptador | Ciclo |
|-----------|-------|
| OrdenRepositorioSqlServer | Scoped |
| InventarioRepositorioSqlServer | Scoped |
| PublicadorEventosRabbitMq | Singleton |
| ClienteInventarioHttp | Scoped |

## Endpoints como adaptadores de entrada

Los endpoints se agrupan por recurso en clases de extensión.

## Repositorios como adaptadores de salida

Los repositorios implementan los puertos de salida y conocen EF Core.

## Configuración del arranque

El arranque se organiza con métodos de extensión por área de configuración.

## Pruebas de la configuración

Los tests verifican los registros y los ciclos de vida.

## Cierre del módulo 3

El proyecto AceriaApp dispone de:

- Organización por capas con regla de dependencia.
- Puertos y adaptadores en capas separadas.
- Separación física entre dominio, aplicación e infraestructura.
- Contenedor de dependencias configurado con métodos de extensión.
- Setenta y cuatro pruebas unitarias acumuladas en catorce proyectos de tests.
- Doce puntos completados (1.1 a 1.5, 2.1 a 2.4 y 3.1 a 3.4).

## Corrección de compatibilidad con el repositorio vigente

La implementación de partida no es `AceriaApp.Monolito.Api`, sino la Minimal API del proyecto `M02_APIS_REST_ASPNET_CORE/PROYECTO/2.4-documentacion-openapi`. Los ejemplos de esta ficha describen conceptos de diseño; su implementación real se incorpora al código en 3.3 y 3.4, con puertos de aplicación e infraestructura SQL Server. No se considera registrado un adaptador solo por mencionarlo en un catálogo.
