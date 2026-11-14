#!/usr/bin/env python3
"""Reconstrucción de M01 desde vacío, leyendo el manual, sin copiar snapshots.

Genera la solución y los proyectos de tests desde configuración .NET 8
reproducible; extrae los fuentes y documentos de los pasos del Markdown.
Genera una migración con EF Core desde el modelo, no copia la migración canónica.
Reconstruye los cinco puntos de forma acumulativa y valida su funcionamiento.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import uuid
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"M01_INTRODUCCION_MICROSERVICIOS"
MANUAL=MOD/"PRACTICAS/M01_PRACTICAS.md"
STAGES=[
"1.1-monolito-vs-microservicios","1.2-ventajas-inconvenientes",
"1.3-principios-diseno","1.4-organizacion-solucion","1.5-buenas-practicas"]
API="src/AceriaApp.Monolito.Api"
TESTS={1:"AceriaApp.Monolito.Tests",2:"AceriaApp.Metricas.Tests",
       3:"AceriaApp.Diseno.Tests",4:"AceriaApp.Organizacion.Tests",
       5:"AceriaApp.BuenasPracticas.Tests"}
COUNTS=[1,9,13,18,23]
# (Paso del manual, ruta de código o documento a crear desde ese paso).
STEPS={
 1:[(11,API+"/Dominio/Orden.cs"),
    (12,API+"/Infraestructura/AceriaDbContext.cs"),
    (13,API+"/Program.cs"),
    (17,"tests/AceriaApp.Monolito.Tests/OrdenTests.cs"),
    (19,"docs/ADR-001-monolito-vs-microservicios.md"),(20,"README.md")],
 2:[(4,"docs/analisis-ventajas-inconvenientes.md"),
    (6,API+"/Metricas/MetricasAcoplamiento.cs"),
    (7,API+"/Metricas/MetricasServicio.cs"),
    (8,API+"/Metricas/AnalizadorMonolito.cs"),
    (13,"tests/AceriaApp.Metricas.Tests/MetricasAcoplamientoTests.cs"),
    (14,"tests/AceriaApp.Metricas.Tests/MetricasServicioTests.cs"),
    (15,"tests/AceriaApp.Metricas.Tests/AnalizadorMonolitoTests.cs"),
    (19,"README.md"),(20,"docs/ADR-002-metricas-acoplamiento.md")],
 3:[(4,"docs/principios-diseno.md"),
    (6,API+"/Diseno/LimiteServicio.cs"),
    (7,API+"/Diseno/ValidadorLimiteServicio.cs"),
    (9,API+"/Diseno/CatalogoLimites.cs"),
    (14,"tests/AceriaApp.Diseno.Tests/ValidadorLimiteServicioTests.cs"),
    (15,"tests/AceriaApp.Diseno.Tests/CatalogoLimitesTests.cs"),
    (19,"README.md"),(20,"docs/ADR-003-principios-diseno.md")],
 4:[(4,"docs/organizacion-solucion.md"),
    (6,API+"/Organizacion/ConvencionNombres.cs"),
    (7,API+"/Organizacion/ValidadorConvencionNombres.cs"),
    (9,API+"/Organizacion/CatalogoProyectos.cs"),
    (14,"tests/AceriaApp.Organizacion.Tests/ValidadorConvencionNombresTests.cs"),
    (15,"tests/AceriaApp.Organizacion.Tests/CatalogoProyectosTests.cs"),
    (19,"README.md"),(20,"docs/ADR-004-organizacion-solucion.md")],
 5:[(4,"docs/buenas-practicas.md"),
    (6,API+"/BuenasPracticas/Practica.cs"),
    (7,API+"/BuenasPracticas/ValidadorBuenasPracticas.cs"),
    (9,API+"/BuenasPracticas/CatalogoPracticas.cs"),
    (14,"tests/AceriaApp.BuenasPracticas.Tests/ValidadorBuenasPracticasTests.cs"),
    (15,"tests/AceriaApp.BuenasPracticas.Tests/CatalogoPracticasTests.cs"),
    (19,"README.md"),(20,"docs/ADR-005-buenas-practicas.md")]
}
SKIP={"obj","bin","TestResults",".vs",".qa","_trx"}


def fragments():
    text=MANUAL.read_text(encoding="utf-8-sig")
    fence=re.escape(chr(96)*3)
    if len(re.findall("(?m)^"+fence,text))!=104:
        raise RuntimeError("El número original de 52 bloques ha cambiado")
    heads=[]
    for n in range(1,6):
        x=re.search(r"(?m)^# Punto 1\."+str(n)+r" — ",text)
        if not x:raise RuntimeError(f"Falta punto 1.{n}")
        heads.append(x.start())
    result={}
    for i,start in enumerate(heads):
        section=text[start:heads[i+1] if i<4 else len(text)]
        steps=list(re.finditer(r"(?m)^### Paso (\d+) — ",section))
        if [int(x.group(1)) for x in steps]!=list(range(1,25)):
            raise RuntimeError(f"No están los 24 pasos de 1.{i+1}")
        for k,st in enumerate(steps):
            body=section[st.end():steps[k+1].start() if k+1<len(steps) else len(section)]
            chunks=list(re.finditer(
                "(?m)^"+fence+r"(\w*)\n([\s\S]*?)^"+fence+r"\s*$",body))
            if chunks:
                result[f"1.{i+1}.{int(st.group(1))}"]=[
                    (x.group(1),x.group(2)) for x in chunks]
    for p,items in STEPS.items():
        for step,path in items:
            key=f"1.{p}.{step}"
            blocks=result.get(key,[])
            expected="markdown" if path.endswith(".md") else "csharp"
            if len(blocks)!=1 or blocks[0][0]!=expected:
                raise RuntimeError(f"Bloque no inequívoco {key} -> {path}")
    return result


def write(root,relative,content):
    p=root/relative
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(content.rstrip()+"\n",encoding="utf-8")


def run(args,cwd,env,timeout=850):
    print("$ "+" ".join(map(str,args)),flush=True)
    p=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,
       stderr=subprocess.STDOUT,text=True,encoding="utf-8",errors="replace",
       timeout=timeout)
    print(p.stdout[-5000:],flush=True)
    if p.returncode:raise RuntimeError(f"Fallo ejecutando {args} en {cwd}")
    return p.stdout


def initial(root):
    write(root,".gitignore","bin/\nobj/\n*.user\n*.suo\n.vs/\nTestResults/")
    write(root,API+"/appsettings.json",json.dumps({
      "ConnectionStrings":{"AceriaDb":(
        "Server=.\\SQLEXPRESS;Database=AceriaDb;Trusted_Connection=True;"
        "TrustServerCertificate=True")},
      "Logging":{"LogLevel":{"Default":"Information",
                            "Microsoft.AspNetCore":"Warning"}},
      "AllowedHosts":"*"},indent=2))
    write(root,API+"/appsettings.Development.json",
      json.dumps({"Logging":{"LogLevel":{"Default":"Information",
                         "Microsoft.AspNetCore":"Warning"}}}))
    write(root,API+"/Properties/launchSettings.json",json.dumps({"profiles":{
      "http":{"commandName":"Project","launchBrowser":True,"launchUrl":"swagger",
        "environmentVariables":{"ASPNETCORE_ENVIRONMENT":"Development"},
        "applicationUrl":"http://localhost:5000"},
      "https":{"commandName":"Project","launchBrowser":True,"launchUrl":"swagger",
        "environmentVariables":{"ASPNETCORE_ENVIRONMENT":"Development"},
        "applicationUrl":"https://localhost:7000;http://localhost:5000"}}}))
    write(root,API+"/AceriaApp.Monolito.Api.csproj",(
      '<Project Sdk="Microsoft.NET.Sdk.Web">\n<PropertyGroup>\n'
      '<TargetFramework>net8.0</TargetFramework><Nullable>enable</Nullable>'
      '<ImplicitUsings>enable</ImplicitUsings></PropertyGroup>\n<ItemGroup>\n'
      '<PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />\n'
      '<PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.0">'
      '<PrivateAssets>all</PrivateAssets>'
      '<IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>'
      '</PackageReference>\n'
      '<PackageReference Include="Swashbuckle.AspNetCore" Version="6.6.2" />\n'
      '</ItemGroup></Project>'))


def test_project():
    return ('<Project Sdk="Microsoft.NET.Sdk">\n<PropertyGroup>\n'
            '<TargetFramework>net8.0</TargetFramework>'
            '<IsPackable>false</IsPackable><IsTestProject>true</IsTestProject>'
            '<ImplicitUsings>enable</ImplicitUsings><Nullable>enable</Nullable>'
            '</PropertyGroup><ItemGroup>\n'
            '<PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.9.0" />\n'
            '<PackageReference Include="xunit" Version="2.6.6" />\n'
            '<PackageReference Include="xunit.runner.visualstudio" Version="2.5.6" />\n'
            '<PackageReference Include="FluentAssertions" Version="6.12.2" />\n'
            '</ItemGroup><ItemGroup>\n'
            '<ProjectReference Include="../../src/AceriaApp.Monolito.Api/AceriaApp.Monolito.Api.csproj" />'
            '</ItemGroup></Project>')


def code_set(root):
    return {x.relative_to(root).as_posix() for x in root.rglob("*.cs")
            if x.is_file() and not any(p in SKIP for p in x.parts)
            and "Migraciones" not in x.parts}


def solution_projects(root,env):
    r=run(["dotnet","sln","AceriaApp.sln","list"],root,env)
    return sorted(x.strip().replace("\\","/").casefold()
         for x in r.splitlines() if x.strip().lower().endswith(".csproj"))


def make_all(base,env,ef):
    blocks=fragments()
    previous=None
    report=[]
    for point in range(1,6):
        dest=base/STAGES[point-1]
        if previous is None:
            dest.mkdir(parents=True)
            initial(dest)
            run(["dotnet","new","sln","-n","AceriaApp"],dest,env)
            run(["dotnet","sln","AceriaApp.sln","add",
                 API+"/AceriaApp.Monolito.Api.csproj"],dest,env)
        else:
            shutil.copytree(previous,dest,ignore=shutil.ignore_patterns(
                 "obj","bin","TestResults","_trx",".qa",".vs"))
        for step,path in STEPS[point]:
            write(dest,path,blocks[f"1.{point}.{step}"][0][1])
        project=TESTS[point]
        testpath=f"tests/{project}/{project}.csproj"
        write(dest,testpath,test_project())
        run(["dotnet","sln","AceriaApp.sln","add",testpath],dest,env)
        if point==1 and ef:
            run(["dotnet","restore","AceriaApp.sln","--nologo"],dest,env)
            run(["dotnet","build","AceriaApp.sln","-c","Release",
                 "--no-restore","--nologo"],dest,env)
            run([ef,"migrations","add","Inicial","--project",API,
                 "--startup-project",API,"--output-dir",
                 "Infraestructura/Migraciones","--no-build",
                 "--configuration","Release"],dest,env)
        ref=MOD/"PROYECTO"/STAGES[point-1]
        actual=code_set(dest)
        expected=code_set(ref)
        if actual!=expected:
            raise RuntimeError(f"M01.1.{point} C# falta={sorted(expected-actual)} "
                               f"extra={sorted(actual-expected)}")
        actual_solution=solution_projects(dest,env)
        expected_solution=sorted(p.relative_to(ref).as_posix().casefold()
            for p in ref.rglob("*.csproj") if p.is_file())
        if actual_solution!=expected_solution:
            raise RuntimeError(f"M01.1.{point}: membresía de la solución diferente")
        state={"point":f"1.{point}","manual_files":len(STEPS[point]),
               "code_files":len(actual),"sln_projects":len(actual_solution),
               "structure":"PASS"}
        report.append(state)
        print("M01 DESDE VACIO "+json.dumps(state,ensure_ascii=True),flush=True)
        previous=dest
    return report


def passed_tests(path):
    files=list(path.glob("*.trx"))
    if not files:raise RuntimeError("No se encontraron informes TRX")
    total=passed=failed=skipped=0
    for file in files:
        c=ET.parse(file).getroot().find(".//{*}Counters")
        if c is None:raise RuntimeError(f"TRX inválido {file}")
        total+=int(c.get("total",0));passed+=int(c.get("passed",0))
        failed+=int(c.get("failed",0))
        skipped+=int(c.get("notExecuted",0))
    if passed!=total or failed or skipped:
        raise RuntimeError(f"xUnit: total={total} PASS={passed} FAIL={failed} SKIP={skipped}")
    return passed


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--e2e",action="store_true",help="Windows SQL Express + HTTP E2E")
    ap.add_argument("--report",type=Path,default=ROOT/"M01_RECONSTRUCCION_CERO.md")
    args=ap.parse_args()
    ws=Path(os.getenv("RUNNER_TEMP",tempfile.gettempdir()))/(
       "m01_blank_"+uuid.uuid4().hex[:9])
    env=os.environ.copy()
    env.update({"DOTNET_CLI_TELEMETRY_OPTOUT":"1","DOTNET_NOLOGO":"1",
                "PYTHONIOENCODING":"utf-8"})
    ws.mkdir()
    tools=ws/"herramientas"
    run(["dotnet","tool","install","dotnet-ef","--version","8.0.0",
         "--tool-path",str(tools)],ws,env)
    ef=str(tools/("dotnet-ef.exe" if os.name=="nt" else "dotnet-ef"))
    base=ws/"etapas"
    rows=make_all(base,env,ef)
    for i,stage in enumerate(STAGES):
        folder=base/stage
        run(["dotnet","restore","AceriaApp.sln","--nologo"],folder,env)
        run(["dotnet","build","AceriaApp.sln","-c","Release",
             "--no-restore","--nologo"],folder,env)
        trx=folder/"_trx"
        trx.mkdir()
        run(["dotnet","test","AceriaApp.sln","-c","Release","--no-build",
             "--no-restore","--logger","trx",
             "--results-directory",str(trx)],folder,env,timeout=1200)
        count=passed_tests(trx)
        if count!=COUNTS[i]:
            raise RuntimeError(f"M01 1.{i+1}: {count} pruebas, esperado {COUNTS[i]}")
        rows[i]["xunit_pass"]=count
        print(f"RECONSTRUIDO M01.1.{i+1}: xUnit {count}/{COUNTS[i]} PASS",flush=True)
    integration=None
    if args.e2e:
        from validar_m01_windows import e2e_http
        last=base/STAGES[-1]
        local=env.copy()
        local["ASPNETCORE_ENVIRONMENT"]="Development"
        local["ConnectionStrings__AceriaDb"]=(
            "Server=.\\SQLEXPRESS;Database=AceriaM01_"
            + uuid.uuid4().hex[:9]
            +";Trusted_Connection=True;TrustServerCertificate=True;Encrypt=False")
        options=["--project",API,"--startup-project",API,
                 "--no-build","--configuration","Release"]
        try:
            run([ef,"database","update",*options],last,local)
            integration=e2e_http(last,local)
        finally:
            try:run([ef,"database","drop","--force",*options],last,local)
            except Exception as ex:print("ADVERTENCIA DB: "+str(ex),flush=True)
    lines=["# M01 reconstruido desde carpeta vacía","",
      "Se crean proyectos y solución desde metadatos .NET 8; los C# y documentos "
      "didácticos proceden de los bloques del Markdown corregido y no se copian "
      "del proyecto canónico. Cada etapa usa el estado reconstruido anterior.",
      "La migración se genera con EF Core desde el modelo, por lo que su "
      "identificador no es el mismo del material preentregado.",
      "",
      "| Punto | Archivos del manual | C# | Proyectos .sln | xUnit PASS |",
      "|---|---:|---:|---:|---:|"]
    for row in rows:
        lines.append(f"| {row['point']} | {row['manual_files']} | "
          f"{row['code_files']} | {row['sln_projects']} | {row['xunit_pass']} |")
    lines +=["","**SQL Server Express y HTTP:** "
             +json.dumps(integration or {"no_ejecutado":True},ensure_ascii=False),
             "","**Límites:** no emula clics de Visual Studio; no realiza "
             "retos opcionales. La construcción desde vacío es una comprobación "
             "adicional al itinerario principal, cuyo material de alumno sí "
             "proporciona la estructura inicial preparada. No se exige igualdad "
             "de GUIDs de solución o bytes de migraciones autogeneradas.",""]
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text("\n".join(lines),encoding="utf-8")
    print("INFORME "+str(args.report))
    print("PASS M01 desde vacío: 5/5 etapas + 64 xUnit acumulados"
          +(" + SQL/HTTP" if integration else ""),flush=True)

if __name__=="__main__":
    main()
