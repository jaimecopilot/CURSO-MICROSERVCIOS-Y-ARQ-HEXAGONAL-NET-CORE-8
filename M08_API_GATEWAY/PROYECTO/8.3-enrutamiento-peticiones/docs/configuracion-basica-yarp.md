# Configuración básica de YARP — Punto 8.2

## YARP

Biblioteca de .NET para construir proxies inversos y gateways. El proyecto AceriaApp.Gateway de este módulo utiliza Yarp.ReverseProxy 2.2.0 y tiene como destino net8.0. Se ejecuta como proceso independiente, sin acceso a las bases ni referencias al dominio.

## Ruta

Relación entre una petición entrante y un cluster destino.

## Cluster

Conjunto de destinos a los que se enruta una petición.

## Relación ruta-cluster

Varias rutas pueden apuntar al mismo cluster.

## Integración con ASP.NET Core

    builder.Services.AddReverseProxy()
        .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

    app.MapReverseProxy();


## Estructura de la configuración

    {
      "ReverseProxy": {
        "Routes": {
          "ordenes": {
            "ClusterId": "produccion-cluster",
            "Match": { "Path": "/api/v1/ordenes/{**resto}" }
          },
          "materiales": {
            "ClusterId": "inventario-cluster",
            "Match": { "Path": "/api/v1/materiales/{**resto}", "Methods": [ "GET", "HEAD" ] }
          }
        },
        "Clusters": {
          "produccion-cluster": {
            "Destinations": {
              "produccion": { "Address": "http://localhost:5105/" }
            }
          },
          "inventario-cluster": {
            "Destinations": {
              "inventario-1": { "Address": "http://localhost:5106/" }
            }
          }
        }
      }
    }


## Transformaciones

Adaptan la petición antes de enviarla al destino o la respuesta antes de devolverla al cliente. Las transformaciones declarativas se configuran en `Transforms` de la ruta. En 8.2 la propagación del identificador validado y el ajuste de Location se implementan en C#; el middleware de M07 valida la correlación antes de reenviarla. Las transformaciones del alias de Inventario se incorporan en 8.3.

## Configuración por entorno

Puede complementarse con `appsettings.Development.json`, `appsettings.Production.json` y variables de entorno según el despliegue. La configuración entregada del gateway está en `appsettings.json`; las direcciones de destino se pueden sustituir con claves como `ReverseProxy__Clusters__produccion-cluster__Destinations__produccion__Address`. El recorrido local utiliza Gateway 5100, Producción 5105 e Inventario 5106. Los nombres DNS ASCII de un entorno de contenedores solo funcionan si esa red los resuelve.

## Buenas prácticas

1. Identificadores descriptivos.
2. Configuración separada por entorno.
3. Transformaciones solo cuando son necesarias.
4. Documentar en el ADR.
5. Validar con un test.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Proyecto gateway | AceriaApp.Gateway |
| Configuración | appsettings.json |
| Rutas | Órdenes y comunicación de Producción; materiales y planificaciones de Inventario |
| Clusters | produccion-cluster hacia 5105 e inventario-cluster hacia 5106 en 8.2 |
| Transformaciones | Propagación de correlación validada y Location público; el alias de prefijo se añade en 8.3 |
| Validación | Tests del catálogo y del proxy con Kestrel; la integración SQL y RabbitMQ se acredita por separado |

## Alcance comprobable de esta etapa

El proyecto ejecutable AceriaApp.Gateway se construye en el paso 8.2.16. El catálogo es una descripción separada, no el archivo que YARP carga. La configuración completa incluye también las rutas de Producción y comunicación y las planificaciones de Inventario. Clientes.Api sigue siendo conceptual y no existe como tercer backend del laboratorio. En 8.4 se añade un segundo destino de Inventario en 5107; Producción conserva un destino.

El directorio anterior se conserva intacto. Las copias del punto actual incluyen los cambios completos indicados en el manual.
