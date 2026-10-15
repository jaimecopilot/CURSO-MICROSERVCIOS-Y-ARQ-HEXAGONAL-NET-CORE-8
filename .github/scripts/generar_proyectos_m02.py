#!/usr/bin/env python3
"""Genera los cuatro proyectos cumulativos M02 desde M01/1.5. Ejecución en CI .NET 8."""
from pathlib import Path
import shutil, subprocess, hashlib, json, re, textwrap
ROOT=Path("M02_APIS_REST_ASPNET_CORE")
SRC=Path("M01_INTRODUCCION_MICROSERVICIOS/PROYECTO/1.5-buenas-practicas")
NAMES=["2.1-diseno-apis-rest","2.2-recursos-verbos-codigos","2.3-validacion-peticiones","2.4-documentacion-openapi"]
TEST_NAMES=["DisenoRest","CatalogoRecursos","Validacion","Documentacion"]
def put(p, s):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(textwrap.dedent(s).lstrip("\n"),encoding="utf-8")
def add_to_sln(root,name):
    subprocess.run(["dotnet","sln",str(root/"AceriaApp.sln"),"add",str(root/"tests"/("AceriaApp."+name+".Tests")/("AceriaApp."+name+".Tests.csproj"))],check=True)
def new_test(root,name):
    directory=root/"tests"/("AceriaApp."+name+".Tests")
    directory.mkdir(parents=True,exist_ok=True)
    tpl=(root/"tests"/"AceriaApp.BuenasPracticas.Tests"/"AceriaApp.BuenasPracticas.Tests.csproj").read_text(encoding="utf-8")
    if name=="Documentacion":
        tpl=tpl.replace('    <PackageReference Include="xunit"','    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="8.0.0" />\n    <PackageReference Include="xunit"')
    put(directory/("AceriaApp."+name+".Tests.csproj"),tpl)
    add_to_sln(root,name)
def csharp(root,area,name,source):
    put(root/"src"/"AceriaApp.Monolito.Api"/area/(name+".cs"),source)
def testcase(root,area,name,source):
    put(root/"tests"/("AceriaApp."+area+".Tests")/(name+".cs"),source)
def add_package(root,dependency,version):
    p=root/"src"/"AceriaApp.Monolito.Api"/"AceriaApp.Monolito.Api.csproj"
    s=p.read_text(encoding="utf-8")
    s=s.replace('    <PackageReference Include="Swashbuckle.AspNetCore"',f'    <PackageReference Include="{dependency}" Version="{version}" />\n    <PackageReference Include="Swashbuckle.AspNetCore"')
    put(p,s)
