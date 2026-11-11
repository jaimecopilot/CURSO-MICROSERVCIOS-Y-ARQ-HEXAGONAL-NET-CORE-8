#!/usr/bin/env python3
"""E2E M02: reconstruye código, proyectos y configuración solo desde Markdown."""
import argparse,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"M02_APIS_REST_ASPNET_CORE"
LAB=BASE/"PRACTICAS/M02_PRACTICAS.md"
STAGES=["2.1-diseno-apis-rest","2.2-recursos-verbos-codigos","2.3-validacion-peticiones","2.4-documentacion-openapi"]
API=Path("src/AceriaApp.Api")
TEST=Path("tests/AceriaApp.Api.Tests")
PROG=API/"Program.cs"
EXPECTED=[3,7,12,16]
SOURCES=set(("2.1.4 2.1.6 2.1.7 2.1.9 2.1.10 2.1.12 2.1.13 2.1.14 2.1.15 2.1.17 2.1.22 2.1.23 "
"2.2.4 2.2.5 2.2.11 2.2.14 2.2.16 2.2.18 2.2.21 2.2.22 2.2.23 "
"2.3.4 2.3.5 2.3.6 2.3.8 2.3.14 2.3.15 2.3.16 2.3.17 2.3.22 "
"2.4.3 2.4.4 2.4.5 2.4.6 2.4.7 2.4.8 2.4.12 2.4.13 2.4.14 2.4.15 2.4.16 2.4.20 2.4.22 2.4.23").split())
BUILDS=SOURCES-{"2.1.4","2.1.6","2.1.7","2.1.9","2.1.10","2.2.21","2.2.22","2.3.5","2.3.6","2.4.20","2.4.22"}
class Broken(Exception):pass
def check(value,message):
    if not value:raise Broken(message)
def replace_once(text,old,new,step):
    check(text.count(old)==1,step+" necesita un unico marcador: "+old[:100]+" (hay "+str(text.count(old))+")")
    return text.replace(old,new,1)
def read(w,rel):
    p=w/rel;check(p.is_file(),"No existe "+str(p));return p.read_text(encoding="utf-8")
def write(w,rel,txt):
    p=w/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(txt.rstrip()+"\n",encoding="utf-8")
def append_program(w,code):
    write(w,PROG,replace_once(read(w,PROG),"app.Run();",code.rstrip()+"\n\napp.Run();","append API"))
def insert_class(w,path,code):
    s=read(w,path);pos=s.rfind("\n}");check(pos>=0,"No se cierra la clase en "+str(path))
    write(w,path,s[:pos]+"\n"+code.rstrip()+"\n"+s[pos:])
def using(w,stmt):
    s=read(w,PROG)
    if stmt not in s:write(w,PROG,stmt+"\n"+s)
def before_build(w,code):
    write(w,PROG,replace_once(read(w,PROG),"var app=builder.Build();",code+"\n\nvar app=builder.Build();","DI"))
def chain(w,name,code):
    s=read(w,PROG);p=re.compile(r'\.WithName\("'+name+r'"\)\.WithTags\("Ordenes"\)[\s\S]*?;')
    matches=list(p.finditer(s));check(len(matches)==1,name+": falta cadena de ruta")
    m=matches[0];write(w,PROG,s[:m.start()]+code.strip()+s[m.end():])
