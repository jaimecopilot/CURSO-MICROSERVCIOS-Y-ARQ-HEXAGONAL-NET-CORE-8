# M08 — Cobertura canónica y correcciones

**Autor del curso: JAIME GALLO**

Este documento relaciona el temario canónico con la adaptación acumulativa del repositorio. Distingue cobertura editorial, decisiones técnicas y evidencia de ejecución. Una declaración del catálogo o una revisión narrativa no acredita comportamiento de proxy ni integración con infraestructura real.

## Identidad y base de comparación

La exportación original `Curso Micro Haxagonal Net Core 8.md` contiene el temario y los cuatro desarrollos completos de M08. Su SHA-256 es `28044646ed46801f1cc86bbb5e9df56f02175796ccaa0d58e6e27ec39c651091`. El ZIP incluye además una representación HTML y un prompt maestro TXT; no incluye una solución ejecutable de M08. La exportación íntegra no forma parte del material docente del repositorio.

La base remota aprobada es `16a1a0783e14eaf1c4cdb07f25a13d6719f286d2`. El punto 7.4 de M07 aporta 34 proyectos, 22 proyectos de pruebas, 403 pruebas y 42 documentos. M01–M07 se conservan. Los formatos y restricciones anteriores del curso prevalecen sobre referencias históricas a carpetas de autoría, duraciones o herramientas obsoletas.

Los hashes de la tabla siguiente corresponden a cada respuesta canónica extraída, desde el título del punto hasta su cierre, uniendo líneas con LF y un salto final. Las líneas se refieren al Markdown íntegro identificado arriba.

| Punto | Líneas inclusivas | SHA-256 de respuesta canónica |
|---|---|---|
| 8.1 | 44816–46046 | `235f70ef76a6626fe38831d61976ce0c9328405ec56d74d462bdbda5b22ac39b` |
| 8.2 | 46093–47313 | `4a0b1371e7efb11e1bf6c88e6dc24da6eb4288369220b4b3e5590142fc29a3f7` |
| 8.3 | 47372–48564 | `dbec507d6cece7f2bcc8339e04a902839a53e7be67176fc7cc5b0e8059e52438` |
| 8.4 | 48588–49805 | `0d8b86522d6d5965108bdb6aeab59ebf5d90aedd18b69b5472901d9559269d38` |

## Cobertura teórica

`TEORIA/M08_TEORIA.md` conserva los cuarenta bloques y sus objetivos y resúmenes. Cada bloque incorpora una sección `Ampliación didáctica aplicada a AceriaApp` con fundamento, ejemplo, límite y comprobación. Los cuarenta ejemplos conservan el contenido conceptual y corrigen los contratos de biblioteca que se detallan después. Sus 280 líneas físicas disponen de explicación individual, incluidas las vacías. Las doce figuras se suministran en SVG y PNG con interpretación junto a cada imagen.

La revisión editorial comparó 165 líneas sustantivas de prosa, encabezados y resumen del original con el texto final, aplicando únicamente las sustituciones explícitas de corrección. No se eliminó ningún bloque. Los fragmentos son didácticos; la configuración completa y los resultados ejecutados se documentan en prácticas e informes de validación.

