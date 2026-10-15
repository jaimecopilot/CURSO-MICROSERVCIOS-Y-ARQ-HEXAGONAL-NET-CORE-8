Punto 2.4 — Documentación mediante OpenAPI (Swagger)

Módulo 2: Desarrollo de APIs REST con ASP.NET Core
Duración: 53 minutos (26 minutos de teoría + 27 minutos de práctica)
Objetivos de aprendizaje:

· Comprender el estándar OpenAPI y su relación con Swagger.
· Comprender la generación automática de documentación a partir del código.
· Comprender la estructura de un documento OpenAPI y sus secciones principales.
· Comprender las anotaciones de metadatos en Minimal API.
· Añadir al proyecto AceriaApp la documentación OpenAPI con metadatos, ejemplos y versionado, y un test unitario que verifique la documentación. Cerrar el módulo 2 con el resumen del estado del proyecto.

---

PARTE TEÓRICA (26 minutos)

Bloque 1 — El estándar OpenAPI

OpenAPI es una especificación para describir APIs REST de forma legible por máquinas y por personas. La especificación define la estructura de un documento que describe los endpoints, los parámetros, los cuerpos de petición, las respuestas y los esquemas de datos. El documento se escribe en JSON o en YAML. La especificación se originó en el proyecto Swagger y fue donada a la OpenAPI Initiative en 2015. La versión actual es la 3.1, aunque la 3.0 sigue siendo la más adoptada. OpenAPI no es un framework ni una biblioteca: es un formato de descripción. Las herramientas que lo consumen pueden generar documentación, clientes, servidores de prueba y tests automáticos.

```text
Estructura de un documento OpenAPI:

openapi: 3.0.3
info:
  title: AceriaApp.Ordenes.Api
  version: v1
paths:
  /api/v1/ordenes:
    get:
      summary: Lista las órdenes
      responses:
        '200':
          description: Lista de órdenes
```

Línea 1: openapi: 3.0.3 → versión de la especificación.
Línea 2: info: → sección de metadatos de la API.
Línea 3: title: AceriaApp.Ordenes.Api → título de la API.
Línea 4: version: v1 → versión del contrato.
Línea 5: paths: → sección de endpoints.
Línea 6: /api/v1/ordenes: → ruta del endpoint.
Línea 7: get: → método HTTP.
Línea 8: summary: Lista las órdenes → resumen del endpoint.
Línea 9: responses: → sección de respuestas.
Línea 10: '200': → código de respuesta.
Línea 11: description: Lista de órdenes → descripción de la respuesta.

Un documento OpenAPI describe la API de forma completa y estructurada. La estructura permite que las herramientas generen documentación interactiva, clientes en distintos lenguajes y pruebas automáticas. La generación automática evita la documentación obsoleta porque el documento se deriva del código. La derivación del código no es automática por defecto: requiere que el código incluya los metadatos necesarios. Los metadatos se añaden con anotaciones, con atributos o con configuración explícita. El curso usa las anotaciones de Minimal API y la configuración de SwaggerGen.

---

Bloque 2 — Swagger y Swagger UI

Swagger es el nombre original del proyecto que dio lugar a OpenAPI. En la práctica, el término Swagger se usa para referirse a tres cosas: el formato de descripción, las herramientas de generación y la interfaz de usuario. La interfaz de usuario se llama Swagger UI y permite explorar la API de forma interactiva. Swagger UI lee el documento OpenAPI generado por el servidor y construye una página web que muestra los endpoints, los parámetros y las respuestas. La página incluye un botón para probar cada endpoint directamente desde el navegador. La combinación de OpenAPI y Swagger UI proporciona documentación viva y ejecutable.

```csharp
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
```

Línea 1: builder.Services.AddEndpointsApiExplorer(); → habilita la exploración de endpoints.
Línea 2: builder.Services.AddSwaggerGen(); → registra el generador de Swagger.
Línea 3: var app = builder.Build(); → construye la aplicación.
Línea 4: if (app.Environment.IsDevelopment()) → solo en desarrollo.
Línea 5: { → abre el bloque.
Línea 6: app.UseSwagger(); → habilita el endpoint del documento OpenAPI.
Línea 7: app.UseSwaggerUI(); → habilita la interfaz gráfica.
Línea 8: } → cierra el bloque.