def docs(root,name,source): put(root/"docs"/name,source)
def readme(root,n,extra):
    nstage=n+1
    tests=[31,36,42,51][n]
    doc=["diseno-apis-rest.md","catalogo-recursos.md","validacion-peticiones.md","documentacion-openapi.md"][n]
    title=["Diseño de APIs REST","Recursos, verbos HTTP y códigos de respuesta","Validación de peticiones","Documentación mediante OpenAPI (Swagger)"][n]
    put(root/"README.md",f"""# Punto 2.{nstage} — {title}

## Objetivo
Construir una evolución verificable del monolito AceriaApp aplicando los conceptos de diseño de APIs REST.

## Estado de la solución
- Solución AceriaApp.sln con {7+n} proyectos en total (una API y {6+n} proyectos de pruebas).
- {tests} pruebas previstas en la solución completa, pendientes de comprobar mediante CI.
- Documento docs/{doc} y las decisiones arquitectónicas acumuladas.
- El proyecto es independiente: conserva los archivos del punto previo salvo integraciones aditivas documentadas.

## Cómo ejecutarlo
1. Abrir AceriaApp.sln en Visual Studio con SDK .NET 8.
2. Restaurar con dotnet restore AceriaApp.sln.
3. Compilar con dotnet build AceriaApp.sln.
4. Ejecutar dotnet test AceriaApp.sln.
5. Configurar SQL Server Express e iniciar la API con dotnet run --project src/AceriaApp.Monolito.Api.

## Qué incorpora este punto
{extra}

## Documentación
- docs/{doc}
- Los ADR previos conservados sin alteración.
""")
def adr(root,id,slug,title,decision):
    docs(root,f"ADR-{id:03d}-{slug}.md",f"""# ADR-{id:03d} — {title}

## Estado
Aceptado

## Contexto
AceriaApp necesita ampliar su contrato HTTP sin confundir los recursos de negocio con las entidades de persistencia.

## Decisión
{decision}

## Alternativas consideradas
Se descartó la documentación exclusivamente manual por su riesgo de obsolescencia y los nombres de rutas orientados a verbos por su menor consistencia.

## Consecuencias
La evolución queda trazada en cada carpeta autónoma. Los cambios de arranque, cuando son imprescindibles, se hacen únicamente en la copia nueva de Program.cs. Las pruebas deben contrastar el funcionamiento, no solo la existencia de archivos.
""")
def generate():
    if not SRC.is_dir(): raise SystemExit("No existe la carpeta M01/1.5 de partida")
    ROOT.mkdir(exist_ok=True)
    old=SRC
    manifest=[]
    for i,n in enumerate(NAMES):
        dest=ROOT/"PROYECTO"/n
        if dest.exists(): shutil.rmtree(dest)
        shutil.copytree(old,dest,ignore=shutil.ignore_patterns("bin","obj",".vs","TestResults"))
        root=dest
        if i==0:
            import sys
            sys.path.insert(0,str(Path(".github/scripts").resolve()))
            from e2e_m01 import activate_step
            for paso in range(1,25): activate_step(root,"1.5",paso)
        new_test(root,TEST_NAMES[i])
        if i==0: stage21(root)
        elif i==1: stage22(root)
        elif i==2: stage23(root)
        else: stage24(root)
        # Comparación integral del contenido heredado salvo integración de arranque
        deviations=[]
        for file in old.rglob("*"):
            if not file.is_file():continue
            rel=file.relative_to(old)
            if any(x in ("bin","obj",".vs","TestResults") for x in rel.parts): continue
            if str(rel).replace("\\","/") in ("README.md","AceriaApp.sln"):continue
            if i==0 and rel.suffix==".cs" and "INICIO PASO 1.5" in file.read_text(encoding="utf-8"):
                deviations.append(str(rel));continue
            if str(rel).replace("\\","/") in ("src/AceriaApp.Monolito.Api/Program.cs","src/AceriaApp.Monolito.Api/AceriaApp.Monolito.Api.csproj"): 
                if i>=2: deviations.append(str(rel));continue
            target=root/rel
            if not target.exists() or hashlib.sha256(file.read_bytes()).digest()!=hashlib.sha256(target.read_bytes()).digest():
                raise ValueError(f"Archivo heredado modificado o ausente: {rel}, {n}")
        manifest.append({"punto":n,"solucion":str(root/"AceriaApp.sln"),"proyectos":7+i,"pruebas_esperadas":[31,36,42,51][i],"excepciones_documentadas":deviations})
        old=root
    put(ROOT/"manifiesto_proyectos.json",json.dumps(manifest,ensure_ascii=False,indent=2))