| Punto/bloque | Título canónico | Ubicación de teoría y criterio de conservación |
|---|---|---|
| 8.1 / 1 | Definición de API Gateway | Punto 8.1, bloque 1; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.1 / 2 | Responsabilidades del API Gateway | Punto 8.1, bloque 2; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.1 / 3 | Lo que un API Gateway no debe hacer | Punto 8.1, bloque 3; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.1 / 4 | Diferencia entre API Gateway y balanceador | Punto 8.1, bloque 4; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.1 / 5 | Patrones de API Gateway | Punto 8.1, bloque 5; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.1 / 6 | Funciones transversales del API Gateway | Punto 8.1, bloque 6; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.1 / 7 | API Gateway y seguridad | Punto 8.1, bloque 7; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.1 / 8 | API Gateway y observabilidad | Punto 8.1, bloque 8; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.1 / 9 | Ventajas e inconvenientes del API Gateway | Punto 8.1, bloque 9; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.1 / 10 | Aplicación al proyecto del curso | Punto 8.1, bloque 10; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.2 / 1 | Definición de YARP | Punto 8.2, bloque 1; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.2 / 2 | Concepto de ruta en YARP | Punto 8.2, bloque 2; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.2 / 3 | Concepto de cluster en YARP | Punto 8.2, bloque 3; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.2 / 4 | Relación entre ruta y cluster | Punto 8.2, bloque 4; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.2 / 5 | Integración de YARP con ASP.NET Core | Punto 8.2, bloque 5; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.2 / 6 | Estructura de la configuración | Punto 8.2, bloque 6; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.2 / 7 | Transformaciones de YARP | Punto 8.2, bloque 7; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.2 / 8 | Configuración por entorno | Punto 8.2, bloque 8; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.2 / 9 | Buenas prácticas de configuración de YARP | Punto 8.2, bloque 9; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.2 / 10 | Aplicación al proyecto del curso | Punto 8.2, bloque 10; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.3 / 1 | Proceso de coincidencia de rutas | Punto 8.3, bloque 1; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.3 / 2 | Patrones de ruta | Punto 8.3, bloque 2; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.3 / 3 | Precedencia de rutas | Punto 8.3, bloque 3; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.3 / 4 | Transformaciones de ruta | Punto 8.3, bloque 4; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.3 / 5 | Transformaciones de cabecera | Punto 8.3, bloque 5; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.3 / 6 | Transformaciones de consulta | Punto 8.3, bloque 6; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.3 / 7 | Orden de aplicación de las transformaciones | Punto 8.3, bloque 7; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.3 / 8 | Enrutamiento basado en cabeceras | Punto 8.3, bloque 8; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.3 / 9 | Buenas prácticas de enrutamiento | Punto 8.3, bloque 9; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.3 / 10 | Aplicación al proyecto del curso | Punto 8.3, bloque 10; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.4 / 1 | Definición de balanceo de carga | Punto 8.4, bloque 1; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.4 / 2 | Algoritmos de balanceo | Punto 8.4, bloque 2; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.4 / 3 | Configuración de destinos múltiples | Punto 8.4, bloque 3; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.4 / 4 | Pesos de destino | Punto 8.4, bloque 4; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.4 / 5 | Algoritmo de balanceo en YARP | Punto 8.4, bloque 5; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.4 / 6 | Balanceo y health checks | Punto 8.4, bloque 6; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.4 / 7 | Balanceo en contenedores | Punto 8.4, bloque 7; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.4 / 8 | Estrategias de escalado | Punto 8.4, bloque 8; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.4 / 9 | Buenas prácticas de balanceo de carga | Punto 8.4, bloque 9; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |
| 8.4 / 10 | Aplicación al proyecto del curso y cierre del curso | Punto 8.4, bloque 10; desarrollo conservado, ejemplo corregido si procede y ampliación técnica propia. |

## Cobertura de práctica y artefactos

El contrato de reconstrucción mantiene 24 pasos por punto, 96 en total. La tabla enumera los pasos canónicos que deben poder localizarse en cada etapa del manual. La implementación añade el gateway real y sus ensayos dentro de esos recorridos sin sustituir los catálogos originales. La comprobación final de manual, reconstrucción, proyectos y pruebas corresponde a los informes generados sobre la revisión concreta; esta matriz no declara esas ejecuciones terminadas.