La configuración de Swagger en ASP.NET Core se realiza en dos fases. La primera fase registra los servicios con AddEndpointsApiExplorer y AddSwaggerGen. La segunda fase habilita los middleware con UseSwagger y UseSwaggerUI. La primera fase se ejecuta antes de builder.Build(). La segunda fase se ejecuta después. La separación entre las dos fases es una consecuencia del modelo de arranque de ASP.NET Core. El curso configura Swagger solo en el entorno de desarrollo para no exponer la documentación en producción.

---

Bloque 3 — Estructura de un documento OpenAPI

Un documento OpenAPI se organiza en secciones. La sección info contiene los metadatos de la API: título, versión, descripción y contacto. La sección servers contiene las URL base de la API. La sección paths contiene los endpoints con sus métodos y parámetros. La sección components contiene los esquemas de datos reutilizables. La sección security contiene los esquemas de autenticación. La sección tags contiene las etiquetas que agrupan los endpoints. Cada sección tiene una estructura definida por la especificación. La estructura es la misma independientemente del lenguaje o del framework que genere el documento.

```yaml
openapi: 3.0.3
info:
  title: AceriaApp.Monolito.Api
  version: v1
  description: API del monolito de referencia.
servers:
  - url: https://localhost:7000
paths:
  /api/v1/ordenes:
    get:
      tags:
        - Ordenes
      summary: Lista las órdenes
      responses:
        '200':
          description: Lista de órdenes
components:
  schemas:
    OrdenDto:
      type: object
      properties:
        id:
          type: string
          format: uuid
        cliente:
          type: string
```

Línea 1: openapi: 3.0.3 → versión de la especificación.
Línea 2: info: → metadatos de la API.
Línea 3: title: AceriaApp.Monolito.Api → título.
Línea 4: version: v1 → versión del contrato.
Línea 5: description: API del monolito de referencia. → descripción.
Línea 6: servers: → URL base de la API.
Línea 7: - url: https://localhost:7000 → URL del servidor.
Línea 8: paths: → endpoints.
Línea 9: /api/v1/ordenes: → ruta del endpoint.
Línea 10: get: → método HTTP.
Línea 11: tags: → etiquetas del endpoint.
Línea 12: - Ordenes → etiqueta del endpoint.
Línea 13: summary: Lista las órdenes → resumen.
Línea 14: responses: → respuestas.
Línea 15: '200': → código de respuesta.
Línea 16: description: Lista de órdenes → descripción de la respuesta.
Línea 17: components: → esquemas reutilizables.
Línea 18: schemas: → esquemas de datos.
Línea 19: OrdenDto: → nombre del esquema.
Línea 20: type: object → tipo del esquema.
Línea 21: properties: → propiedades del esquema.
Línea 22: id: → primera propiedad.
Línea 23: type: string → tipo de la propiedad.
Línea 24: format: uuid → formato de la propiedad.
Línea 25: cliente: → segunda propiedad.
Línea 26: type: string → tipo de la propiedad.

La estructura del documento OpenAPI se organiza de forma jerárquica. La sección paths contiene un objeto por ruta. Cada ruta contiene un objeto por método. Cada método contiene los parámetros, el cuerpo de petición y las respuestas. La sección components contiene los esquemas reutilizables que se referencian desde los endpoints con $ref. La reutilización de esquemas evita la duplicación de definiciones. La estructura jerárquica del documento refleja la estructura de la API y facilita la navegación.

---

Bloque 4 — Anotaciones de metadatos en Minimal API

Minimal API permite añadir metadatos a los endpoints con métodos de extensión. Los métodos más usados son WithName, WithSummary, WithDescription, WithTags, Produces y ProducesProblem. El método WithName asigna un nombre único al endpoint. El método WithSummary añade un resumen corto. El método WithDescription añade una descripción larga. El método WithTags agrupa el endpoint bajo una etiqueta. El método Produces declara el tipo de respuesta. El método ProducesProblem declara el tipo de respuesta de error.

```csharp
app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) =>
    await db.Ordenes.AsNoTracking().ToListAsync())
    .WithName("ListarOrdenes")
    .WithSummary("Lista todas las órdenes")
    .WithDescription("Devuelve la lista completa de órdenes de producción.")
    .WithTags("Ordenes")
    .Produces<List<Orden>>(StatusCodes.Status200OK)
    .ProducesProblem(StatusCodes.Status500InternalServerError);
```