def stage21(root):
    docs(root,"diseno-apis-rest.md","""# Diseño de APIs REST — 2.1
## Contrato de recursos
Las rutas identifican colecciones y recursos; no expresan órdenes en forma de verbos. La elección de versión en URI es una convención del curso, no un requisito universal de REST.
## Restricciones
Cliente-servidor, ausencia de estado, cacheabilidad, interfaz uniforme, capas y código bajo demanda (opcional).
## Rutas principales
- GET /api/v1/ordenes
- GET /api/v1/ordenes/{id}
- POST /api/v1/ordenes
- GET /api/v1/ordenes/{id}/lineas (contrato de futuro, todavía no implementado)
## Reglas del validador de ejemplo
El ejemplo valida prefijo api, versión vN y ausencia de segmentos de acción reservados. No constituye un verificador completo de cumplimiento REST ni sustituye una revisión del contrato.
## Representaciones
JSON es la representación implementada. Una cabecera Accept no garantiza automáticamente soporte para XML ni devolución 406.
""")
    adr(root,6,"diseno-apis-rest","Convenciones REST","Se adoptan rutas versionadas /api/v1 con nombres de colección, semántica HTTP y un validador básico de nomenclatura.")
    csharp(root,"DisenoRest","UriRest",r"""
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
            if (!string.IsNullOrWhiteSpace(Identificador)) partes.Add(Identificador);
            if (!string.IsNullOrWhiteSpace(SubRecurso)) partes.Add(SubRecurso);
            return "/" + string.Join("/", partes);
        }
    }
    """)
    csharp(root,"DisenoRest","ValidadorUriRest",r"""
    using System.Text.RegularExpressions;
    namespace AceriaApp.Monolito.Api.DisenoRest;
    public class ValidadorUriRest
    {
        private static readonly HashSet<string> VerbosProhibidos = new(StringComparer.OrdinalIgnoreCase)
            { "crear", "obtener", "listar", "actualizar", "eliminar", "get", "post", "put", "patch", "delete" };
        public ResultadoUri Validar(string? uri)
        {
            var errores = new List<string>();
            if (string.IsNullOrWhiteSpace(uri)) return new(false, new[] { "La URI es obligatoria." });
            if (!uri.StartsWith("/api/", StringComparison.Ordinal)) errores.Add("La URI no empieza por '/api/'.");
            var partes = uri.Split('?', 2)[0].Trim('/').Split('/');
            if (partes.Length < 3 || !Regex.IsMatch(partes[1], @"^v[1-9]\d*$"))
                errores.Add("La URI no incluye versión después de 'api'.");
            if (partes.Length < 3 || string.IsNullOrWhiteSpace(partes[2]))
                errores.Add("La URI no identifica un recurso.");
            foreach (var parte in partes.Skip(2))
                if (VerbosProhibidos.Contains(parte))
                    errores.Add($"La URI contiene un verbo prohibido: '{parte}'.");
            return new(errores.Count==0,errores);
        }
    }
    public record ResultadoUri(bool EsValida, IReadOnlyList<string> Errores);
    """)
    csharp(root,"DisenoRest","CatalogoUris",r"""
    namespace AceriaApp.Monolito.Api.DisenoRest;
    public class CatalogoUris
    {
        private readonly IReadOnlyList<string> _uris;
        public CatalogoUris(IEnumerable<string> uris) => _uris = uris.ToArray();
        public IEnumerable<string> UrisValidas(ValidadorUriRest validador) =>
            _uris.Where(u => validador.Validar(u).EsValida);
        public IEnumerable<string> UrisInvalidas(ValidadorUriRest validador) =>
            _uris.Where(u => !validador.Validar(u).EsValida);
        // RETO 2.1: agregar Resumen y ResumenUris según la guía de prácticas.
    }
    """)
    testcase(root,"DisenoRest","ValidadorUriRestTests",r"""
    using AceriaApp.Monolito.Api.DisenoRest;
    using Xunit;
    namespace AceriaApp.DisenoRest.Tests;
    public class ValidadorUriRestTests
    {
        private readonly ValidadorUriRest _v = new();
        [Fact] public void Valida_UriDeColeccion() { Assert.True(_v.Validar("/api/v1/ordenes").EsValida); }
        [Fact] public void Rechaza_SinPrefijo() { Assert.False(_v.Validar("/ordenes").EsValida); }
        [Fact] public void Rechaza_SinVersion() { Assert.False(_v.Validar("/api/ordenes").EsValida); }
        [Fact] public void Rechaza_SegmentoDeAccion() { Assert.False(_v.Validar("/api/v1/crear").EsValida); }
    }
    """)
    testcase(root,"DisenoRest","UriRestTests",r"""
    using AceriaApp.Monolito.Api.DisenoRest;
    using Xunit;
    namespace AceriaApp.DisenoRest.Tests;
    public class UriRestTests
    {
        [Fact] public void Construir_Coleccion() => Assert.Equal("/api/v1/ordenes",new UriRest {Recurso="ordenes"}.Construir());
        [Fact] public void Construir_Identificador() => Assert.Equal("/api/v1/ordenes/123",new UriRest {Recurso="ordenes", Identificador="123"}.Construir());
        [Fact] public void Construir_SubRecurso() => Assert.Equal("/api/v1/ordenes/123/lineas",new UriRest {Recurso="ordenes", Identificador="123", SubRecurso="lineas"}.Construir());
    }
    """)
    testcase(root,"DisenoRest","CatalogoUrisTests",r"""
    using AceriaApp.Monolito.Api.DisenoRest;
    using Xunit;
    namespace AceriaApp.DisenoRest.Tests;
    public class CatalogoUrisTests
    {
        [Fact] public void Separa_ValidasYNoValidas()
        {
            var c=new CatalogoUris(new[]{"/api/v1/ordenes","/api/v1/ordenes/123","/ordenes","/api/v1/crear"});
            Assert.Equal(2,c.UrisValidas(new ValidadorUriRest()).Count());
            Assert.Equal(2,c.UrisInvalidas(new ValidadorUriRest()).Count());
        }
    }
    """)
    readme(root,0,"- Documento REST y ADR-006.\n- Clases de construcción, validación básica de URI y catálogo.\n- Ocho pruebas nuevas; no se modifica el código heredado de M01.")