def steps_from_md():
    source=LAB.read_text(encoding="utf-8")
    check("Al terminar esta actividad habrás realizado una modificación de código" not in source,"Hay texto repetitivo")
    matches=list(re.finditer(r'^### PASO (2\.[1-4]\.\d+) — (.+)$',source,re.M))
    expected=[f"2.{p}.{n}" for p in range(1,5) for n in range(1,25)]
    check([m.group(1) for m in matches]==expected,"El Markdown no tiene 96 pasos ordenados")
    result={}
    for i,m in enumerate(matches):
        body=source[m.end():matches[i+1].start() if i+1<len(matches) else len(source)]
        artifact_pattern=r'<!-- M02_ARCHIVO (\{[^\n]+\}) -->\n```(csharp|xml|json|http|text)\n([\s\S]*?)\n```'
        artifacts=[]
        for tagged in re.finditer(artifact_pattern,body):
            info=json.loads(tagged.group(1))
            check(info['paso']==m.group(1),'Archivo fuera de su paso: '+str(info))
            check(not Path(info['ruta']).is_absolute() and '..' not in Path(info['ruta']).parts,'Ruta insegura')
            artifacts.append({**info,'codigo':tagged.group(3)})
        csharp=re.findall(r'```csharp\n([\s\S]*?)\n```',re.sub(artifact_pattern,'',body))
        check("**Procedimiento guiado.**" in body and "**Verificación concreta.**" in body,m.group(1)+": falta procedimiento o comprobacion")
        guided=re.search(r'\*\*Procedimiento guiado\.\*\*\n\n((?:[1-9]\. [^\n]+\n){4,})',body)
        check(guided is not None,m.group(1)+": se requieren cuatro acciones concretas numeradas")
        items=[int(n) for n in re.findall(r'^([1-9])\. ',guided.group(1),re.M)]
        check(items==[1,2,3,4],m.group(1)+": secuencia no es 1,2,3,4")
        verification=re.search(r'\*\*Verificación concreta\.\*\* ([^\n]+)',body)
        check(verification is not None and len(verification.group(1).split())>=9,m.group(1)+": verificacion sin detalle suficiente")
        check("**Acción.**" not in body,m.group(1)+": queda plantilla antigua")
        for code in csharp:
            check(all(x==m.group(1) for x in re.findall(r'// INICIO PASO (2\.[1-4]\.\d+)',code)),m.group(1)+": marcador discordante")
        result[m.group(1)]={"title":m.group(2),"codes":csharp,"body":body,"archivos":artifacts}
    return result
def prepare(tmp,index,prior):
    dest=tmp/STAGES[index]
    if prior:
        shutil.copytree(prior,dest,ignore=shutil.ignore_patterns("obj","bin","TestResults"))
    else:
        dest.mkdir(parents=True)
    return dest

def publish(source,destination):
    # Solo README.md es editorial y se conserva fuera de la reconstrucción.
    # La etapa completa se reemplaza: ningún .cs, proyecto o ajuste anterior puede colarse.
    check(not destination.is_symlink(),"El destino de publicación no puede ser un enlace")
    source=source.resolve();destination=destination.resolve()
    check(source.is_dir(),"No existe la etapa reconstruida: "+str(source))
    check(source!=destination and source not in destination.parents and destination not in source.parents,
          "Origen y destino de publicación deben ser carpetas independientes")
    check(not destination.exists() or destination.is_dir(),"El destino no es una carpeta")
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="."+destination.name+"-publicacion-",dir=destination.parent) as tmp:
        replacement=Path(tmp)/"nueva"
        replacement.mkdir()
        for item in source.rglob("*"):
            relative=item.relative_to(source)
            if not item.is_file() or any(x in ("obj","bin","TestResults") for x in relative.parts):continue
            target=replacement/relative
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(item,target)
        for relative in (Path("README.md"),):
            editorial=destination/relative
            if editorial.is_file() and not (replacement/relative).exists():
                shutil.copy2(editorial,replacement/relative)
        previous=Path(tmp)/"anterior"
        if destination.exists():os.replace(destination,previous)
        try:
            os.replace(replacement,destination)
        except OSError:
            if previous.exists():os.replace(previous,destination)
            raise


