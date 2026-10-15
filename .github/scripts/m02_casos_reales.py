"""Ocho casos guiados complementarios: código HTTP real, depuración y resultados."""
CASE_STUDIES={
(1,12):(
"Del navegador hasta una consulta EF Core",
"""Este caso demuestra el trayecto completo de una petición GET antes de añadir pruebas.
Abre §src/AceriaApp.Api/Program.cs§ y coloca un punto de interrupción justo dentro
de §app.MapGet("/api/v1/ordenes", ...)§. Ejecuta la API con F5 usando el perfil
Development y abre §AceriaApp.http§. Envía §GET /api/v1/ordenes§. Cuando Visual Studio
se detenga, inspecciona el argumento §AceriaDbContext db§. No lo ha creado el
cliente HTTP: lo resolvió el contenedor de dependencias a partir de
§AddDbContext§, configurado antes de construir la aplicación.

Continúa paso por paso. §db.Ordenes§ representa la tabla de órdenes;
§AsNoTracking()§ indica que EF Core no va a mantener seguimiento de cambios
en las entidades recuperadas. Esta opción resulta apropiada cuando no se
pretende modificar esas mismas entidades. §OrderBy(x => x.FechaCreacion)§
establece un orden reproducible de presentación, y §ToListAsync§ ejecuta la
consulta. Si no hay filas, el resultado será una lista vacía, que debe
traducirse en un estado 200 con §[]§ en el cuerpo JSON.

La llamada §OrdenDto.Desde§ realiza el límite entre persistencia y
representación. El cliente no recibe una instancia del contexto ni detalles
sobre una tabla; recibe un objeto JSON con los campos públicos de la orden.
La ruta de detalle añade una comprobación: si el Guid es válido pero la
consulta no encuentra ninguna fila, el servidor responde 404. Comprueba
esta situación con el identificador inexistente del archivo HTTP.
Si recibes una excepción de conexión en lugar de 200 o 404, revisa
que LocalDB está instalado y que la cadena de conexión apunta a
§(localdb)\\MSSQLLocalDB§.

**Demostración de aprendizaje:** explica por qué §Results.Ok§ y
§Results.NotFound§ pertenecen al contrato HTTP y no al modelo de dominio.
Cambia temporalmente una ruta en Program.cs y observa cómo deja de coincidir
la petición anterior; restaura el código y vuelve a comprobarlo.
"""),
(1,24):(
"Probar una API de lectura sin depender de una base instalada en CI",
"""Abre el proyecto de pruebas y localiza §ApiFactory.cs§. Esta clase deriva
de §WebApplicationFactory<Program>§ y arranca una aplicación real de
ASP.NET Core en memoria. La aplicación del alumno sigue conectándose a
LocalDB cuando se ejecuta en Windows; exclusivamente dentro de la fábrica
de tests se sustituye el proveedor por EF Core InMemory. Esa decisión
mantiene las pruebas reproducibles y permite que se ejecuten en un runner
Linux, pero no autoriza a utilizar InMemory como sustituto de SQL Server
para verificar todo su comportamiento.

El primer test consulta la colección vacía y espera 200; el segundo
construye un Guid nuevo, lo incorpora a la ruta de detalle y espera 404.
Para comprobar el caso positivo se introduce una entidad Orden en la
base de la prueba, se confirma SaveChangesAsync y después se envía
un GET al mismo identificador. La respuesta se deserializa a OrdenDto.
El test debe contrastar al menos el identificador y uno de los campos,
porque comprobar solamente un 200 no garantiza que haya aparecido la
orden correcta.

Ejecuta desde la terminal integrada §dotnet test§ indicando el proyecto
§tests/AceriaApp.Api.Tests§. Si un test que insertó una entidad recibe
404, revisa que el mismo contexto de la fábrica comparta base y nombre
durante la inserción y el GET. Si el código compila pero el servidor
de pruebas no arranca, comprueba que el programa expone
§public partial class Program§ y que el proyecto de tests referencia
la API.

**Reto de cierre del punto:** escribe una prueba para el filtro opcional
por cliente de la colección. Inserta dos órdenes de clientes diferentes,
haz la consulta con un parámetro §cliente§ y compara los identificadores.
La prueba debe rechazar una implementación que devuelva todas las filas.
"""),
(2,12):(
"Una transacción observable: POST, Location, GET y PUT",
"""El primer recorrido de escritura empieza con el método POST. Ejecuta
la aplicación y abre §AceriaApp.http§. Envía un cuerpo JSON válido:

§§§json
{"cliente":"ACX-001","material":"CHAPA-3MM","cantidad":10}
§§§

Utiliza la URI §/api/v1/ordenes§ y el verbo POST. La operación construye
una entidad nueva de Orden con los datos del contrato. El identificador
y la fecha se asignan en el servidor. Cuando §SaveChangesAsync§ confirma
la inserción, §Results.CreatedAtRoute§ prepara un estado 201 con una
cabecera §Location§. Abre esa cabecera: no es un mensaje decorativo,
sino una ruta que puede usarse después para recuperar la orden.

Envía ahora GET a la URI de §Location§ y comprueba que el JSON contiene
cliente ACX-001, material CHAPA-3MM y cantidad 10. Guarda el Guid obtenido:
lo necesitarás para PUT, PATCH y DELETE. Si GET no encuentra la orden,
pregunta qué base de datos usa cada petición y si el POST realizó
§SaveChangesAsync§. El hecho de que el POST devuelva un cuerpo con un ID
no demuestra por sí solo que se haya insertado una fila.

Para entender PUT, envía a §/api/v1/ordenes/{id}§ un cuerpo con cliente
ACX-002, material CHAPA-5MM y cantidad 14. El endpoint localiza la
orden mediante §FindAsync(id)§, modifica tres propiedades editables
y persiste el cambio. El resultado normal es 204, sin un cuerpo de
respuesta que copiar. Ejecuta un nuevo GET: el Guid debe ser el mismo,
mientras que los tres campos editables reflejan los nuevos valores.

**Comprobación:** compara lo que cambió y lo que permaneció intacto.
El ID, el Estado y la FechaCreacion son valores controlados por el
servidor. Si un PUT crea silenciosamente una orden con un Guid inexistente,
no está cumpliendo el contrato concreto de este ejemplo.
"""),
(2,24):(
"PATCH, eliminación e idempotencia: observar el estado final",
"""Conserva la orden creada en el caso anterior. Ejecuta PATCH sobre
§/api/v1/ordenes/{id}/cantidad§ con el cuerpo:

§§§json
{"cantidad":15}
§§§

Comprueba que el código es 200 y que la representación devuelta contiene
Cantidad=15, Cliente=ACX-002 y Material=CHAPA-5MM. Esto demuestra que
PATCH no ha reconstruido el objeto perdiendo otras propiedades. En
el método C# correspondiente solo se reasigna §orden.Cantidad§;
no se realiza un §new Orden§ ni un §db.Ordenes.Add§.

A continuación ejecuta DELETE con el mismo Guid. El servidor localiza
la orden, ejecuta §Remove§, confirma §SaveChangesAsync§ y devuelve 204.
Envía después GET del mismo identificador: debe producir 404. El recurso
ya no existe, aunque la ruta como plantilla siga registrada en la API.
Si vuelves a ejecutar DELETE, puede responder 404 porque la orden
ya no se encuentra. Esto no contradice la idempotencia de DELETE:
el estado final sigue siendo ausencia del recurso.

Realiza una segunda secuencia para reproducir conflicto de estado.
Crea otra orden, ejecuta POST sobre §/{id}/finalizar§ y después
intenta actualizarla con PUT o PATCH. La operación debe devolver 409
sin modificar los datos. La política del taller comprueba Estado=Finalizada
antes de escribir; el problema no es que el JSON sea inválido, sino
que esa transición ya no está permitida. En otra petición distinta
envía Cantidad=501: aunque el rango de valores del contrato admite
501, la capacidad del taller está limitada a 500 y devuelve 422.

**Reto final:** repite exactamente el mismo PUT sobre una orden pendiente
dos veces. Comprueba que el cliente, material y cantidad quedan iguales.
La idempotencia se entiende observando el efecto final, no contando
solamente códigos 204.
"""),
(3,12):(
"Comprobar que el filtro realmente impide entrar al manejador",
"""Arranca el proyecto 2.3 y abre §ValidationFilter.cs§ y §Program.cs§
al mismo tiempo. Coloca un breakpoint dentro de §InvokeAsync§ y otro
en la primera instrucción del manejador POST que crea la orden.
Prepara una petición con Cliente vacío y los demás campos válidos.
El deserializador de ASP.NET Core construirá CrearOrdenRequest
porque el JSON tiene una estructura compatible; a continuación se
ejecutará el filtro al que se asoció §AddEndpointFilter§.

Inspecciona el valor §request§ en el depurador y observa cómo
§ValidateAsync§ devuelve §IsValid=false§. El filtro agrupa los
§ValidationFailure§ por nombre de propiedad y pasa el diccionario
a §Results.ValidationProblem§. El manejador POST no debe ejecutarse,
ni tampoco debe llamarse §SaveChangesAsync§. La respuesta HTTP
contiene un 400 y un objeto JSON con la propiedad §errors§.

Repite con un cuerpo válido. El filtro volverá a ejecutarse, pero esta
vez §IsValid§ será verdadero y se llamará a §await next(context)§.
El breakpoint del manejador POST debe alcanzarse. La orden se
persiste y el servidor devuelve 201. Esta comparación entre las
dos trazas es la demostración más importante del punto: crear una
clase validadora y registrarla en DI no basta; hay que conectarla
al endpoint que recibe la petición.

Comprueba después PUT y PATCH. El primero utiliza el contrato
CrearOrdenRequest y el segundo ActualizarCantidadRequest. Cada uno
debe utilizar el tipo genérico correcto al añadir el filtro. Un error
común consiste en filtrar solamente POST y creer que todos los
verbos quedan automáticamente protegidos. En ese caso PUT o PATCH
aceptarían datos que POST rechaza.

**Verificación:** enviar Cantidad=0 debe devolver 400 con una entrada
en errors; Cantidad=501 debe producir 422 porque es una regla del negocio.
"""),
(3,24):(
"Del error 400 al 409: tres pruebas con causas diferentes",
"""Para comprobar la separación de responsabilidades, prepara primero
un POST de cantidad 10.001. Es un número entero válido desde el punto
de vista sintáctico, pero infringe la regla §InclusiveBetween(1,10000)§.
Por tanto, FluentValidation genera un error semántico y el filtro
devuelve 400. Inspecciona el campo §errors§: debe identificar Cantidad.
No necesitas consultar SQL Server para determinar que un valor está
fuera de ese intervalo.

Envía después exactamente el mismo cuerpo, cambiando Cantidad a 501.
El validador semántico deja pasar el valor, porque 501 pertenece al
rango de entrada. El manejador POST comprueba entonces la capacidad
del taller y decide responder 422. La decisión podría depender en
el futuro de inventario, estado de las máquinas o política comercial;
por esa razón no es idéntica a una comprobación de formato. Este
es un contrato elegido para el ejercicio, no una regla universal
que obligue a todas las APIs a usar 422.

La tercera prueba necesita un recurso persistido. Crea una orden con
cantidad 10, recupera su Guid, ejecútale §/finalizar§ y después envía
un PUT de modificación. El servidor devuelve 409 porque el recurso
está en un estado incompatible con la modificación. Un 409 no significa
que el tipo §int§ de Cantidad sea inválido: significa que el recurso
existente no admite la operación solicitada.

Escribe pruebas en §ValidacionHttpTests.cs§ que cubran las tres
situaciones. Usa §WebApplicationFactory§ para hacer peticiones HTTP
reales y comprobar el código que recibe un consumidor. La prueba de
400 debe revisar §errors§; las de 422 y 409 comprueban la distinción
de política y estado.

**Control de regresión:** después de añadir filtros, vuelve a ejecutar
GET de lista y detalle. Ninguna regla de validación debería convertir
una lectura válida en un fallo de contrato.
"""),
(4,12):(
"Desde MapGet hasta paths: interpretar Swagger JSON",
"""Inicia la API 2.4 en Development y abre la URL
§http://localhost:5082/swagger/v1/swagger.json§. Este documento no
se guarda a mano en la carpeta docs. Lo produce SwaggerGen cuando
la aplicación solicita información sobre los endpoints de
ASP.NET Core. Busca la propiedad §info§: debe contener el título de
AceriaApp y la versión v1 que registró §SwaggerDoc§.

Continúa con la sección §paths§. Busca §/api/v1/ordenes§ y despliega
sus operaciones §get§ y §post§. Cada operación representa un
manejador declarado mediante MapGet o MapPost. La sección muestra
los tipos de cuerpo de entrada y las respuestas descritas con
§Produces§, §ProducesProblem§ y otros metadatos. Una ruta ausente
en el documento puede indicar que no está registrada, que la
exploración no está configurada o que sus metadatos son incompletos.
No lo arregles escribiendo una ruta ficticia en un YAML separado.

Abre a continuación Swagger UI en §/swagger§. La interfaz interpreta
el JSON y permite visualizar los endpoints agrupados con §WithTags§.
Selecciona GET de colección, ejecuta Try it out y compara el estado
200 con el del archivo HTTP del alumno. Las dos herramientas consumen
la misma API; Swagger UI no proporciona un servidor de ejemplo
independiente.

En §Program.cs§ revisa §WithSummary§ y §Produces§. Añade o corrige
el resumen del GET y vuelve a descargar el JSON: el metadato
cambia porque la fuente de la documentación es el código. Esta
relación bidireccional entre implementar y documentar es precisamente
el aprendizaje del punto 2.4.

**Error habitual:** configurar AddSwaggerGen pero olvidar
§app.UseDocumentacion()§ después de Build. En ese caso los servicios
pueden estar registrados y, sin embargo, /swagger devolver 404.
"""),
(4,24):(
"Contrato de ejemplo y prueba en Production",
"""La sección §components.schemas§ documenta objetos que pueden
reutilizarse desde varias operaciones. Busca §CrearOrdenRequest§.
Debe exponer las propiedades cliente, material y cantidad. El
§SchemaFilter§ §EjemploCrearOrden§ incorpora valores orientativos
para esos campos; no crea ninguna orden. El propósito es ayudar
a quien consume el API a preparar un cuerpo JSON compatible.

Desde Swagger UI abre el POST de órdenes y utiliza Try it out.
Envía un JSON con ACX-001, CHAPA-3MM y cantidad 10; el servidor
debe devolver 201 y Location. Guarda el identificador y solicita
GET de detalle desde la misma interfaz. Si obtienes una respuesta
distinta, revisa el cuerpo, las reglas de validación y la conexión
a la base de datos; no concluyas que el contrato está bien porque
Swagger haya dibujado el formulario.

Para probar la documentación automáticamente, abre
§ContratoOpenApiTests.cs§. La prueba arranca WebApplicationFactory,
solicita el JSON real y analiza sus propiedades con JsonDocument.
Comprueba §info.version§, las rutas de §paths§ y el esquema de
CrearOrdenRequest con su §example§. La prueba debe fallar si el
endpoint POST se elimina sin actualizar el contrato de la API.

Finalmente crea la fábrica de tests con §UseEnvironment("Production")§
y vuelve a solicitar §/swagger/v1/swagger.json§. El método
§UseDocumentacion§ restringe la publicación a Development;
por eso la respuesta esperada es 404. Esta comprobación enseña
a separar la presencia de un paquete de su exposición pública.

**Reto final:** modifica §WithSummary§ de PATCH, arranca de nuevo
y comprueba en el JSON de §paths§ que el resumen se actualizó.
No escribas un documento OpenAPI manual: la prueba debe demostrar
que la documentación sigue derivándose de la implementación.
""")
}
def caso(stage,number):
    title,body=CASE_STUDIES[(stage,number)]
    return f"#### Caso práctico completo — {title}\n\n"+body.replace("§",chr(96))+"\n\n"