def stage22(root):
    docs(root,"catalogo-recursos.md","""# Catálogo de recursos — 2.2
## Contrato
| Recurso | URI | Métodos previstos |
|---|---|---|
| Orden | /api/v1/ordenes | GET, POST |
| Orden | /api/v1/ordenes/{id} | GET, PUT, PATCH, DELETE |
| Línea | /api/v1/ordenes/{id}/lineas | GET, POST |
| Material | /api/v1/materiales | GET, POST |
## Semántica
GET es seguro e idempotente. PUT y DELETE son idempotentes, pero la respuesta de un reintento puede cambiar. PATCH puede ser idempotente dependiendo de la operación. Las tablas de resultados del ejercicio son un subconjunto didáctico, no un inventario exhaustivo de códigos HTTP permitidos.
## Errores
Problem Details se documenta según RFC 9457, sucesora de RFC 7807. No confundir metadatos declarados en OpenAPI con implementación de respuestas.
""")
    adr(root,7,"catalogo-recursos","Catálogo de recursos","Se documenta un subconjunto de recursos de acería y códigos esperados en un catálogo explícito y testeable.")
    csharp(root,"CatalogoRecursos","CombinacionVerboCodigo",r"""
    namespace AceriaApp.Monolito.Api.CatalogoRecursos;
    public class CombinacionVerboCodigo
    {
        public string Verbo { get; init; }=string.Empty;
        public int Codigo { get; init; }
    }
    """)
    csharp(root,"CatalogoRecursos","ValidadorCombinacionVerboCodigo",r"""
    namespace AceriaApp.Monolito.Api.CatalogoRecursos;
    public class ValidadorCombinacionVerboCodigo
    {
        private static readonly Dictionary<string,int[]> CodigosPorVerbo=new(StringComparer.OrdinalIgnoreCase)
        {
            ["GET"]=new[]{200,404}, ["POST"]=new[]{201,400,409,422},
            ["PUT"]=new[]{200,204,400,404,409,422},
            ["PATCH"]=new[]{200,204,400,404,409,422},
            ["DELETE"]=new[]{204,404}
        };
        public ResultadoCombinacion Validar(CombinacionVerboCodigo combinacion)
        {
            var errores=new List<string>();
            if(!CodigosPorVerbo.TryGetValue(combinacion.Verbo,out var codigos))
            {
                errores.Add($"Verbo no permitido: '{combinacion.Verbo}'.");
                return new(false,errores);
            }
            if(!codigos.Contains(combinacion.Codigo))
                errores.Add($"Código '{combinacion.Codigo}' no permitido para el verbo '{combinacion.Verbo}'.");
            return new(errores.Count==0,errores);
        }
    }
    public record ResultadoCombinacion(bool EsValida,IReadOnlyList<string> Errores);
    """)
    csharp(root,"CatalogoRecursos","CatalogoCombinaciones",r"""
    namespace AceriaApp.Monolito.Api.CatalogoRecursos;
    public class CatalogoCombinaciones
    {
        private readonly IReadOnlyList<CombinacionVerboCodigo> _combinaciones;
        public CatalogoCombinaciones(IEnumerable<CombinacionVerboCodigo> combinaciones) =>
            _combinaciones=combinaciones.ToArray();
        public IEnumerable<CombinacionVerboCodigo> CombinacionesValidas(ValidadorCombinacionVerboCodigo v) =>
            _combinaciones.Where(c=>v.Validar(c).EsValida);
        public IEnumerable<CombinacionVerboCodigo> CombinacionesInvalidas(ValidadorCombinacionVerboCodigo v) =>
            _combinaciones.Where(c=>!v.Validar(c).EsValida);
        // RETO 2.2: agregar Resumen y record ResumenCombinaciones.
    }
    """)
    testcase(root,"CatalogoRecursos","ValidadorCombinacionVerboCodigoTests",r"""
    using AceriaApp.Monolito.Api.CatalogoRecursos;
    using Xunit;
    namespace AceriaApp.CatalogoRecursos.Tests;
    public class ValidadorCombinacionVerboCodigoTests
    {
        private readonly ValidadorCombinacionVerboCodigo _v=new();
        [Theory] [InlineData("GET",200)] [InlineData("POST",201)]
        public void Acepta_CombinacionesDelContrato(string verbo,int codigo) =>
            Assert.True(_v.Validar(new(){Verbo=verbo,Codigo=codigo}).EsValida);
        [Fact] public void Rechaza_Get201() => Assert.False(_v.Validar(new(){Verbo="GET",Codigo=201}).EsValida);
        [Fact] public void Rechaza_VerboNoDeclarado() => Assert.False(_v.Validar(new(){Verbo="OPTIONS",Codigo=200}).EsValida);
    }
    """)
    testcase(root,"CatalogoRecursos","CatalogoCombinacionesTests",r"""
    using AceriaApp.Monolito.Api.CatalogoRecursos;
    using Xunit;
    namespace AceriaApp.CatalogoRecursos.Tests;
    public class CatalogoCombinacionesTests
    {
        [Fact] public void Catalogo_SeparaConjuntos()
        {
            var c=new CatalogoCombinaciones(new CombinacionVerboCodigo[]{
                new(){Verbo="GET",Codigo=200},new(){Verbo="POST",Codigo=201},
                new(){Verbo="GET",Codigo=201},new(){Verbo="OPTIONS",Codigo=200}});
            var v=new ValidadorCombinacionVerboCodigo();
            Assert.Equal(2,c.CombinacionesValidas(v).Count());
            Assert.Equal(2,c.CombinacionesInvalidas(v).Count());
        }
    }
    """)
    readme(root,1,"- Catálogo de recursos y ADR-007.\n- Validador de combinaciones verbo-código; cinco nuevos casos xUnit.\n- La tabla valida una convención local; no todos los códigos HTTP posibles.")
