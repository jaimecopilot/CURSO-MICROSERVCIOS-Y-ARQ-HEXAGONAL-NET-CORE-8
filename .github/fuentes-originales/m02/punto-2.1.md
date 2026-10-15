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

PARTE PRÁCTICA (27 minutos)

Ejercicio: Añadir al punto 1.5 un documento de diseño de APIs REST en docs/, una clase de validación de URIs REST en el proyecto monolítico y un test unitario que verifique la validación. El punto 2.1 parte del contenido del punto 1.5 sin modificar ningún archivo existente: solo añade archivos nuevos. El punto 2.1 es el primer punto del módulo 2 y se crea en la carpeta modulo-2-apis-rest-aspnet-core.

Ubicación de trabajo: C:\cursos\AceriaApp\


---

Paso 1 — Crear la estructura del módulo 2 y del punto 2.1

Acción 1: Abrir la terminal integrada de Visual Studio 2026 con Ctrl+ñ (o Ctrl+``  en teclados no españoles).
Acción 2: Escribir cd C:\cursos\AceriaApp y pulsar Enter.
Acción 3: Escribir mkdir modulo-2-apis-rest-aspnet-core y pulsar Enter.
Acción 4: Escribir mkdir modulo-2-apis-rest-aspnet-core\2.1-diseno-apis-rest y pulsar Enter.
Acción 5: Escribir xcopy modulo-1-introduccion-microservicios\1.5-buenas-practicas modulo-2-apis-rest-aspnet-core\2.1-diseno-apis-rest /E /I /H /Y y pulsar Enter.
Acción 6: Escribir dir modulo-2-apis-rest-aspnet-core\2.1-diseno-apis-rest y pulsar Enter para verificar que se ha copiado el contenido.

Por qué se hace: cada punto del curso parte del contenido del punto anterior. El punto 2.1 es el primer punto del módulo 2 y parte del punto 1.5, que es el último punto del módulo 1. La copia se hace en la carpeta del módulo 2.

Errores comunes:

· Usar copy en lugar de xcopy: copy no copia carpetas de forma recursiva.
· Olvidar el flag /E: no se copian las subcarpetas vacías.
· Olvidar el flag /I: xcopy pregunta si el destino es un directorio cuando no existe.
· Olvidar el flag /Y: xcopy pide confirmación para sobrescribir.
· Copiar desde el punto 1.4 en lugar del 1.5: se pierde el contenido del último punto del módulo 1.

Verificación: al ejecutar dir modulo-2-apis-rest-aspnet-core\2.1-diseno-apis-rest, deben aparecer AceriaApp.sln, README.md, src, tests y docs.


---

Paso 2 — Abrir la solución copiada en Visual Studio 2026

Acción 1: Escribir cd modulo-2-apis-rest-aspnet-core\2.1-diseno-apis-rest y pulsar Enter.
Acción 2: Escribir start AceriaApp.sln y pulsar Enter.
Acción 3: Verificar que Visual Studio 2026 abre la solución y muestra los proyectos heredados del punto 1.5: AceriaApp.Monolito.Api, AceriaApp.Monolito.Tests, AceriaApp.Metricas.Tests, AceriaApp.Diseno.Tests, AceriaApp.Organizacion.Tests y AceriaApp.BuenasPracticas.Tests.
Acción 4: Verificar que la solución compila con Ctrl+Shift+B y que la salida muestra Build succeeded..

Por qué se hace: abrir la solución copiada permite trabajar en el punto 2.1 sobre la base del punto 1.5. La compilación verifica que la copia es correcta.

Errores comunes:

· Abrir la solución del punto 1.5 en lugar de la del punto 2.1: los cambios se aplican al punto equivocado.
· No compilar antes de empezar: si la copia tiene errores, los cambios posteriores fallan.
· Tener la API del punto 1.5 en ejecución: el puerto queda ocupado y la compilación falla.

Verificación: Visual Studio 2026 muestra la solución AceriaApp con los seis proyectos heredados del punto 1.5 y la compilación es correcta.


---

Paso 3 — Verificar que la carpeta docs contiene los documentos del punto 1.5

Acción 1: En el panel Solution Explorer, expandir la carpeta docs del punto 2.1.
Acción 2: Verificar que contiene ADR-001 a ADR-005, analisis-ventajas-inconvenientes.md, principios-diseno.md, organizacion-solucion.md y buenas-practicas.md.
Acción 3: Verificar que ninguno de los nueve documentos se ha modificado.
Acción 4: Verificar que la carpeta docs no contiene ningún archivo nuevo del punto 2.1 todavía.