Línea 1: app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) => → declara el endpoint.
Línea 2: await db.Ordenes.AsNoTracking().ToListAsync()) → devuelve la lista.
Línea 3: .WithName("ListarOrdenes") → asigna un nombre único.
Línea 4: .WithSummary("Lista todas las órdenes") → añade un resumen.
Línea 5: .WithDescription("Devuelve la lista completa de órdenes de producción.") → añade una descripción.
Línea 6: .WithTags("Ordenes") → agrupa el endpoint bajo la etiqueta.
Línea 7: .Produces<List<Orden>>(StatusCodes.Status200OK) → declara el tipo de respuesta.
Línea 8: .ProducesProblem(StatusCodes.Status500InternalServerError); → declara el tipo de error.

Las anotaciones tienen dos consecuencias prácticas. La primera es que el documento OpenAPI se genera con metadatos completos. La segunda es que Swagger UI muestra la información en la interfaz. La combinación de ambas mejora la experiencia del consumidor. Las anotaciones se aplican de forma consistente en todos los endpoints. La consistencia es lo que permite que la documentación sea uniforme y predecible.

---

Bloque 5 — Esquemas de datos y DTOs

Los esquemas de datos se derivan de los tipos usados en los endpoints. Un record de respuesta produce un esquema con sus propiedades. Un record de petición produce un esquema con sus propiedades. Los esquemas se incluyen en la sección components del documento OpenAPI. Los endpoints referencian los esquemas con $ref. La referencia evita la duplicación de definiciones. La derivación de esquemas a partir de los tipos requiere que los tipos sean públicos y que sus propiedades sean accesibles. Los tipos anidados se incluyen como esquemas separados.

```csharp
public record OrdenDto(
    Guid Id,
    string Cliente,
    string Material,
    int Cantidad,
    DateTime FechaCreacion);

app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) =>
    await db.Ordenes
        .Select(o => new OrdenDto(o.Id, o.Cliente, o.Material, o.Cantidad, o.FechaCreacion))
        .ToListAsync())
    .Produces<List<OrdenDto>>(StatusCodes.Status200OK);
```

Línea 1: public record OrdenDto( → declara el esquema de respuesta.
Línea 2: Guid Id, → identificador de la orden.
Línea 3: string Cliente, → nombre del cliente.
Línea 4: string Material, → material solicitado.
Línea 5: int Cantidad, → cantidad solicitada.
Línea 6: DateTime FechaCreacion); → fecha de creación.
Línea 7: app.MapGet("/api/v1/ordenes", async (AceriaDbContext db) => → declara el endpoint.
Línea 8: await db.Ordenes → consulta las órdenes.
Línea 9: .Select(o => new OrdenDto(...)) → proyecta la entidad al DTO.
Línea 10: .ToListAsync()) → materializa la lista.
Línea 11: .Produces<List<OrdenDto>>(StatusCodes.Status200OK); → declara el tipo de respuesta.

La derivación de esquemas a partir de los tipos tiene dos consecuencias prácticas. La primera es que el contrato público está documentado de forma exacta. La segunda es que la evolución del contrato se refleja automáticamente en la documentación. La separación entre entidad y DTO del punto 2.1 se mantiene: los esquemas se derivan de los DTOs, no de las entidades. La separación garantiza que la documentación no expone la implementación interna del servicio.

---

Bloque 6 — Ejemplos en la documentación

Los ejemplos en la documentación muestran al consumidor cómo usar la API. Los ejemplos se añaden con anotaciones o con configuración explícita. Un ejemplo puede ser de petición o de respuesta. Un ejemplo de petición muestra el JSON que el cliente debe enviar. Un ejemplo de respuesta muestra el JSON que el servidor devuelve. Los ejemplos facilitan la integración y reducen el tiempo de prueba. La adopción de ejemplos es una buena práctica de documentación.

```yaml
components:
  schemas:
    CrearOrdenRequest:
      type: object
      properties:
        cliente:
          type: string
          example: ACX-001
        material:
          type: string
          example: CHAPA-3MM
        cantidad:
          type: integer
          example: 10
```

