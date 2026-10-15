Punto 2.2 — Recursos, verbos HTTP y códigos de respuesta

Módulo 2: Desarrollo de APIs REST con ASP.NET Core
Duración: 53 minutos (26 minutos de teoría + 27 minutos de práctica)
Objetivos de aprendizaje:

· Comprender el concepto de recurso y su representación en una API REST.
· Aplicar los verbos HTTP con su semántica correcta.
· Seleccionar el código de respuesta adecuado a cada situación.
· Comprender la relación entre verbo, código de respuesta y estado del recurso.
· Añadir al proyecto AceriaApp una clase de validación de combinaciones verbo-código y un catálogo de recursos del dominio.


---

PARTE TEÓRICA (26 minutos)

Bloque 1 — El recurso como unidad de diseño

Un recurso es una entidad identificable que puede ser referenciada y manipulada a través de una API. No es lo mismo que una entidad de base de datos ni que una clase del dominio. Un recurso es una abstracción que agrupa los datos y las operaciones que el cliente puede realizar sobre ellos. Un recurso puede corresponder a una fila de una tabla, a una vista que combina varias tablas o a un agregado de negocio. La decisión de qué constituye un recurso se toma desde la perspectiva del cliente, no desde la perspectiva del modelo de datos. Un recurso bien definido expone solo los datos que el cliente necesita y solo las operaciones que el cliente puede realizar.

Recursos del dominio de la acería:  
  
Orden         → orden de producción.  
LineaOrden    → línea de una orden.  
Material      → materia prima.  
Cliente       → empresa compradora.  
Movimiento    → movimiento de inventario.

Línea 1: Orden → recurso que representa una orden de producción.
Línea 2: LineaOrden → recurso que representa una línea de una orden.
Línea 3: Material → recurso que representa una materia prima.
Línea 4: Cliente → recurso que representa una empresa compradora.
Línea 5: Movimiento → recurso que representa un movimiento de inventario.

Cada recurso tiene una representación por defecto y puede tener representaciones alternativas. La representación por defecto es la que el servidor devuelve cuando el cliente no especifica ninguna preferencia. La representación alternativa se negocia con la cabecera Accept. El recurso también tiene un estado interno que el servidor gestiona, pero que no se expone directamente al cliente. El cliente solo ve la representación, no el estado. Esta separación entre recurso y representación es una de las propiedades más importantes del estilo REST y la que permite que el mismo recurso se consuma desde clientes con formatos distintos.

La identificación de recursos del dominio de la acería sigue un criterio de negocio, no de base de datos. La tabla Ordenes de la base de datos puede contener columnas internas que no forman parte del recurso Orden. La columna IdempotencyKey, por ejemplo, es un detalle de implementación que no se expone como parte del recurso. Del mismo modo, el recurso Orden puede combinar datos de varias tablas para formar una representación coherente desde la perspectiva del cliente. El recurso es una proyección diseñada para el consumo, no un reflejo de la estructura de persistencia.


---

Bloque 2 — Representaciones del recurso

Una representación es la forma concreta en la que un recurso se transmite entre cliente y servidor. La representación por defecto en las APIs REST modernas es JSON. JSON es un formato de texto ligero, legible y ampliamente soportado. Otras representaciones posibles son XML, YAML, CSV o binario. La representación se selecciona mediante negociación de contenido. El cliente envía la cabecera Accept con los formatos que acepta, y el servidor responde con el formato que puede generar. Si el servidor no puede generar ninguno de los formatos solicitados, responde con el código 406 Not Acceptable.

public record OrdenRepresentacion(  
    Guid Id,  
    string Cliente,  
    string Material,  
    int Cantidad,  
    DateTime FechaCreacion);

Línea 1: public record OrdenRepresentacion( → declara la representación de una orden.
Línea 2: Guid Id, → identificador de la orden.
Línea 3: string Cliente, → nombre del cliente.
Línea 4: string Material, → material solicitado.
Línea 5: int Cantidad, → cantidad solicitada.
Línea 6: DateTime FechaCreacion); → fecha de creación.

La representación no contiene toda la información del recurso: contiene solo la información que el cliente necesita. Si el recurso Orden tiene veinte propiedades internas, la representación puede exponer solo cinco. La selección de qué propiedades se exponen se realiza en función de los casos de uso del cliente. Una representación de colección puede exponer menos propiedades que una representación de detalle. La distinción entre representación de colección y representación de detalle es una práctica habitual para reducir el tamaño de las respuestas y mejorar el rendimiento.


---

Bloque 3 — Verbos HTTP y su semántica completa

Los verbos HTTP tienen una semántica definida por el estándar y por las convenciones del ecosistema REST. El verbo GET recupera una representación del recurso. El verbo POST crea un recurso nuevo. El verbo PUT reemplaza un recurso existente. El verbo PATCH modifica parcialmente un recurso existente. El verbo DELETE elimina un recurso existente. Cada verbo tiene tres propiedades: seguridad, idempotencia y cacheabilidad. La seguridad indica si el verbo modifica el estado del servidor. La idempotencia indica si ejecutar el verbo varias veces produce el mismo resultado que ejecutarlo una vez. La cacheabilidad indica si la respuesta puede almacenarse en caché.

Propiedades de los verbos:  
  
Verbo   | Seguro | Idempotente | Cacheable  
--------|--------|-------------|----------  
GET     | Sí     | Sí          | Sí  
POST    | No     | No          | No  
PUT     | No     | Sí          | No  
PATCH   | No     | No          | No  
DELETE  | No     | Sí          | No

Línea 1: GET → seguro, idempotente, cacheable.
Línea 2: POST → no seguro, no idempotente, no cacheable.
Línea 3: PUT → no seguro, idempotente, no cacheable.
Línea 4: PATCH → no seguro, no idempotente, no cacheable.
Línea 5: DELETE → no seguro, idempotente, no cacheable.

La elección del verbo correcto no es una cuestión de preferencia: es una cuestión de semántica. Si se usa POST para reemplazar un recurso, se pierde la idempotencia y los reintentos pueden duplicar la operación. Si se usa GET para crear un recurso, se pierde la seguridad y los rastreadores pueden crear recursos sin querer. La semántica correcta de los verbos es la base de la comunicación fiable entre cliente y servidor. Un endpoint que usa el verbo incorrecto es un endpoint que falla en producción de formas difíciles de diagnosticar.


---

Bloque 4 — Verbos en colecciones y en recursos concretos

La combinación de verbo y URI define la operación. Los verbos se aplican de forma distinta a colecciones y a recursos concretos. Sobre una colección, GET devuelve la lista, POST crea un elemento nuevo y DELETE elimina la colección completa. Sobre un recurso concreto, GET devuelve el recurso, PUT lo reemplaza, PATCH lo modifica parcialmente y DELETE lo elimina. La combinación de verbo y URI produce operaciones con semántica clara y predecible. La previsibilidad permite que el cliente sepa qué esperar sin consultar la documentación.

Combinaciones verbo-URI:  
  
GET    /api/v1/ordenes          → lista de órdenes.  
POST   /api/v1/ordenes          → crear orden.  
GET    /api/v1/ordenes/{id}     → orden concreta.  
PUT    /api/v1/ordenes/{id}     → reemplazar orden.  
PATCH  /api/v1/ordenes/{id}     → modificar orden.  
DELETE /api/v1/ordenes/{id}     → eliminar orden.

Línea 1: GET /api/v1/ordenes → recupera la colección.
Línea 2: POST /api/v1/ordenes → crea un elemento nuevo.
Línea 3: GET /api/v1/ordenes/{id} → recupera un recurso concreto.
Línea 4: PUT /api/v1/ordenes/{id} → reemplaza el recurso concreto.
Línea 5: PATCH /api/v1/ordenes/{id} → modifica parcialmente el recurso.
Línea 6: DELETE /api/v1/ordenes/{id} → elimina el recurso concreto.