def apply(key,steps,w):
    for artifact in steps[key]["archivos"]:
        write(w,Path(artifact["ruta"]),artifact["codigo"])
    cc=steps[key]["codes"]
    def code(n=0):
        check(len(cc)>n,key+": falta bloque C# "+str(n));return cc[n]
    if key=="2.1.4":write(w,API/"Modelo/Orden.cs",code())
    elif key in ("2.1.6","2.1.7"):write(w,API/"Modelo/OrdenDto.cs",code())
    elif key=="2.1.9":write(w,API/"Datos/AceriaDbContext.cs",code())
    elif key=="2.1.10":insert_class(w,API/"Datos/AceriaDbContext.cs",code())
    elif key=="2.1.12":
        check("EnsureCreated" not in code(),"El paso 2.1.12 anticipa el 2.1.13")
        write(w,PROG,"using AceriaApp.Api.Datos;\nusing AceriaApp.Api.Modelo;\nusing Microsoft.EntityFrameworkCore;\n\nvar builder=WebApplication.CreateBuilder(args);\n"+code()+"\nvar app=builder.Build();\n\napp.Run();\npublic partial class Program {}\n")
    elif key in ("2.1.13","2.1.14","2.1.17"):append_program(w,code())
    elif key=="2.1.15":
        s=read(w,PROG)
        match=re.compile(r'var ordenes = await db\.Ordenes\s*\n\s*\.OrderBy')
        check(len(match.findall(s))==1 and "AsNoTracking" in code(),"GET sin transformación 2.1.15")
        write(w,PROG,match.sub("var ordenes = await db.Ordenes.AsNoTracking()\n        .OrderBy",s))
    elif key=="2.1.22":write(w,TEST/"ApiFactory.cs",code())
    elif key=="2.1.23":write(w,TEST/"GetTests.cs",code())
    elif key=="2.2.4":write(w,API/"Contratos/ContratosOrden.cs",code())
    elif key=="2.2.5":
        using(w,"using AceriaApp.Api.Contratos;");append_program(w,code())
    elif key in ("2.2.11","2.2.14","2.2.16","2.2.18"):append_program(w,code())
    elif key=="2.2.21":write(w,TEST/"EscrituraTests.cs",code())
    elif key in ("2.2.22","2.2.23"):insert_class(w,TEST/"EscrituraTests.cs",code())
    elif key=="2.3.4":write(w,API/"Validacion/Validadores.cs",code())
    elif key=="2.3.5":
        s=read(w,API/"Validacion/Validadores.cs")
        rules=[line.strip() for line in code().splitlines() if line.strip().startswith("RuleFor(")]
        check(len(rules)==2,key+": faltan reglas")
        anchor="RuleFor(x => x.Cliente).NotEmpty().MaximumLength(100);"
        write(w,API/"Validacion/Validadores.cs",replace_once(s,anchor,anchor+"\n        "+"\n        ".join(rules),key))
    elif key=="2.3.6":write(w,API/"Validacion/Validadores.cs",read(w,API/"Validacion/Validadores.cs")+"\n"+code())
    elif key=="2.3.8":write(w,API/"Validacion/ValidationFilter.cs",code())
    elif key=="2.3.14":
        using(w,"using AceriaApp.Api.Validacion;\nusing FluentValidation;")
        check("AddValidatorsFromAssemblyContaining" in code(),key+": registro ausente")
        before_build(w,"builder.Services.AddValidatorsFromAssemblyContaining<CrearOrdenValidator>();")
    elif key in ("2.3.15","2.3.16","2.3.17"):
        s=read(w,PROG)
        guard='    if(string.IsNullOrWhiteSpace(request.Cliente)||string.IsNullOrWhiteSpace(request.Material)||request.Cantidad<=0)\n        return Results.BadRequest(new {error="Cliente, material y cantidad son obligatorios."});\n'
        if key=="2.3.15":
            check(s.count(guard)==2,"Dos validaciones provisionales no encontradas")
            s=s.replace(guard,"")
        if key=="2.3.17":
            s=replace_once(s,'    if(request.Cantidad<=0) return Results.BadRequest(new {error="Cantidad debe ser positiva."});\n',"",key)
        write(w,PROG,s)
        name={"2.3.15":"CrearOrden","2.3.16":"ReemplazarOrden","2.3.17":"CambiarCantidad"}[key]
        chain(w,name,code())
    elif key=="2.3.22":write(w,TEST/"ValidacionHttpTests.cs",code())
    elif key=="2.4.3":write(w,API/"Documentacion/DocumentacionExtensions.cs",code())
    elif key=="2.4.4":insert_class(w,API/"Documentacion/DocumentacionExtensions.cs",code())
    elif key=="2.4.5":
        f=API/"Documentacion/DocumentacionExtensions.cs"
        write(w,f,"using Microsoft.OpenApi.Models;\n"+replace_once(read(w,f),"services.AddSwaggerGen();",code(),key))
    elif key=="2.4.6":
        using(w,"using AceriaApp.Api.Documentacion;");before_build(w,"builder.Services.AddDocumentacion();")
    elif key=="2.4.7":insert_class(w,API/"Documentacion/DocumentacionExtensions.cs",code())
    elif key=="2.4.8":append_program(w,"app.UseDocumentacion();")
    elif key=="2.4.12":
        chain(w,"ListarOrdenes",code());chain(w,"ObtenerOrdenPorId",code(1))
    elif key=="2.4.13":chain(w,"CrearOrden",code())
    elif key=="2.4.14":
        chain(w,"ReemplazarOrden",code().split(";")[0]+";")
        chain(w,"CambiarCantidad",code(1))
    elif key=="2.4.15":
        chain(w,"EliminarOrden",code().split(";")[0]+";")
        chain(w,"FinalizarOrden",code(1))
    elif key=="2.4.16":
        f=API/"Documentacion/DocumentacionExtensions.cs"
        s="using AceriaApp.Api.Contratos;\nusing Microsoft.OpenApi.Any;\nusing Swashbuckle.AspNetCore.SwaggerGen;\n"+read(w,f)
        check("SchemaFilter<EjemploCrearOrden>" in code(1),key+": filtro no registrado")
        s=replace_once(s,"    });\n});","    });\n    options.SchemaFilter<EjemploCrearOrden>();\n});",key)
        write(w,f,s+"\n"+code())
    elif key=="2.4.20":write(w,TEST/"ContratoOpenApiTests.cs",code())
    elif key=="2.4.22":insert_class(w,TEST/"ContratoOpenApiTests.cs",code())
    elif key=="2.4.23":
        insert_class(w,TEST/"ContratoOpenApiTests.cs",code())
        insert_class(w,TEST/"ContratoOpenApiTests.cs",code(1))
    elif key in SOURCES:raise Broken("No se ha implementado "+key)
    else:return bool(steps[key]["archivos"])
    return True