| Punto/paso | Requisito canónico | Adaptación del acumulado |
|---|---|---|
| 8.1 / 1 | Crear la estructura del módulo 8 y del punto 8.1 | Crear etapa independiente desde la anterior; conservar los puntos aprobados. |
| 8.1 / 2 | Abrir la solución copiada en Visual Studio 2026 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.1 / 3 | Verificar que la carpeta `docs` contiene los documentos del punto 7.4 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.1 / 4 | Crear el documento de introducción al API Gateway en `docs` | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.1 / 5 | Crear la carpeta `ApiGateway` en el proyecto monolítico | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.1 / 6 | Crear la clase `RutaGateway` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.1 / 7 | Crear la clase `ValidadorApiGateway` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.1 / 8 | Añadir los `using` necesarios en `ValidadorApiGateway` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.1 / 9 | Crear la clase `CatalogoRutas` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.1 / 10 | Añadir el `using` necesario en `CatalogoRutas` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.1 / 11 | Crear el proyecto de tests del punto 8.1 | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.1 / 12 | Añadir la referencia del proyecto de tests a la API monolítica | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.1 / 13 | Añadir el paquete `FluentAssertions` al proyecto de tests | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.1 / 14 | Crear el archivo `ValidadorApiGatewayTests.cs` | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.1 / 15 | Crear el archivo `CatalogoRutasTests.cs` | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.1 / 16 | Compilar la solución completa | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.1 / 17 | Ejecutar todos los tests del punto 8.1 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.1 / 18 | Ejecutar todos los tests de la solución | Usar los recuentos efectivos del acumulado, sin trasladar cifras históricas del chat. |
| 8.1 / 19 | Crear el README del punto 8.1 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.1 / 20 | Crear el ADR-031 del punto 8.1 | Conservar ADR-031/032/033/034 según punto y explicar la implementación real. |
| 8.1 / 21 | Verificar que no se ha modificado ningún archivo del punto 7.4 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.1 / 22 | Verificar la estructura del punto 8.1 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.1 / 23 | Verificar el `.gitignore` del punto 8.1 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.1 / 24 | Hacer el commit del punto 8.1 y verificar el estado final | Conservar la trazabilidad de versión y estado; publicar según el procedimiento autorizado del proyecto. |
| 8.2 / 1 | Crear la carpeta del punto 8.2 a partir del punto 8.1 | Crear etapa independiente desde la anterior; conservar los puntos aprobados. |
| 8.2 / 2 | Abrir la solución copiada en Visual Studio 2026 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.2 / 3 | Verificar que la carpeta `docs` contiene los documentos del punto 8.1 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.2 / 4 | Crear el documento de configuración básica de YARP en `docs` | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.2 / 5 | Crear la carpeta `ConfiguracionYarp` en el proyecto monolítico | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.2 / 6 | Crear la clase `ClusterYarp` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.2 / 7 | Crear la clase `ValidadorConfiguracionYarp` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.2 / 8 | Añadir los `using` necesarios en `ValidadorConfiguracionYarp` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.2 / 9 | Crear la clase `CatalogoClusters` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.2 / 10 | Añadir el `using` necesario en `CatalogoClusters` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.2 / 11 | Crear el proyecto de tests del punto 8.2 | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.2 / 12 | Añadir la referencia del proyecto de tests a la API monolítica | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.2 / 13 | Añadir el paquete `FluentAssertions` al proyecto de tests | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.2 / 14 | Crear el archivo `ValidadorConfiguracionYarpTests.cs` | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.2 / 15 | Crear el archivo `CatalogoClustersTests.cs` | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.2 / 16 | Compilar la solución completa | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.2 / 17 | Ejecutar todos los tests del punto 8.2 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.2 / 18 | Ejecutar todos los tests de la solución | Usar los recuentos efectivos del acumulado, sin trasladar cifras históricas del chat. |
| 8.2 / 19 | Crear el README del punto 8.2 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.2 / 20 | Crear el ADR-032 del punto 8.2 | Conservar ADR-031/032/033/034 según punto y explicar la implementación real. |
| 8.2 / 21 | Verificar que no se ha modificado ningún archivo del punto 8.1 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.2 / 22 | Verificar la estructura del punto 8.2 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.2 / 23 | Verificar el `.gitignore` del punto 8.2 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.2 / 24 | Hacer el commit del punto 8.2 y verificar el estado final | Conservar la trazabilidad de versión y estado; publicar según el procedimiento autorizado del proyecto. |
| 8.3 / 1 | Crear la carpeta del punto 8.3 a partir del punto 8.2 | Crear etapa independiente desde la anterior; conservar los puntos aprobados. |
| 8.3 / 2 | Abrir la solución copiada en Visual Studio 2026 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.3 / 3 | Verificar que la carpeta `docs` contiene los documentos del punto 8.2 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.3 / 4 | Crear el documento de enrutamiento de peticiones en `docs` | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.3 / 5 | Crear la carpeta `Enrutamiento` en el proyecto monolítico | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.3 / 6 | Crear la clase `ReglaEnrutamiento` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.3 / 7 | Crear la clase `ValidadorEnrutamiento` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.3 / 8 | Añadir los `using` necesarios en `ValidadorEnrutamiento` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.3 / 9 | Crear la clase `CatalogoReglasEnrutamiento` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.3 / 10 | Añadir el `using` necesario en `CatalogoReglasEnrutamiento` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.3 / 11 | Crear el proyecto de tests del punto 8.3 | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.3 / 12 | Añadir la referencia del proyecto de tests a la API monolítica | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.3 / 13 | Añadir el paquete `FluentAssertions` al proyecto de tests | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.3 / 14 | Crear el archivo `ValidadorEnrutamientoTests.cs` | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.3 / 15 | Crear el archivo `CatalogoReglasEnrutamientoTests.cs` | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.3 / 16 | Compilar la solución completa | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.3 / 17 | Ejecutar todos los tests del punto 8.3 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.3 / 18 | Ejecutar todos los tests de la solución | Usar los recuentos efectivos del acumulado, sin trasladar cifras históricas del chat. |
| 8.3 / 19 | Crear el README del punto 8.3 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.3 / 20 | Crear el ADR-033 del punto 8.3 | Conservar ADR-031/032/033/034 según punto y explicar la implementación real. |
| 8.3 / 21 | Verificar que no se ha modificado ningún archivo del punto 8.2 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.3 / 22 | Verificar la estructura del punto 8.3 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.3 / 23 | Verificar el `.gitignore` del punto 8.3 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.3 / 24 | Hacer el commit del punto 8.3 y verificar el estado final | Conservar la trazabilidad de versión y estado; publicar según el procedimiento autorizado del proyecto. |
| 8.4 / 1 | Crear la carpeta del punto 8.4 a partir del punto 8.3 | Crear etapa independiente desde la anterior; conservar los puntos aprobados. |
| 8.4 / 2 | Abrir la solución copiada en Visual Studio 2026 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.4 / 3 | Verificar que la carpeta `docs` contiene los documentos del punto 8.3 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.4 / 4 | Crear el documento de balanceo de carga en `docs` | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.4 / 5 | Crear la carpeta `Balanceo` en el proyecto monolítico | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.4 / 6 | Crear la clase `ClusterBalanceo` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.4 / 7 | Crear la clase `ValidadorBalanceo` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.4 / 8 | Añadir los `using` necesarios en `ValidadorBalanceo` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.4 / 9 | Crear la clase `CatalogoClustersBalanceo` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.4 / 10 | Añadir el `using` necesario en `CatalogoClustersBalanceo` | Adaptar a AceriaApp.Api y conservar modelo, validador, catálogo y contratos del ejercicio. |
| 8.4 / 11 | Crear el proyecto de tests del punto 8.4 | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.4 / 12 | Añadir la referencia del proyecto de tests a la API monolítica | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.4 / 13 | Añadir el paquete `FluentAssertions` al proyecto de tests | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.4 / 14 | Crear el archivo `ValidadorBalanceoTests.cs` | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.4 / 15 | Crear el archivo `CatalogoClustersBalanceoTests.cs` | Conservar casos originales y referencias del acumulado; añadir pruebas reales del proxy por separado. |
| 8.4 / 16 | Compilar la solución completa | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.4 / 17 | Ejecutar todos los tests del punto 8.4 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.4 / 18 | Ejecutar todos los tests de la solución | Usar los recuentos efectivos del acumulado, sin trasladar cifras históricas del chat. |
| 8.4 / 19 | Crear el README del punto 8.4 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.4 / 20 | Crear el ADR-034 del punto 8.4 | Conservar ADR-031/032/033/034 según punto y explicar la implementación real. |
| 8.4 / 21 | Verificar que no se ha modificado ningún archivo del punto 8.3 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.4 / 22 | Verificar la estructura del punto 8.4 y la estructura completa del curso | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.4 / 23 | Verificar el `.gitignore` del punto 8.4 | Conservar el requisito en la etapa correspondiente y añadir verificaciones funcionales cuando corresponda. |
| 8.4 / 24 | Hacer el commit del punto 8.4 y verificar el estado final del curso | Conservar la trazabilidad de versión y estado; publicar según el procedimiento autorizado del proyecto. |