La combinación de verbo y URI también determina el código de respuesta adecuado. GET sobre una colección devuelve 200 con la lista. POST sobre una colección devuelve 201 con la cabecera Location y el recurso creado. GET sobre un recurso concreto devuelve 200 o 404. PUT y PATCH devuelven 200 con el recurso actualizado o 204 sin cuerpo. DELETE devuelve 204 o 404. La relación entre verbo, URI y código de respuesta es sistemática y predecible.


---

Bloque 5 — Códigos de respuesta y su relación con el verbo

Los códigos de respuesta expresan el resultado de la operación. La relación entre verbo y código de respuesta es sistemática. GET devuelve 200 si encuentra el recurso y 404 si no lo encuentra. POST devuelve 201 si crea el recurso y 400 si la petición es inválida. PUT devuelve 200 o 204 si reemplaza el recurso y 404 si no existe. PATCH devuelve 200 o 204 si modifica el recurso y 404 si no existe. DELETE devuelve 204 si elimina el recurso y 404 si no existe. La sistematicidad de la relación permite al cliente anticipar el código de respuesta.

Relación verbo-código:  
  
GET    /ordenes          → 200 OK  
POST   /ordenes          → 201 Created  
GET    /ordenes/{id}     → 200 OK | 404 Not Found  
PUT    /ordenes/{id}     → 200 OK | 204 No Content | 404 Not Found  
PATCH  /ordenes/{id}     → 200 OK | 204 No Content | 404 Not Found  
DELETE /ordenes/{id}     → 204 No Content | 404 Not Found

Línea 1: GET /ordenes → 200 OK → recuperación exitosa de la colección.
Línea 2: POST /ordenes → 201 Created → creación exitosa del recurso.
Línea 3: GET /ordenes/{id} → 200 OK | 404 → recuperación exitosa o recurso no encontrado.
Línea 4: PUT /ordenes/{id} → 200 | 204 | 404 → reemplazo exitoso o recurso no encontrado.
Línea 5: PATCH /ordenes/{id} → 200 | 204 | 404 → modificación exitosa o recurso no encontrado.
Línea 6: DELETE /ordenes/{id} → 204 | 404 → eliminación exitosa o recurso no encontrado.

La elección entre 200 y 204 depende de si la respuesta incluye un cuerpo. 200 indica éxito con cuerpo. 204 indica éxito sin cuerpo. En un PUT o PATCH, si el servidor devuelve el recurso actualizado, usa 200. Si no devuelve nada, usa 204. En un DELETE, el servidor usa 204 porque el recurso ya no existe y no hay cuerpo que devolver. La elección entre 200 y 204 es una decisión de diseño que se documenta y se mantiene consistente en toda la API.


---

Bloque 6 — Códigos de error del cliente

Los códigos de error del cliente se agrupan en la familia 4xx. Los más usados son 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 405 Method Not Allowed, 409 Conflict y 422 Unprocessable Entity. El código 400 indica que la petición está mal formada o tiene un error de sintaxis. El código 401 indica que falta autenticación. El código 403 indica que la autenticación es correcta pero el cliente no tiene permisos. El código 404 indica que el recurso no existe. El código 405 indica que el verbo no está permitido sobre el recurso. El código 409 indica un conflicto de estado. El código 422 indica que la entidad es sintácticamente correcta pero semánticamente inválida.

Códigos de error del cliente:  
  
400 Bad Request           → petición mal formada.  
401 Unauthorized          → falta autenticación.  
403 Forbidden             → sin permisos.  
404 Not Found             → recurso no encontrado.  
405 Method Not Allowed    → verbo no permitido.  
409 Conflict              → conflicto de estado.  
422 Unprocessable Entity  → entidad semánticamente inválida.

Línea 1: 400 Bad Request → petición mal formada.
Línea 2: 401 Unauthorized → falta autenticación.
Línea 3: 403 Forbidden → autenticación correcta, sin permisos.
Línea 4: 404 Not Found → recurso no encontrado.
Línea 5: 405 Method Not Allowed → verbo no permitido.
Línea 6: 409 Conflict → conflicto de estado.
Línea 7: 422 Unprocessable Entity → entidad semánticamente inválida.

La distinción entre 400 y 422 es una de las más sutiles. El código 400 se usa cuando la petición no se puede procesar por un error de formato o de sintaxis. El código 422 se usa cuando la petición se puede procesar pero la entidad no cumple las reglas de negocio. Un JSON mal formado produce 400. Un JSON bien formado con un campo Cantidad negativo produce 422. La distinción permite al cliente distinguir entre un error de programación y un error de datos. La distinción también permite a las herramientas de monitorización separar los errores de infraestructura de los errores de negocio.


---

Bloque 7 — Códigos de error del servidor

Los códigos de error del servidor se agrupan en la familia 5xx. Los más usados son 500 Internal Server Error, 501 Not Implemented, 502 Bad Gateway, 503 Service Unavailable y 504 Gateway Timeout. El código 500 indica un error no controlado del servidor. El código 501 indica que el servidor no implementa la funcionalidad solicitada. El código 502 indica que un servidor intermedio recibió una respuesta inválida del servidor destino. El código 503 indica que el servicio no está disponible temporalmente. El código 504 indica que un servidor intermedio no recibió respuesta del servidor destino a tiempo.

Códigos de error del servidor:  
  
500 Internal Server Error  → error no controlado.  
501 Not Implemented        → funcionalidad no implementada.  
502 Bad Gateway            → respuesta inválida del servidor destino.  
503 Service Unavailable    → servicio no disponible.  
504 Gateway Timeout        → timeout en servidor intermedio.

Línea 1: 500 Internal Server Error → error no controlado.
Línea 2: 501 Not Implemented → funcionalidad no implementada.
Línea 3: 502 Bad Gateway → respuesta inválida del servidor destino.
Línea 4: 503 Service Unavailable → servicio no disponible.
Línea 5: 504 Gateway Timeout → timeout en servidor intermedio.

La elección del código 5xx adecuado es importante para la monitorización y para la comunicación con el cliente. Un 500 indica un error del servidor que requiere investigación. Un 503 indica que el servicio no está disponible temporalmente y que el cliente puede reintentar más tarde. Un 504 indica que un servidor intermedio no recibió respuesta a tiempo. La distinción permite a los sistemas de monitorización clasificar los errores y generar alertas específicas para cada tipo. La práctica de devolver siempre 500 para cualquier error del servidor oculta información valiosa.


---

Bloque 8 — Problem details como formato de error

El formato problem details está definido en la RFC 7807 y describe la estructura de un error en una API REST. Los campos principales son type, title, status, detail e instance. El campo type identifica el tipo de error con una URI. El campo title es un resumen legible del error. El campo status es el código HTTP. El campo detail explica el error concreto. El campo instance identifica la instancia concreta del error. El formato se usa en todas las respuestas de error para que el cliente pueda procesarlas de forma uniforme.

{  
  "type": "https://acería.local/errores/validacion",  
  "title": "Error de validación",  
  "status": 400,  
  "detail": "El campo Cantidad debe ser mayor que cero.",  
  "instance": "/api/v1/ordenes"  
}

Línea 1: { → abre el objeto de error.
Línea 2: "type": "https://acería.local/errores/validacion", → identifica el tipo de error.
Línea 3: "title": "Error de validación", → resumen legible del error.
Línea 4: "status": 400, → código HTTP del error.
Línea 5: "detail": "El campo Cantidad debe ser mayor que cero.", → detalle del error.
Línea 6: "instance": "/api/v1/ordenes" → instancia concreta del error.
Línea 7: } → cierra el objeto de error.

El formato problem details se implementa en ASP.NET Core con la clase Results.Problem. La clase acepta los campos title, detail, statusCode y otros opcionales. La implementación por defecto usa el tipo about:blank cuando no se especifica. La adopción del formato evita la duplicación de estructuras de error y facilita la integración con herramientas de monitorización. El formato se usa en todos los endpoints que devuelven errores.


---

Bloque 9 — Catálogo de recursos y combinaciones válidas

