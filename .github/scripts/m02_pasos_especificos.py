"""Guía propia de cada paso: acciones y pruebas que corresponden al código C#."""
# Una entrada por cada paso del 1 al 24; no son textos genéricos intercambiables.
SPECS={
1:[
("Archivo > Nuevo > Proyecto > ASP.NET Core Empty. Selecciona C#, .NET 8 y el nombre AceriaApp.Api. No marques autenticación.","Verifica el TargetFramework net8.0 y arranca el proyecto vacío."),
("Abre Program.cs y localiza CreateBuilder, Build y Run. Ejecuta con F5, observa la dirección del perfil local y detén Kestrel.","Kestrel escucha en el puerto anunciado; no es una prueba de base de datos."),
("Diseña las rutas GET /api/v1/ordenes y GET /api/v1/ordenes/{id:guid}. Explica qué recurso identifica cada una.","Las dos rutas usan sustantivos en plural, y el detalle tiene un Guid."),
("Añade la carpeta Modelo. Crea Orden.cs con Guid Id, Cliente, Material, Cantidad, Estado y FechaCreacion; compara con la clase de referencia.","La clase Orden compila, y el estado inicial es Pendiente."),
("En Orden.cs observa que Id se genera por defecto y FechaCreacion emplea UtcNow. Distingue los datos que proporciona el servidor de los del cliente.","No se reciben el Id ni la fecha desde una petición de creación."),
("En Modelo crea OrdenDto.cs como record público con los datos que va a serializar JSON; no lo conviertas en entidad de EF Core.","El compilador distingue Orden de OrdenDto."),
("Añade a OrdenDto un método estático Desde(Orden x); construye el record usando las propiedades de una orden.","El DTO contiene el mismo Id y datos públicos que la entidad."),
("Desde Administrar paquetes NuGet instala Microsoft.EntityFrameworkCore.SqlServer 8.x en AceriaApp.Api, o utiliza dotnet add package con versión 8.","La compilación reconoce UseSqlServer."),
("Crea Datos/AceriaDbContext.cs; haz que herede de DbContext y declara DbSet<Orden> Ordenes.","Al compilar, el contexto conoce Orden y puede consultarla."),
("En OnModelCreating configura HasKey(Id), las longitudes de Cliente y Material y los campos obligatorios.","El modelo restringe tamaños de columna y reconoce la clave."),
("En appsettings.json añade ConnectionStrings:AceriaApp con (localdb)\\MSSQLLocalDB y Database=AceriaAppM02. No sustituyas LocalDB por SQLite.","La cadena se lee desde Configuration y apunta al servidor local."),
("En Program.cs, antes de builder.Build, añade AddDbContext<AceriaDbContext> con UseSqlServer y GetConnectionString.","El manejador HTTP podrá recibir AceriaDbContext por inyección."),
("En Development crea la base de enseñanza con Database.EnsureCreatedAsync usando un scope; deja escrito que en producción se usarían migraciones.","Al arrancar en Windows aparece la base AceriaAppM02 si LocalDB está instalado."),
("En Program.cs escribe MapGet de /api/v1/ordenes y recibe AceriaDbContext como argumento del lambda.","El endpoint queda registrado y responde a GET."),
("Dentro de MapGet consulta db.Ordenes.AsNoTracking, materializa la lista y aplica OrdenDto.Desde a cada entidad.","La salida expone DTOs y no instancias de la entidad EF Core."),
("Abre AceriaApp.http, ejecuta GET de colección y comprueba el código y el JSON aunque la tabla esté vacía.","La respuesta es 200 y un arreglo JSON; no 404."),
("Añade MapGet /api/v1/ordenes/{id:guid} y recibe Guid id y DbContext inyectado.","La ruta coincide con un identificador Guid válido."),
("Busca mediante FirstOrDefaultAsync y devuelve Results.NotFound cuando la orden no existe; usa Results.Ok cuando aparece.","Un GUID nuevo devuelve 404 sin excepción 500."),
("Envía una ruta con identificador que no es GUID y otra con GUID inexistente; anota qué parte resuelve el enrutador y cuál el manejador.","Comprendes la diferencia entre plantilla que no coincide y recurso ausente."),
("En Visual Studio abre o crea AceriaApp.http, define @Host y dos peticiones GET con la ruta versionada.","Puedes ejecutar ambos GET sin copiar URLs del navegador."),
("Crea un proyecto xUnit AceriaApp.Api.Tests y referencia AceriaApp.Api; instala Microsoft.AspNetCore.Mvc.Testing 8.","Las clases de tests referencian Program de la API."),
("Crea ApiFactory derivada de WebApplicationFactory<Program>; sustituye solo para pruebas el proveedor por EF Core InMemory.","Las pruebas arrancan ASP.NET Core en memoria; la aplicación real conserva LocalDB."),
("Crea GetTests y tres casos: colección 200, GUID inexistente 404, orden insertada recuperada como OrdenDto.","dotnet test ejecuta los tres casos con resultado satisfactorio."),
("Como reto, acepta ?cliente=ACX-001 en el GET de colección y aplica Where solo cuando se recibe cliente; crea un test.","La colección devuelve únicamente órdenes del cliente indicado.")
],
2:[
("Abre la etapa 2.1 ya programada; copia tu solución de trabajo a la carpeta del punto 2.2 y ejecuta los GET existentes.","La lista sigue devolviendo 200 y el detalle inexistente 404."),
("Construye una tabla con GET/POST/PUT/PATCH/DELETE y las URIs de órdenes; anota cuándo será 201, 204, 400, 404, 409 y 422.","La tabla coincide con las rutas que programarás, sin acciones Git."),
("En la carpeta Contratos dibuja qué acepta el cliente y qué genera el servidor. No recibas Orden directamente desde JSON.","Id, Estado y FechaCreacion quedan fuera del contrato de creación."),
("Crea ContratosOrden.cs con CrearOrdenRequest(Cliente, Material, Cantidad) y ActualizarCantidadRequest(Cantidad).","Los dos records compilan y se distinguen del OrdenDto de salida."),
("En Program.cs declara MapPost /api/v1/ordenes con CrearOrdenRequest y AceriaDbContext. Explica cómo se enlaza JSON.","La URL acepta POST con Content-Type application/json."),
("Dentro de POST crea una entidad Orden con los campos del contrato, ejecuta db.Ordenes.Add y SaveChangesAsync.","Una nueva fila queda persistida en LocalDB."),
("Devuelve Results.CreatedAtRoute usando el nombre ObtenerOrdenPorId y el identificador generado.","El resultado es 201 con cabecera Location."),
("Envía POST con ACX-001, CHAPA-3MM y 10; copia el identificador y ejecuta GET de detalle.","GET muestra los mismos valores guardados por POST."),
("En 2.2, antes de introducir FluentValidation, añade un BadRequest provisional ante Cliente o Material vacíos y Cantidad no positiva.","La petición inválida produce 400 y no crea una orden."),
("Rechaza Cantidad superior a 500 por política de capacidad con Results.Problem statusCode 422.","El JSON de capacidad 501 produce 422; se distingue de 400."),
("Declara MapPut /api/v1/ordenes/{id:guid} con Guid, CrearOrdenRequest y AceriaDbContext.","PUT puede buscar un recurso por identificador."),
("En el PUT carga FindAsync(id), devuelve 404 si no existe y sustituye los tres campos editables; SaveChangesAsync.","PUT válido responde 204 y mantiene el mismo Guid."),
("Tras PUT ejecuta GET del mismo recurso y comprueba Cliente, Material y Cantidad nuevos.","La consulta evidencia que el cambio se persistió."),
("Declara MapPatch /api/v1/ordenes/{id:guid}/cantidad con ActualizarCantidadRequest.","PATCH admite un cuerpo que contiene solo Cantidad."),
("Guarda la nueva cantidad y devuelve Results.Ok(OrdenDto.Desde(orden)); consulta después y verifica que Cliente sigue igual.","Se obtiene 200 y no cambian datos no incluidos en el parche."),
("Declara MapDelete /api/v1/ordenes/{id:guid}; usa FindAsync, Remove y SaveChangesAsync.","DELETE existente devuelve 204."),
("Llama GET al recurso recién eliminado y después repite DELETE sobre su Id.","El GET devuelve 404 y el recurso sigue ausente."),
("Declara POST /api/v1/ordenes/{id:guid}/finalizar para establecer Estado=Finalizada y guardar.","La transición devuelve 200 y el DTO indica Finalizada."),
("En PUT y PATCH comprueba Estado=Finalizada antes de modificar y devuelve Problem con 409.","Ninguna modificación se guarda sobre una orden finalizada."),
("En DELETE bloquea también la eliminación de una orden finalizada devolviendo 409.","Un recurso finalizado permanece en la base tras DELETE fallido."),
("Añade EscrituraTests con POST, verifica 201, Location y GET posterior del recurso creado.","El test confirma creación y posterior consulta por HTTP."),
("En el test del ciclo completo ejecuta PUT, PATCH y DELETE, leyendo el DTO después de cada cambio.","Se comprueban 204, 200, 204 y después 404."),
("Añade pruebas de capacidad 501 y conflicto tras finalizar; ejecuta todo el proyecto xUnit.","La batería comprueba las respuestas 422 y 409."),
("Como reto envía dos PUT idénticos y dos DELETE sobre el mismo Guid. Distingue efecto final de código HTTP.","El estado del recurso no se duplica y el segundo DELETE no lo restaura.")
],
3:[
("Abre el proyecto del punto 2.2 y comprueba GET, POST, PUT, PATCH y DELETE antes de modificarlo.","Los tests de escritura siguen pasando."),
("Envía tres cuerpos distintos: JSON roto, cantidad 0 y cantidad 501; anota si debe actuar el framework, el validador o el negocio.","Distingues sintaxis, semántica y regla de capacidad."),
("Instala FluentValidation.DependencyInjectionExtensions compatible con .NET 8 en el proyecto de API.","AbstractValidator y AddValidatorsFromAssemblyContaining se resuelven."),
("Crea Validadores.cs con CrearOrdenValidator y reglas RuleFor de Cliente con NotEmpty y MaximumLength(100).","Un cliente vacío infringe una regla semántica."),
("En ese validador incorpora Material obligatorio y Cantidad InclusiveBetween(1,10000).","La cantidad 0 o 10001 es inválida; 501 cumple el rango."),
("Añade ActualizarCantidadValidator para el request de PATCH y su regla de cantidad.","PATCH comparte el criterio semántico del campo Cantidad."),
("Instancia los validadores en un test sencillo y observa IsValid y Errors con peticiones válidas e inválidas.","Comprendes ValidationResult antes de conectar HTTP."),
("Crea ValidationFilter.cs e implementa IEndpointFilter y su InvokeAsync.","El filtro recibe EndpointFilterInvocationContext y EndpointFilterDelegate."),
("En InvokeAsync usa context.Arguments.OfType<T>().FirstOrDefault para localizar el contrato de la petición.","Un request ausente no provoca NullReferenceException."),
("Invoca ValidateAsync pasando RequestAborted desde HttpContext para respetar cancelaciones.","No continúa una operación que el cliente ha cancelado."),
("Agrupa result.Errors por PropertyName y construye un diccionario string[] de mensajes.","Cada propiedad tiene su colección de errores."),
("Ante fallo devuelve Results.ValidationProblem(errors) sin invocar el manejador siguiente.","La respuesta incluye status 400 y el campo errors."),
("Si IsValid es verdadero retorna await next(context); razona qué sucede al omitirlo.","El endpoint se ejecuta solo cuando la validación pasa."),
("Antes de builder.Build registra los validadores mediante AddValidatorsFromAssemblyContaining<CrearOrdenValidator>().","El filtro puede resolver IValidator<CrearOrdenRequest>."),
("Añade AddEndpointFilter<ValidationFilter<CrearOrdenRequest>>() al MapPost real.","POST con Cliente vacío devuelve 400 en vez de guardar una fila."),
("Añade el mismo filtro de CrearOrdenRequest al MapPut.","PUT inválido no modifica la orden almacenada."),
("Añade AddEndpointFilter<ValidationFilter<ActualizarCantidadRequest>>() al MapPatch.","PATCH con Cantidad=0 devuelve 400."),
("Envía un POST con Material vacío y comprueba código, Content-Type y ausencia de inserción.","El código es 400 y la base permanece sin cambios."),
("Examina el JSON Problem Details y localiza en errors el nombre de la propiedad rechazada.","El cliente puede mostrar el mensaje bajo el campo correcto."),
("Compara un POST de cantidad 10001 con otro de 501 y anota el origen del error.","El primero devuelve 400, el segundo 422."),
("Crea, finaliza e intenta editar una orden: no es un fallo semántico, sino un conflicto de estado.","Se recibe 409 y los datos no cambian."),
("Crea ValidacionHttpTests con peticiones reales para Cliente, Material, Cantidad y política de negocio.","Las respuestas se prueban a través del pipeline completo."),
("Ejecuta los tests GET y de escritura anteriores, además de las nuevas pruebas de validación.","El filtrado no rompe las rutas que ya funcionaban."),
("Reto: incorpora WithMessage a una regla y comprueba desde un test HTTP el texto dentro de errors.","El mensaje devuelto es específico y mantiene status 400.")
],
4:[
("Abre la etapa 2.3 y anota sus rutas, DTOs, estados 200/201/204/400/409/422 antes de documentarla.","La futura documentación reflejará endpoints ya comprobados."),
("Instala Swashbuckle.AspNetCore 6.6.2 para .NET 8 en el proyecto API, no solo en tests.","AddSwaggerGen y UseSwagger están disponibles."),
("Crea Documentacion/DocumentacionExtensions.cs y una clase estática DocumentacionExtensions.","La configuración OpenAPI queda separada de Program.cs."),
("En AddDocumentacion registra AddEndpointsApiExplorer y AddSwaggerGen con opciones.","Los servicios descubren los endpoints Minimal API."),
("Configura SwaggerDoc v1 con título, versión, descripción y contacto de AceriaApp.","La sección info del JSON muestra esos valores."),
("En Program.cs llama builder.Services.AddDocumentacion() antes de builder.Build().","Se registra el generador en el contenedor."),
("En UseDocumentacion coloca UseSwagger y UseSwaggerUI dentro de la condición IsDevelopment.","Swagger no se publica automáticamente en Production."),
("Llama app.UseDocumentacion() después de construir la aplicación y abre /swagger desde Visual Studio.","La interfaz presenta los endpoints del proyecto."),
("Descarga /swagger/v1/swagger.json como texto JSON, no una cadena YAML fabricada.","La petición devuelve 200 y el documento empieza por openapi."),
("Busca las secciones info, paths y components; identifica las rutas de órdenes y sus verbos.","GET, POST, PUT, PATCH y DELETE figuran donde corresponde."),
("En Program.cs examina WithName y WithTags para agrupar los endpoints de órdenes.","Los nombres se utilizan también en CreatedAtRoute."),
("Agrega WithSummary y Produces a los GET y comprueba 200 y 404.","El documento describe la lectura y la ausencia del recurso."),
("Documenta POST con Produces<OrdenDto>(201) y ProducesValidationProblem(400).","Swagger enumera creación y error de contrato."),
("Documenta PUT y PATCH con sus códigos, evitando declarar respuestas inventadas.","La documentación debe coincidir con los Results usados."),
("Documenta DELETE y el conflicto 409 de órdenes finalizadas.","El consumidor puede anticipar una eliminación rechazada."),
("Crea EjemploCrearOrden : ISchemaFilter y asigna OpenApiObject para los tres campos del request.","El esquema contiene cliente, material y cantidad ilustrativos."),
("En JSON comprueba components.schemas.CrearOrdenRequest.example y explica que no son datos persistidos.","El ejemplo aparece en la sección reusable de esquemas."),
("En Swagger UI utiliza Try it out para enviar POST de orden y observar 201 y Location.","Se crea un recurso de verdad desde el explorador HTTP."),
("Copia el GUID obtenido y ejecuta GET de detalle desde la UI.","GET responde 200 con el DTO de la misma orden."),
("En ContratoOpenApiTests, usa WebApplicationFactory para solicitar el JSON real.","El test descarga la respuesta del servidor y la analiza."),
("Comprueba info.version y rutas de paths con operaciones get y post.","Un cambio de ruta erróneo hace fallar el contrato."),
("Agrega un test que compruebe CrearOrdenRequest y su propiedad example en components.schemas.","El esquema se genera a partir del contrato público."),
("Ejecuta el test en Environment Production y solicita /swagger/v1/swagger.json.","El endpoint no se publica y responde 404."),
("Reto: añade un resumen específico a PATCH y comprueba que paths muestra summary actualizado.","Se verifica que el documento evoluciona al modificar el código.")
]
}
def obtener(n,k):return SPECS[n][k-1]