Línea 1: components: → sección de esquemas reutilizables.
Línea 2: schemas: → esquemas de datos.
Línea 3: CrearOrdenRequest: → esquema de petición.
Línea 4: type: object → tipo del esquema.
Línea 5: properties: → propiedades del esquema.
Línea 6: cliente: → primera propiedad.
Línea 7: type: string → tipo de la propiedad.
Línea 8: example: ACX-001 → ejemplo del valor.
Línea 9: material: → segunda propiedad.
Línea 10: type: string → tipo de la propiedad.
Línea 11: example: CHAPA-3MM → ejemplo del valor.
Línea 12: cantidad: → tercera propiedad.
Línea 13: type: integer → tipo de la propiedad.
Línea 14: example: 10 → ejemplo del valor.

Los ejemplos tienen dos consecuencias prácticas. La primera es que el consumidor ve cómo se usa la API sin necesidad de leer toda la documentación. La segunda es que las herramientas pueden generar clientes con ejemplos precargados. La adopción de ejemplos es especialmente útil en APIs con contratos complejos. El curso usa ejemplos en los esquemas de petición y de respuesta.

---

Bloque 7 — Versionado de la documentación

La documentación se versiona junto con el contrato. Cada versión del contrato tiene su propio documento OpenAPI. Swagger UI permite seleccionar la versión que se quiere consultar. La selección se realiza con el método SwaggerDoc que registra cada versión. La versión de la documentación coincide con la versión del contrato en la URL. La coincidencia permite que el consumidor consulte la documentación de la versión que usa. El versionado de la documentación es una consecuencia del versionado del contrato.

```csharp
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "AceriaApp.Monolito.Api",
        Version = "v1",
        Description = "API del monolito de referencia."
    });
});

app.UseSwaggerUI(options =>
{
    options.SwaggerEndpoint("/swagger/v1/swagger.json", "AceriaApp.Monolito.Api v1");
});
```

Línea 1: builder.Services.AddSwaggerGen(options => → registra el generador.
Línea 2: { → abre el bloque.
Línea 3: options.SwaggerDoc("v1", new OpenApiInfo → registra la versión v1.
Línea 4: { → abre el bloque de metadatos.
Línea 5: Title = "AceriaApp.Monolito.Api", → título de la API.
Línea 6: Version = "v1", → versión del contrato.
Línea 7: Description = "API del monolito de referencia." → descripción.
Línea 8: }); → cierra el bloque.
Línea 9: }); → cierra la configuración.
Línea 10: app.UseSwaggerUI(options => → configura Swagger UI.
Línea 11: { → abre el bloque.
Línea 12: options.SwaggerEndpoint("/swagger/v1/swagger.json", "AceriaApp.Monolito.Api v1"); → registra el endpoint del documento.
Línea 13: }); → cierra el bloque.

El versionado de la documentación tiene dos consecuencias prácticas. La primera es que el consumidor puede consultar la versión que usa. La segunda es que la documentación de versiones antiguas sigue disponible mientras el contrato antiguo siga activo. La combinación de ambas permite la evolución sin romper a los consumidores. El curso usa el versionado en la URL y en la documentación de forma coherente.

---

Bloque 8 — Documentación de errores y problem details

La documentación incluye los códigos de error y el formato problem details. El método ProducesProblem declara el tipo de error. El método ProducesValidationProblem declara el tipo de error de validación. La documentación muestra los códigos de error esperados para cada endpoint. La inclusión de los errores en la documentación permite al consumidor anticipar las respuestas. La anticipación reduce el tiempo de integración y mejora la experiencia del consumidor.

```csharp
app.MapPost("/api/v1/ordenes", async (CrearOrdenRequest request, AceriaDbContext db) =>
{
    // lógica del endpoint
})
.WithName("CrearOrden")
.WithSummary("Crea una orden")
.Produces<OrdenDto>(StatusCodes.Status201Created)
.ProducesValidationProblem(StatusCodes.Status400BadRequest)
.ProducesProblem(StatusCodes.Status500InternalServerError);
```

Línea 1: app.MapPost("/api/v1/ordenes", async (CrearOrdenRequest request, AceriaDbContext db) => → declara el endpoint POST.
Línea 2: { → abre el cuerpo del lambda.
Línea 3: // lógica del endpoint → comentario del cuerpo.
Línea 4: }) → cierra el lambda.
Línea 5: .WithName("CrearOrden") → asigna un nombre único.
Línea 6: .WithSummary("Crea una orden") → añade un resumen.
Línea 7: .Produces<OrdenDto>(StatusCodes.Status201Created) → declara la respuesta exitosa.
Línea 8: .ProducesValidationProblem(StatusCodes.Status400BadRequest) → declara el error de validación.
Línea 9: .ProducesProblem(StatusCodes.Status500InternalServerError); → declara el error interno.

