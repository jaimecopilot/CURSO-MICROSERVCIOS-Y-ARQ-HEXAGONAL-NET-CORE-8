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

PARTE PRÁCTICA (27 minutos)

Ejercicio: Añadir al punto 2.3 un documento de documentación OpenAPI en docs/, una clase de configuración de metadatos en el proyecto monolítico y un test unitario que verifique la configuración de OpenAPI. Cerrar el módulo 2 con el resumen del estado del proyecto. El punto 2.4 parte del contenido del punto 2.3 sin modificar ningún archivo existente: solo añade archivos nuevos.

Ubicación de trabajo: C:\cursos\AceriaApp\modulo-2-apis-rest-aspnet-core\

---

Paso 1 — Crear la carpeta del punto 2.4 a partir del punto 2.3

Acción 1: Abrir la terminal integrada de Visual Studio 2026 con Ctrl+ñ (o Ctrl+``  en teclados no españoles).
Acción 2: Escribir cd C:\cursos\AceriaApp\modulo-2-apis-rest-aspnet-core y pulsar Enter.
Acción 3: Escribir mkdir 2.4-documentacion-openapi y pulsar Enter.
Acción 4: Escribir xcopy 2.3-validacion-peticiones 2.4-documentacion-openapi /E /I /H /Y y pulsar Enter.
Acción 5: Escribir dir 2.4-documentacion-openapi y pulsar Enter para verificar que se ha copiado el contenido.

Por qué se hace: cada punto del curso parte del contenido del punto anterior. El punto 2.4 se construye sobre el punto 2.3 copiando su contenido y añadiendo archivos nuevos sin modificar los existentes.

Errores comunes:

· Usar copy en lugar de xcopy: copy no copia carpetas de forma recursiva.
· Olvidar el flag /E: no se copian las subcarpetas vacías.
· Olvidar el flag /I: xcopy pregunta si el destino es un directorio cuando no existe.
· Olvidar el flag /Y: xcopy pide confirmación para sobrescribir.

Verificación: al ejecutar dir 2.4-documentacion-openapi, deben aparecer AceriaApp.sln, README.md, src, tests y docs.

---

Paso 2 — Abrir la solución copiada en Visual Studio 2026

Acción 1: Escribir cd 2.4-documentacion-openapi y pulsar Enter.
Acción 2: Escribir start AceriaApp.sln y pulsar Enter.
Acción 3: Verificar que Visual Studio 2026 abre la solución y muestra los proyectos heredados del punto 2.3: AceriaApp.Monolito.Api, AceriaApp.Monolito.Tests, AceriaApp.Metricas.Tests, AceriaApp.Diseno.Tests, AceriaApp.Organizacion.Tests, AceriaApp.BuenasPracticas.Tests, AceriaApp.DisenoRest.Tests, AceriaApp.CatalogoRecursos.Tests y AceriaApp.Validacion.Tests.
Acción 4: Verificar que la solución compila con Ctrl+Shift+B y que la salida muestra Build succeeded..

Por qué se hace: abrir la solución copiada permite trabajar en el punto 2.4 sobre la base del punto 2.3. La compilación verifica que la copia es correcta.

Errores comunes:

· Abrir la solución del punto 2.3 en lugar de la del punto 2.4: los cambios se aplican al punto equivocado.
· No compilar antes de empezar: si la copia tiene errores, los cambios posteriores fallan.
· Tener la API del punto 2.3 en ejecución: el puerto queda ocupado y la compilación falla.

Verificación: Visual Studio 2026 muestra la solución AceriaApp con los nueve proyectos heredados del punto 2.3 y la compilación es correcta.

---

Paso 3 — Verificar que la carpeta docs contiene los documentos del punto 2.3

Acción 1: En el panel Solution Explorer, expandir la carpeta docs del punto 2.4.
Acción 2: Verificar que contiene ADR-001 a ADR-008, analisis-ventajas-inconvenientes.md, principios-diseno.md, organizacion-solucion.md, buenas-practicas.md, diseno-apis-rest.md, catalogo-recursos.md y validacion-peticiones.md.
Acción 3: Verificar que ninguno de los doce documentos se ha modificado.
Acción 4: Verificar que la carpeta docs no contiene ningún archivo nuevo del punto 2.4 todavía.