Un catálogo de recursos es una lista estructurada de los recursos que expone la API, con sus URIs, sus verbos permitidos y sus códigos de respuesta esperados. El catálogo sirve como contrato de referencia para el equipo y como base para la documentación automática. La estructura del catálogo incluye el nombre del recurso, la URI base, los verbos permitidos y los códigos de respuesta esperados para cada verbo. La validación automática del catálogo comprueba que las combinaciones de verbo y código son coherentes. La coherencia del catálogo es la base de la previsibilidad de la API.

Catálogo de recursos:  
  
Recurso      | URI base                  | Verbos permitidos  
-------------|---------------------------|------------------  
Orden        | /api/v1/ordenes           | GET, POST  
Orden        | /api/v1/ordenes/{id}      | GET, PUT, PATCH, DELETE  
LineaOrden   | /api/v1/ordenes/{id}/lineas | GET, POST  
Material     | /api/v1/materiales        | GET, POST

Línea 1: Recurso | URI base | Verbos permitidos → cabecera de la tabla.
Línea 2: Orden | /api/v1/ordenes | GET, POST → colección de órdenes.
Línea 3: Orden | /api/v1/ordenes/{id} | GET, PUT, PATCH, DELETE → orden concreta.
Línea 4: LineaOrden | /api/v1/ordenes/{id}/lineas | GET, POST → colección de líneas.
Línea 5: Material | /api/v1/materiales | GET, POST → colección de materiales.

La validación automática del catálogo comprueba tres cosas: que los verbos permitidos sean coherentes con la URI, que los códigos de respuesta sean coherentes con los verbos y que las URIs sigan las reglas de diseño. La comprobación se realiza con una clase de validación que recorre el catálogo y devuelve la lista de incoherencias. La validación automática evita que un endpoint con un verbo incorrecto o un código de respuesta inadecuado llegue a producción. La validación se ejecuta en los tests y en el pipeline de compilación.


---

Bloque 10 — Aplicación al proyecto del curso

El proyecto del curso aplica los conceptos de recursos, verbos y códigos de respuesta en cada endpoint. Los recursos se identifican con URIs que siguen las cinco reglas del punto 2.1. Los verbos se eligen según su semántica. Los códigos de respuesta se eligen según la relación sistemática entre verbo y resultado. El formato problem details se usa en todos los errores. El catálogo de recursos se documenta y se valida automáticamente. La aplicación conjunta produce una API predecible y coherente.

Aplicación al proyecto del curso:  
  
Recursos identificados   → Orden, LineaOrden, Material, Cliente.  
Verbos por recurso       → GET, POST, PUT, PATCH, DELETE.  
Códigos por verbo        → 200, 201, 204, 400, 404, 409, 422, 500.  
Formato de error         → problem details.  
Catálogo documentado     → docs/catalogo-recursos.md.  
Validación automática    → clase ValidadorCatalogoRecursos.

Línea 1: Recursos identificados → lista de recursos del dominio.
Línea 2: Verbos por recurso → combinaciones verbo-URI.
Línea 3: Códigos por verbo → relación sistemática verbo-código.
Línea 4: Formato de error → problem details.
Línea 5: Catálogo documentado → documento de catálogo.
Línea 6: Validación automática → clase de validación.

La aplicación de estos conceptos prepara el proyecto para el punto 2.3, donde se estudiará la validación de peticiones con FluentValidation. La validación de peticiones se apoya en los recursos y en los códigos de respuesta definidos en el punto 2.2. El punto 2.3 usará los recursos del catálogo para validar las peticiones de creación y de modificación. El punto 2.2 establece la base que se aplicará en los dos puntos siguientes del módulo 2.


---

Resumen rápido de la teoría

· Un recurso es una entidad identificable que agrupa datos y operaciones desde la perspectiva del cliente.
· Las representaciones transmiten los recursos y se negocian con la cabecera Accept.
· Los verbos HTTP tienen tres propiedades: seguridad, idempotencia y cacheabilidad.
· La combinación de verbo y URI define la operación con semántica clara.
· La relación entre verbo y código de respuesta es sistemática y predecible.
· Los códigos 4xx indican errores del cliente y los 5xx errores del servidor.
· El formato problem details estructura las respuestas de error de forma uniforme.
· El catálogo de recursos documenta y valida las combinaciones de verbo y código.


---

PARTE PRÁCTICA (27 minutos)

Ejercicio: Añadir al punto 2.1 un documento de catálogo de recursos en docs/, una clase de validación de combinaciones verbo-código en el proyecto monolítico y un test unitario que verifique la validación. El punto 2.2 parte del contenido del punto 2.1 sin modificar ningún archivo existente: solo añade archivos nuevos.

Ubicación de trabajo: C:\cursos\AceriaApp\modulo-2-apis-rest-aspnet-core\


---

Paso 1 — Crear la carpeta del punto 2.2 a partir del punto 2.1

Acción 1: Abrir la terminal integrada de Visual Studio 2026 con Ctrl+ñ (o Ctrl+``  en teclados no españoles).
Acción 2: Escribir cd C:\cursos\AceriaApp\modulo-2-apis-rest-aspnet-core y pulsar Enter.
Acción 3: Escribir mkdir 2.2-recursos-verbos-codigos y pulsar Enter.
Acción 4: Escribir xcopy 2.1-diseno-apis-rest 2.2-recursos-verbos-codigos /E /I /H /Y y pulsar Enter.
Acción 5: Escribir dir 2.2-recursos-verbos-codigos y pulsar Enter para verificar que se ha copiado el contenido.

Por qué se hace: cada punto del curso parte del contenido del punto anterior. El punto 2.2 se construye sobre el punto 2.1 copiando su contenido y añadiendo archivos nuevos sin modificar los existentes.

Errores comunes:

· Usar copy en lugar de xcopy: copy no copia carpetas de forma recursiva.
· Olvidar el flag /E: no se copian las subcarpetas vacías.
· Olvidar el flag /I: xcopy pregunta si el destino es un directorio cuando no existe.
· Olvidar el flag /Y: xcopy pide confirmación para sobrescribir.

Verificación: al ejecutar dir 2.2-recursos-verbos-codigos, deben aparecer AceriaApp.sln, README.md, src, tests y docs.


---

Paso 2 — Abrir la solución copiada en Visual Studio 2026

Acción 1: Escribir cd 2.2-recursos-verbos-codigos y pulsar Enter.
Acción 2: Escribir start AceriaApp.sln y pulsar Enter.
Acción 3: Verificar que Visual Studio 2026 abre la solución y muestra los proyectos heredados del punto 2.1: AceriaApp.Monolito.Api, AceriaApp.Monolito.Tests, AceriaApp.Metricas.Tests, AceriaApp.Diseno.Tests, AceriaApp.Organizacion.Tests, AceriaApp.BuenasPracticas.Tests y AceriaApp.DisenoRest.Tests.
Acción 4: Verificar que la solución compila con Ctrl+Shift+B y que la salida muestra Build succeeded..

Por qué se hace: abrir la solución copiada permite trabajar en el punto 2.2 sobre la base del punto 2.1. La compilación verifica que la copia es correcta.

Errores comunes:

· Abrir la solución del punto 2.1 en lugar de la del punto 2.2: los cambios se aplican al punto equivocado.
· No compilar antes de empezar: si la copia tiene errores, los cambios posteriores fallan.
· Tener la API del punto 2.1 en ejecución: el puerto queda ocupado y la compilación falla.

Verificación: Visual Studio 2026 muestra la solución AceriaApp con los siete proyectos heredados del punto 2.1 y la compilación es correcta.


---

Paso 3 — Verificar que la carpeta docs contiene los documentos del punto 2.1