# Los motivos se seleccionan por el comportamiento real que se programa
# (no por una numeración arbitraria de cinco en cinco).
REASON_GROUPS={
1:[
(3,"El programa aún se está preparando: comprobar SDK, arranque y URI antes de introducir persistencia permite aislar errores de herramienta frente a errores de API."),
(7,"La entidad y el DTO cumplen funciones diferentes. La primera modela los datos persistidos y el segundo limita el contrato JSON que puede ver el consumidor."),
(13,"El acceso a datos se configura en infraestructura mediante EF Core y DI. LocalDB es la base efectiva de la API; EnsureCreated se usa solo durante el aprendizaje."),
(20,"El verbo GET no modifica recursos. MapGet recibe dependencias y parámetros, consulta la orden y traduce el resultado a 200 o 404 con DTOs."),
(23,"WebApplicationFactory prueba la aplicación como servidor HTTP: permite distinguir compilación C# de comportamiento observable del enrutamiento y la serialización."),
(24,"El filtrado de la colección conserva la idea de recurso y añade una consulta con parámetros, sin transformar el endpoint en una operación RPC.")
],
2:[
(4,"El diseño de las rutas y los contratos evita recibir propiedades de servidor desde JSON. El resultado público se devuelve mediante OrdenDto, no directamente desde la entidad."),
(8,"El POST crea un recurso y debe confirmar la inserción mediante SaveChangesAsync. CreatedAtRoute devuelve 201 y un enlace Location utilizable mediante GET."),
(10,"Un cuerpo incorrecto es distinto de una regla del negocio. En 2.2 el 400 es provisional; 501 unidades reciben 422 por la capacidad limitada del taller."),
(13,"PUT sustituye los campos editables de una orden existente. Si el Guid no identifica un recurso debe devolver 404, no crear silenciosamente otro."),
(15,"PATCH realiza un cambio parcial de Cantidad y conserva los demás datos. Su resultado debe verificarse con una lectura posterior."),
(17,"DELETE quita un recurso persistido. La consulta posterior puede devolver 404; esa diferencia no impide que la eliminación sea idempotente."),
(20,"La transición Finalizada cambia el estado de negocio. PUT, PATCH y DELETE deben respetarlo y producir 409 si se intenta una operación incompatible."),
(23,"Los tests deben confirmar los efectos de POST, PUT, PATCH, DELETE, la capacidad del taller y el conflicto de estado a través de peticiones HTTP reales."),
(24,"La idempotencia habla del efecto final: repetir PUT no multiplica los recursos, y repetir DELETE no restaura lo eliminado. Las respuestas HTTP pueden diferir.")
],
3:[
(3,"La deserialización de un cuerpo JSON y la validación semántica no son lo mismo. Primero el framework interpreta el mensaje y después se comprueban las reglas de datos."),
(7,"FluentValidation expresa reglas sobre los contratos de entrada y devuelve errores por campo; no debe confundirse un record con el validador que lo inspecciona."),
(13,"El filtro ejecuta ValidateAsync antes del manejador y utiliza Results.ValidationProblem si falla; solo invoca next(context) cuando la petición es válida."),
(17,"El registro de validadores en DI no ejecuta la validación. AddEndpointFilter debe asociarse a cada POST, PUT o PATCH que acepte ese contrato."),
(21,"Un 400 por datos fuera del rango, un 422 por la capacidad y un 409 por el estado de una orden pertenecen a causas diferentes que el cliente debe distinguir."),
(24,"Las pruebas HTTP recorren el pipeline completo y comprueban que los fallos se comunican como Problem Details sin alterar los datos.")
],
4:[
(5,"Swashbuckle descubre la API real desde ASP.NET Core: registrar AddSwaggerGen y definir SwaggerDoc produce un documento estándar a partir de rutas y tipos."),
(10,"La publicación de Swagger UI y JSON ocurre después de construir la aplicación y se restringe a Development; la documentación no debe inventarse manualmente."),
(15,"Los metadatos de una operación declaran rutas, respuestas y esquemas; son documentación de un comportamiento que ya fue implementado y probado."),
(19,"Un ejemplo JSON ilustra el contrato de entrada. Swagger UI permite usarlo para enviar una petición real, pero no crea datos hasta ejecutar el endpoint."),
(23,"Descargar el JSON OpenAPI con WebApplicationFactory y comprobar info, paths y schemas es una prueba contractual real; en Production debe respetarse el 404."),
(24,"Cambiar un WithSummary y ver reflejada la modificación en el JSON demuestra la vinculación de la documentación con el código ejecutado.")
]
}
ERROR_GROUPS={
1:["Si falla el inicio, revisa que hayas seleccionado ASP.NET Core Empty y net8.0; no es necesario instalar controladores.",
   "Si no compilan Orden u OrdenDto, comprueba namespaces y tipos. No conviertas la entidad en el contrato JSON.",
   "Si falla UseSqlServer, revisa la dependencia NuGet. Si LocalDB no responde, verifica la instancia MSSQLLocalDB.",
   "Si aparece 404, revisa Guid, la plantilla {id:guid} y la existencia de la orden; en colección vacía corresponde 200.",
   "Si falla ApiFactory, comprueba Program partial y el registro de DbContext con InMemory solo para tests.",
   "Si el filtro no cambia el resultado, revisa el nombre cliente en la query y la condición Where."],
2:["Si el JSON puede cambiar el ID o Estado, el contrato de entrada está exponiendo datos internos; utiliza CrearOrdenRequest.",
   "Si el POST no persiste, verifica SaveChangesAsync; si Location falta, revisa CreatedAtRoute y el nombre de GET.",
   "Si un 501 da 400, la condición provisional está mezclada con la política de capacidad; distingue ambos casos.",
   "Si el PUT no actualiza, revisa FindAsync(id) y SaveChangesAsync. El GUID no debe cambiar.",
   "Si PATCH cambia otros campos, no reasignes Cliente ni Material desde ActualizarCantidadRequest.",
   "Si DELETE devuelve éxito pero GET encuentra la orden, revisa Remove y SaveChangesAsync.",
   "Si una orden finalizada cambia de estado o desaparece, comprueba la condición Estado antes de escribir.",
   "Si una prueba de escritura pasa sin volver a consultar la orden, no ha demostrado persistencia; añade el GET posterior.",
   "Si se crean órdenes duplicadas al repetir PUT, se está usando Add en lugar de actualizar la entidad encontrada."],
3:["Si JSON roto produce un error inesperado, revisa Content-Type y la estructura del cuerpo antes del validador.",
   "Si RuleFor no compila, revisa FluentValidation y el using. Comprueba la diferencia entre NotEmpty y límites numéricos.",
   "Si una petición inválida llega al endpoint, revisa el orden de ejecución y la condición IsValid antes de next(context).",
   "Si se acepta una petición inválida, puede faltar AddEndpointFilter aunque los validadores estén registrados en DI.",
   "Si aparece 500 en vez de 400/422/409, revisa qué capa lanza la excepción y transforma el error de forma adecuada.",
   "Si el test solo instancia un record, no prueba HTTP; usa WebApplicationFactory y examina errors del JSON."],
4:["Si SwaggerGen no se resuelve, revisa la versión de Swashbuckle compatible con .NET 8.",
   "Si /swagger devuelve 404 en Development, comprueba AddDocumentacion y UseDocumentacion y el entorno.",
   "Si falta un código de respuesta, añade Produces/ProducesProblem al endpoint correspondiente sin inventar comportamientos.",
   "Si no aparece example, comprueba SchemaFilter y el tipo CrearOrdenRequest usado en el esquema.",
   "Si el JSON no incluye rutas, comprueba MapGet/MapPost y que las pruebas apuntan al servidor correcto.",
   "Si el summary no cambia, modifica WithSummary en el endpoint real y vuelve a solicitar el documento."]
}
def explicacion_especifica(n,k):
    return next(reason for limit,reason in REASON_GROUPS[n] if k<=limit)
def error_especifico(n,k):
    grupo=next(i for i,(limit,_) in enumerate(REASON_GROUPS[n]) if k<=limit)
    return ERROR_GROUPS[n][grupo]
