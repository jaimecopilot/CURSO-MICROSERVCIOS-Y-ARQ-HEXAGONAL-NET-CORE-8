Punto 2.1 — Diseño de APIs REST

Módulo 2: Desarrollo de APIs REST con ASP.NET Core
Duración: 53 minutos (26 minutos de teoría + 27 minutos de práctica)
Objetivos de aprendizaje:

· Comprender los principios del estilo arquitectónico REST.
· Identificar los recursos como unidad central del diseño de una API REST.
· Comprender la relación entre recursos, URIs y representaciones.
· Comprender el principio de interfaz uniforme y su aplicación en ASP.NET Core.
· Añadir al proyecto AceriaApp un documento de diseño de APIs REST y una clase de validación de URIs REST.


---

PARTE TEÓRICA (26 minutos)

Bloque 1 — Definición de REST

REST es un estilo arquitectónico definido por Roy Fielding en su tesis doctoral de 2000. No es un protocolo ni un estándar, sino un conjunto de restricciones que, aplicadas de forma conjunta, producen un sistema con propiedades específicas. Las restricciones son seis: cliente-servidor, sin estado, cacheable, interfaz uniforme, sistema en capas y código bajo demanda. Cada restricción aporta una propiedad al sistema. La restricción de cliente-servidor separa las responsabilidades de la interfaz de usuario y del almacenamiento de datos. La restricción de sin estado garantiza que cada petición contenga toda la información necesaria para ser procesada. La restricción de cacheable permite que las respuestas se almacenen para reducir la carga. La restricción de interfaz uniforme simplifica la arquitectura global.

Restricciones de REST:  
  
1. Cliente-servidor  
2. Sin estado  
3. Cacheable  
4. Interfaz uniforme  
5. Sistema en capas  
6. Código bajo demanda (opcional)

Línea 1: 1. Cliente-servidor → primera restricción, separa interfaz y almacenamiento.
Línea 2: 2. Sin estado → segunda restricción, cada petición contiene toda la información.
Línea 3: 3. Cacheable → tercera restricción, las respuestas se pueden almacenar.
Línea 4: 4. Interfaz uniforme → cuarta restricción, simplifica la arquitectura.
Línea 5: 5. Sistema en capas → quinta restricción, permite intermediarios.
Línea 6: 6. Código bajo demanda → sexta restricción, opcional.

Las seis restricciones no son obligatorias por separado: son un conjunto. Un sistema que aplica cinco de las seis no es REST, es un sistema parcialmente REST. La restricción de interfaz uniforme es la que más impacto tiene en el diseño de una API. Se descompone en cuatro sub-restricciones: identificación de recursos, manipulación de recursos a través de representaciones, mensajes auto-descriptivos e hipermedia como motor del estado de la aplicación. Las cuatro sub-restricciones guían el diseño de las URIs y de los métodos HTTP. El curso aplica las cuatro sub-restricciones al diseño de la API de la acería.

La aplicación de las seis restricciones produce un sistema con propiedades medibles: escalabilidad, simplicidad, modificabilidad y visibilidad. La propiedad de escalabilidad se obtiene de la restricción sin estado y de la restricción cacheable. La propiedad de simplicidad se obtiene de la restricción de interfaz uniforme. La propiedad de modificabilidad se obtiene de la restricción de sistema en capas. La propiedad de visibilidad se obtiene de la restricción de mensajes auto-descriptivos. Las cuatro propiedades son las razones por las que REST se ha convertido en el estilo dominante para APIs web.


---

Bloque 2 — Recursos como unidad central del diseño

Un recurso es cualquier entidad identificable que puede ser referenciada y manipulada. En una API REST, los recursos son la unidad central del diseño. Una orden es un recurso. Un material es un recurso. Un cliente es un recurso. La colección de órdenes también es un recurso. Cada recurso se identifica con una URI única. La URI no describe acciones, describe entidades. La diferencia entre una URI que describe acciones y una URI que describe entidades es la diferencia entre RPC y REST. Una URI como /api/crearOrden describe una acción. Una URI como /api/v1/ordenes describe una entidad.

URIs de recursos:  
  
/api/v1/ordenes           → colección de órdenes.  
/api/v1/ordenes/{id}      → orden concreta.  
/api/v1/ordenes/{id}/lineas → líneas de una orden concreta.  
/api/v1/materiales       → colección de materiales.  
/api/v1/clientes         → colección de clientes.

