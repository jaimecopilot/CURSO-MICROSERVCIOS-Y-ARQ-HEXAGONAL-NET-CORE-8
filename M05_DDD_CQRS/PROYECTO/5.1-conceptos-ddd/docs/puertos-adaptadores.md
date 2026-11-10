# Puertos y adaptadores — Punto 3.2

## Puerto

Interfaz que define cómo el núcleo se comunica con el exterior. Se define en el núcleo.

## Adaptador

Clase que implementa un puerto y conecta el núcleo con una tecnología concreta. Se define en el exterior.

## Tipos de puerto

- Puerto de entrada: lo que el núcleo ofrece al exterior.
- Puerto de salida: lo que el núcleo necesita del exterior.

## Tipos de adaptador

- Adaptador de entrada: traduce entre el protocolo y los puertos de entrada.
- Adaptador de salida: traduce entre los puertos de salida y la tecnología concreta.

## Puertos del proyecto

| Puerto | Tipo | Ubicación |
|--------|------|-----------|
| IOrdenServicio | Entrada | Aplicación |
| IInventarioServicio | Entrada | Aplicación |
| IOrdenRepositorio | Salida | Aplicación |
| IInventarioRepositorio | Salida | Aplicación |
| IPublicadorEventos | Salida | Aplicación |

## Adaptadores del proyecto

| Adaptador | Tipo | Ubicación |
|-----------|------|-----------|
| Endpoints de Minimal API | Entrada | Presentación |
| OrdenRepositorioSqlServer | Salida | Infraestructura |
| InventarioRepositorioSqlServer | Salida | Infraestructura |
| PublicadorEventosRabbitMq | Salida | Infraestructura |

## Inversión de dependencias

El núcleo depende del puerto. El adaptador implementa el puerto. El contenedor inyecta la implementación.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Puertos de entrada | Interfaces de casos de uso |
| Puertos de salida | Interfaces de recursos externos |
| Adaptadores entrada | Endpoints de Minimal API |
| Adaptadores salida | Repositorios SQL Server, publicador de eventos |
| Inversión | Registro en el contenedor de dependencias |

## Corrección de compatibilidad con el repositorio vigente

La implementación de partida no es `AceriaApp.Monolito.Api`, sino la Minimal API del proyecto `M02_APIS_REST_ASPNET_CORE/PROYECTO/2.4-documentacion-openapi`. Los ejemplos de esta ficha describen conceptos de diseño; su implementación real se incorpora al código en 3.3 y 3.4, con puertos de aplicación e infraestructura SQL Server. No se considera registrado un adaptador solo por mencionarlo en un catálogo.
