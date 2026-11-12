# Introducción al patrón API Gateway — Punto 8.1

## Definición

Componente que actúa como punto de entrada único a un conjunto de servicios.

## Responsabilidades

- Enrutamiento: dirigir la petición al servicio.
- Traducción: puede adaptar protocolos cuando se implementa esa capacidad; este laboratorio publica HTTP mediante un proxy inverso.
- Agregación: puede combinar respuestas mediante una implementación específica; el proxy de este módulo no incorpora agregación de negocio.
- Políticas transversales: puede concentrar autenticación, autorización y limitación de tasa si se configuran sus componentes. Los flags del catálogo no las activan.

## Lo que no debe hacer

- Contener reglas de negocio.
- Transformar el modelo del dominio.
- Introducir un punto único de fallo sin medidas de disponibilidad. Una sola instancia del gateway sí constituye ese riesgo; la redundancia requiere un despliegue adicional.
- Almacenar el estado de negocio de los servicios.
- Acceder directamente a la base de datos.

## Diferencia con balanceador

| Aspecto | Balanceador | Gateway |
|---------|-------------|---------|
| Distribuye entre | Instancias de un servicio o un conjunto de destinos | Servicios y, si se configura, sus instancias |
| Capa | Puede operar en transporte o en aplicación | Aplicación |
| Conoce rutas | Un balanceador HTTP puede conocerlas | Usa rutas para seleccionar el servicio |

## Patrones

- Gateway único.
- Gateway por cliente.
- Gateway por dominio.
- BFF (Backend For Frontend).

## Funciones transversales

- Autenticación, autorización y limitación de tasa: capacidades posibles que requieren registro y configuración; no están implementadas por los indicadores de los catálogos.
- Registro: el gateway ejecutable reutiliza el middleware JSON de M07.
- Monitorización: las señales del gateway complementan las de cada servicio; no sustituyen sus comprobaciones de dependencias.

## Seguridad

Un gateway puede aplicar políticas de seguridad configuradas expresamente. En este laboratorio se delimitan las rutas publicadas y se valida el identificador de correlación. No se han instalado autenticación, autorización ni cuotas mediante los flags del catálogo. La validación de negocio sigue en los servicios; impedir el acceso directo a los backends requiere controles de red adicionales.

## Observabilidad

El gateway registra sus propias peticiones y propaga el identificador de correlación validado por el middleware de M07. Producción e Inventario conservan sus propios registros y sus responsabilidades de salud. Una cabecera de correlación inválida se sustituye en el borde y el valor validado se reenvía a los servicios.

## Ventajas

- Simplificación del cliente.
- Centralización de políticas.
- Ocultación de la topología.
- Observabilidad.

## Inconvenientes

- Punto único de fallo.
- Latencia adicional.
- Complejidad operativa.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Gateway | Catálogo de diseño en 8.1; proceso AceriaApp.Gateway con YARP a partir de 8.2 |
| Rutas | Recursos de Producción e Inventario; Clientes es un ejemplo conceptual |
| Políticas | Registro y correlación implementados; autenticación y cuotas solo declaradas en el catálogo |
| Punto de entrada | Gateway público en 5100; los puertos de backend siguen accesibles en el entorno local |
| Validación | Tests del catálogo; desde 8.2 se añaden pruebas de proxy HTTP real |

## Alcance comprobable de esta etapa

Los flags AplicaAutenticacion y AplicaRateLimit son declaraciones del catálogo. No activan middleware. Clientes.Api es un ejemplo de diseño; no existe un tercer backend implementado en este laboratorio.

El directorio anterior se conserva intacto. Las copias del punto actual incluyen los cambios completos indicados en el manual.