Por qué se hace: el punto 2.4 parte del contenido del punto 2.3, que ya incluye la carpeta docs con doce documentos. No se modifica ningún documento existente.

Errores comunes:

· Modificar alguno de los ADR o documentos existentes: viola la regla de no modificar archivos del punto anterior.
· Eliminar algún documento existente: pierde la trazabilidad del punto 2.3.
· Crear la carpeta docs si ya existe: mkdir falla.

Verificación: la carpeta docs contiene los doce documentos del punto 2.3 sin modificaciones.

---

Paso 4 — Crear el documento de documentación OpenAPI en docs

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta docs.
Acción 2: Seleccionar Add → New Item → Text File y nombrar el archivo documentacion-openapi.md.
Acción 3: Escribir exactamente el siguiente contenido:

```markdown
# Documentación OpenAPI — Punto 2.4

## Estándar OpenAPI

Especificación para describir APIs REST. Versión 3.0.3.

## Swagger UI

Interfaz gráfica que lee el documento OpenAPI y permite explorar la API.

## Secciones del documento

- `info`: metadatos de la API.
- `servers`: URL base.
- `paths`: endpoints.
- `components`: esquemas reutilizables.
- `security`: esquemas de autenticación.
- `tags`: agrupación de endpoints.

## Anotaciones de Minimal API

- `WithName`: nombre único del endpoint.
- `WithSummary`: resumen corto.
- `WithDescription`: descripción larga.
- `WithTags`: agrupación.
- `Produces`: tipo de respuesta.
- `ProducesProblem`: tipo de error.
- `ProducesValidationProblem`: tipo de error de validación.

## Esquemas

Los esquemas se derivan de los DTOs y se referencian con `$ref`.

## Ejemplos

Los ejemplos se añaden en los esquemas de petición y de respuesta.

## Versionado

La versión de la documentación coincide con la versión del contrato en la URL.

## Herramientas que consumen OpenAPI

- Swagger UI.
- OpenAPI Generator.
- Postman.
- ReDoc.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Metadatos | `WithName`, `WithSummary`, `WithDescription`, `WithTags` |
| Esquemas | Derivados de los DTOs |
| Ejemplos | Añadidos en los esquemas |
| Versionado | v1 en URL y documentación |
| Errores | `ProducesProblem`, `ProducesValidationProblem` |

## Cierre del módulo 2

El proyecto AceriaApp dispone de:

- API Minimal con endpoints REST.
- Recursos identificados con URIs que siguen las cinco reglas.
- Verbos HTTP con semántica correcta.
- Códigos de respuesta adecuados a cada situación.
- Validación de peticiones en tres niveles.
- Documentación OpenAPI con metadatos, esquemas y ejemplos.
- Cuarenta y cuatro pruebas unitarias acumuladas en diez proyectos de tests.
- Nueve puntos completados (1.1 a 1.5 y 2.1 a 2.4).
```

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que el archivo aparece en la carpeta docs sin subrayados rojos.

Por qué se hace: el documento de documentación OpenAPI es el artefacto de docs específico del punto 2.4. Incluye el cierre del módulo 2 con el resumen del estado del proyecto. No modifica los doce documentos existentes del punto 2.3.

Errores comunes:

· Nombrar el archivo con otro nombre: rompe la trazabilidad del punto.
· Modificar los ADR existentes: viola la regla de no modificar archivos del punto anterior.
· Guardar el archivo en la raíz del punto en lugar de docs: rompe la estructura del repositorio.

Verificación: el archivo docs\documentacion-openapi.md existe con las once secciones.

---

Paso 5 — Crear la carpeta Documentacion en el proyecto monolítico

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre el proyecto AceriaApp.Monolito.Api.
Acción 2: Seleccionar Add → New Folder y nombrar la carpeta Documentacion.
Acción 3: Verificar que la carpeta Documentacion aparece dentro de AceriaApp.Monolito.Api sin afectar a las carpetas existentes.
Acción 4: Verificar que no se ha modificado ningún archivo existente del punto 2.3.

Por qué se hace: la carpeta Documentacion albergará las clases de configuración de OpenAPI. Se crea como carpeta nueva sin tocar las carpetas existentes.

Errores comunes:

· Crear la carpeta dentro de alguna de las carpetas existentes: rompe la separación de responsabilidades.
· Modificar las carpetas existentes: viola la regla de no modificar archivos del punto anterior.
· Crear la carpeta con otro nombre: rompe la convención del curso.

Verificación: la carpeta Documentacion existe dentro de AceriaApp.Monolito.Api y las carpetas existentes permanecen intactas.

---

Paso 6 — Crear la clase MetadatosApi

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta Documentacion.
Acción 2: Seleccionar Add → Class y nombrar la clase MetadatosApi.cs.
Acción 3: Escribir exactamente el siguiente código:

```csharp
namespace AceriaApp.Monolito.Api.Documentacion;

public class MetadatosApi
{
    public string Titulo { get; init; } = "AceriaApp.Monolito.Api";
    public string Version { get; init; } = "v1";
    public string Descripcion { get; init; } = "API del monolito de referencia.";
    public string ContactoNombre { get; init; } = "Equipo AceriaApp";
    public string ContactoEmail { get; init; } = "equipo@acería.local";
}
```

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: la clase MetadatosApi modela los metadatos que se usan en la configuración de OpenAPI. Los valores por defecto se aplican al proyecto del curso.

Errores comunes:

· Olvidar el namespace: la clase no se resuelve desde otros archivos.
· No inicializar las propiedades de tipo string: el compilador emite advertencias de nulabilidad.
· Usar set en lugar de init: permite modificar la instancia después de crearla.

Verificación: la clase MetadatosApi compila sin errores y expone cinco propiedades.

---

Paso 7 — Crear la clase ConfiguracionOpenApi

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta Documentacion.
Acción 2: Seleccionar Add → Class y nombrar la clase ConfiguracionOpenApi.cs.
Acción 3: Escribir exactamente el siguiente código:

```csharp
namespace AceriaApp.Monolito.Api.Documentacion;

public class ConfiguracionOpenApi
{
    public MetadatosApi Metadatos { get; init; } = new();
    public bool PublicarSwaggerUI { get; init; } = true;
    public string RutaDocumento { get; init; } = "/swagger/v1/swagger.json";
    public string NombreDocumento { get; init; } = "AceriaApp.Monolito.Api v1";

    public bool EsEntornoDeDesarrollo(string entorno)
    {
        return string.Equals(entorno, "Development", StringComparison.OrdinalIgnoreCase);
    }
}
```

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: la clase ConfiguracionOpenApi agrupa los parámetros de la configuración de OpenAPI y expone un método para comprobar el entorno. Es el punto de entrada para la configuración de la documentación.

Errores comunes:

· Olvidar el using System;: StringComparison no se resuelve.
· No inicializar Metadatos con new(): la clase lanza NullReferenceException.
· Usar == en lugar de string.Equals con StringComparison: la comparación no es robusta.

Verificación: la clase ConfiguracionOpenApi compila sin errores y expone cuatro propiedades y un método.

---

Paso 8 — Añadir el using necesario en ConfiguracionOpenApi

Acción 1: En el panel Solution Explorer, hacer doble clic en ConfiguracionOpenApi.cs.
Acción 2: Añadir la línea using System; al principio del archivo si no está presente.
Acción 3: Verificar que no hay subrayados rojos en StringComparison.
Acción 4: Pulsar Ctrl+S para guardar el archivo.

Por qué se hace: el tipo StringComparison pertenece a System. En proyectos con ImplicitUsings desactivado, hay que añadir el using explícito.

Errores comunes:

· Añadir using System.Text; en lugar de System: no resuelve StringComparison.
· Añadir el using después del namespace: el compilador no lo reconoce.
· Olvidar el using y confiar en ImplicitUsings: el proyecto puede tenerlo desactivado.

Verificación: ConfiguracionOpenApi.cs compila sin errores y no muestra subrayados rojos.

---

Paso 9 — Crear la clase ConstructorDocumentoOpenApi

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta Documentacion.
Acción 2: Seleccionar Add → Class y nombrar la clase ConstructorDocumentoOpenApi.cs.
Acción 3: Escribir exactamente el siguiente código:

```csharp
namespace AceriaApp.Monolito.Api.Documentacion;

public class ConstructorDocumentoOpenApi
{
    public string ConstruirCabecera(MetadatosApi metadatos)
    {
        return $"openapi: 3.0.3\ninfo:\n  title: {metadatos.Titulo}\n  version: {metadatos.Version}\n  description: {metadatos.Descripcion}";
    }

    public string ConstruirRuta(string recurso, string version)
    {
        return $"/api/{version}/{recurso}";
    }
}
```

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: la clase ConstructorDocumentoOpenApi construye la cabecera del documento OpenAPI y las rutas de los recursos. Es la base para verificar que la configuración produce las cadenas esperadas.

Errores comunes:

· Olvidar el namespace: la clase no se resuelve desde otros archivos.
· Usar comillas simples en lugar de dobles en las cadenas interpoladas: el compilador emite error.
· No escapar los saltos de línea: la cabecera no tiene el formato correcto.

Verificación: la clase ConstructorDocumentoOpenApi compila sin errores y expone dos métodos.

---

Paso 10 — Crear el proyecto de tests del punto 2.4

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta tests.
Acción 2: Seleccionar Add → New Project.
Acción 3: Seleccionar la plantilla xUnit Test Project, nombrar el proyecto AceriaApp.Documentacion.Tests y pulsar Create.
Acción 4: Verificar que el proyecto aparece en la solución y que se ha creado la carpeta tests\AceriaApp.Documentacion.Tests.

Por qué se hace: el punto 2.4 añade un proyecto de tests específico para las clases de documentación. Se crea como proyecto nuevo sin modificar los proyectos de tests existentes.

Errores comunes:

· Crear el proyecto dentro de src en lugar de tests: rompe la estructura.
· Modificar los proyectos de tests del punto 2.3: viola la regla de no modificar archivos del punto anterior.
· Usar dotnet new mstest: el curso usa xUnit.

Verificación: el proyecto AceriaApp.Documentacion.Tests aparece en la solución y su carpeta existe en tests\AceriaApp.Documentacion.Tests.

---

Paso 11 — Añadir la referencia del proyecto de tests a la API monolítica

Acción 1: En la terminal, escribir dotnet add tests\AceriaApp.Documentacion.Tests\AceriaApp.Documentacion.Tests.csproj reference src\AceriaApp.Monolito.Api\AceriaApp.Monolito.Api.csproj y pulsar Enter.
Acción 2: Verificar que la salida muestra Reference added successfully.
Acción 3: Verificar que el archivo AceriaApp.Documentacion.Tests.csproj contiene la referencia.

Por qué se hace: la referencia permite que el proyecto de tests acceda a las clases de Documentacion del proyecto monolítico.

Errores comunes:

· Añadir la referencia en dirección inversa: crea una dependencia circular.
· Olvidar el nombre completo del archivo .csproj: el comando falla.
· Ejecutar el comando desde la carpeta equivocada: la ruta relativa no se resuelve.

Verificación: el archivo AceriaApp.Documentacion.Tests.csproj contiene un ProjectReference al proyecto monolítico.

---

Paso 12 — Añadir el paquete FluentAssertions al proyecto de tests

Acción 1: Escribir dotnet add tests\AceriaApp.Documentacion.Tests\AceriaApp.Documentacion.Tests.csproj package FluentAssertions y pulsar Enter.
Acción 2: Escribir dotnet list tests\AceriaApp.Documentacion.Tests\AceriaApp.Documentacion.Tests.csproj package y pulsar Enter.
Acción 3: Verificar que la salida muestra FluentAssertions con su versión.

Por qué se hace: FluentAssertions proporciona la sintaxis de aserción usada en el curso. Se añade al nuevo proyecto de tests sin modificar los proyectos de tests existentes.

Errores comunes:

· Instalar una versión preliminar: el curso usa la última estable.
· Olvidar el paquete: Should() no se resuelve en los tests.
· Añadir el paquete al proyecto equivocado: los tests no compilan.

Verificación: la salida de dotnet list package muestra FluentAssertions con una versión estable.

---

Paso 13 — Crear el archivo MetadatosApiTests.cs

Acción 1: En el panel Solution Explorer, expandir tests → AceriaApp.Documentacion.Tests.
Acción 2: Hacer doble clic en UnitTest1.cs y renombrarlo a MetadatosApiTests.cs.
Acción 3: Escribir exactamente el siguiente código:

```csharp
using AceriaApp.Monolito.Api.Documentacion;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Documentacion.Tests;

public class MetadatosApiTests
{
    [Fact]
    public void MetadatosApi_ConValoresPorDefecto_DevuelveValoresEsperados()
    {
        var metadatos = new MetadatosApi();

        metadatos.Titulo.Should().Be("AceriaApp.Monolito.Api");
        metadatos.Version.Should().Be("v1");
        metadatos.Descripcion.Should().Be("API del monolito de referencia.");
        metadatos.ContactoNombre.Should().Be("Equipo AceriaApp");
        metadatos.ContactoEmail.Should().Be("equipo@acería.local");
    }

    [Fact]
    public void MetadatosApi_ConValoresPersonalizados_DevuelveValoresPersonalizados()
    {
        var metadatos = new MetadatosApi
        {
            Titulo = "AceriaApp.Ordenes.Api",
            Version = "v2",
            Descripcion = "API de órdenes de producción."
        };

        metadatos.Titulo.Should().Be("AceriaApp.Ordenes.Api");
        metadatos.Version.Should().Be("v2");
        metadatos.Descripcion.Should().Be("API de órdenes de producción.");
    }
}
```

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: los tests verifican que la clase MetadatosApi devuelve los valores por defecto esperados y que acepta valores personalizados.

Errores comunes:

· Olvidar el using AceriaApp.Monolito.Api.Documentacion;: la clase no se resuelve.
· Usar Assert.Equal en lugar de Should().Be(): el curso usa FluentAssertions.
· No cubrir el caso de valores personalizados: la inicialización no se verifica.

Verificación: el archivo MetadatosApiTests.cs compila y contiene dos métodos de test.

---

Paso 14 — Crear el archivo ConfiguracionOpenApiTests.cs

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre el proyecto AceriaApp.Documentacion.Tests.
Acción 2: Seleccionar Add → Class y nombrar la clase ConfiguracionOpenApiTests.cs.
Acción 3: Escribir exactamente el siguiente código:

```csharp
using AceriaApp.Monolito.Api.Documentacion;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Documentacion.Tests;

public class ConfiguracionOpenApiTests
{
    private readonly ConfiguracionOpenApi _configuracion = new();

    [Fact]
    public void ConfiguracionOpenApi_ConValoresPorDefecto_DevuelveValoresEsperados()
    {
        _configuracion.PublicarSwaggerUI.Should().BeTrue();
        _configuracion.RutaDocumento.Should().Be("/swagger/v1/swagger.json");
        _configuracion.NombreDocumento.Should().Be("AceriaApp.Monolito.Api v1");
    }

    [Fact]
    public void EsEntornoDeDesarrollo_ConDevelopment_DevuelveTrue()
    {
        _configuracion.EsEntornoDeDesarrollo("Development").Should().BeTrue();
    }

    [Fact]
    public void EsEntornoDeDesarrollo_ConProduction_DevuelveFalse()
    {
        _configuracion.EsEntornoDeDesarrollo("Production").Should().BeFalse();
    }

    [Fact]
    public void EsEntornoDeDesarrollo_IgnoraMayusculas()
    {
        _configuracion.EsEntornoDeDesarrollo("development").Should().BeTrue();
    }
}
```

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: los tests verifican los valores por defecto de la configuración y el comportamiento del método EsEntornoDeDesarrollo con distintos valores de entrada.

Errores comunes:

· Olvidar el using AceriaApp.Monolito.Api.Documentacion;: la clase no se resuelve.
· Usar Assert.True en lugar de Should().BeTrue(): el curso usa FluentAssertions.
· No cubrir el caso de mayúsculas: la comparación robusta no se verifica.

Verificación: el archivo ConfiguracionOpenApiTests.cs compila y contiene cuatro métodos de test.

---

Paso 15 — Crear el archivo ConstructorDocumentoOpenApiTests.cs

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre el proyecto AceriaApp.Documentacion.Tests.
Acción 2: Seleccionar Add → Class y nombrar la clase ConstructorDocumentoOpenApiTests.cs.
Acción 3: Escribir exactamente el siguiente código:

```csharp
using AceriaApp.Monolito.Api.Documentacion;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Documentacion.Tests;

public class ConstructorDocumentoOpenApiTests
{
    private readonly ConstructorDocumentoOpenApi _constructor = new();

    [Fact]
    public void ConstruirCabecera_ConMetadatosPorDefecto_IncluyeTituloYVersion()
    {
        var metadatos = new MetadatosApi();

        var cabecera = _constructor.ConstruirCabecera(metadatos);

        cabecera.Should().Contain("openapi: 3.0.3");
        cabecera.Should().Contain("title: AceriaApp.Monolito.Api");
        cabecera.Should().Contain("version: v1");
    }

    [Fact]
    public void ConstruirRuta_ConRecursoYVersion_DevuelveRutaEsperada()
    {
        var ruta = _constructor.ConstruirRuta("ordenes", "v1");

        ruta.Should().Be("/api/v1/ordenes");
    }

    [Fact]
    public void ConstruirRuta_ConVersionV2_DevuelveRutaConV2()
    {
        var ruta = _constructor.ConstruirRuta("ordenes", "v2");

        ruta.Should().Be("/api/v2/ordenes");
    }
}
```

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: los tests verifican que la cabecera del documento incluye la versión de OpenAPI y los metadatos, y que las rutas se construyen correctamente con la versión del contrato.

Errores comunes:

· Olvidar el using AceriaApp.Monolito.Api.Documentacion;: las clases no se resuelven.
· Usar Assert.Contains en lugar de Should().Contain(): el curso usa FluentAssertions.
· No cubrir el caso de versión v2: el versionado no se verifica.

Verificación: el archivo ConstructorDocumentoOpenApiTests.cs compila y contiene tres métodos de test.

---

Paso 16 — Compilar la solución completa

Acción 1: Escribir dotnet build AceriaApp.sln y pulsar Enter.
Acción 2: Verificar que la salida muestra Build succeeded. y 0 Warning(s), 0 Error(s).
Acción 3: Verificar que el tiempo de compilación es inferior a 240 segundos.

Por qué se hace: compilar la solución completa verifica que todos los proyectos, incluidos los nuevos, se resuelven correctamente.

Errores comunes:

· Tener la API en ejecución: el archivo .dll está bloqueado y la compilación falla.
· No restaurar paquetes: dotnet build restaura por defecto, pero si hay un error de red, hay que ejecutar dotnet restore primero.
· Usar una versión distinta del SDK: dotnet --version debe devolver 8.x.x.

Verificación: la salida debe mostrar Build succeeded. con 0 Error(s).

---

Paso 17 — Ejecutar todos los tests del punto 2.4

Acción 1: Escribir dotnet test tests\AceriaApp.Documentacion.Tests\AceriaApp.Documentacion.Tests.csproj y pulsar Enter.
Acción 2: Verificar que la salida muestra Passed! - Failed: 0, Passed: 9, Skipped: 0.
Acción 3: Verificar que el tiempo total es inferior a 30 segundos.

Por qué se hace: ejecutar los tests del punto 2.4 verifica que las clases de documentación funcionan correctamente.

Errores comunes:

· Ejecutar dotnet test sin especificar el proyecto: ejecuta también los tests de los puntos anteriores, lo que alarga el tiempo.
· No compilar antes: dotnet test compila por defecto, pero si hay errores, los tests no se ejecutan.
· Tener la API en ejecución: el puerto puede estar ocupado.

Verificación: la salida debe mostrar Passed! - Failed: 0, Passed: 9, Skipped: 0, Total: 9.

---

Paso 18 — Ejecutar todos los tests de la solución

Acción 1: Escribir dotnet test AceriaApp.sln --no-build y pulsar Enter.
Acción 2: Verificar que la salida muestra Passed! - Failed: 0, Passed: 51, Skipped: 0.
Acción 3: Verificar que el tiempo total es inferior a 240 segundos.

Por qué se hace: ejecutar todos los tests de la solución verifica que los tests de los puntos anteriores y del punto 2.4 pasan conjuntamente.

Errores comunes:

· No haber compilado antes: --no-build falla si no hay artefactos.
· Tener tests de otros módulos: la solución solo contiene los proyectos de este punto.
· Modificar los tests de los puntos anteriores: viola la regla de no modificar archivos del punto anterior.

Verificación: la salida debe mostrar Passed! - Failed: 0, Passed: 51, Skipped: 0, Total: 51.

---