Los pasos históricos que indican “no modificar ningún archivo” se interpretan como preservación de la etapa anterior. La nueva etapa puede modificar su propia solución y configuración para añadir componentes efectivos. La solución acumulativa del repositorio se llama `AceriaApp`; los namespaces se adaptan a su proyecto `AceriaApp.Api` y no se crea otro monolito para reproducir un nombre histórico.

| Punto | Clases conceptuales conservadas | Pruebas de catálogo base | Documento / ADR | Reto aislado |
|---|---|---:|---|---|
| 8.1 | RutaGateway, ValidadorApiGateway, CatalogoRutas, ResultadoApiGateway | 12 | introduccion-api-gateway.md / ADR-031-introduccion-api-gateway.md | ResumenApiGateway: total 3, servicios 3, autenticación declarada 3. |
| 8.2 | ClusterYarp, ValidadorConfiguracionYarp, CatalogoClusters, ResultadoConfiguracionYarp | 10 | configuracion-basica-yarp.md / ADR-032-configuracion-basica-yarp.md | ResumenConfiguracionYarp: clusters 3, destinos 3, configuración por entorno declarada 3. |
| 8.3 | ReglaEnrutamiento, ValidadorEnrutamiento, CatalogoReglasEnrutamiento, ResultadoEnrutamiento | 10 | enrutamiento-peticiones.md / ADR-033-enrutamiento-peticiones.md | ResumenEnrutamiento: total 4, ruta 4, cabecera 4, consulta 2. |
| 8.4 | ClusterBalanceo, ValidadorBalanceo, CatalogoClustersBalanceo, ResultadoBalanceo | 10 | balanceo-carga.md / ADR-034-balanceo-carga.md | ResumenBalanceo: clusters 3, destinos 7, pesos declarados 1, health checks declarados 3. |