Línea 1: /api/v1/ordenes → recurso de colección de órdenes.
Línea 2: /api/v1/ordenes/{id} → recurso de orden concreta.
Línea 3: /api/v1/ordenes/{id}/lineas → recurso de líneas de una orden.
Línea 4: /api/v1/materiales → recurso de colección de materiales.
Línea 5: /api/v1/clientes → recurso de colección de clientes.

La identificación de recursos con URIs tiene tres consecuencias prácticas. La primera es que las URIs se construyen con sustantivos en plural para las colecciones. La segunda es que las relaciones entre recursos se expresan con anidamiento de URIs. La tercera es que las URIs no contienen verbos. Las tres consecuencias se aplican de forma uniforme en toda la API. La uniformidad es lo que permite que un cliente genérico pueda navegar la API sin conocerla de antemano. La uniformidad también facilita la documentación automática con OpenAPI.


---

Bloque 3 — Representaciones y negociación de contenido

Un recurso es un concepto abstracto. Su representación es la forma concreta en la que se transmite. Un mismo recurso puede tener varias representaciones: JSON, XML, texto plano. La representación se selecciona mediante negociación de contenido. El cliente envía la cabecera Accept con los formatos que acepta. El servidor responde con el formato que puede generar. La negociación evita que el cliente tenga que especificar el formato en la URI. La representación JSON es la más común en APIs REST modernas. El curso usa JSON como representación por defecto.

// El cliente envía:  
// Accept: application/json  
  
app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) =>  
    await db.Ordenes.AsNoTracking().ToListAsync());

Línea 1: // El cliente envía: → comentario que indica el ejemplo.
Línea 2: // Accept: application/json → cabecera del cliente.
Línea 3: app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) => → declara el endpoint GET.
Línea 4: await db.Ordenes.AsNoTracking().ToListAsync()); → devuelve la lista en JSON.

La representación tiene dos consecuencias prácticas. La primera es que la misma URI puede devolver formatos distintos según la cabecera Accept. La segunda es que el servidor puede devolver 406 Not Acceptable si no puede generar ningún formato solicitado. La negociación de contenido es una de las sub-restricciones de la interfaz uniforme. Su aplicación correcta evita que el cliente tenga que usar URIs distintas para formatos distintos.


---

Bloque 4 — Métodos HTTP y su semántica

Los métodos HTTP expresan la operación que se realiza sobre el recurso. Cada método tiene una semántica definida por el estándar. Los métodos principales son cinco: GET, POST, PUT, PATCH y DELETE. GET recupera una representación del recurso. POST crea un recurso nuevo. PUT reemplaza un recurso existente. PATCH modifica parcialmente un recurso existente. DELETE elimina un recurso existente. Cada método tiene dos propiedades importantes: idempotencia y seguridad. Un método es seguro si no modifica el estado del servidor. Un método es idempotente si ejecutarlo varias veces produce el mismo resultado que ejecutarlo una vez.

Métodos HTTP:  
  
GET     /api/v1/ordenes        → lista de órdenes. Seguro, idempotente.  
GET     /api/v1/ordenes/{id}   → orden concreta. Seguro, idempotente.  
POST    /api/v1/ordenes        → crear orden. No seguro, no idempotente.  
PUT     /api/v1/ordenes/{id}   → reemplazar orden. No seguro, idempotente.  
PATCH   /api/v1/ordenes/{id}   → modificar orden. No seguro, no idempotente.  
DELETE  /api/v1/ordenes/{id}   → eliminar orden. No seguro, idempotente.

Línea 1: GET /api/v1/ordenes → recupera la colección. Seguro e idempotente.
Línea 2: GET /api/v1/ordenes/{id} → recupera una orden. Seguro e idempotente.
Línea 3: POST /api/v1/ordenes → crea una orden. No seguro, no idempotente.
Línea 4: PUT /api/v1/ordenes/{id} → reemplaza una orden. No seguro, idempotente.
Línea 5: PATCH /api/v1/ordenes/{id} → modifica parcialmente. No seguro, no idempotente.
Línea 6: DELETE /api/v1/ordenes/{id} → elimina una orden. No seguro, idempotente.

