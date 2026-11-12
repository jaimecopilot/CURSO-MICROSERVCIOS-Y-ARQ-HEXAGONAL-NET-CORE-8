# ADR-032: Configuración básica de YARP

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado el patrón API Gateway. Es necesario definir la implementación concreta del gateway.

## Decisión
Se adopta Yarp.ReverseProxy 2.2.0 en AceriaApp.Gateway, con destino net8.0 y proceso independiente. `appsettings.json` contiene `ReverseProxy`, con `Routes` y `Clusters`. Se publican las órdenes y comunicación de Producción y los materiales y planificaciones de Inventario; Clientes no es un backend implementado. En 8.2 el gateway escucha en 5100 y apunta a Producción 5105 e Inventario 5106; en 8.4 Inventario añade 5107 y Producción mantiene un destino. Las direcciones se pueden sustituir por configuración de entorno. La correlación se valida mediante el middleware de M07 y se propaga mediante código; Location conserva una referencia pública. Los alias y la eliminación de /inventario se incorporan en 8.3. Se comprueban tanto el catálogo como el proxy real con Kestrel; SQL y RabbitMQ se acreditan mediante integración.

## Alternativas consideradas
- Ocelot: no se adopta para mantener la biblioteca YARP elegida en este laboratorio ASP.NET Core.
- Nginx: descartado por estar fuera del stack .NET.
- Gateway personalizado: descartado por complejidad.

## Consecuencias
- Positivas: integración con ASP.NET Core, configuración declarativa, coherencia con el stack.
- Negativas: la configuración requiere mantenimiento por entorno.
- Mitigación: la validación automática y las buenas prácticas documentadas.

## Alcance comprobable de esta etapa

El proyecto ejecutable AceriaApp.Gateway se construye en el paso 8.2.16. El catálogo es una descripción separada, no el archivo que YARP carga. Los nombres DNS ASCII para contenedores requieren una red que los resuelva; el recorrido local utiliza localhost y puertos explícitos. Aceptado expresa esta decisión arquitectónica, no un PASS de CI.

El directorio anterior se conserva intacto. Las copias del punto actual incluyen los cambios completos indicados en el manual.