Los cuatro retos mantienen sus records, cálculos y comprobaciones. Se ejecutan sobre copias aisladas para evitar que un reto anterior cambie los recuentos obligatorios de las etapas siguientes. La lista de comprobaciones de cada validador se conserva, incluidas restricciones didácticas más estrechas que YARP. La práctica debe explicar su alcance local en vez de atribuir esas restricciones a la biblioteca.

## Correcciones técnicas y docentes

| Tema | Afirmación o ejemplo histórico | Corrección y motivo | Cobertura |
|---|---|---|---|
| Pruebas finales | Cierre 8.4: 298; README histórico: 307. | La propia validación histórica corrige 298 a 307 para aquella conversación. En este repositorio la base M07 es 403; M08 aporta 42 casos originales más pruebas funcionales nuevas. El total final debe proceder de la ejecución, sin inventarlo ni sumar retos a etapas obligatorias. | 8.4 bloque 10; manual e informes. |
| Clientes | Catálogo con Ordenes.Api, Inventario.Api y Clientes.Api presentado como tres servicios implantados. | Conservar los tres conceptos; publicar solo servicios existentes de Producción e Inventario. Clientes es ejemplo de análisis. | 8.1/8.2 bloque 10 y catálogos. |
| Indicadores de políticas | AplicaAutenticacion, AplicaRateLimit, TieneDireccionValida, CombinadoConHealthChecks. | Son declaraciones de modelos. No autentican, limitan, validan una URI real ni sondean un destino. Solo atribuir capacidad a componentes y ensayos efectivos. | 8.1 bloques 6–7; 8.2 bloques 3/10; 8.4 bloque 10. |
| Pesos | Weight en el destino como opción nativa de YARP. | DestinationConfig 2.2 no contiene Weight. Se explica ponderación conceptual y Metadata; aplicar pesos exige ILoadBalancingPolicy personalizada. El laboratorio usa RoundRobin sin ponderación. | 8.2 bloque 3; 8.4 bloques 2–5. |
| Consulta desde ruta | QueryParameterFromRoute / RouteValueKey. | Usar QueryRouteParameter con Set/Append cuyo valor es el nombre de la captura. | 8.3 bloque 6. |
| Consulta desde cabecera | QueryParameterFromHeader / HeaderName como transform incorporado. | No presentarlo como clave válida. QueryValueParameter fija canal=gateway; copiar una cabecera requiere código específico y revisión de datos. | 8.3 bloque 6. |
| Correlación | RequestHeader X-Correlation-Id con Set=generated. | Es un literal, no un generador. Validar/generar en middleware y propagar el valor efectivo. X-Canal=Gateway sí es un literal intencionado. | 8.1 bloque 8; 8.2 bloque 7; 8.3 bloque 5. |
| DNS | Nombres acería-... acentuados en ejemplos de contenedores. | Emplear nombres ASCII aceria-... y distinguir red interna de puertos locales. | 8.2 bloques 3/6/8; 8.4 bloques 3–5/7. |
| Selección de rutas | Primera coincidencia según posición en JSON. | Explicar endpoint routing, Order, especificidad y condiciones de Match. Resolver ambigüedad por contrato, no por posición textual. | 8.3 bloques 1–3. |
| Order | Rechazar negativos como si fuera requisito YARP. | El validador conceptual exige no negativos; YARP admite enteros negativos. | 8.3 bloques 3/9. |
| Transformación obligatoria | Al menos un indicador true por regla. | Mantener la política didáctica del catálogo y explicar que YARP puede reenviar sin transformar. | 8.3 bloque 9. |
| Orden de transformaciones | Siempre ruta, después cabeceras, después consulta. | Se respeta la lista configurada, sin reordenación universal por tipo. | 8.3 bloque 7. |
| Eliminación de cabecera | Remove como operación genérica de RequestHeader. | Set/Append y claves específicas RequestHeaderRemove / ResponseHeaderRemove. | 8.3 bloque 5. |
| Prefijos | Quitar /api/v1 aunque el backend lo espera. | El alias elimina /inventario y conserva /api/v1; limitarlo a materiales y planificaciones, sin publicar endpoints internos. | 8.2 bloque 7; 8.3 bloques 4/10. |
| Balanceadores | Solo capa de transporte. | Distinguir balanceadores L4 y L7; YARP combina encaminamiento HTTP y reparto entre destinos. | 8.1 bloque 4. |
| Salud total | Suponer que ninguna instancia sana siempre implica retirada de todas con valores predeterminados. | Fijar HealthyAndUnknown. HealthyOrPanic puede habilitar todos al no quedar elegibles. Diferenciar ventana de detección, fallo total y recuperación. | 8.4 bloque 6 y configuración final. |
| Red | Ocultar topología equivale a bloquear acceso directo. | La publicación de un contrato no reemplaza restricciones de red ni autorización del backend. | 8.1 bloques 1/7/9. |
| Estado | Gateway sin estado como ausencia de cualquier estado técnico. | Evitar estado de negocio o sesión exclusivo; conexiones, configuración y salud son estado operativo legítimo. | 8.1 bloque 3. |
| Evidencia | Catálogo correcto equivale a proxy ejecutado. | Separar catálogo, Kestrel real controlado y servicios con SQL/AMQP reales. No presentar pruebas omitidas ni respuestas sintéticas como integración acreditada. | Introducción y ampliaciones de los cuatro puntos. |