La semántica de los métodos tiene dos consecuencias prácticas. La primera es que los métodos seguros pueden ser cacheados por intermediarios sin riesgo. La segunda es que los métodos idempotentes pueden ser reintentados sin riesgo de duplicación. La combinación de ambas propiedades determina qué métodos pueden reintentarse automáticamente. GET, PUT y DELETE pueden reintentarse. POST y PATCH no pueden reintentarse sin una clave de idempotencia. La semántica correcta de los métodos es la base de la comunicación fiable.


---

Bloque 5 — Códigos de estado HTTP

Los códigos de estado HTTP expresan el resultado de la operación. Se organizan en cinco familias: 1xx informativos, 2xx éxito, 3xx redirección, 4xx error del cliente, 5xx error del servidor. Cada familia tiene códigos específicos para situaciones concretas. Los códigos más usados en APIs REST son 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity y 500 Internal Server Error. La elección del código adecuado permite que el cliente distinga entre situaciones distintas sin analizar el cuerpo de la respuesta.

Códigos de estado habituales:  
  
200 OK                    → operación exitosa con cuerpo.  
201 Created               → recurso creado, con cabecera Location.  
204 No Content            → operación exitosa sin cuerpo.  
400 Bad Request           → error de validación o formato.  
401 Unauthorized          → falta autenticación.  
403 Forbidden             → autenticación correcta, sin permisos.  
404 Not Found             → recurso no encontrado.  
409 Conflict              → conflicto de estado.  
422 Unprocessable Entity  → entidad semánticamente inválida.  
500 Internal Server Error → error del servidor.

Línea 1: 200 OK → operación exitosa con cuerpo.
Línea 2: 201 Created → recurso creado, con cabecera Location.
Línea 3: 204 No Content → operación exitosa sin cuerpo.
Línea 4: 400 Bad Request → error de validación o formato.
Línea 5: 401 Unauthorized → falta autenticación.
Línea 6: 403 Forbidden → sin permisos.
Línea 7: 404 Not Found → recurso no encontrado.
Línea 8: 409 Conflict → conflicto de estado.
Línea 9: 422 Unprocessable Entity → entidad semánticamente inválida.
Línea 10: 500 Internal Server Error → error del servidor.

La elección del código de estado tiene dos consecuencias prácticas. La primera es que el cliente puede reaccionar de forma distinta a cada código sin analizar el cuerpo. La segunda es que los intermediarios pueden cachear o no cachear según el código. Los códigos 2xx son cacheables según las cabeceras. Los códigos 4xx y 5xx no son cacheables por defecto. La elección correcta del código es la base de la comunicación predecible entre cliente y servidor.


---

Bloque 6 — Diseño de URIs en APIs REST

El diseño de URIs sigue cinco reglas prácticas. La primera es usar sustantivos en plural para las colecciones. La segunda es usar el identificador del recurso concreto después de la colección. La tercera es anidar las relaciones con sub-rutas. La cuarta es no incluir verbos en las URIs. La quinta es versionar la API en la propia URI. La aplicación conjunta de las cinco reglas produce URIs predecibles y consistentes. La consistencia permite que un cliente genérico pueda navegar la API sin conocerla de antemano.

Reglas de diseño de URIs:  
  
1. Sustantivos en plural        → /ordenes, /materiales.  
2. Identificador tras colección → /ordenes/{id}.  
3. Anidamiento de relaciones    → /ordenes/{id}/lineas.  
4. Sin verbos                   → no /crearOrden.  
5. Versionado en la URI         → /api/v1/ordenes.

Línea 1: 1. Sustantivos en plural → colecciones con sustantivo plural.
Línea 2: 2. Identificador tras colección → identificador después de la colección.
Línea 3: 3. Anidamiento de relaciones → sub-rutas para relaciones.
Línea 4: 4. Sin verbos → las URIs no contienen verbos.
Línea 5: 5. Versionado en la URI → la versión va en la URI.

Las cinco reglas se aplican de forma uniforme en toda la API. La uniformidad es lo que distingue una API REST de una API RPC. La uniformidad también facilita la documentación automática con OpenAPI, la generación de clientes y la integración con herramientas de monitorización. La violación de cualquiera de las cinco reglas rompe la uniformidad y obliga al cliente a conocer la API de antemano. El curso aplica las cinco reglas al diseño de la API de la acería.


---

Bloque 7 — Interfaz uniforme en ASP.NET Core