Acción 1: En el panel Solution Explorer, expandir la carpeta docs del punto 2.2.
Acción 2: Verificar que contiene ADR-001 a ADR-006, analisis-ventajas-inconvenientes.md, principios-diseno.md, organizacion-solucion.md, buenas-practicas.md y diseno-apis-rest.md.
Acción 3: Verificar que ninguno de los diez documentos se ha modificado.
Acción 4: Verificar que la carpeta docs no contiene ningún archivo nuevo del punto 2.2 todavía.

Por qué se hace: el punto 2.2 parte del contenido del punto 2.1, que ya incluye la carpeta docs con diez documentos. No se modifica ningún documento existente.

Errores comunes:

· Modificar alguno de los ADR o documentos existentes: viola la regla de no modificar archivos del punto anterior.
· Eliminar algún documento existente: pierde la trazabilidad del punto 2.1.
· Crear la carpeta docs si ya existe: mkdir falla.

Verificación: la carpeta docs contiene los diez documentos del punto 2.1 sin modificaciones.


---

Paso 4 — Crear el documento de catálogo de recursos en docs

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta docs.
Acción 2: Seleccionar Add → New Item → Text File y nombrar el archivo catalogo-recursos.md.
Acción 3: Escribir exactamente el siguiente contenido:

# Catálogo de recursos — Punto 2.2  
  
## Recursos del dominio  
  
- Orden.  
- LineaOrden.  
- Material.  
- Cliente.  
- Movimiento.  
  
## Catálogo de combinaciones verbo-URI  
  
| Recurso | URI base | Verbos permitidos |  
|---------|----------|-------------------|  
| Orden | /api/v1/ordenes | GET, POST |  
| Orden | /api/v1/ordenes/{id} | GET, PUT, PATCH, DELETE |  
| LineaOrden | /api/v1/ordenes/{id}/lineas | GET, POST |  
| LineaOrden | /api/v1/ordenes/{id}/lineas/{lid} | GET, PUT, DELETE |  
| Material | /api/v1/materiales | GET, POST |  
| Material | /api/v1/materiales/{id} | GET, PUT, PATCH, DELETE |  
| Cliente | /api/v1/clientes | GET, POST |  
| Cliente | /api/v1/clientes/{id} | GET, PUT, DELETE |  
  
## Códigos de respuesta por verbo  
  
| Verbo | Códigos esperados |  
|-------|-------------------|  
| GET | 200, 404 |  
| POST | 201, 400, 409, 422 |  
| PUT | 200, 204, 400, 404, 409, 422 |  
| PATCH | 200, 204, 400, 404, 409, 422 |  
| DELETE | 204, 404 |  
  
## Formato de error  
  
Problem details según RFC 7807.  
  
## Aplicación al proyecto del curso  
  
| Elemento | Aplicación |  
|----------|------------|  
| Recursos | Orden, LineaOrden, Material, Cliente, Movimiento |  
| Verbos | GET, POST, PUT, PATCH, DELETE |  
| Códigos | 200, 201, 204, 400, 404, 409, 422, 500 |  
| Formato de error | Problem details |

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que el archivo aparece en la carpeta docs sin subrayados rojos.

Por qué se hace: el documento de catálogo de recursos es el artefacto de docs específico del punto 2.2. No modifica los diez documentos existentes del punto 2.1.

Errores comunes:

· Nombrar el archivo con otro nombre: rompe la trazabilidad del punto.
· Modificar los ADR existentes: viola la regla de no modificar archivos del punto anterior.
· Guardar el archivo en la raíz del punto en lugar de docs: rompe la estructura del repositorio.

Verificación: el archivo docs\catalogo-recursos.md existe con las seis secciones.


---

Paso 5 — Crear la carpeta CatalogoRecursos en el proyecto monolítico

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre el proyecto AceriaApp.Monolito.Api.
Acción 2: Seleccionar Add → New Folder y nombrar la carpeta CatalogoRecursos.
Acción 3: Verificar que la carpeta CatalogoRecursos aparece dentro de AceriaApp.Monolito.Api sin afectar a las carpetas Dominio, Infraestructura, Metricas, Diseno, Organizacion, BuenasPracticas y DisenoRest.
Acción 4: Verificar que no se ha modificado ningún archivo existente del punto 2.1.

Por qué se hace: la carpeta CatalogoRecursos albergará las clases de catálogo y validación de combinaciones verbo-código. Se crea como carpeta nueva sin tocar las carpetas existentes.

Errores comunes:

· Crear la carpeta dentro de alguna de las carpetas existentes: rompe la separación de responsabilidades.
· Modificar las carpetas existentes: viola la regla de no modificar archivos del punto anterior.
· Crear la carpeta con otro nombre: rompe la convención del curso.

Verificación: la carpeta CatalogoRecursos existe dentro de AceriaApp.Monolito.Api y las carpetas existentes permanecen intactas.


---

Paso 6 — Crear la clase CombinacionVerboCodigo

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta CatalogoRecursos.
Acción 2: Seleccionar Add → Class y nombrar la clase CombinacionVerboCodigo.cs.
Acción 3: Escribir exactamente el siguiente código:

namespace AceriaApp.Monolito.Api.CatalogoRecursos;  
  
public class CombinacionVerboCodigo  
{  
    public string Verbo { get; init; } = string.Empty;  
    public int Codigo { get; init; }  
}

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: la clase CombinacionVerboCodigo modela la pareja de verbo y código de respuesta que el validador comprobará. Es la unidad mínima de validación.

Errores comunes:

· Olvidar el namespace: la clase no se resuelve desde otros archivos.
· No inicializar Verbo con string.Empty: el compilador emite advertencia de nulabilidad.
· Usar set en lugar de init: permite modificar la instancia después de crearla.

Verificación: la clase CombinacionVerboCodigo compila sin errores y expone dos propiedades.


---

Paso 7 — Crear la clase ValidadorCombinacionVerboCodigo

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta CatalogoRecursos.
Acción 2: Seleccionar Add → Class y nombrar la clase ValidadorCombinacionVerboCodigo.cs.
Acción 3: Escribir exactamente el siguiente código:

namespace AceriaApp.Monolito.Api.CatalogoRecursos;  
  
public class ValidadorCombinacionVerboCodigo  
{  
    private static readonly Dictionary<string, int[]> CodigosPorVerbo = new()  
    {  
        { "GET", new[] { 200, 404 } },  
        { "POST", new[] { 201, 400, 409, 422 } },  
        { "PUT", new[] { 200, 204, 400, 404, 409, 422 } },  
        { "PATCH", new[] { 200, 204, 400, 404, 409, 422 } },  
        { "DELETE", new[] { 204, 404 } }  
    };  
  
    public ResultadoCombinacion Validar(CombinacionVerboCodigo combinacion)  
    {  
        var errores = new List<string>();  
  
        if (!CodigosPorVerbo.ContainsKey(combinacion.Verbo))  
        {  
            errores.Add($"Verbo no permitido: '{combinacion.Verbo}'.");  
            return new ResultadoCombinacion(false, errores);  
        }  
  
        if (!CodigosPorVerbo[combinacion.Verbo].Contains(combinacion.Codigo))  
        {  
            errores.Add($"Código '{combinacion.Codigo}' no permitido para el verbo '{combinacion.Verbo}'.");  
        }  
  
        return new ResultadoCombinacion(errores.Count == 0, errores);  
    }  
}  
  
public record ResultadoCombinacion(bool EsValida, IReadOnlyList<string> Errores);

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: la clase ValidadorCombinacionVerboCodigo comprueba que un verbo está permitido y que el código de respuesta es coherente con el verbo. La tabla de códigos por verbo está definida como un diccionario estático.

Errores comunes:

· Olvidar el using System.Collections.Generic;: Dictionary<string, int[]> y List<string> no se resuelven.
· Olvidar el using System.Linq;: Contains no se resuelve.
· No comprobar si el verbo existe antes de acceder al diccionario: lanza KeyNotFoundException.

Verificación: la clase ValidadorCombinacionVerboCodigo compila sin errores y expone un método y un record.


---

Paso 8 — Añadir los using necesarios en ValidadorCombinacionVerboCodigo