def run(args,w,key):
    p=subprocess.run(args,cwd=w,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
        text=True,errors="replace",timeout=360,env={**os.environ,"DOTNET_NOLOGO":"1"})
    check(p.returncode==0,key+" ha fallado\n"+p.stdout[-5000:])
    return p.stdout
def match_reference(stage,w):
    ref=BASE/"PROYECTO"/stage
    expected={x.relative_to(ref) for x in ref.rglob("*.cs") if "obj" not in x.parts and "bin" not in x.parts}
    actual={x.relative_to(w) for x in w.rglob("*.cs") if "obj" not in x.parts and "bin" not in x.parts}
    check(expected==actual,f"{stage}: archivos fuente distintos: falta {expected-actual} sobra {actual-expected}")
    for rel in expected:
        original=(ref/rel).read_text(encoding="utf-8")
        coded=(w/rel).read_text(encoding="utf-8")
        for name in re.findall(r'public\s+(?:sealed\s+)?(?:class|record)\s+(\w+)',original):
            check(name in coded,f"{rel}: falta clase/record {name}")
        if rel==PROG:
            for method,route in re.findall(r'app\.Map(Get|Post|Put|Patch|Delete)\("([^"]+)"',original):
                check(f'app.Map{method}("{route}"' in coded,f"{rel}: falta {method} {route}")
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",type=Path,default=Path("m02-e2e.json"))
    ap.add_argument("--no-tests",action="store_true",help="Reconstruye sin compilar ni ejecutar pruebas")
    ap.add_argument("--output-dir",type=Path,help="Publica las cuatro etapas reconstruidas en esta carpeta")
    ap.add_argument("--compare-reference",action="store_true",help="Compara la estructura C# con PROYECTO tras reconstruir")
    args=ap.parse_args()
    report={"fecha_utc":datetime.now(timezone.utc).isoformat(),"pasos":[],"etapas":[]}
    try:
        steps=steps_from_md()
        with tempfile.TemporaryDirectory(prefix="m02-lab-") as tmp:
            previous=None
            for index,stage in enumerate(STAGES):
                w=prepare(Path(tmp),index,previous);builds=0
                for number in range(1,25):
                    key=f"2.{index+1}.{number}";did=apply(key,steps,w)
                    row={"paso":key,"titulo":steps[key]["title"],
                         "tipo":"codigo_reconstruido_desde_md" if did else "verificacion_textual_o_manual",
                         "resultado":"RECONSTRUIDO" if did else "NO_AUTOMATIZABLE",
                         "bloques_csharp":len(steps[key]["codes"])}
                    if key in BUILDS and not args.no_tests:
                        run(["dotnet","build",str(w/API/"AceriaApp.Api.csproj"),"-c","Release"],w,key)
                        builds+=1;row["compilacion"]="PASS"
                    report["pasos"].append(row)
                tests=None
                if not args.no_tests:
                    log=run(["dotnet","test",str(w/TEST/"AceriaApp.Api.Tests.csproj"),"-c","Release"],w,stage)
                    m=re.search(r'Passed:\s*(\d+).*?Total:\s*(\d+)',log)
                    check(m is not None and int(m.group(1))==EXPECTED[index] and int(m.group(2))==EXPECTED[index],
                        "Conteo xUnit distinto en "+stage+": "+log[-1500:])
                    tests=int(m.group(1))
                if args.compare_reference:match_reference(stage,w)
                if args.output_dir:publish(w,args.output_dir.resolve()/stage)
                report["etapas"].append({"punto":f"2.{index+1}","compilaciones":builds,
                   "tests":tests,"expected":EXPECTED[index],
                   "resultado":"SIN_EJECUTAR_TESTS" if args.no_tests else "PASS",
                   "origen":"codigo, csproj y configuracion creados desde Markdown"})
                print(f"{stage}: {builds} compilaciones / {tests} tests",flush=True)
                previous=w
        check(len(report["pasos"])==96,"No hay evidencia de los 96 pasos")
        report["resumen"]={"resultado":"SIN_TESTS" if args.no_tests else "PASS","pasos":96,
            "pasos_codigo":sum(x["tipo"]=="codigo_reconstruido_desde_md" for x in report["pasos"]),
            "pasos_manual_o_verificacion":sum(x["tipo"]!="codigo_reconstruido_desde_md" for x in report["pasos"]),
            "tests_por_etapa":EXPECTED}
        report["retos_optativos"]={"resultado":"MANUAL_NO_EJECUTADO",
            "motivo":"Los pasos 2.x.24 proponen cambios abiertos y no contienen archivos C# completos que puedan reconstruirse sin decidir la solución del alumno.",
            "pasos":["2.1.24","2.2.24","2.3.24","2.4.24"]}
    except Exception as exc:
        report["resumen"]={"resultado":"FAIL","detalle":str(exc)}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report["resumen"],ensure_ascii=False),flush=True)
    if report["resumen"]["resultado"]=="FAIL":sys.exit(1)
if __name__=="__main__":main()
