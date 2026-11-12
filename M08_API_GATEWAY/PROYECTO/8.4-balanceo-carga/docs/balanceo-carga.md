# Balanceo de carga básico — Punto 8.4

## Definición

Distribución del tráfico entre varias instancias de un servicio.

## Algoritmos de balanceo

- RoundRobin: distribución cíclica.
- Random: distribución aleatoria.
- LeastRequests: instancia con menos peticiones.
- PowerOfTwoChoices: mejor entre dos aleatorias.
- Ponderado: concepto de distribución según pesos; requiere una política personalizada y no está implementado en este laboratorio.

## Configuración de destinos múltiples

    {
      "ReverseProxy": {
        "Clusters": {
          "inventario-cluster": {
            "LoadBalancingPolicy": "RoundRobin",
            "Destinations": {
              "inventario-1": { "Address": "http://localhost:5106/" },
              "inventario-2": { "Address": "http://localhost:5107/" }
            }
          },
          "produccion-cluster": {
            "Destinations": {
              "produccion": { "Address": "http://localhost:5105/" }
            }
          }
        }
      }
    }


## Pesos de destino

YARP no incorpora una propiedad nativa `Weight` en la configuración de destinos utilizada aquí. Un dato Weight en metadatos solo tendría efecto si una extensión lo interpretara y una política personalizada seleccionara los destinos según ese dato. El indicador TienePesos del catálogo expresa una decisión conceptual; no instala esa extensión. El laboratorio utiliza dos destinos equivalentes de Inventario sin ponderación.

## Algoritmo en YARP

La propiedad `LoadBalancingPolicy` del cluster configura el algoritmo. Este módulo fija `RoundRobin` expresamente en inventario-cluster; no depende del algoritmo predeterminado de YARP. La sobrecarga sin argumentos de `MapReverseProxy()` incorpora el middleware de balanceo. El reparto cíclico se aplica a solicitudes nuevas entre destinos disponibles; no garantiza igual duración de trabajo ni reintenta escrituras.

## Balanceo y health checks

El cluster de Inventario activa sondeos a `/health/ready`, con intervalo y timeout de un segundo, política `ConsecutiveFailures` y umbral de dos fallos consecutivos. `AvailableDestinationsPolicy: HealthyAndUnknown` permite destinos sanos o todavía no clasificados y excluye los marcados Unhealthy. Si no queda ninguno disponible, devuelve 503; una petición ya asignada puede fallar durante la detección. Un sondeo satisfactorio permite reincorporar la instancia recuperada sin reiniciar el gateway. Estos checks deben configurarse: declarar su intención en el catálogo no los activa.

## Balanceo en contenedores

- Kubernetes: Service balancea entre pods.
- Docker Swarm: Service balancea entre tasks.
- Gateway: balancea entre instancias del servicio.

## Estrategias de escalado

- Horizontal: añade instancias.
- Vertical: aumenta recursos.
- Automático: ajusta instancias según métricas.

## Buenas prácticas

1. Disponer de varios destinos en el servicio cuyo reparto se quiere comprobar. Aquí Inventario tiene dos y Producción conserva uno; no se declara alta disponibilidad completa del sistema.
2. Algoritmo adecuado al contexto.
3. Combinar con health checks.
4. Registrar métricas por instancia.
5. Validar con un test.

## Cierre del módulo 8

El cierre del módulo exige comprobar el estado siguiente en los proyectos reconstruidos y sus informes:

- Patrón API Gateway con punto de entrada único.
- Configuración de YARP con rutas y clusters.
- Enrutamiento con precedencia, transformaciones y orden.
- Balanceo RoundRobin entre dos destinos de Inventario y un destino de Producción.
- Inventario final de 39 proyectos, 26 proyectos de pruebas y 50 documentos.
- Objetivo de 491 pruebas acumuladas sin omisiones en la etapa 8.4; se acredita ejecutándolas, no mediante esta descripción.
- Cobertura docente de ocho módulos y 34 puntos; el cierre requiere las evidencias Linux, Windows y PDF y su revisión.

## Cierre del curso

El recorrido del curso reúne los módulos siguientes:

| Módulo | Tema | Puntos |
|--------|------|-------:|
| 1 | Introducción a los microservicios | 5 |
| 2 | APIs REST con ASP.NET Core | 4 |
| 3 | Arquitectura hexagonal | 4 |
| 4 | Patrones de arquitectura | 5 |
| 5 | DDD y CQRS | 5 |
| 6 | Comunicación entre microservicios | 3 |
| 7 | Observabilidad y resiliencia | 4 |
| 8 | Publicación mediante API Gateway | 4 |
| Total | Ocho módulos | 34 |

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Clusters | Inventario: 5106 y 5107; Producción: 5105 |
| Política | RoundRobin explícito en Inventario; sin pesos |
| Health checks | Sondeos activos de Inventario y HealthyAndUnknown; todos Unhealthy produce 503 |
| Identidad | X-Instancia distingue inventario-1 e inventario-2; ambas usan la misma base SQL |
| Validación | Tests del catálogo y Kestrel; integración real de SQL, RabbitMQ y LocalDB acreditada por sus informes |

## Alcance comprobable de esta etapa

El comportamiento a verificar es reparto entre ambas identidades, retirada de un destino caído, respuesta 503 cuando todos están no disponibles y reincorporación al recuperarse. Los informes deben corresponder a los mismos archivos y revisión que se entregan. Los recuentos esperados y el estado Aceptado de los ADR no equivalen a un resultado PASS de CI.

El directorio anterior se conserva intacto. Las copias del punto actual incluyen los cambios completos indicados en el manual.