Acción 1: En el panel Solution Explorer, hacer doble clic en ValidadorCombinacionVerboCodigo.cs.
Acción 2: Añadir las líneas using System.Collections.Generic; y using System.Linq; al principio del archivo si no están presentes.
Acción 3: Verificar que no hay subrayados rojos en Dictionary, List<string> ni en Contains.
Acción 4: Pulsar Ctrl+S para guardar el archivo.

Por qué se hace: los tipos Dictionary<string, int[]> y List<string> pertenecen a System.Collections.Generic. El método Contains pertenece a System.Linq. En proyectos con ImplicitUsings desactivado, hay que añadir los usings explícitos.

Errores comunes:

· Añadir solo System.Collections.Generic y olvidar System.Linq: Contains no se resuelve.
· Añadir los usings después del namespace: el compilador no los reconoce.
· Olvidar los usings y confiar en ImplicitUsings: el proyecto puede tenerlo desactivado.

Verificación: ValidadorCombinacionVerboCodigo.cs compila sin errores y no muestra subrayados rojos.


---

Paso 9 — Crear la clase CatalogoCombinaciones

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta CatalogoRecursos.
Acción 2: Seleccionar Add → Class y nombrar la clase CatalogoCombinaciones.cs.
Acción 3: Escribir exactamente el siguiente código:

namespace AceriaApp.Monolito.Api.CatalogoRecursos;  
  
public class CatalogoCombinaciones  
{  
    private readonly List<CombinacionVerboCodigo> _combinaciones;  
  
    public CatalogoCombinaciones(List<CombinacionVerboCodigo> combinaciones)  
    {  
        _combinaciones = combinaciones;  
    }  
  
    public IEnumerable<CombinacionVerboCodigo> CombinacionesValidas(ValidadorCombinacionVerboCodigo validador)  
    {  
        return _combinaciones.Where(c => validador.Validar(c).EsValida);  
    }  
  
    public IEnumerable<CombinacionVerboCodigo> CombinacionesInvalidas(ValidadorCombinacionVerboCodigo validador)  
    {  
        return _combinaciones.Where(c => !validador.Validar(c).EsValida);  
    }  
}

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: la clase CatalogoCombinaciones agrupa las combinaciones verbo-código del proyecto y permite filtrarlas por validez.

Errores comunes:

· No inicializar _combinaciones en el constructor: la clase lanza NullReferenceException.
· Olvidar using System.Linq;: Where no se resuelve.
· Devolver List<CombinacionVerboCodigo> en lugar de IEnumerable<CombinacionVerboCodigo>: expone la implementación interna.

Verificación: la clase CatalogoCombinaciones compila sin errores y expone un constructor y dos métodos.


---

Paso 10 — Añadir el using necesario en CatalogoCombinaciones

Acción 1: En el panel Solution Explorer, hacer doble clic en CatalogoCombinaciones.cs.
Acción 2: Añadir la línea using System.Linq; al principio del archivo si no está presente.
Acción 3: Verificar que no hay subrayados rojos en Where.
Acción 4: Pulsar Ctrl+S para guardar el archivo.

Por qué se hace: el método Where pertenece a System.Linq. En proyectos con ImplicitUsings desactivado, hay que añadir el using explícito.

Errores comunes:

· Añadir using System.Collections.Generic; en lugar de System.Linq: no resuelve Where.
· Añadir el using después del namespace: el compilador no lo reconoce.
· Olvidar el using y confiar en ImplicitUsings: el proyecto puede tenerlo desactivado.

Verificación: CatalogoCombinaciones.cs compila sin errores y no muestra subrayados rojos.


---

Paso 11 — Crear el proyecto de tests del punto 2.2

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta tests.
Acción 2: Seleccionar Add → New Project.
Acción 3: Seleccionar la plantilla xUnit Test Project, nombrar el proyecto AceriaApp.CatalogoRecursos.Tests y pulsar Create.
Acción 4: Verificar que el proyecto aparece en la solución y que se ha creado la carpeta tests\AceriaApp.CatalogoRecursos.Tests.

Por qué se hace: el punto 2.2 añade un proyecto de tests específico para las clases de catálogo de recursos. Se crea como proyecto nuevo sin modificar los proyectos de tests existentes.

Errores comunes:

· Crear el proyecto dentro de src en lugar de tests: rompe la estructura.
· Modificar los proyectos de tests del punto 2.1: viola la regla de no modificar archivos del punto anterior.
· Usar dotnet new mstest: el curso usa xUnit.

Verificación: el proyecto AceriaApp.CatalogoRecursos.Tests aparece en la solución y su carpeta existe en tests\AceriaApp.CatalogoRecursos.Tests.


---

Paso 12 — Añadir la referencia del proyecto de tests a la API monolítica

Acción 1: En la terminal, escribir dotnet add tests\AceriaApp.CatalogoRecursos.Tests\AceriaApp.CatalogoRecursos.Tests.csproj reference src\AceriaApp.Monolito.Api\AceriaApp.Monolito.Api.csproj y pulsar Enter.
Acción 2: Verificar que la salida muestra Reference added successfully.
Acción 3: Verificar que el archivo AceriaApp.CatalogoRecursos.Tests.csproj contiene la referencia.

Por qué se hace: la referencia permite que el proyecto de tests acceda a las clases de CatalogoRecursos del proyecto monolítico.

Errores comunes:

· Añadir la referencia en dirección inversa: crea una dependencia circular.
· Olvidar el nombre completo del archivo .csproj: el comando falla.
· Ejecutar el comando desde la carpeta equivocada: la ruta relativa no se resuelve.

Verificación: el archivo AceriaApp.CatalogoRecursos.Tests.csproj contiene un ProjectReference al proyecto monolítico.


---

Paso 13 — Añadir el paquete FluentAssertions al proyecto de tests

Acción 1: Escribir dotnet add tests\AceriaApp.CatalogoRecursos.Tests\AceriaApp.CatalogoRecursos.Tests.csproj package FluentAssertions y pulsar Enter.
Acción 2: Escribir dotnet list tests\AceriaApp.CatalogoRecursos.Tests\AceriaApp.CatalogoRecursos.Tests.csproj package y pulsar Enter.
Acción 3: Verificar que la salida muestra FluentAssertions con su versión.

Por qué se hace: FluentAssertions proporciona la sintaxis de aserción usada en el curso. Se añade al nuevo proyecto de tests sin modificar los proyectos de tests existentes.

Errores comunes:

· Instalar una versión preliminar: el curso usa la última estable.
· Olvidar el paquete: Should() no se resuelve en los tests.
· Añadir el paquete al proyecto equivocado: los tests no compilan.

Verificación: la salida de dotnet list package muestra FluentAssertions con una versión estable.


---

Paso 14 — Crear el archivo ValidadorCombinacionVerboCodigoTests.cs

Acción 1: En el panel Solution Explorer, expandir tests → AceriaApp.CatalogoRecursos.Tests.
Acción 2: Hacer doble clic en UnitTest1.cs y renombrarlo a ValidadorCombinacionVerboCodigoTests.cs.
Acción 3: Escribir exactamente el siguiente código:

using AceriaApp.Monolito.Api.CatalogoRecursos;  
using FluentAssertions;  
using Xunit;  
  
namespace AceriaApp.CatalogoRecursos.Tests;  
  
public class ValidadorCombinacionVerboCodigoTests  
{  
    private readonly ValidadorCombinacionVerboCodigo _validador = new();  
  
    [Fact]  
    public void Validar_GetCon200_DevuelveValida()  
    {  
        var combinacion = new CombinacionVerboCodigo { Verbo = "GET", Codigo = 200 };  
  
        var resultado = _validador.Validar(combinacion);  
  
        resultado.EsValida.Should().BeTrue();  
        resultado.Errores.Should().BeEmpty();  
    }  
  