def stage23(root):
    docs(root,"validacion-peticiones.md","""# Validación de peticiones — 2.3
## Sintaxis
El JSON malformado o un tipo no convertible impide el enlace. Nullable Reference Types no convierte por sí solo una propiedad string en requisito de runtime para Minimal API.
## Reglas semánticas
FluentValidation comprueba Cliente, Material y Cantidad en CrearOrdenRequest.
## Negocio
Las comprobaciones de stock, existencia de cliente y concurrencia pertenecen a aplicación/dominio y no se implementan en esta práctica.
## Integración
La extensión AddValidacion registra validadores y ValidationFilter<T> construye ValidationProblem. Registrar el validador no activa por sí solo el filtro: hay que asociarlo a endpoints compatibles.
## Códigos
Se establece la convención 400 para datos de entrada inválidos, y 422 para determinadas reglas semánticas de dominio cuando el contrato lo requiera; no es una obligación universal de HTTP.
""")
    adr(root,8,"validacion-peticiones","FluentValidation y filtros","Se encapsula el registro de validadores en ValidacionExtensions y se reserva la ejecución del filtro para endpoints que acepten el DTO validado.")
    add_package(root,"FluentValidation.DependencyInjectionExtensions","11.11.0")
    csharp(root,"Validacion","CrearOrdenRequest",r"""
    namespace AceriaApp.Monolito.Api.Validacion;
    public record CrearOrdenRequest(string Cliente,string Material,int Cantidad);
    """)
    csharp(root,"Validacion","CrearOrdenRequestValidator",r"""
    using FluentValidation;
    namespace AceriaApp.Monolito.Api.Validacion;
    public class CrearOrdenRequestValidator:AbstractValidator<CrearOrdenRequest>
    {
        public CrearOrdenRequestValidator()
        {
            RuleFor(x=>x.Cliente).NotEmpty().WithMessage("El cliente es obligatorio.")
                .MaximumLength(100).WithMessage("El cliente no puede superar 100 caracteres.");
            RuleFor(x=>x.Material).NotEmpty().WithMessage("El material es obligatorio.")
                .MaximumLength(100).WithMessage("El material no puede superar 100 caracteres.");
            RuleFor(x=>x.Cantidad).GreaterThan(0).WithMessage("La cantidad debe ser mayor que cero.")
                .LessThanOrEqualTo(10000).WithMessage("La cantidad no puede superar 10000.");
        }
    }
    """)
    csharp(root,"Validacion","ValidationFilter",r"""
    using FluentValidation;
    namespace AceriaApp.Monolito.Api.Validacion;
    public class ValidationFilter<T>:IEndpointFilter where T:class
    {
        private readonly IValidator<T> _validator;
        public ValidationFilter(IValidator<T> validator) => _validator=validator;
        public async ValueTask<object?> InvokeAsync(EndpointFilterInvocationContext context,EndpointFilterDelegate next)
        {
            var request=context.Arguments.OfType<T>().FirstOrDefault();
            if(request is null) return Results.BadRequest();
            var result=await _validator.ValidateAsync(request);
            if(!result.IsValid)
            {
                var errors=result.Errors.GroupBy(e=>e.PropertyName)
                    .ToDictionary(g=>g.Key,g=>g.Select(e=>e.ErrorMessage).ToArray());
                return Results.ValidationProblem(errors);
            }
            return await next(context);
        }
    }
    """)
    csharp(root,"Validacion","ValidacionExtensions",r"""
    using FluentValidation;
    namespace AceriaApp.Monolito.Api.Validacion;
    public static class ValidacionExtensions
    {
        public static IServiceCollection AddValidacion(this IServiceCollection services)
        {
            services.AddValidatorsFromAssemblyContaining<CrearOrdenRequestValidator>();
            return services;
        }
    }
    """)
    p=root/"src/AceriaApp.Monolito.Api/Program.cs"
    s=p.read_text(encoding="utf-8")
    s="using AceriaApp.Monolito.Api.Validacion;\n"+s
    s=s.replace("builder.Services.AddSwaggerGen();","builder.Services.AddSwaggerGen();\nbuilder.Services.AddValidacion();")
    put(p,s)
    testcase(root,"Validacion","CrearOrdenRequestValidatorTests",r"""
    using AceriaApp.Monolito.Api.Validacion;
    using Xunit;
    namespace AceriaApp.Validacion.Tests;
    public class CrearOrdenRequestValidatorTests
    {
        private readonly CrearOrdenRequestValidator _v=new();
        [Fact] public void Acepta_PeticionValida() => Assert.True(_v.Validate(new CrearOrdenRequest("ACX-001","CHAPA-3MM",10)).IsValid);
        [Fact] public void Rechaza_ClienteVacio() => Assert.False(_v.Validate(new CrearOrdenRequest("","CHAPA-3MM",10)).IsValid);
        [Fact] public void Rechaza_CantidadNegativa() => Assert.False(_v.Validate(new CrearOrdenRequest("ACX-001","CHAPA-3MM",-5)).IsValid);
        [Fact] public void Rechaza_CantidadExcesiva() => Assert.False(_v.Validate(new CrearOrdenRequest("ACX-001","CHAPA-3MM",20000)).IsValid);
    }
    """)
    testcase(root,"Validacion","CrearOrdenRequestTests",r"""
    using AceriaApp.Monolito.Api.Validacion;
    using Xunit;
    namespace AceriaApp.Validacion.Tests;
    public class CrearOrdenRequestTests
    {
        [Fact] public void Contrato_AsignaValores()
        {
            var p=new CrearOrdenRequest("ACX-001","CHAPA-3MM",10);
            Assert.Equal("ACX-001",p.Cliente); Assert.Equal("CHAPA-3MM",p.Material); Assert.Equal(10,p.Cantidad);
        }
        [Fact] public void Contrato_PermiteRepresentarCadenaVacia()
        {
            var p=new CrearOrdenRequest("","CHAPA-3MM",10);
            Assert.Equal("",p.Cliente);
        }
    }
    """)
    readme(root,2,"- Contrato y validador de creación, filtro reutilizable y ADR-008.\n- Program.cs incorpora únicamente dos líneas aditivas: using AceriaApp.Monolito.Api.Validacion; y builder.Services.AddValidacion();.\n- ValidacionExtensions contiene el registro y las seis pruebas nuevas no se atribuyen indebidamente al filtro.")
