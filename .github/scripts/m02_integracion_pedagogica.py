#!/usr/bin/env python3
"""M02: integración pedagógica de las fuentes originales y código verificado.

Teoría: reconstruye desde las CUATRO fuentes originales, conserva los 40 bloques
y ocho figuras, amplía dentro de cada punto con ASP.NET Core 8.
Prácticas: 96 pasos NUEVOS de diseño-programación-prueba, sin Git ni trámites.
Requiere las cuatro soluciones REST probadas en PROYECTO/.
No cambia fuentes-originales, M01 ni módulos posteriores.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path
from m02_pasos_especificos import obtener as paso_especifico, explicacion_especifica, error_especifico

MODULE=Path("M02_APIS_REST_ASPNET_CORE")
NAMES=["2.1-diseno-apis-rest","2.2-recursos-verbos-codigos",
       "2.3-validacion-peticiones","2.4-documentacion-openapi"]
TITLES=["Del diseño REST a los primeros endpoints GET",
        "Recursos, verbos, persistencia y respuestas HTTP",
        "Validación efectiva de peticiones con FluentValidation",
        "Documento OpenAPI generado y comprobado con Swagger"]
# Cinco núcleos por punto enlazan la fuente teórica a la implementación,
# y las 40 lecciones originales permanecen en el mismo orden.
LESSONS=[
[
("Recurso y representación","Modelo/Orden.cs","Orden",
 "REST identifica órdenes mediante una URI estable. ASP.NET Core no pide implementar un validador de cadenas para disponer de enrutamiento: la llamada MapGet asocia un verbo y una plantilla de ruta al manejador real. Hay que distinguir la entidad Orden, que EF Core persiste, de la representación pública que recibe el consumidor. Conocer los atributos Id, Cliente, Material, Cantidad, Estado y FechaCreacion permite justificar después por qué no todos se aceptan como entrada."),
("DTO público","Modelo/OrdenDto.cs","OrdenDto",
 "El record OrdenDto representa el JSON de salida. El método Desde transforma explícitamente la entidad a una representación. Esta distinción reduce el acoplamiento entre el esquema de la tabla y el contrato HTTP. Si se cambiara una propiedad interna de Orden no tendría por qué aparecer automáticamente en la respuesta; el método de conversión es precisamente el lugar donde decidir qué se publica."),
("Persistencia mediante EF Core","Datos/AceriaDbContext.cs","AceriaDbContext",
 "El contexto contiene DbSet<Orden> y las restricciones de las columnas. La API se ejecuta sobre SQL Server Express LocalDB en el ordenador del alumno. Registrar AddDbContext permite que los endpoints reciban el contexto mediante inyección de dependencias: no hay que crear el contexto con new dentro de cada manejador. En tests se sustituye solamente el proveedor por InMemory para evitar depender de Windows."),
("Endpoint GET de colección","Program.cs","MapGet",
 "El manejador obtiene AceriaDbContext, usa AsNoTracking para consultar sin seguimiento y devuelve Results.Ok con una secuencia de DTOs. En una colección vacía se responde 200 y una lista JSON vacía, pues la colección como recurso existe aunque no contenga elementos. La respuesta debe inspeccionarse desde AceriaApp.http, no deducirse de que el código compile."),
("GET individual y pruebas HTTP","Program.cs","ObtenerOrdenPorId",
 "La plantilla {id:guid} restringe el parámetro de ruta a GUID válidos. El manejador consulta una orden específica y decide entre Results.Ok y Results.NotFound. Una petición a un GUID inexistente no debería convertirse en 500 ni en una respuesta 200 con contenido vacío. WebApplicationFactory inicia la aplicación en memoria y permite comprobar 200 y 404 sobre los endpoints auténticos.")
],
[
("Contrato de entrada","Contratos/ContratosOrden.cs","CrearOrdenRequest",
 "El servidor debe recibir solamente Cliente, Material y Cantidad en CrearOrdenRequest. El ID, el Estado y la FechaCreacion pertenecen al control interno del servicio. Por eso no reutilizamos Orden como cuerpo de entrada. Este diseño protege el contrato público y delimita claramente los datos que el cliente puede modificar."),
("POST y creación","Program.cs","MapPost",
 "MapPost convierte un cuerpo JSON en CrearOrdenRequest. Al construir Orden y añadirla al DbContext todavía no se ha confirmado una inserción; SaveChangesAsync ejecuta la escritura. CreatedAtRoute utiliza el nombre ObtenerOrdenPorId para incluir un vínculo al recurso y devolver 201 Created. En prácticas se enviará POST y se seguirá Location con GET para demostrar persistencia real."),
("PUT y sustitución","Program.cs","MapPut",
 "El ejemplo PUT reemplaza los campos editables de una orden ya existente, conservando los valores que controla el servidor. No debe inventar una nueva orden cuando el identificador no existe: en nuestro contrato responde 404. Cuando una orden ya está finalizada la regla del dominio impide editarla y se comunica un conflicto 409."),
("PATCH especializado","Program.cs","MapPatch",
 "El endpoint PATCH de este curso cambia exclusivamente Cantidad. La elección de una ruta especializada para ese campo evita introducir JSON Patch en un módulo introductorio. El alumno comprobará que Cliente y Material no cambian después de aplicar la modificación parcial."),
("DELETE, estado e idempotencia","Program.cs","MapDelete",
 "DELETE busca el recurso y ejecuta Remove y SaveChangesAsync. La primera eliminación devuelve 204; la consulta posterior devuelve 404. La idempotencia describe el estado final del sistema, no la obligación de devolver exactamente el mismo código en peticiones repetidas. Para reproducir 409 se añade la transición POST finalizar y se intenta editar una orden cuyo estado ya no permite modificaciones.")
],
[
("Niveles de validación","Validacion/Validadores.cs","RuleFor",
 "ASP.NET Core comprueba aspectos de la deserialización del JSON, FluentValidation aplica reglas semánticas y el manejador aplica decisiones del dominio. Un cuerpo con cantidad 0 falla la semántica; cantidad 501 satisface el rango del contrato pero supera el límite de negocio de 500. El objetivo es demostrar por qué el primer caso produce 400 y el segundo 422."),
("Validador semántico","Validacion/Validadores.cs","CrearOrdenValidator",
 "CrearOrdenValidator deriva de AbstractValidator y declara reglas NotEmpty, MaximumLength e InclusiveBetween. El validador es código C# ejecutable, no una anotación narrativa. Permite reutilizar reglas en POST y PUT y establecer pruebas de frontera cuando la cantidad es 0, 1, 500, 501 y 10001."),
("Filtro de endpoint","Validacion/ValidationFilter.cs","InvokeAsync",
 "ValidationFilter recibe el argumento de la petición, ejecuta ValidateAsync y agrupa errores por propiedad. Si hay fallos devuelve Results.ValidationProblem con el campo errors; solo cuando IsValid es verdadero continúa mediante next(context). Omitir esa condición permitiría procesar datos rechazados."),
("Registrar no es ejecutar","Program.cs","AddEndpointFilter",
 "AddValidatorsFromAssemblyContaining registra servicios en el contenedor, pero no aplica reglas de manera automática a un endpoint. Para ejecutar la validación se utiliza AddEndpointFilter en POST, PUT y PATCH con el contrato correspondiente. Los tests deben comprobar el comportamiento HTTP, no limitarse a instanciar un validador."),
("Problem Details y conflictos","Program.cs","Results.Problem",
 "Un error de validación 400 debe ofrecer mensajes por propiedad. Una capacidad de taller incumplida se documenta en el contrato como 422. Intentar modificar una orden finalizada genera un 409 porque depende del estado persistido. La diferencia permite a los clientes automatizar el tratamiento de errores.")
],
[
("Generación real","Documentacion/DocumentacionExtensions.cs","AddSwaggerGen",
 "OpenAPI no es una cadena YAML fabricada para satisfacer un test superficial. Swashbuckle descubre los endpoints realmente declarados en ASP.NET Core y genera el documento JSON. AddEndpointsApiExplorer registra la exploración de rutas y SwaggerDoc aporta metadatos de la versión v1."),
("Conexión en Program.cs","Program.cs","AddDocumentacion",
 "La aplicación debe ejecutar AddDocumentacion antes de builder.Build y UseDocumentacion después. El primer método registra servicios y el segundo habilita el middleware. Definir una clase de extensión que nunca se invoca en Program.cs no documenta nada."),
("Metadatos y códigos","Program.cs","Produces",
 "WithName, WithSummary, WithTags, Produces, ProducesProblem y ProducesValidationProblem describen operaciones reales. Declarar que un endpoint puede devolver 400 no hace que valide: la validación efectiva ya se incorporó en 2.3. La documentación debe corresponder a lo que el runtime responde."),
("Ejemplos y contratos","Documentacion/DocumentacionExtensions.cs","EjemploCrearOrden",
 "SchemaFilter permite mostrar en components.schemas un ejemplo de CrearOrdenRequest con cliente, material y cantidad. El ejemplo no crea una fila en SQL Server; explica el cuerpo que puede enviar el consumidor. El DTO de salida, en cambio, describe la representación de una orden ya existente."),
("Comprobar OpenAPI por HTTP","Program.cs","UseDocumentacion",
 "Swagger UI facilita explorar las operaciones y ejecutarlas desde el navegador. WebApplicationFactory descarga /swagger/v1/swagger.json y contrasta versión, paths y schemas. Otra prueba establece Production y exige que el endpoint de documentación no se publique. Así se comprueba el documento generado y no una cadena aislada del servidor.")
]
]
# Son 24 ejercicios concretos por punto, con una progresión ejecutable.
# Los pasos de los originales se han reemplazado por programación y pruebas;
# la materia conceptual original permanece en los 40 bloques de teoría.
PRACTICE_TITLES=[
[
"Crear el proyecto ASP.NET Core Empty desde Visual Studio",
"Explorar Program.cs, Kestrel y el perfil de arranque",
"Dibujar los recursos y decidir las dos URIs GET",
"Crear carpeta Modelo y entidad Orden",
"Explicar ID Guid, Estado y FechaCreacion de la entidad",
"Crear OrdenDto como contrato de salida",
"Programar la conversión OrdenDto.Desde",
"Instalar EF Core 8 para SQL Server",
"Crear AceriaDbContext y DbSet<Orden>",
"Configurar OnModelCreating, clave y longitudes",
"Configurar la cadena de conexión a LocalDB",
"Registrar AceriaDbContext mediante AddDbContext",
"Crear la base didáctica solo en Development",
"Escribir el endpoint GET de colección",
"Utilizar AsNoTracking y proyectar a DTO",
"Ejecutar GET y verificar 200 con lista vacía",
"Escribir el GET individual con {id:guid}",
"Devolver NotFound cuando no existe la orden",
"Comprobar diferencias entre ruta incorrecta y recurso ausente",
"Crear AceriaApp.http y enviar peticiones desde Visual Studio",
"Crear el proyecto xUnit de pruebas HTTP",
"Configurar WebApplicationFactory y base aislada para tests",
"Probar 200, 404 y DTO mediante GetTests",
"Reto: incorporar consulta por cliente y explicar su URI"
],
[
"Recuperar el estado GET funcional sin modificarlo",
"Diseñar la tabla verbo, URI, petición y respuesta",
"Separar contrato de entrada y DTO de salida",
"Crear CrearOrdenRequest y ActualizarCantidadRequest",
"Programar MapPost y recibir JSON de una orden",
"Persistir la orden con Add y SaveChangesAsync",
"Devolver 201 y Location con CreatedAtRoute",
"Enviar POST y consultar por GET la orden creada",
"Rechazar provisionalmente peticiones sin datos",
"Comprobar la política del taller y respuesta 422",
"Programar MapPut con identificador Guid",
"Modificar Cliente, Material y Cantidad con PUT",
"Comprobar 204 y consultar por GET los cambios",
"Programar MapPatch para cambiar solo Cantidad",
"Comprobar que PATCH no modifica los demás campos",
"Programar MapDelete para eliminar una orden",
"Verificar 204 seguido de GET 404",
"Programar la transición de estado finalizar",
"Bloquear PUT y PATCH para órdenes finalizadas",
"Bloquear DELETE y devolver conflicto 409",
"Escribir pruebas HTTP POST y Location",
"Escribir pruebas HTTP PUT, PATCH y DELETE",
"Probar automáticamente 422 y 409",
"Reto: comprobar idempotencia y efecto persistente"
],
[
"Comprobar endpoints anteriores y localizar sus contratos",
"Distinguir JSON incorrecto, semántica y negocio",
"Instalar FluentValidation.DependencyInjectionExtensions",
"Crear CrearOrdenValidator y reglas de Cliente",
"Definir Material y rango válido de Cantidad",
"Crear ActualizarCantidadValidator para PATCH",
"Ejecutar validadores y estudiar ValidationResult",
"Crear ValidationFilter genérico de Minimal API",
"Obtener la petición de EndpointFilterInvocationContext",
"Ejecutar ValidateAsync y respetar RequestAborted",
"Agrupar errores por campo con LINQ",
"Responder mediante Results.ValidationProblem",
"Permitir next(context) solo cuando IsValid",
"Registrar validadores en el contenedor DI",
"Conectar filtro de CrearOrdenRequest al POST",
"Conectar filtro de CrearOrdenRequest al PUT",
"Conectar filtro de ActualizarCantidadRequest al PATCH",
"Enviar POST incorrecto y comprobar status 400",
"Inspeccionar la propiedad errors del Problem Details",
"Probar límite 10001 frente a la capacidad 501",
"Reproducir 409 con orden ya finalizada",
"Crear pruebas de validación mediante HTTP",
"Verificar que los GET siguen sin regresiones",
"Reto: personalizar mensajes y comprobar errores"
],
[
"Comprobar el contrato REST que se va a documentar",
"Instalar Swashbuckle.AspNetCore compatible con .NET 8",
"Crear carpeta Documentacion y extensiones de configuración",
"Registrar AddEndpointsApiExplorer y AddSwaggerGen",
"Configurar SwaggerDoc con información y versión v1",
"Conectar AddDocumentacion en Program.cs",
"Configurar UseSwagger y Swagger UI en Development",
"Conectar UseDocumentacion y abrir /swagger",
"Descargar el JSON real /swagger/v1/swagger.json",
"Identificar info, paths, components y schemas",
"Aplicar WithName y WithTags a los endpoints",
"Documentar GET con WithSummary y Produces",
"Documentar POST con 201 y ValidationProblem 400",
"Documentar PUT y PATCH con códigos alternativos",
"Documentar DELETE y el conflicto 409",
"Crear SchemaFilter EjemploCrearOrden",
"Inspeccionar example de CrearOrdenRequest en Swagger",
"Ejecutar un POST desde Swagger UI",
"Consultar la orden creada desde la propia UI",
"Crear tests HTTP del documento OpenAPI real",
"Comprobar rutas GET y POST en paths",
"Comprobar schema y ejemplo de petición",
"Comprobar que Production responde 404 para Swagger",
"Reto: documentar PATCH y verificar su summary en JSON"
]
]
FILE_BY_POINT=[
["src/AceriaApp.Api/Modelo/Orden.cs","src/AceriaApp.Api/Modelo/OrdenDto.cs",
 "src/AceriaApp.Api/Datos/AceriaDbContext.cs","src/AceriaApp.Api/Program.cs",
 "tests/AceriaApp.Api.Tests/ApiFactory.cs",
 "tests/AceriaApp.Api.Tests/GetTests.cs"],
["src/AceriaApp.Api/Contratos/ContratosOrden.cs","src/AceriaApp.Api/Program.cs",
 "tests/AceriaApp.Api.Tests/EscrituraTests.cs"],
["src/AceriaApp.Api/Validacion/Validadores.cs",
 "src/AceriaApp.Api/Validacion/ValidationFilter.cs",
 "src/AceriaApp.Api/Program.cs","tests/AceriaApp.Api.Tests/ValidacionHttpTests.cs"],
["src/AceriaApp.Api/Documentacion/DocumentacionExtensions.cs",
 "src/AceriaApp.Api/Program.cs","tests/AceriaApp.Api.Tests/ContratoOpenApiTests.cs"]
]
CODE_STEPS=[
{4:0,6:1,7:1,9:2,12:3,14:3,17:3,21:4,22:4,23:5},
{4:0,5:1,7:1,11:1,14:1,16:1,18:1,21:2,22:2},
{4:0,6:0,8:1,11:1,14:2,15:2,17:2,22:3},
{3:0,4:0,6:1,8:1,12:1,16:0,20:2}
]
RESPONSE_HINT=[
["GET /api/v1/ordenes → 200 + JSON","GET /api/v1/ordenes/{id} → 200 / 404"],
["POST /api/v1/ordenes → 201 + Location","PUT /{id} → 204",
 "PATCH /{id}/cantidad → 200","DELETE /{id} → 204 / 404",
 "POST /{id}/finalizar → 200 / 409","Cantidad 501 → 422"],
["Cliente vacío → 400 + errors","Cantidad 10001 → 400 + errors",
 "Cantidad 501 → 422","Orden finalizada → 409"],
["GET /swagger/v1/swagger.json → 200 en Development",
 "info.version → v1","paths contiene GET y POST → Rutas descubiertas","schemas contiene CrearOrdenRequest → Contrato registrado",
 "GET /swagger/v1/swagger.json → 404 en Production"]
]
def read(stage:int,relative:str):
    return (MODULE/"PROYECTO"/NAMES[stage-1]/relative).read_text(encoding="utf-8").strip()
def fenced(value:str,lang="csharp"):
    return "\n\n"+chr(96)*3+lang+"\n"+value.rstrip()+"\n"+chr(96)*3+"\n\n"
def code_excerpt(stage:int,index:int,step:int|None=None):
    p=FILE_BY_POINT[stage-1][index]
    v=read(stage,p)
    if p.endswith("Program.cs"):
        lines=v.splitlines()
        targets={
            1:{12:"2.1.7",14:"2.1.8",17:"2.1.9"},
            2:{5:"2.2.5",7:"2.2.5",11:"2.2.7",14:"2.2.8",
               16:"2.2.9",18:"2.2.10"},
            3:{14:"REGISTRO_VALIDACION",15:"FILTRO_POST",17:"FILTRO_PATCH"},
            4:{6:"REGISTRO_OPENAPI",8:"PUBLICACION_OPENAPI",12:"ANOTACIONES_GET"},
        }
        key=targets.get(stage,{}).get(step,"2.1.8")
        if key=="REGISTRO_VALIDACION":
            return p,"using FluentValidation;\n"+next(l for l in lines if "AddValidatorsFromAssemblyContaining" in l).strip()
        if key=="FILTRO_POST":
            at=next(i for i,l in enumerate(lines) if 'WithName("CrearOrden")' in l)
            return p,"\n".join(lines[at:at+4])
        if key=="FILTRO_PATCH":
            at=next(i for i,l in enumerate(lines) if 'WithName("CambiarCantidad")' in l)
            return p,"\n".join(lines[at:at+4])
        if key=="REGISTRO_OPENAPI":
            return p,next(l.strip() for l in lines if "builder.Services.AddDocumentacion()" in l)
        if key=="PUBLICACION_OPENAPI":
            return p,next(l.strip() for l in lines if "app.UseDocumentacion()" in l)
        if key=="ANOTACIONES_GET":
            at=next(i for i,l in enumerate(lines) if 'WithName("ListarOrdenes")' in l)
            return p,"\n".join(lines[at:at+3])
        starts=[i for i,l in enumerate(lines) if "INICIO PASO "+key in l]
        if starts:
            a=starts[0]
            b=next((i for i in range(a+1,len(lines)) if "INICIO PASO" in lines[i]),len(lines))
            return p,"\n".join(lines[a:b]).strip()
    return p,v
def enrich_theory(base:str):
    sections=re.split(r"(?=^## Punto 2\.[1-4] —)",base,flags=re.M)
    if len(sections)!=5:raise ValueError("No se encuentran los cuatro puntos de teoría")
    out=sections[0].replace("# M02 — Teoría de desarrollo de APIs REST",
        "# M02 — Teoría completa: diseño REST e implementación con ASP.NET Core 8",1)
    for stage,part in enumerate(sections[1:],1):
        blocks=re.split(r"(?=^### Bloque \d+ —)",part,flags=re.M)
        if len(blocks)!=11:raise ValueError(f"El punto 2.{stage} tiene {len(blocks)-1} bloques")
        out+=blocks[0]
        for n,bl in enumerate(blocks[1:],1):
            out+=bl
            if n in (2,4,6,8,10):
                topic,relative,search,explain=LESSONS[stage-1][(n//2)-1]
                out+=f"\n\n#### Del concepto a ASP.NET Core 8: {topic}\n\n"
                out+=explain+"\n\n"
                out+="**Aplicación en el proyecto real.** "
                out+=f"Este comportamiento está materializado en §{relative}§ del "
                out+=f"estado §{NAMES[stage-1]}§. Busca la instrucción §{search}§ "
                out+="y sigue su ejecución con un punto de interrupción. "
                out+="En las prácticas no se pedirá únicamente crear una clase: "
                out+="el alumno construirá el recurso, enviará la petición y observará "
                out+="el código HTTP y, cuando proceda, la escritura en SQL Server Express LocalDB.\n\n"
                # 2 códigos completos por punto, los demás con referencia,
                # evitando reproducir Program.cs muchas veces.
                if n in (4,8):
                    examples={
                        (1,4):(1,None),(1,8):(3,14),
                        (2,4):(1,5),(2,8):(1,14),
                        (3,4):(0,None),(3,8):(1,None),
                        (4,4):(0,None),(4,8):(1,12)
                    }
                    pos,stepnumber=examples[(stage,n)]
                    path,snippet=code_excerpt(stage,pos,stepnumber)
                    out+=f"**Código de referencia probado:** §{path}§\n"
                    out+=fenced(snippet)
                out+="**Qué debe saber explicar el alumno.** Qué parte del contrato REST "
                out+="se resuelve en ASP.NET Core, qué parte escribe el programador, "
                out+="qué objeto se inyecta, qué ocurre si la entrada falla y por qué "
                out+="la respuesta HTTP es la indicada. Esta comprobación enlaza "
                out+="la explicación teórica con las acciones posteriores.\n\n"
    out=out.replace("§",chr(96))
    if len(re.findall(r"(?m)^### Bloque \d+ —",out))!=40:raise ValueError("Bloques perdidos")
    if out.count("](IMAGENES/")!=8:raise ValueError("Gráficos de teoría perdidos")
    return out
def steps_doc():
    out="""# M02 — Prácticas integrales: programar y probar APIs REST con .NET 8