    [Fact]  
    public void Validar_PostCon201_DevuelveValida()  
    {  
        var combinacion = new CombinacionVerboCodigo { Verbo = "POST", Codigo = 201 };  
  
        var resultado = _validador.Validar(combinacion);  
  
        resultado.EsValida.Should().BeTrue();  
    }  
  
    [Fact]  
    public void Validar_GetCon201_DevuelveError()  
    {  
        var combinacion = new CombinacionVerboCodigo { Verbo = "GET", Codigo = 201 };  
  
        var resultado = _validador.Validar(combinacion);  
  
        resultado.EsValida.Should().BeFalse();  
        resultado.Errores.Should().Contain(e => e.Contains("no permitido"));  
    }  
  
    [Fact]  
    public void Validar_VerboDesconocido_DevuelveError()  
    {  
        var combinacion = new CombinacionVerboCodigo { Verbo = "OPTIONS", Codigo = 200 };  
  
        var resultado = _validador.Validar(combinacion);  
  
        resultado.EsValida.Should().BeFalse();  
        resultado.Errores.Should().Contain(e => e.Contains("Verbo no permitido"));  
    }  
}

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: los tests verifican que el validador acepta combinaciones correctas y rechaza combinaciones con código no permitido para el verbo y con verbo desconocido.

Errores comunes:

· Olvidar el using AceriaApp.Monolito.Api.CatalogoRecursos;: las clases no se resuelven.
· Usar Assert.True en lugar de Should().BeTrue(): el curso usa FluentAssertions.
· No cubrir el caso de verbo desconocido: el test no verifica el mensaje de error.

Verificación: el archivo ValidadorCombinacionVerboCodigoTests.cs compila y contiene cuatro métodos de test.


---

Paso 15 — Crear el archivo CatalogoCombinacionesTests.cs

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre el proyecto AceriaApp.CatalogoRecursos.Tests.
Acción 2: Seleccionar Add → Class y nombrar la clase CatalogoCombinacionesTests.cs.
Acción 3: Escribir exactamente el siguiente código:

using AceriaApp.Monolito.Api.CatalogoRecursos;  
using FluentAssertions;  
using Xunit;  
  
namespace AceriaApp.CatalogoRecursos.Tests;  
  
public class CatalogoCombinacionesTests  
{  
    [Fact]  
    public void CombinacionesValidas_FiltraCorrectamente()  
    {  
        var combinaciones = new List<CombinacionVerboCodigo>  
        {  
            new() { Verbo = "GET", Codigo = 200 },  
            new() { Verbo = "POST", Codigo = 201 },  
            new() { Verbo = "GET", Codigo = 201 },  
            new() { Verbo = "OPTIONS", Codigo = 200 }  
        };  
        var catalogo = new CatalogoCombinaciones(combinaciones);  
        var validador = new ValidadorCombinacionVerboCodigo();  
  
        var validas = catalogo.CombinacionesValidas(validador).ToList();  
        var invalidas = catalogo.CombinacionesInvalidas(validador).ToList();  
  
        validas.Should().HaveCount(2);  
        invalidas.Should().HaveCount(2);  
    }  
}

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: el test verifica que el catálogo filtra correctamente las combinaciones válidas y las inválidas.

Errores comunes:

· Olvidar using System.Collections.Generic;: List<T> no se resuelve.
· Olvidar using System.Linq;: ToList() no se resuelve.
· No comprobar los recuentos: el test podría pasar por casualidad.

Verificación: el archivo CatalogoCombinacionesTests.cs compila y contiene un método de test.


---

Paso 16 — Compilar la solución completa

Acción 1: Escribir dotnet build AceriaApp.sln y pulsar Enter.
Acción 2: Verificar que la salida muestra Build succeeded. y 0 Warning(s), 0 Error(s).
Acción 3: Verificar que el tiempo de compilación es inferior a 180 segundos.

Por qué se hace: compilar la solución completa verifica que todos los proyectos, incluidos los nuevos, se resuelven correctamente.

Errores comunes:

· Tener la API en ejecución: el archivo .dll está bloqueado y la compilación falla.
· No restaurar paquetes: dotnet build restaura por defecto, pero si hay un error de red, hay que ejecutar dotnet restore primero.
· Usar una versión distinta del SDK: dotnet --version debe devolver 8.x.x.

Verificación: la salida debe mostrar Build succeeded. con 0 Error(s).


---

Paso 17 — Ejecutar todos los tests del punto 2.2

Acción 1: Escribir dotnet test tests\AceriaApp.CatalogoRecursos.Tests\AceriaApp.CatalogoRecursos.Tests.csproj y pulsar Enter.
Acción 2: Verificar que la salida muestra Passed! - Failed: 0, Passed: 5, Skipped: 0.
Acción 3: Verificar que el tiempo total es inferior a 30 segundos.

Por qué se hace: ejecutar los tests del punto 2.2 verifica que las clases de catálogo de recursos funcionan correctamente.

Errores comunes:

· Ejecutar dotnet test sin especificar el proyecto: ejecuta también los tests de los puntos anteriores, lo que alarga el tiempo.
· No compilar antes: dotnet test compila por defecto, pero si hay errores, los tests no se ejecutan.
· Tener la API en ejecución: el puerto puede estar ocupado.

Verificación: la salida debe mostrar Passed! - Failed: 0, Passed: 5, Skipped: 0, Total: 5.


---

Paso 18 — Ejecutar todos los tests de la solución

Acción 1: Escribir dotnet test AceriaApp.sln --no-build y pulsar Enter.
Acción 2: Verificar que la salida muestra Passed! - Failed: 0, Passed: 36, Skipped: 0.
Acción 3: Verificar que el tiempo total es inferior a 180 segundos.

Por qué se hace: ejecutar todos los tests de la solución verifica que los tests de los puntos 1.1 a 1.5 y de los puntos 2.1 y 2.2 pasan conjuntamente.

Errores comunes:

· No haber compilado antes: --no-build falla si no hay artefactos.
· Tener tests de otros módulos: la solución solo contiene los proyectos de este punto.
· Modificar los tests de los puntos anteriores: viola la regla de no modificar archivos del punto anterior.

Verificación: la salida debe mostrar Passed! - Failed: 0, Passed: 36, Skipped: 0, Total: 36.


---

Paso 19 — Crear el README del punto 2.2

Acción 1: En la carpeta del punto 2.2-recursos-verbos-codigos, hacer clic derecho y seleccionar Add → New Item → Text File.
Acción 2: Nombrar el archivo README.md.
Acción 3: Escribir exactamente el siguiente contenido:

# Punto 2.2 — Recursos, verbos HTTP y códigos de respuesta  
  
## Objetivo  
Comprender el concepto de recurso, aplicar los verbos HTTP con su semántica correcta y seleccionar el código de respuesta adecuado. Añadir al proyecto las clases de catálogo y validación de combinaciones verbo-código.  
  
## Estado del proyecto  
- Solución `AceriaApp.sln` con nueve proyectos.  
- Documento `docs/catalogo-recursos.md` con el catálogo de recursos, verbos y códigos.  
- Clases `CombinacionVerboCodigo`, `ValidadorCombinacionVerboCodigo` y `CatalogoCombinaciones` en `src/AceriaApp.Monolito.Api/CatalogoRecursos/`.  
- Cinco tests nuevos en `tests/AceriaApp.CatalogoRecursos.Tests`.  
- Los tests acumulados suman 36 pruebas unitarias.  
  
## Cómo ejecutarlo  
1. Abrir `AceriaApp.sln` en Visual Studio 2026.  
2. Verificar que SQL Server Express está arrancado.  
3. Ejecutar `dotnet ef database update` en `src\AceriaApp.Monolito.Api`.  
4. Ejecutar `dotnet run` en `src\AceriaApp.Monolito.Api`.  
5. Navegar a `https://localhost:7xxx/swagger`.  
6. Ejecutar `dotnet test AceriaApp.sln` para verificar los tests.  
  