def stage24(root):
    docs(root,"documentacion-openapi.md","""# Documentación OpenAPI — 2.4
## Contrato generado
El middleware Swagger expone /swagger/v1/swagger.json exclusivamente en desarrollo. El documento se deriva de los endpoints de Program.cs, no se escribe a mano.
## Metadatos
Se exponen título, versión v1, descripción y contacto técnico ficticio.
## Secciones
info, paths, components y responses documentan lo realmente publicado. Las secciones servers, security o tags solo aparecen cuando corresponda.
## Ejemplos y esquemas
Los DTOs generarán esquemas cuando se usen como parámetros o respuestas declarados. SwaggerGen no infiere automáticamente los mensajes de FluentValidation.
## Verificación de integración
WebApplicationFactory inicia la aplicación, solicita el JSON, comprueba openapi, info.version y paths; también verifica que la ruta no se publique en Production.
## Cierre del módulo
- Cincuenta y una pruebas previstas en nueve proyectos de pruebas; diez proyectos en la solución.
- Nueve puntos acumulados (1.1 a 1.5 y 2.1 a 2.4).
- SQL Server Express sigue siendo el proveedor EF Core del curso.
""")
    adr(root,9,"documentacion-openapi","Documentación ejecutable","Se emplea SwaggerGen real, encapsulado en extensiones, y WebApplicationFactory para comprobar la respuesta HTTP.")
    csharp(root,"Documentacion","MetadatosApi",r"""
    namespace AceriaApp.Monolito.Api.Documentacion;
    public class MetadatosApi
    {
        public string Titulo {get;init;}="AceriaApp.Monolito.Api";
        public string Version {get;init;}="v1";
        public string Descripcion {get;init;}="API del monolito de referencia.";
        public string ContactoNombre {get;init;}="Equipo AceriaApp";
        public string ContactoEmail {get;init;}="equipo@aceria.local";
    }
    """)
    csharp(root,"Documentacion","ConfiguracionOpenApi",r"""
    namespace AceriaApp.Monolito.Api.Documentacion;
    public class ConfiguracionOpenApi
    {
        public MetadatosApi Metadatos {get;init;}=new();
        public bool PublicarSwaggerUI {get;init;}=true;
        public string RutaDocumento {get;init;}="/swagger/v1/swagger.json";
        public string NombreDocumento {get;init;}="AceriaApp.Monolito.Api v1";
        public bool EsEntornoDeDesarrollo(string entorno) =>
            string.Equals(entorno,"Development",StringComparison.OrdinalIgnoreCase);
        // RETO 2.4: añadir EsEntornoDeProduccion y su test.
    }
    """)
    csharp(root,"Documentacion","DocumentacionExtensions",r"""
    using Microsoft.OpenApi.Models;
    namespace AceriaApp.Monolito.Api.Documentacion;
    public static class DocumentacionExtensions
    {
        public static IServiceCollection AddDocumentacionOpenApi(
            this IServiceCollection services,MetadatosApi metadatos)
        {
            services.AddEndpointsApiExplorer();
            services.AddSwaggerGen(options => options.SwaggerDoc(metadatos.Version,new OpenApiInfo
            {
                Title=metadatos.Titulo,Version=metadatos.Version,
                Description=metadatos.Descripcion,
                Contact=new OpenApiContact { Name=metadatos.ContactoNombre,Email=metadatos.ContactoEmail}
            }));
            return services;
        }
        public static WebApplication UseDocumentacionOpenApi(
            this WebApplication app,ConfiguracionOpenApi configuracion)
        {
            if(configuracion.EsEntornoDeDesarrollo(app.Environment.EnvironmentName))
            {
                app.UseSwagger();
                if(configuracion.PublicarSwaggerUI)
                    app.UseSwaggerUI(options=>options.SwaggerEndpoint(
                        configuracion.RutaDocumento,configuracion.NombreDocumento));
            }
            return app;
        }
    }
    """)
    p=root/"src/AceriaApp.Monolito.Api/Program.cs"
    s=p.read_text(encoding="utf-8")
    s="using AceriaApp.Monolito.Api.Documentacion;\n"+s
    s=s.replace("builder.Services.AddEndpointsApiExplorer();\nbuilder.Services.AddSwaggerGen();",
                "builder.Services.AddDocumentacionOpenApi(new MetadatosApi());")
    s=s.replace("if (app.Environment.IsDevelopment())\n{\n    app.UseSwagger();\n    app.UseSwaggerUI();\n}",
                "app.UseDocumentacionOpenApi(new ConfiguracionOpenApi());")
    s=s.replace('await db.Ordenes.AsNoTracking().ToListAsync());',
                'await db.Ordenes.AsNoTracking().ToListAsync())\n    .WithName("ListarOrdenes").WithSummary("Lista las órdenes").WithTags("Ordenes")\n    .Produces<List<Orden>>(StatusCodes.Status200OK);')
    s=s.replace('    return Results.Created($"/api/v1/ordenes/{orden.Id}", orden);\n});',
                '    return Results.Created($"/api/v1/ordenes/{orden.Id}", orden);\n})\n    .WithName("CrearOrden").WithSummary("Crea una orden").WithTags("Ordenes")\n    .Produces<Orden>(StatusCodes.Status201Created);')
    s+="\n// Permite las pruebas reales de integración con WebApplicationFactory.\npublic partial class Program { }\n"
    put(p,s)
    testcase(root,"Documentacion","MetadatosApiTests",r"""
    using AceriaApp.Monolito.Api.Documentacion;
    using Xunit;
    namespace AceriaApp.Documentacion.Tests;
    public class MetadatosApiTests
    {
        [Fact] public void Metadatos_PorDefecto()
        {
            var m=new MetadatosApi();
            Assert.Equal("v1",m.Version); Assert.Equal("AceriaApp.Monolito.Api",m.Titulo);
            Assert.Equal("equipo@aceria.local",m.ContactoEmail);
        }
        [Fact] public void Metadatos_Personalizables()
        {
            var m=new MetadatosApi{Titulo="AceriaApp.Ordenes.Api",Version="v2"};
            Assert.Equal("v2",m.Version); Assert.Equal("AceriaApp.Ordenes.Api",m.Titulo);
        }
    }
    """)
    testcase(root,"Documentacion","ConfiguracionOpenApiTests",r"""
    using AceriaApp.Monolito.Api.Documentacion;
    using Xunit;
    namespace AceriaApp.Documentacion.Tests;
    public class ConfiguracionOpenApiTests
    {
        private readonly ConfiguracionOpenApi _c=new();
        [Fact] public void ValoresPorDefecto() => Assert.Equal("/swagger/v1/swagger.json",_c.RutaDocumento);
        [Fact] public void Desarrollo_IgnoraMayusculas() => Assert.True(_c.EsEntornoDeDesarrollo("development"));
        [Fact] public void Produccion_NoEsDesarrollo() => Assert.False(_c.EsEntornoDeDesarrollo("Production"));
    }
    """)
    testcase(root,"Documentacion","DocumentacionExtensionsTests",r"""
    using Microsoft.AspNetCore.Mvc.Testing;
    using Microsoft.AspNetCore.Hosting;
    using System.Text.Json;
    using Xunit;
    namespace AceriaApp.Documentacion.Tests;
    public class DocumentacionExtensionsTests
    {
        [Fact] public async Task Swagger_EnDesarrollo_DevuelveJsonOpenApi()
        {
            using var f=new WebApplicationFactory<Program>().WithWebHostBuilder(b=>b.UseEnvironment("Development"));
            using var cliente=f.CreateClient();
            var respuesta=await cliente.GetAsync("/swagger/v1/swagger.json");
            respuesta.EnsureSuccessStatusCode();
            using var json=JsonDocument.Parse(await respuesta.Content.ReadAsStringAsync());
            Assert.True(json.RootElement.TryGetProperty("openapi",out _));
        }
        [Fact] public async Task Swagger_ContieneVersion()
        {
            using var f=new WebApplicationFactory<Program>().WithWebHostBuilder(b=>b.UseEnvironment("Development"));
            using var json=JsonDocument.Parse(await f.CreateClient().GetStringAsync("/swagger/v1/swagger.json"));
            Assert.Equal("v1",json.RootElement.GetProperty("info").GetProperty("version").GetString());
        }
        [Fact] public async Task Swagger_DocumentaOrdenes()
        {
            using var f=new WebApplicationFactory<Program>().WithWebHostBuilder(b=>b.UseEnvironment("Development"));
            using var json=JsonDocument.Parse(await f.CreateClient().GetStringAsync("/swagger/v1/swagger.json"));
            Assert.True(json.RootElement.GetProperty("paths").TryGetProperty("/api/v1/ordenes",out _));
        }
        [Fact] public async Task Swagger_NoSePublicaEnProduccion()
        {
            using var f=new WebApplicationFactory<Program>().WithWebHostBuilder(b=>b.UseEnvironment("Production"));
            var response=await f.CreateClient().GetAsync("/swagger/v1/swagger.json");
            Assert.Equal(System.Net.HttpStatusCode.NotFound,response.StatusCode);
        }
    }
    """)
    readme(root,3,"- SwaggerGen y SwaggerUI configurados desde DocumentacionExtensions; metadatos reales.\n- Program.cs de esta copia integra las extensiones y anota los endpoints.\n- WebApplicationFactory contrasta la respuesta HTTP real del documento en Development y su ausencia en Production.\n- Nueve pruebas nuevas y ADR-009.")
if __name__=="__main__":
    generate()
    print("Proyectos M02 generados:",", ".join(NAMES))
