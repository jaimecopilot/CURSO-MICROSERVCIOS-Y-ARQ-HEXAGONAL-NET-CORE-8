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