La interfaz uniforme se materializa en ASP.NET Core con cuatro elementos. El primero es el enrutamiento, que asocia URIs a manejadores. El segundo es el enlace de parámetros, que asocia partes de la petición a parámetros del manejador. El tercero es la serialización, que convierte objetos a JSON y viceversa. El cuarto es la negociación de contenido, que selecciona el formato de la respuesta. Los cuatro elementos se configuran en el arranque de la aplicación. La configuración correcta produce una API uniforme sin código repetido en cada endpoint.

var builder = WebApplication.CreateBuilder(args);  
builder.Services.AddEndpointsApiExplorer();  
builder.Services.AddSwaggerGen();  
  
var app = builder.Build();  
  
app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) =>  
    await db.Ordenes.AsNoTracking().ToListAsync());  
  
app.MapGet("/api/v1/ordenes/{id:guid}", async (Guid id, AceriaDbContext db) =>  
{  
    var orden = await db.Ordenes.AsNoTracking().FirstOrDefaultAsync(o => o.Id == id);  
    return orden is not null ? Results.Ok(orden) : Results.NotFound();  
});  
  
app.Run();

Línea 1: var builder = WebApplication.CreateBuilder(args); → crea el constructor de la aplicación.
Línea 2: builder.Services.AddEndpointsApiExplorer(); → habilita la exploración de endpoints.
Línea 3: builder.Services.AddSwaggerGen(); → registra el generador de Swagger.
Línea 4: var app = builder.Build(); → construye la aplicación.
Línea 5: app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) => → declara el endpoint de colección.
Línea 6: await db.Ordenes.AsNoTracking().ToListAsync()); → devuelve la lista.
Línea 7: app.MapGet("/api/v1/ordenes/{id:guid}", async (Guid id, AceriaDbContext db) => → declara el endpoint de detalle.
Línea 8: { → abre el cuerpo del lambda.
Línea 9: var orden = await db.Ordenes.AsNoTracking().FirstOrDefaultAsync(o => o.Id == id); → consulta la orden.
Línea 10: return orden is not null ? Results.Ok(orden) : Results.NotFound(); → devuelve 200 o 404.
Línea 11: }); → cierra el lambda.
Línea 12: app.Run(); → arranca el servidor.

La configuración de la interfaz uniforme tiene dos consecuencias prácticas. La primera es que los endpoints siguen un patrón común que facilita la lectura. La segunda es que la documentación OpenAPI se genera automáticamente a partir de los endpoints. La combinación de ambas reduce el coste de mantenimiento y mejora la experiencia del consumidor. La interfaz uniforme es una de las propiedades más valiosas de REST.


---

Bloque 8 — Recursos anidados y relaciones

Los recursos pueden anidarse para expresar relaciones. Una orden tiene líneas. Una línea tiene materiales. Las relaciones se expresan con sub-rutas. La URI /api/v1/ordenes/{id}/lineas expresa la colección de líneas de una orden concreta. La URI /api/v1/ordenes/{id}/lineas/{lineaId} expresa una línea concreta. El anidamiento tiene un límite práctico: no se anidan más de dos niveles para evitar URIs excesivamente largas. Las relaciones que superan dos niveles se expresan con recursos independientes y parámetros de consulta.

Anidamiento de recursos:  
  
/api/v1/ordenes                    → colección de órdenes.  
/api/v1/ordenes/{id}               → orden concreta.  
/api/v1/ordenes/{id}/lineas        → líneas de una orden.  
/api/v1/ordenes/{id}/lineas/{lid}  → línea concreta.  
  
Alternativa sin anidar:  
  
/api/v1/lineas?ordenId={id}        → líneas filtradas por orden.

Línea 1: /api/v1/ordenes → colección de órdenes.
Línea 2: /api/v1/ordenes/{id} → orden concreta.
Línea 3: /api/v1/ordenes/{id}/lineas → líneas de una orden.
Línea 4: /api/v1/ordenes/{id}/lineas/{lid} → línea concreta.
Línea 5: /api/v1/lineas?ordenId={id} → alternativa sin anidar.

El anidamiento tiene dos consecuencias prácticas. La primera es que las relaciones se expresan de forma natural. La segunda es que las URIs pueden volverse largas si se anidan demasiados niveles. La regla práctica es anidar solo cuando la relación es de composición: la línea no existe sin la orden. Cuando la relación es de asociación, se usa un recurso independiente con parámetros de consulta. La distinción entre composición y asociación es la clave para decidir cuándo anidar.


---

Bloque 9 — Paginación, filtrado y ordenación