## Referencias primarias comprobadas

Se consultó documentación oficial de Microsoft para verificar contratos de YARP. Los enlaces de Learn pueden abrir su edición actual; el proyecto conserva net8.0 y Yarp.ReverseProxy 2.2.0.

- [Configuración YARP](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/yarp/config-files).
- [Transformaciones de petición](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/yarp/transforms-request).
- [Transformaciones y extensibilidad](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/yarp/transforms).
- [Balanceo incorporado y personalizado](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/yarp/load-balancing).
- [Propiedades DestinationConfig de YARP 2.2](https://learn.microsoft.com/en-us/dotnet/api/yarp.reverseproxy.configuration.destinationconfig?view=yarp-2.2).
- [Salud y destinos disponibles](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/yarp/dests-health-checks).
- [Cabeceras y precedencia](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/yarp/header-routing).

## Criterios editoriales y estado de evidencia

Se separan teoría y prácticas, sin eliminar contenido conceptual ni retos. Se excluyen duraciones, metaconversación, razonamiento interno de la exportación y el bloque global «Errores comunes del ejercicio completo». Se conservan las instrucciones y los diagnósticos útiles por paso. Las explicaciones de ejemplos son listas con cita exacta de su línea física, sin agrupar varias líneas bajo una sola viñeta.

El generador `.github/scripts/m08_crear_figuras.py` produce doce SVG y doce PNG. La revisión visual de las figuras comprueba topología, dirección de flechas, corredores libres y texto dentro de tarjetas. La generación de PDF y su revisión de páginas se realizan por separado, sobre el Markdown final; no se declara cobertura visual de un PDF a partir de sus figuras aisladas.

La evidencia editorial disponible acredita 40 bloques, 40 ampliaciones, 40 ejemplos, 280 líneas explicadas y 12 figuras con interpretación. Los informes de reconstrucción, pruebas, integración Linux, Windows/LocalDB y PDF deben completar el cierre verificable. Las cifras funcionales y el hash final de cada entrega se toman de esos informes; esta matriz evita convertir requisitos pendientes en resultados observados.


## Revisión de coherencia de ejemplos previa al PDF

Se ajustaron también los ejemplos y sus citas físicas para que no contradigan las matizaciones de la prosa: estado de negocio/sesión exclusivo en 8.1.3; contadores como capacidad posible y no acreditada en 8.1.8; precedencia con el mismo Order en 8.3.3 y 8.3.9; Order y especificidad en 8.3.10; dos destinos de Inventario y uno de Producción en 8.4.10; exclusión de unhealthy bajo HealthyAndUnknown en 8.4.6. El pequeño ejemplo de transformaciones 8.2.7 sigue el orden de la explicación: prefijo y después cabecera. El ejemplo de seguridad aclara que limitar tasa contribuye a mitigar abuso, sin equivaler a protección general contra ataques.

En el pase final también se alinearon las descripciones de las viñetas modificadas y las frases de prosa y resumen sobre selección de rutas, para evitar que una explicación anterior mantuviese una prioridad absoluta ya corregida en el ejemplo. El cierre especifica los destinos efectivos por servicio y la continuidad ante fallo se condiciona a detección, capacidad y dependencias disponibles.