## Qué se ha añadido respecto al punto anterior  
- Documento `docs/catalogo-recursos.md`.  
- Carpeta `CatalogoRecursos` en el proyecto monolítico con tres clases nuevas.  
- Proyecto `tests/AceriaApp.CatalogoRecursos.Tests` con cinco tests nuevos.  
- No se ha modificado ningún archivo del punto 2.1.  
  
## Documentación  
- [ADR-001](docs/ADR-001-monolito-vs-microservicios.md) a [ADR-006](docs/ADR-006-diseno-apis-rest.md) (heredados).  
- [Catálogo de recursos](docs/catalogo-recursos.md).

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que el README del punto 2.1 no se ha modificado.

Por qué se hace: el README del punto 2.2 explica el objetivo, el estado, la ejecución y los añadidos. No modifica el README del punto 2.1.

Errores comunes:

· Modificar el README del punto 2.1: viola la regla de no modificar archivos del punto anterior.
· Omitir la sección Qué se ha añadido respecto al punto anterior: pierde la trazabilidad.
· Escribir el README en la carpeta del punto 2.1: rompe la separación.

Verificación: el archivo README.md existe en la carpeta del punto 2.2 con las cinco secciones.


---

Paso 20 — Crear el ADR-007 del punto 2.2

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta docs.
Acción 2: Seleccionar Add → New Item → Text File y nombrar el archivo ADR-007-catalogo-recursos.md.
Acción 3: Escribir exactamente el siguiente contenido:

# ADR-007: Catálogo de recursos y validación de combinaciones verbo-código  
  
## Estado  
Aceptado  
  
## Contexto  
El proyecto AceriaApp ha adoptado el estilo REST en el punto 2.1. Es necesario definir el catálogo de recursos del dominio, los verbos permitidos sobre cada recurso y los códigos de respuesta esperados, y validar automáticamente la coherencia de las combinaciones.  
  
## Decisión  
Se adopta un catálogo de recursos con cinco recursos del dominio (Orden, LineaOrden, Material, Cliente, Movimiento) y sus combinaciones verbo-URI. Se definen los códigos de respuesta esperados por verbo. Se implementa un validador automático que comprueba la coherencia de cada combinación verbo-código.  
  
## Alternativas consideradas  
- Validación manual de las combinaciones: descartado por falta de trazabilidad.  
- Uso de códigos no estándar: descartado por romper la uniformidad de la API.  
  
## Consecuencias  
- Positivas: catálogo trazable, validación automática, coherencia de la API.  
- Negativas: la tabla de códigos por verbo puede requerir ajuste.  
- Mitigación: revisar la tabla al final del módulo 2.

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que los ADR-001 a ADR-006 no se han modificado.

Por qué se hace: el ADR-007 documenta la decisión de adoptar el catálogo de recursos y la validación automática. Es un artefacto nuevo del punto 2.2 que no modifica los ADR existentes.

Errores comunes:

· Modificar los ADR anteriores: viola la regla de no modificar archivos del punto anterior.
· Omitir la sección Alternativas consideradas: el ADR pierde valor.
· Nombrar el archivo sin el prefijo ADR-007: rompe la convención.

Verificación: el archivo docs\ADR-007-catalogo-recursos.md existe con las cinco secciones.


---

Paso 21 — Verificar que no se ha modificado ningún archivo del punto 2.1

Acción 1: En la terminal, escribir cd C:\cursos\AceriaApp y pulsar Enter.
Acción 2: Escribir fc /L modulo-2-apis-rest-aspnet-core\2.1-diseno-apis-rest\docs\ADR-006-diseno-apis-rest.md modulo-2-apis-rest-aspnet-core\2.2-recursos-verbos-codigos\docs\ADR-006-diseno-apis-rest.md y pulsar Enter.
Acción 3: Verificar que la salida muestra FC: no differences encountered.
Acción 4: Escribir fc /L modulo-2-apis-rest-aspnet-core\2.1-diseno-apis-rest\docs\diseno-apis-rest.md modulo-2-apis-rest-aspnet-core\2.2-recursos-verbos-codigos\docs\diseno-apis-rest.md y pulsar Enter.
Acción 5: Verificar que la salida muestra FC: no differences encountered.

Por qué se hace: la comparación con fc verifica que los documentos del punto 2.1 no se han modificado.

Errores comunes:

· Usar comp en lugar de fc: comp compara binarios y no muestra diferencias de texto.
· Olvidar el flag /L: fc compara en modo ASCII y muestra líneas largas sin ajuste.
· Comparar archivos de carpetas equivocadas: la comparación no es válida.

Verificación: los dos documentos del punto 2.1 no muestran diferencias.


---

Paso 22 — Verificar la estructura del punto 2.2

Acción 1: Escribir tree /F modulo-2-apis-rest-aspnet-core\2.2-recursos-verbos-codigos y pulsar Enter.
Acción 2: Verificar que la salida muestra AceriaApp.sln, README.md, src\AceriaApp.Monolito.Api\CatalogoRecursos con las tres clases nuevas, tests\AceriaApp.CatalogoRecursos.Tests con los dos archivos de tests y docs con el catálogo de recursos y el ADR-007.
Acción 3: Verificar que las carpetas Dominio, Infraestructura, Metricas, Diseno, Organizacion, BuenasPracticas y DisenoRest del punto 2.1 permanecen intactas.
Acción 4: Verificar que no existe ninguna carpeta labs ni ningún archivo metaprompt.md ni verificacion.md.

Por qué se hace: la verificación estructural confirma que el punto 2.2 añade archivos nuevos sin modificar los existentes.

Errores comunes:

· Crear carpetas auxiliares que no pertenecen a la estructura: rompe la convención.
· Modificar las carpetas del punto 2.1: viola la regla de no modificar.
· Omitir la carpeta CatalogoRecursos: los tests no encuentran las clases.

Verificación: la estructura contiene los archivos nuevos y conserva los del punto 2.1.


---

Paso 23 — Verificar el .gitignore del punto 2.2

Acción 1: Verificar que el archivo .gitignore existe en la carpeta del punto 2.2 (copiado del punto 2.1).
Acción 2: Abrir el archivo .gitignore con Visual Studio 2026.
Acción 3: Verificar que contiene las líneas bin/, obj/, *.user, *.suo, .vs/ y TestResults/.
Acción 4: Verificar que no se ha modificado respecto al punto 2.1.
Acción 5: Pulsar Ctrl+S si no hay cambios y cerrar el archivo.

Por qué se hace: el .gitignore se hereda del punto 2.1 sin modificaciones. La verificación confirma que no se ha tocado.

Errores comunes:

· Modificar el .gitignore copiado del punto 2.1: viola la regla de no modificar archivos del punto anterior.
· Eliminar alguna línea: el repositorio se llena de artefactos.
· Crear el .gitignore con otro nombre: el archivo no se reconoce.

Verificación: el .gitignore existe y contiene las seis líneas sin modificaciones.


---

Paso 24 — Hacer el commit del punto 2.2 y verificar el estado final

Acción 1: Escribir cd C:\cursos\AceriaApp y pulsar Enter.
Acción 2: Escribir git add . y pulsar Enter.
Acción 3: Escribir git commit -m "Punto 2.2: recursos, verbos HTTP y códigos de respuesta" y pulsar Enter.
Acción 4: Escribir git log --oneline y pulsar Enter para verificar los siete commits.
Acción 5: Escribir git status y pulsar Enter para verificar que el árbol está limpio.

Por qué se hace: el commit del punto 2.2 registra el estado acumulado del proyecto. Los siete commits consecutivos permiten comparar el estado del proyecto entre puntos consecutivos y entre módulos completos.

Errores comunes:

· No tener configurado user.name y user.email: git commit falla.
· Añadir la carpeta bin/ y obj/ al commit: el .gitignore lo evita.
· Hacer commit antes de git add .: no hay cambios en el índice.

Verificación: git log --oneline muestra siete commits: del punto 1.1 al 1.5, del punto 2.1 y del punto 2.2. git status muestra nothing to commit, working tree clean.


---

