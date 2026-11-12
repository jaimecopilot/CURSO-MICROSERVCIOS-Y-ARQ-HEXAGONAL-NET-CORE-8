# ADR-031: Adopción del patrón API Gateway

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha cerrado el módulo 7 con observabilidad y resiliencia. Es necesario definir un punto de entrada único para los servicios y centralizar las preocupaciones transversales.

## Decisión
Se adopta el patrón API Gateway como entrada pública de los recursos de Producción e Inventario. El punto 8.1 modela sus responsabilidades y desde 8.2 se ejecuta un proceso YARP independiente. Reutiliza el registro JSON y la correlación de M07; autenticación, autorización y limitación de tasa requieren componentes adicionales y no se implementan mediante flags del catálogo. Clientes es un ejemplo conceptual, sin tercer backend. El gateway no contiene reglas de negocio, no transforma el dominio, no persiste estado de negocio ni accede a las bases. Una instancia única sí introduce un riesgo de disponibilidad; la redundancia es una medida adicional de despliegue. Los tests del catálogo comprueban las declaraciones y las pruebas de proxy verifican el comportamiento HTTP implementado.

## Alternativas consideradas
- Exposición directa de los servicios: descartado por falta de centralización.
- Gateway por cliente: descartado por simplicidad del proyecto.
- Balanceador sin gateway: no se elige como sustituto de la publicación por rutas y las responsabilidades de entrada adoptadas.

## Consecuencias
- Positivas: simplificación del cliente, centralización de políticas, ocultación de la topología, observabilidad.
- Negativas: punto único de fallo, latencia adicional, complejidad operativa.
- Mitigación prevista: redundancia del gateway, monitorización y despliegue con varias instancias. El laboratorio local no despliega esa redundancia ni bloquea por sí mismo el acceso directo a los backends.

## Alcance comprobable de esta etapa

Los flags AplicaAutenticacion y AplicaRateLimit son declaraciones del catálogo. No activan middleware. Clientes.Api es un ejemplo de diseño; no existe un tercer backend implementado en este laboratorio.

El directorio anterior se conserva intacto. Las copias del punto actual incluyen los cambios completos indicados en el manual.