**Autor: JAIME GALLO**

## Metodología de trabajo

Cada apartado parte del diseño REST explicado en teoría y culmina en **código
ejecutable y peticiones HTTP**. Se trabaja con Visual Studio, ASP.NET Core 8
Minimal API, EF Core 8 y SQL Server Express LocalDB. Los cuatro estados de
referencia están en §PROYECTO/2.1§ a §PROYECTO/2.4§: no son simulaciones,
sino proyectos con endpoints reales probados por HTTP.

La actividad práctica no requiere operaciones Git. El alumnado construye
primero la etapa 2.1, incorpora los verbos HTTP en 2.2, conecta la validación
en 2.3 y documenta el mismo servicio en 2.4. Para contrastar el resultado,
puede abrir por separado los proyectos de referencia. La copia no sustituye
la escritura y comprensión de código.

**Persistencia:** la API del alumno utiliza SQL Server Express LocalDB.
Los tests de integración usan EF Core InMemory únicamente para ejecutarse
de forma independiente en GitHub Actions. §EnsureCreated§ se emplea en
desarrollo para simplificar el arranque del ejercicio; no se propone para
despliegues productivos.

---

"""
    for stage,titles in enumerate(PRACTICE_TITLES,1):
        out+=f"## Punto 2.{stage} — {TITLES[stage-1]}\n\n"
        out+=f"**Proyecto comprobado:** §PROYECTO/{NAMES[stage-1]}§. "
        out+="El punto comienza estudiando el contrato de recursos y concluye "
        out+="con una ejecución verificable. Ninguna comprobación sustituye a "
        out+="un endpoint realmente implementado.\n\n"
        for number,title in enumerate(titles,1):
            lesson=LESSONS[stage-1][min((number-1)//5,4)]
            accion,comprobacion=paso_especifico(stage,number)
            out+=f"### PASO 2.{stage}.{number} — {title}\n\n"
            out+=f"**Objetivo del paso.** {title}. "
            out+="Al terminar esta actividad habrás realizado una modificación "
            out+="de código o comprobado una propiedad concreta del contrato REST.\n\n"
            out+="**Acciones guiadas.** "+accion+" "
            out+="Trabaja sobre la copia de tu solución de esta etapa y guarda "
            out+="el archivo antes de ejecutar la aplicación. "
            out+="Cuando el código usa `MapGet`, `MapPost`, `MapPut`, `MapPatch` "
            out+="o `MapDelete`, consulta también la tabla de verbos del punto "
            out+="para justificar la URI y la respuesta.\n\n"
            if number in CODE_STEPS[stage-1]:
                idx=CODE_STEPS[stage-1][number]
                file,source=code_excerpt(stage,idx,number)
                out+=f"**Código real contrastado: `{file}`**. "
                out+="Es el estado final del archivo en la solución verificada; "
                out+="si ya has creado parte del mismo en pasos anteriores, incorpora "
                out+="solo lo que corresponde a esta actividad y conserva lo demás.\n"
                out+=fenced(source)
            elif stage==2 and number in (6,8,12,13,15,17,19,20):
                out+="**Referencia de código:** `src/AceriaApp.Api/Program.cs`. "
                out+="Busca el método HTTP correspondiente y su llamada a "
                out+="`SaveChangesAsync`. Comprueba el comportamiento indicado "
                out+="en la acción antes de continuar.\n\n"
            elif stage==3 and number in (9,10,12,13,16,18,19,20):
                out+="**Referencia de código:** `src/AceriaApp.Api/Validacion/ValidationFilter.cs` "
                out+="y el endpoint de `Program.cs` sobre el que se instala el filtro. "
                out+="Comprueba dónde se produce `ValidationProblem` y dónde se llama "
                out+="a `next(context)`.\n\n"
            elif stage==4 and number in (5,7,9,10,11,13,14,15,17,18,19,21,22,23):
                out+="**Referencia de código:** `DocumentacionExtensions.cs`, "
                out+="`Program.cs` o `ContratoOpenApiTests.cs` según el caso. "
                out+="La prueba debe leer el documento generado, no un texto YAML "
                out+="escrito a mano.\n\n"
            else:
                out+="**Código relacionado:** consulta los archivos del proyecto "
                out+=f"`PROYECTO/{NAMES[stage-1]}` para contrastar las declaraciones "
                out+="que acabas de añadir, sin copiar anticipadamente etapas posteriores.\n\n"
            out+="**Por qué funciona así.** "+explicacion_especifica(stage,number)+"\n\n"
            out+="**Verificación concreta.** "+comprobacion+" "
            if number in (23,24):
                out+="Ejecuta además las pruebas xUnit del proyecto de esta etapa "
                out+="para confirmar que el ejercicio no ha roto los endpoints anteriores.\n\n"
            else:
                out+="Usa la herramienta HTTP o el depurador solo si este paso "
                out+="interactúa con una ruta; los cambios de configuración y modelo "
                out+="se verifican primero con la compilación.\n\n"
            fix=error_especifico(stage,number)
            out+="**Si algo falla.** "+fix+"\n\n"
        out+="### Matriz de comprobación del punto\n\n"
        out+="| Comportamiento | Resultado esperado |\n|:---|:---|\n"
        for outcome in RESPONSE_HINT[stage-1]:
            a,b=outcome.split(" → ",1)
            out+=f"| §{a}§ | {b} |\n"
        out+="\n**Reto integrador.** Reconstruye sin consultar la solución "
        out+="el último endpoint o validación practicada y añade una prueba "
        out+="HTTP que demuestre su resultado. Describe el recurso, el "
        out+="verbo, el contrato y el código devuelto. Si no puedes reproducir "
        out+="una respuesta, vuelve al primer paso que introdujo el comportamiento.\n\n---\n\n"
    return out.replace("§",chr(96))
def main():
    target=Path("_m02_base_original")
    subprocess.run([sys.executable,".github/scripts/construir_m02_desde_fuentes.py",
                    "--salida",str(target)],check=True)
    base=(target/"M02_TEORIA.md").read_text(encoding="utf-8")
    theory=enrich_theory(base)
    practices=steps_doc()
    if re.search(r"\bgit\s+(?:add|commit|status|log|push|checkout)\b",practices,re.I):
        raise ValueError("Prácticas contienen comandos Git")
    if len(re.findall(r"(?m)^### PASO 2\.[1-4]\.\d+ —",practices))!=96:
        raise ValueError("Las prácticas no contienen 96 pasos")
    for n in range(1,5):
        steps=[int(x) for x in re.findall(
            rf"(?m)^### PASO 2\.{n}\.(\d+) —",practices)]
        if steps!=list(range(1,25)):raise ValueError(f"Faltan pasos en 2.{n}")
    (MODULE/"TEORIA"/"M02_TEORIA.md").write_text(theory,encoding="utf-8")
    (MODULE/"PRACTICAS"/"M02_PRACTICAS.md").write_text(practices,encoding="utf-8")
    report={"bloques_originales":40,"graficos":8,"pasos_programacion":96,
            "palabras_teoria":len(theory.split()),
            "palabras_practicas":len(practices.split()),
            "comandos_git_alumno":0,"proyectos_reales":4,
            "originales_intactos":True}
    Path("m02_redisenio_informe.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