Las colecciones grandes no se devuelven completas. Se paginan con parámetros de consulta. Los parámetros habituales son page y pageSize para la paginación, filter para el filtrado y sort para la ordenación. Los parámetros de consulta se expresan con el signo ? después de la URI. La respuesta incluye metadatos de paginación: número de página, tamaño de página, total de elementos y total de páginas. Los metadatos permiten al cliente construir la interfaz de navegación sin conocer la colección completa.

Paginación, filtrado y ordenación:  
  
GET /api/v1/ordenes?page=1&pageSize=20  
GET /api/v1/ordenes?filter=cliente:ACX-001  
GET /api/v1/ordenes?sort=fechaCreacion:desc  
  
Respuesta con metadatos:  
  
{  
  "items": [ ... ],  
  "page": 1,  
  "pageSize": 20,  
  "totalItems": 145,  
  "totalPages": 8  
}

Línea 1: GET /api/v1/ordenes?page=1&pageSize=20 → paginación.
Línea 2: GET /api/v1/ordenes?filter=cliente:ACX-001 → filtrado.
Línea 3: GET /api/v1/ordenes?sort=fechaCreacion:desc → ordenación.
Línea 4: { → abre el objeto de respuesta.
Línea 5: "items": [ ... ], → lista de elementos de la página.
Línea 6: "page": 1, → número de página actual.
Línea 7: "pageSize": 20, → tamaño de página.
Línea 8: "totalItems": 145, → total de elementos.
Línea 9: "totalPages": 8 → total de páginas.

La paginación tiene dos consecuencias prácticas. La primera es que las respuestas se mantienen pequeñas y predecibles. La segunda es que el cliente puede construir la interfaz de navegación con los metadatos. La ausencia de paginación en colecciones grandes produce respuestas lentas, consumo elevado de memoria y dificultad para el cliente. La paginación es una buena práctica obligatoria en cualquier API REST que exponga colecciones.


---

Bloque 10 — Aplicación del diseño REST al proyecto del curso

El proyecto del curso aplica el diseño REST en cada endpoint. Los recursos se identifican con URIs que siguen las cinco reglas. Los métodos HTTP expresan la semántica de la operación. Los códigos de estado expresan el resultado. Las representaciones se negocian con la cabecera Accept. Las colecciones se paginan con parámetros de consulta. Las relaciones se anidan con sub-rutas. El diseño se documenta en un documento de diseño de APIs REST y se audita con una clase de validación de URIs.

Aplicación al proyecto del curso:  
  
Recursos identificados     → /api/v1/ordenes, /api/v1/materiales.  
Métodos HTTP con semántica → GET, POST, PUT, PATCH, DELETE.  
Códigos de estado          → 200, 201, 204, 400, 404, 409, 422, 500.  
Representaciones           → JSON por defecto.  
Paginación                 → page, pageSize.  
Relaciones anidadas        → /ordenes/{id}/lineas.

Línea 1: Recursos identificados → URIs que siguen las cinco reglas.
Línea 2: Métodos HTTP con semántica → métodos con semántica definida.
Línea 3: Códigos de estado → códigos adecuados a cada situación.
Línea 4: Representaciones → JSON por defecto.
Línea 5: Paginación → parámetros de consulta.
Línea 6: Relaciones anidadas → sub-rutas para relaciones.

La aplicación del diseño REST prepara el proyecto para los puntos posteriores del módulo 2. El punto 2.2 estudiará los recursos, verbos y códigos con detalle. El punto 2.3 estudiará la validación de peticiones. El punto 2.4 estudiará la documentación OpenAPI. La base del diseño REST es el fundamento de los tres puntos siguientes. El punto 2.1 establece los conceptos que se aplicarán en los tres puntos siguientes.


---

Resumen rápido de la teoría

· REST es un estilo arquitectónico definido por seis restricciones: cliente-servidor, sin estado, cacheable, interfaz uniforme, sistema en capas y código bajo demanda.
· Los recursos son la unidad central del diseño y se identifican con URIs que siguen cinco reglas.
· Las representaciones se negocian con la cabecera Accept y el formato por defecto es JSON.
· Los métodos HTTP expresan la semántica de la operación y tienen dos propiedades: seguridad e idempotencia.
· Los códigos de estado expresan el resultado de la operación en cinco familias.
· Las colecciones se paginan con parámetros de consulta y las relaciones se anidan con sub-rutas.


---

