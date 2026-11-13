#!/usr/bin/env python3
"""Reconstrucción progresiva de M02.2–M02.4 desde las prácticas redactadas.

Parte del snapshot de referencia 2.1 (cuya construcción desde cero queda
pendiente), NO de los destinos 2.2-2.4. Extrae los fragmentos del manual
corregido, aplica altas/inserciones/sustituciones y compara con los proyectos
de referencia solamente DESPUÉS de construir los archivos.

Una diferencia (incluida falta de archivo) NO se convierte en PASS: se informa.
Esta prueba no sustituye dotnet build/test ni verifica acciones GUI de VS.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

from auditar_reconstruccion_practicas import ROOT, norm, files

FENCE = chr(96) * 3
DIR = ROOT / "M02_APIS_REST_ASPNET_CORE"
STAGES = [
    "2.1-diseno-apis-rest",
    "2.2-recursos-verbos-codigos",
    "2.3-validacion-peticiones",
    "2.4-documentacion-openapi",
]
PROGRAM = "src/AceriaApp.Api/Program.cs"
API_CSPROJ = "src/AceriaApp.Api/AceriaApp.Api.csproj"
EXCLUSION = {"README.md"}
HEAD = re.compile(r"^### PASO (2\.[1-4]\.\d+) —[^\n]*$", re.M)
FENCES = re.compile(r"^" + re.escape(FENCE) + r"([^\n]*)\n([\s\S]*?)^"
                    + re.escape(FENCE), re.M)
DOC = (DIR / "PRACTICAS/M02_PRACTICAS.md").read_text(encoding="utf-8-sig")
MATCHES = list(HEAD.finditer(DOC))
BLOCKS: dict[str, list[str]] = {}
for i, match in enumerate(MATCHES):
    name = match.group(1)
    end = MATCHES[i+1].start() if i+1<len(MATCHES) else len(DOC)
    BLOCKS[name] = [b.group(2).rstrip()+"\n" for b in
                    FENCES.finditer(DOC[match.end():end])]


def snippet(step: str, index: int = 0) -> str:
    matches = BLOCKS.get(step, [])
    if index >= len(matches):
        raise ValueError(f"Sin fragmento {index} en el Paso {step}")
    return matches[index]


def read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8-sig")


def put(root: Path, path: str, content: str):
    dest = root / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content.rstrip()+"\n", encoding="utf-8")


def expect_replace(original: str, old: str, new: str, context: str) -> str:
    number = original.count(old)
    if number != 1:
        raise RuntimeError(f"{context}: ancla debe aparecer una vez; aparece {number}: {old[:90]!r}")
    return original.replace(old, new, 1)


def inside_class(root: Path, path: str, snippets: list[str]):
    content = read(root, path)
    at = content.rfind("}")
    if at < 0:
        raise RuntimeError(f"Archivo sin llave de clase final: {path}")
    content = content[:at] + "\n" + "\n".join(snippets) + "\n" + content[at:]
    put(root,path,content)


def strip_comment_suffix(src: str) -> str:
    return re.sub(r"(?m)^// La cadena de .*?\n", "", src).strip()


def add_before_run(original: str, inserted: str) -> str:
    return expect_replace(original, "app.Run();",
                          inserted.rstrip() + "\n\napp.Run();",
                          "Agregar endpoints antes del arranque")


def update_chain(original: str, name: str, chain: str) -> str:
    matcher = re.compile(
        r'(?ms)^\.WithName\("' + re.escape(name) + r'"\)[\s\S]*?;')
    candidates = list(matcher.finditer(original))
    if len(candidates) != 1:
        raise RuntimeError(f"Cadena {name}: esperada una aparición; hay {len(candidates)}")
    return original[:candidates[0].start()] + strip_comment_suffix(chain) + \
           original[candidates[0].end():]


def stage1(root: Path):
    """Construir el primer punto de M02 a partir de carpeta vacía."""
    root.mkdir(parents=True,exist_ok=True)
    put(root,API_CSPROJ,snippet("2.1.8"))
    put(root,"src/AceriaApp.Api/Properties/launchSettings.json",
        snippet("2.1.2"))
    put(root,"src/AceriaApp.Api/Modelo/Orden.cs",snippet("2.1.4"))
    put(root,"src/AceriaApp.Api/Modelo/OrdenDto.cs",snippet("2.1.7"))
    put(root,"src/AceriaApp.Api/appsettings.json",snippet("2.1.11"))
    put(root,"AceriaApp.http",snippet("2.1.20"))
    db=snippet("2.1.9")
    pos=db.rfind("}")
    if pos<0:raise RuntimeError("Falta cierre de AceriaDbContext")
    db=db[:pos] + snippet("2.1.10") + "\n" + db[pos:]
    put(root,"src/AceriaApp.Api/Datos/AceriaDbContext.cs",db)
    put(root,"tests/AceriaApp.Api.Tests/AceriaApp.Api.Tests.csproj",
        snippet("2.1.22",1))
    put(root,"tests/AceriaApp.Api.Tests/ApiFactory.cs",
        snippet("2.1.22",0))
    put(root,"tests/Compartido/SqlServerPruebas.cs",
        snippet("2.1.22",2))
    put(root,"tests/AceriaApp.Api.Tests/GetTests.cs",
        snippet("2.1.23"))
    program=("using AceriaApp.Api.Datos;\n"
             "using AceriaApp.Api.Modelo;\n"
             "using Microsoft.EntityFrameworkCore;\n\n"
             +snippet("2.1.1",1))
    program=expect_replace(
        program,"var app=builder.Build();",
        snippet("2.1.12").rstrip()+"\nvar app=builder.Build();",
        "Agregar DbContext al contenedor")
    get=snippet("2.1.14")
    get=expect_replace(
        get,
        "var ordenes = await db.Ordenes\n        .OrderBy(x => x.FechaCreacion).ToListAsync(ct);",
        "var ordenes = await db.Ordenes.AsNoTracking()\n"
        "        .OrderBy(x => x.FechaCreacion).ToListAsync(ct);",
        "Cambiar a consultas sin seguimiento")
    insert=(snippet("2.1.13").rstrip()+"\n\n"
            +get.rstrip()+"\n\n"+snippet("2.1.17").rstrip())
    program=add_before_run(program,insert)
    program+="public partial class Program {}\n"
    put(root,PROGRAM,program)


def stage2(root: Path):
    # Se reutiliza el estado ya construido por el estudiante en 2.1.
    put(root, "src/AceriaApp.Api/Contratos/ContratosOrden.cs",
        snippet("2.2.4"))
    put(root, "AceriaApp.http", snippet("2.2.20"))
    test = snippet("2.2.21")
    at = test.rfind("}")
    test = test[:at] + "\n" + snippet("2.2.22") + "\n" + \
           snippet("2.2.23") + "\n" + test[at:]
    put(root,"tests/AceriaApp.Api.Tests/EscrituraTests.cs",test)
    program=read(root,PROGRAM)
    program="using AceriaApp.Api.Contratos;\n"+program
    for step in ("2.2.5","2.2.11","2.2.14","2.2.16","2.2.18"):
        program=add_before_run(program,snippet(step))
    put(root,PROGRAM,program)


def stage3(root: Path):
    put(root,API_CSPROJ,snippet("2.3.3"))
    validators=snippet("2.3.4")
    validators=expect_replace(
        validators,
        "        RuleFor(x => x.Cliente).NotEmpty().MaximumLength(100);",
        "        RuleFor(x => x.Cliente).NotEmpty().MaximumLength(100);\n"
        + "\n".join("        "+x for x in snippet("2.3.5").splitlines()[1:]),
        "Añadir reglas de Material y Cantidad"
    )
    validators+="\n"+snippet("2.3.6")
    put(root,"src/AceriaApp.Api/Validacion/Validadores.cs",validators)
    put(root,"src/AceriaApp.Api/Validacion/ValidationFilter.cs",
        snippet("2.3.8"))
    put(root,"tests/AceriaApp.Api.Tests/ValidacionHttpTests.cs",
        snippet("2.3.22"))
    program=read(root,PROGRAM)
    program="using AceriaApp.Api.Validacion;\nusing FluentValidation;\n"+program
    program=expect_replace(
        program,
        "var app=builder.Build();",
        "builder.Services.AddValidatorsFromAssemblyContaining<CrearOrdenValidator>();\n\nvar app=builder.Build();",
        "Registrar FluentValidation")
    # El manual describe retirar la validación provisional del endpoint porque
    # a partir de 2.3 se ejecutará el filtro tipado (HTTP 400 con ProblemDetails).
    old=("    if(string.IsNullOrWhiteSpace(request.Cliente)||"
         "string.IsNullOrWhiteSpace(request.Material)||request.Cantidad<=0)\n"
         '        return Results.BadRequest(new {error="Cliente, material y cantidad son obligatorios."});\n')
    if program.count(old) != 2:
        raise RuntimeError("No aparecen exactamente dos validaciones provisionales POST/PUT")
    program=program.replace(old,"")
    patch=('    if(request.Cantidad<=0) return Results.BadRequest(new '
           '{error="Cantidad debe ser positiva."});\n')
    program=expect_replace(program,patch,"","Retirar validación provisional PATCH")
    for step,name in [("2.3.15","CrearOrden"),("2.3.16","ReemplazarOrden"),
                      ("2.3.17","CambiarCantidad")]:
        program=update_chain(program,name,snippet(step))
    put(root,PROGRAM,program)


def stage4(root: Path):
    put(root,API_CSPROJ,snippet("2.4.2"))
    base=snippet("2.4.3")
    method=snippet("2.4.4")
    swagger=snippet("2.4.5")
    method=expect_replace(method,"    services.AddSwaggerGen();",
                          swagger.rstrip(),"Configurar AddSwaggerGen")
    method=expect_replace(method,"\n});\n    return services;",
                          "\n    options.SchemaFilter<EjemploCrearOrden>();\n});\n    return services;",
                          "Configurar ejemplo OpenAPI")
    at=base.rfind("}")
    if at<0: raise RuntimeError("Falta cierre de DocumentacionExtensions")
    base=base[:at]+"\n"+method+"\n"+snippet("2.4.7")+"\n"+base[at:]
    base+="\n"+snippet("2.4.16",0)
    imports=("using AceriaApp.Api.Contratos;\nusing Microsoft.OpenApi.Any;\n"
             "using Swashbuckle.AspNetCore.SwaggerGen;\nusing Microsoft.OpenApi.Models;\n")
    put(root,"src/AceriaApp.Api/Documentacion/DocumentacionExtensions.cs",
        imports+base)
    test=snippet("2.4.20")
    at=test.rfind("}")
    test=test[:at]+"\n"+snippet("2.4.22")+"\n"+snippet("2.4.23",0)+\
         "\n"+snippet("2.4.23",1)+"\n"+test[at:]
    put(root,"tests/AceriaApp.Api.Tests/ContratoOpenApiTests.cs",test)
    program=read(root,PROGRAM)
    program="using AceriaApp.Api.Documentacion;\n"+program
    program=expect_replace(program,"var app=builder.Build();",
                          "builder.Services.AddDocumentacion();\n\nvar app=builder.Build();",
                          "Registrar OpenAPI")
    for step,items in (
        ("2.4.12",["ListarOrdenes","ObtenerOrdenPorId"]),
        ("2.4.13",["CrearOrden"]),
        ("2.4.14",["ReemplazarOrden","CambiarCantidad"]),
        ("2.4.15",["EliminarOrden","FinalizarOrden"])
    ):
        for i,name in enumerate(items):
            program=update_chain(program,name,snippet(step,i))
    program=expect_replace(program,"app.Run();",
                           "app.UseDocumentacion();\n\napp.Run();",
                           "Publicar Swagger")
    put(root,PROGRAM,program)


def inspect(stage: int, root: Path):
    target=DIR/"PROYECTO"/STAGES[stage-1]
    built=files(root)
    expected=files(target)
    additions=sorted(set(built)-set(expected))
    missing=sorted(set(expected)-set(built)-EXCLUSION)
    mismatches=sorted(rel for rel in expected.keys()&built.keys()
                      if rel not in EXCLUSION and norm(expected[rel])!=norm(built[rel]))
    return {"stage":f"2.{stage}","checked":len(expected)-len(EXCLUSION),
            "missing":missing,"extras":additions,"different":mismatches,
            "pass":not(missing or additions or mismatches),
            "excluded_documentation":sorted(EXCLUSION&set(expected))}


def materialize(out: Path, *, stage: int = 4, desde_cero: bool = False):
    if out.exists():raise FileExistsError(out)
    steps=[]
    if desde_cero:
        stage1(out)
        first_result=inspect(1,out)
        steps.append(first_result)
        print(f"M02 {first_result['stage']} {first_result}",flush=True)
        if not first_result["pass"]:
            return steps
    else:
        first=DIR/"PROYECTO"/STAGES[0]
        shutil.copytree(first,out,ignore=shutil.ignore_patterns(
            "bin","obj","TestResults","_trx","_test_results",".qa"
        ))
    for current,apply in [(2,stage2),(3,stage3),(4,stage4)]:
        apply(out)
        result=inspect(current,out)
        steps.append(result)
        print(f"M02 {result['stage']} {result}",flush=True)
        if not result["pass"]:
            break
        if current==stage:
            break
    return steps


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",type=Path,default=ROOT/"AUDITORIA_RECONSTRUCCION_M02.md")
    p.add_argument("--output",type=Path,help="Conservar el proyecto reconstruido en este directorio")
    p.add_argument("--stage",type=int,choices=(2,3,4),default=4)
    p.add_argument("--desde-cero",action="store_true",
        help="Reconstruir también 2.1 desde una carpeta vacía")
    args=p.parse_args()
    if args.output:
        results=materialize(args.output,stage=args.stage,desde_cero=args.desde_cero)
    else:
        with tempfile.TemporaryDirectory(prefix="m02_reconstruccion_") as temp:
            results=materialize(Path(temp)/"AceriaApp",stage=args.stage,desde_cero=args.desde_cero)
    lines=["# Reconstrucción incremental de M02", "",
        "Origen: proyecto de referencia 2.1. Las etapas posteriores se construyen "
        "únicamente desde los bloques e instrucciones del Markdown corregido; "
        "no se copia el proyecto de la etapa que queremos obtener.",
        "",
        "README.md es documentación descriptiva y se excluye de la comparación "
        "de código; la equivalencia semántica de ese texto se revisará aparte.",
        "",
        "| Punto | Archivos faltantes | Archivos diferentes | Extras | Resultado |",
        "|---|---:|---:|---:|---|"]
    for r in results:
        lines.append(f"| {r['stage']} | {len(r['missing'])} | "
                     f"{len(r['different'])} | {len(r['extras'])} | "
                     f"{'PASS' if r['pass'] else 'PENDIENTE'} |")
        for key in ("missing","different","extras"):
            for value in r[key]:
                lines.append(f"- {r['stage']} {key}: {value}")
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text("\n".join(lines)+"\n",encoding="utf-8")
    if len(results)!=(args.stage - (0 if args.desde_cero else 1)) or not all(x["pass"] for x in results):
        print("M02: hay diferencias; no se declara reconstrucción completa",flush=True)
        sys.exit(1)
    print("PASS: M02.1-M02.4 reconstruidos desde una carpeta vacía" if args.desde_cero else "PASS: M02.2-M02.4 reconstruidos desde el manual",flush=True)


if __name__=="__main__":
    main()