Por qué se hace: el punto 2.1 parte del contenido del punto 1.5, que ya incluye la carpeta docs con nueve documentos. No se modifica ningún documento existente.

Errores comunes:

· Modificar alguno de los ADR o documentos existentes: viola la regla de no modificar archivos del punto anterior.
· Eliminar algún documento existente: pierde la trazabilidad del punto 1.5.
· Crear la carpeta docs si ya existe: mkdir falla.

Verificación: la carpeta docs contiene los nueve documentos del punto 1.5 sin modificaciones.


---

Paso 4 — Crear el documento de diseño de APIs REST en docs

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta docs.
Acción 2: Seleccionar Add → New Item → Text File y nombrar el archivo diseno-apis-rest.md.
Acción 3: Escribir exactamente el siguiente contenido:

# Diseño de APIs REST — Punto 2.1  
  
## Restricciones de REST  
  
1. Cliente-servidor.  
2. Sin estado.  
3. Cacheable.  
4. Interfaz uniforme.  
5. Sistema en capas.  
6. Código bajo demanda (opcional).  
  
## Recursos  
  
Un recurso es cualquier entidad identificable. Se identifica con una URI única.  
  
## URIs del proyecto  
  
- `/api/v1/ordenes` → colección de órdenes.  
- `/api/v1/ordenes/{id}` → orden concreta.  
- `/api/v1/ordenes/{id}/lineas` → líneas de una orden.  
- `/api/v1/materiales` → colección de materiales.  
- `/api/v1/clientes` → colección de clientes.  
  
## Reglas de diseño de URIs  
  
1. Sustantivos en plural.  
2. Identificador tras la colección.  
3. Anidamiento de relaciones con sub-rutas.  
4. Sin verbos en las URIs.  
5. Versionado en la URI.  
  
## Métodos HTTP  
  
| Método | Semántica | Seguro | Idempotente |  
|--------|-----------|--------|-------------|  
| GET | Recuperar | Sí | Sí |  
| POST | Crear | No | No |  
| PUT | Reemplazar | No | Sí |  
| PATCH | Modificar | No | No |  
| DELETE | Eliminar | No | Sí |  
  
## Códigos de estado  
  
| Código | Significado |  
|--------|-------------|  
| 200 | Operación exitosa con cuerpo |  
| 201 | Recurso creado |  
| 204 | Operación exitosa sin cuerpo |  
| 400 | Error de validación |  
| 401 | Falta autenticación |  
| 403 | Sin permisos |  
| 404 | Recurso no encontrado |  
| 409 | Conflicto de estado |  
| 422 | Entidad no procesable |  
| 500 | Error del servidor |  
  
## Paginación, filtrado y ordenación  
  
- `?page=1&pageSize=20` → paginación.  
- `?filter=cliente:ACX-001` → filtrado.  
- `?sort=fechaCreacion:desc` → ordenación.  
  
## Aplicación al proyecto del curso  
  
| Elemento | Aplicación |  
|----------|------------|  
| Recursos | URIs con sustantivos en plural |  
| Métodos | GET, POST, PUT, PATCH, DELETE |  
| Códigos | 200, 201, 204, 400, 404, 409, 422, 500 |  
| Representaciones | JSON |  
| Paginación | `page`, `pageSize` |  
| Relaciones | Sub-rutas anidadas |

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que el archivo aparece en la carpeta docs sin subrayados rojos.

Por qué se hace: el documento de diseño de APIs REST es el artefacto de docs específico del punto 2.1. No modifica los nueve documentos existentes del punto 1.5.

Errores comunes:

· Nombrar el archivo con otro nombre: rompe la trazabilidad del punto.
· Modificar los ADR existentes: viola la regla de no modificar archivos del punto anterior.
· Guardar el archivo en la raíz del punto en lugar de docs: rompe la estructura del repositorio.

Verificación: el archivo docs\diseno-apis-rest.md existe con las nueve secciones.


---

Paso 5 — Crear la carpeta DisenoRest en el proyecto monolítico

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre el proyecto AceriaApp.Monolito.Api.
Acción 2: Seleccionar Add → New Folder y nombrar la carpeta DisenoRest.
Acción 3: Verificar que la carpeta DisenoRest aparece dentro de AceriaApp.Monolito.Api sin afectar a las carpetas Dominio, Infraestructura, Metricas, Diseno, Organizacion y BuenasPracticas.
Acción 4: Verificar que no se ha modificado ningún archivo existente del punto 1.5.

Por qué se hace: la carpeta DisenoRest albergará las clases de validación de URIs REST. Se crea como carpeta nueva sin tocar las carpetas existentes.