La documentación de errores tiene dos consecuencias prácticas. La primera es que el consumidor ve los códigos de error esperados. La segunda es que las herramientas pueden generar clientes que manejen cada código de forma específica. La adopción de la documentación de errores es una buena práctica que se aplica de forma uniforme en todos los endpoints. El curso documenta los códigos 400, 404, 409, 422 y 500 según corresponda.

---

Bloque 9 — Herramientas que consumen OpenAPI

El documento OpenAPI lo consumen varias herramientas. Swagger UI lo consume para generar la documentación interactiva. OpenAPI Generator lo consume para generar clientes en distintos lenguajes. Postman lo consume para importar la colección de endpoints. ReDoc lo consume para generar documentación de solo lectura. Las herramientas se integran con el documento sin modificar la API. La integración es posible porque el documento es un formato estándar. La estandarización es la que permite que la documentación se reutilice en múltiples herramientas.

```text
Herramientas que consumen OpenAPI:

Swagger UI           → documentación interactiva.
OpenAPI Generator    → clientes en varios lenguajes.
Postman              → colección de endpoints.
ReDoc                → documentación de solo lectura.
```

Línea 1: Swagger UI → documentación interactiva.
Línea 2: OpenAPI Generator → clientes en varios lenguajes.
Línea 3: Postman → colección de endpoints.
Línea 4: ReDoc → documentación de solo lectura.

La integración con herramientas tiene dos consecuencias prácticas. La primera es que la documentación se reutiliza en distintos contextos. La segunda es que el consumidor elige la herramienta que mejor se adapta a su flujo de trabajo. La combinación de ambas reduce el coste de integración y mejora la experiencia del consumidor. El curso usa Swagger UI como herramienta principal y menciona las demás como opciones.

---

Bloque 10 — Aplicación al proyecto del curso

El proyecto del curso aplica la documentación OpenAPI en todos los endpoints. Los metadatos se añaden con las anotaciones de Minimal API. Los esquemas se derivan de los DTOs. Los ejemplos se añaden en los esquemas de petición. La versión del contrato coincide con la versión de la URL. Los códigos de error se documentan con ProducesProblem y ProducesValidationProblem. La documentación se publica con Swagger UI en el entorno de desarrollo. La documentación se cierra con un test que verifica la generación del documento.

```text
Aplicación al proyecto del curso:

Metadatos        → WithName, WithSummary, WithDescription, WithTags.
Esquemas         → derivados de los DTOs.
Ejemplos         → añadidos en los esquemas de petición.
Versionado       → v1 en URL y en documentación.
Errores          → ProducesProblem y ProducesValidationProblem.
Publicación      → Swagger UI en desarrollo.
Verificación     → test de generación del documento.
```

Línea 1: Metadatos → anotaciones de Minimal API.
Línea 2: Esquemas → derivados de los DTOs.
Línea 3: Ejemplos → añadidos en los esquemas de petición.
Línea 4: Versionado → v1 en URL y en documentación.
Línea 5: Errores → documentados con ProducesProblem y ProducesValidationProblem.
Línea 6: Publicación → Swagger UI en desarrollo.
Línea 7: Verificación → test de generación del documento.

La aplicación de la documentación cierra el módulo 2 y prepara el terreno para el módulo 3. El módulo 3 estudiará la arquitectura hexagonal, que reorganizará el código en capas con puertos y adaptadores. La documentación OpenAPI seguirá generándose a partir de los endpoints, independientemente de la organización interna. El punto 2.4 cierra el módulo 2 con el resumen del estado del proyecto.

---

Resumen rápido de la teoría

· OpenAPI es una especificación para describir APIs REST de forma legible por máquinas y personas.
· Swagger UI lee el documento OpenAPI y construye una interfaz interactiva.
· Un documento OpenAPI se organiza en secciones: info, servers, paths, components, security y tags.
· Minimal API permite añadir metadatos con WithName, WithSummary, WithDescription y WithTags.
· Los esquemas de datos se derivan de los DTOs y se referencian con $ref.
· Los ejemplos en los esquemas facilitan la integración del consumidor.
· El versionado de la documentación coincide con el versionado del contrato en la URL.
· Los errores se documentan con ProducesProblem y ProducesValidationProblem.

---