Errores comunes del ejercicio completo

Error Causa Solución
xcopy no copia subcarpetas Falta el flag /E Ejecutar xcopy origen destino /E /I /H /Y
Dictionary<string, int[]> no se resuelve Falta el using System.Collections.Generic; Añadir el using al principio del archivo
Contains no se resuelve Falta el using System.Linq; Añadir el using al principio del archivo
Where no se resuelve Falta el using System.Linq; Añadir el using al principio del archivo
NullReferenceException en CatalogoCombinaciones No se inicializa _combinaciones Inicializar en el constructor
KeyNotFoundException en el validador No se comprueba si el verbo existe Comprobar ContainsKey antes de acceder
El validador acepta códigos no permitidos Falta la comprobación con Contains Revisar la segunda comprobación del método
Should() no se resuelve Falta el paquete FluentAssertions Ejecutar dotnet add package FluentAssertions
El proyecto de tests no compila Falta la referencia al proyecto monolítico Ejecutar dotnet add reference
La compilación falla por el .dll bloqueado La API está en ejecución Detener la API con Ctrl+C


---

Reto resuelto paso a paso

Reto: añadir un método Resumen a CatalogoCombinaciones que devuelva el número de combinaciones válidas, el número de inválidas y el porcentaje de validez, y un test que verifique el cálculo cuando hay tres válidas y dos inválidas.

Paso 1: En CatalogoCombinaciones.cs, añadir el siguiente record al final del archivo:

public record ResumenCombinaciones(int Validas, int Invalidas, double PorcentajeValidez);

Paso 2: Explicar línea por línea:

Línea 1: public record ResumenCombinaciones( → declara un contrato inmutable.
Línea 2: int Validas, → número de combinaciones válidas.
Línea 3: int Invalidas, → número de combinaciones inválidas.
Línea 4: double PorcentajeValidez); → porcentaje de validez.

Paso 3: En CatalogoCombinaciones.cs, añadir el siguiente método dentro de la clase:

public ResumenCombinaciones Resumen(ValidadorCombinacionVerboCodigo validador)  
{  
    var validas = _combinaciones.Count(c => validador.Validar(c).EsValida);  
    var invalidas = _combinaciones.Count - validas;  
    var total = _combinaciones.Count;  
    var porcentaje = total == 0 ? 0 : (double)validas / total * 100;  
    return new ResumenCombinaciones(validas, invalidas, porcentaje);  
}

Paso 4: Explicar línea por línea:

Línea 1: public ResumenCombinaciones Resumen(ValidadorCombinacionVerboCodigo validador) → declara el método.
Línea 2: { → abre el cuerpo.
Línea 3: var validas = _combinaciones.Count(c => validador.Validar(c).EsValida); → cuenta las válidas.
Línea 4: var invalidas = _combinaciones.Count - validas; → calcula las inválidas por diferencia.
Línea 5: var total = _combinaciones.Count; → obtiene el total.
Línea 6: var porcentaje = total == 0 ? 0 : (double)validas / total * 100; → calcula el porcentaje con protección contra división por cero.
Línea 7: return new ResumenCombinaciones(validas, invalidas, porcentaje); → devuelve el resumen.
Línea 8: } → cierra el cuerpo.

Paso 5: Guardar el archivo con Ctrl+S.

Paso 6: En CatalogoCombinacionesTests.cs, añadir el siguiente test:

[Fact]  
public void Resumen_ConTresValidasYDosInvalidas_CalculaPorcentaje()  
{  
    var combinaciones = new List<CombinacionVerboCodigo>  
    {  
        new() { Verbo = "GET", Codigo = 200 },  
        new() { Verbo = "POST", Codigo = 201 },  
        new() { Verbo = "DELETE", Codigo = 204 },  
        new() { Verbo = "GET", Codigo = 201 },  
        new() { Verbo = "POST", Codigo = 200 }  
    };  
    var catalogo = new CatalogoCombinaciones(combinaciones);  
    var validador = new ValidadorCombinacionVerboCodigo();  
  
    var resumen = catalogo.Resumen(validador);  
  
    resumen.Validas.Should().Be(3);  
    resumen.Invalidas.Should().Be(2);  
    resumen.PorcentajeValidez.Should().Be(60.0);  
}

Paso 7: Explicar línea por línea:

Línea 1: [Fact] → marca el método como test de xUnit.
Línea 2: public void Resumen_ConTresValidasYDosInvalidas_CalculaPorcentaje() → declara el test.
Línea 3: { → abre el cuerpo.
Línea 4: var combinaciones = new List<CombinacionVerboCodigo> → crea la lista.
Línea 5: { → abre el inicializador.
Línea 6: new() { Verbo = "GET", Codigo = 200 }, → primera válida.
Línea 7: new() { Verbo = "POST", Codigo = 201 }, → segunda válida.
Línea 8: new() { Verbo = "DELETE", Codigo = 204 }, → tercera válida.
Línea 9: new() { Verbo = "GET", Codigo = 201 }, → primera inválida.
Línea 10: new() { Verbo = "POST", Codigo = 200 } → segunda inválida.
Línea 11: }; → cierra el inicializador.
Línea 12: var catalogo = new CatalogoCombinaciones(combinaciones); → instancia el catálogo.
Línea 13: var validador = new ValidadorCombinacionVerboCodigo(); → instancia el validador.
Línea 14: var resumen = catalogo.Resumen(validador); → invoca el método.
Línea 15: resumen.Validas.Should().Be(3); → verifica las válidas.
Línea 16: resumen.Invalidas.Should().Be(2); → verifica las inválidas.
Línea 17: resumen.PorcentajeValidez.Should().Be(60.0); → verifica el porcentaje.
Línea 18: } → cierra el cuerpo.

Paso 8: Ejecutar dotnet test tests\AceriaApp.CatalogoRecursos.Tests\AceriaApp.CatalogoRecursos.Tests.csproj y verificar que pasan los seis tests.

Paso 9: Verificar que el método Resumen no modifica ningún archivo del punto 2.1.

Paso 10: Hacer commit con git commit -m "Reto 2.2: método Resumen en CatalogoCombinaciones con cálculo de porcentaje".

Verificación: la salida de dotnet test muestra Passed: 6.


---

Resultado esperado

Al finalizar este punto, el alumno debe tener:

· La carpeta modulo-2-apis-rest-aspnet-core/2.2-recursos-verbos-codigos/ con la solución AceriaApp.sln que contiene nueve proyectos.
· El documento docs/catalogo-recursos.md con los recursos, verbos y códigos del proyecto.
· El documento docs/ADR-007-catalogo-recursos.md con la decisión sobre el catálogo y la validación.
· Las clases CombinacionVerboCodigo, ValidadorCombinacionVerboCodigo y CatalogoCombinaciones en src/AceriaApp.Monolito.Api/CatalogoRecursos/.
· El proyecto tests/AceriaApp.CatalogoRecursos.Tests con cinco tests (seis tras el reto).
· Los tests de los puntos 1.1 a 1.5 y 2.1 y 2.2 pasando conjuntamente con dotnet test AceriaApp.sln, total 36 pruebas (37 tras el reto).
· Los ADR-001 a ADR-006 del punto 2.1 sin modificar.
· Siete commits en Git: del punto 1.1 al 1.5, del punto 2.1 y del punto 2.2.


---

Conclusión y enlace al siguiente punto

El punto 2.2 ha completado el diseño de la API REST con el catálogo de recursos, la semántica de los verbos HTTP y la relación sistemática entre verbo y código de respuesta. El proyecto AceriaApp dispone ahora de un catálogo documentado de recursos, un validador automático de combinaciones verbo-código y cinco tests nuevos. Esta base permite avanzar hacia el punto 2.3, donde se estudiará la validación de peticiones con FluentValidation, se aplicarán las reglas de validación a los recursos del catálogo y se devolverán errores en formato problem details.


---

Fin del punto 2.2.

Espero confirmación del usuario antes de continuar con el punto 2.3.