Errores comunes:

· Crear la carpeta dentro de alguna de las carpetas existentes: rompe la separación de responsabilidades.
· Modificar las carpetas existentes: viola la regla de no modificar archivos del punto anterior.
· Crear la carpeta con otro nombre: rompe la convención del curso.

Verificación: la carpeta DisenoRest existe dentro de AceriaApp.Monolito.Api y las carpetas existentes permanecen intactas.


---

Paso 6 — Crear la clase UriRest

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta DisenoRest.
Acción 2: Seleccionar Add → Class y nombrar la clase UriRest.cs.
Acción 3: Escribir exactamente el siguiente código:

namespace AceriaApp.Monolito.Api.DisenoRest;  
  
public class UriRest  
{  
    public string Version { get; init; } = "v1";  
    public string Recurso { get; init; } = string.Empty;  
    public string? Identificador { get; init; }  
    public string? SubRecurso { get; init; }  
  
    public string Construir()  
    {  
        var partes = new List<string> { "api", Version, Recurso };  
        if (!string.IsNullOrEmpty(Identificador))  
        {  
            partes.Add(Identificador);  
        }  
        if (!string.IsNullOrEmpty(SubRecurso))  
        {  
            partes.Add(SubRecurso);  
        }  
        return "/" + string.Join("/", partes);  
    }  
}

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: la clase UriRest modela la construcción de una URI REST a partir de sus partes: versión, recurso, identificador y sub-recurso. Es la base para validar que las URIs del proyecto siguen las reglas de diseño.

Errores comunes:

· Olvidar el namespace: la clase no se resuelve desde otros archivos.
· No inicializar Version con "v1": la versión no se aplica por defecto.
· Usar string en lugar de string? para las propiedades opcionales: el compilador emite advertencias.

Verificación: la clase UriRest compila sin errores y expone cuatro propiedades y un método.


---

Paso 7 — Añadir el using necesario en UriRest

Acción 1: En el panel Solution Explorer, hacer doble clic en UriRest.cs.
Acción 2: Añadir la línea using System.Collections.Generic; al principio del archivo si no está presente.
Acción 3: Verificar que no hay subrayados rojos en List<string>.
Acción 4: Pulsar Ctrl+S para guardar el archivo.

Por qué se hace: el tipo List<string> pertenece a System.Collections.Generic. En proyectos con ImplicitUsings desactivado, hay que añadir el using explícito.

Errores comunes:

· Añadir using System.Linq; en lugar de System.Collections.Generic: no resuelve List<string>.
· Añadir el using después del namespace: el compilador no lo reconoce.
· Olvidar el using y confiar en ImplicitUsings: el proyecto puede tenerlo desactivado.

Verificación: UriRest.cs compila sin errores y no muestra subrayados rojos.


---

Paso 8 — Crear la clase ValidadorUriRest

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta DisenoRest.
Acción 2: Seleccionar Add → Class y nombrar la clase ValidadorUriRest.cs.
Acción 3: Escribir exactamente el siguiente código:

namespace AceriaApp.Monolito.Api.DisenoRest;  
  
public class ValidadorUriRest  
{  
    private static readonly string[] VerbosProhibidos =  
    {  
        "crear", "obtener", "listar", "actualizar", "eliminar",  
        "get", "post", "put", "patch", "delete"  
    };  
  
    public ResultadoUri Validar(string uri)  
    {  
        var errores = new List<string>();  
  
        if (!uri.StartsWith("/api/", StringComparison.Ordinal))  
        {  
            errores.Add("La URI no empieza por '/api/'.");  
        }  
  
        var partes = uri.Trim('/').Split('/');  
        if (partes.Length >= 3 && !partes[1].StartsWith("v", StringComparison.Ordinal))  
        {  
            errores.Add("La URI no incluye versión después de 'api'.");  
        }  
  
        foreach (var verbo in VerbosProhibidos)  
        {  
            if (uri.Contains(verbo, StringComparison.OrdinalIgnoreCase))  
            {  
                errores.Add($"La URI contiene un verbo prohibido: '{verbo}'.");  
            }  
        }  
  
        return new ResultadoUri(errores.Count == 0, errores);  
    }  
}  
  
public record ResultadoUri(bool EsValida, IReadOnlyList<string> Errores);

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: la clase ValidadorUriRest comprueba que una URI sigue las reglas de diseño: empieza por /api/, incluye versión y no contiene verbos prohibidos.

Errores comunes:

· Olvidar el using System.Collections.Generic;: IReadOnlyList<string> y List<string> no se resuelven.
· Olvidar el using System;: StringComparison no se resuelve.
· No usar StringComparison.OrdinalIgnoreCase en la comprobación de verbos: las mayúsculas no se detectan.

Verificación: la clase ValidadorUriRest compila sin errores y expone un método y un record.


---

Paso 9 — Añadir los using necesarios en ValidadorUriRest

Acción 1: En el panel Solution Explorer, hacer doble clic en ValidadorUriRest.cs.
Acción 2: Añadir las líneas using System; y using System.Collections.Generic; al principio del archivo si no están presentes.
Acción 3: Verificar que no hay subrayados rojos en StringComparison ni en IReadOnlyList<string>.
Acción 4: Pulsar Ctrl+S para guardar el archivo.

Por qué se hace: el tipo StringComparison pertenece a System. El tipo IReadOnlyList<string> pertenece a System.Collections.Generic. En proyectos con ImplicitUsings desactivado, hay que añadir los usings explícitos.

Errores comunes:

· Añadir solo uno de los dos usings: los tipos del otro no se resuelven.
· Añadir los usings después del namespace: el compilador no los reconoce.
· Olvidar los usings y confiar en ImplicitUsings: el proyecto puede tenerlo desactivado.

Verificación: ValidadorUriRest.cs compila sin errores y no muestra subrayados rojos.


---

Paso 10 — Crear la clase CatalogoUris

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta DisenoRest.
Acción 2: Seleccionar Add → Class y nombrar la clase CatalogoUris.cs.
Acción 3: Escribir exactamente el siguiente código:

namespace AceriaApp.Monolito.Api.DisenoRest;  
  
public class CatalogoUris  
{  
    private readonly List<string> _uris;  
  
    public CatalogoUris(List<string> uris)  
    {  
        _uris = uris;  
    }  
  
    public IEnumerable<string> UrisValidas(ValidadorUriRest validador)  
    {  
        return _uris.Where(u => validador.Validar(u).EsValida);  
    }  
  
    public IEnumerable<string> UrisInvalidas(ValidadorUriRest validador)  
    {  
        return _uris.Where(u => !validador.Validar(u).EsValida);  
    }  
}

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: la clase CatalogoUris agrupa las URIs del proyecto y permite filtrarlas por validez según el validador.

Errores comunes:

· No inicializar _uris en el constructor: la clase lanza NullReferenceException.
· Olvidar using System.Linq;: Where no se resuelve.
· Devolver List<string> en lugar de IEnumerable<string>: expone la implementación interna.

Verificación: la clase CatalogoUris compila sin errores y expone un constructor y dos métodos.


---

Paso 11 — Añadir el using necesario en CatalogoUris

Acción 1: En el panel Solution Explorer, hacer doble clic en CatalogoUris.cs.
Acción 2: Añadir la línea using System.Linq; al principio del archivo si no está presente.
Acción 3: Verificar que no hay subrayados rojos en Where.
Acción 4: Pulsar Ctrl+S para guardar el archivo.

Por qué se hace: el método Where pertenece a System.Linq. En proyectos con ImplicitUsings desactivado, hay que añadir el using explícito.

Errores comunes:

· Añadir using System.Collections.Generic; en lugar de System.Linq: no resuelve Where.
· Añadir el using después del namespace: el compilador no lo reconoce.
· Olvidar el using y confiar en ImplicitUsings: el proyecto puede tenerlo desactivado.

Verificación: CatalogoUris.cs compila sin errores y no muestra subrayados rojos.


---

Paso 12 — Crear el proyecto de tests del punto 2.1

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta tests.
Acción 2: Seleccionar Add → New Project.
Acción 3: Seleccionar la plantilla xUnit Test Project, nombrar el proyecto AceriaApp.DisenoRest.Tests y pulsar Create.
Acción 4: Verificar que el proyecto aparece en la solución y que se ha creado la carpeta tests\AceriaApp.DisenoRest.Tests.

Por qué se hace: el punto 2.1 añade un proyecto de tests específico para las clases de diseño REST. Se crea como proyecto nuevo sin modificar los proyectos de tests existentes.

Errores comunes:

· Crear el proyecto dentro de src en lugar de tests: rompe la estructura.
· Modificar los proyectos de tests del punto 1.5: viola la regla de no modificar archivos del punto anterior.
· Usar dotnet new mstest: el curso usa xUnit.

Verificación: el proyecto AceriaApp.DisenoRest.Tests aparece en la solución y su carpeta existe en tests\AceriaApp.DisenoRest.Tests.


---

