#!/usr/bin/env python3
"""Auditoría de prácticas M02/M03 y tests Windows con SQL Server real."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import shutil
import tempfile
import time
import urllib.request
import urllib.error
import uuid
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
  2: ("M02_APIS_REST_ASPNET_CORE",
      ["2.1-diseno-apis-rest","2.2-recursos-verbos-codigos",
       "2.3-validacion-peticiones","2.4-documentacion-openapi"], 12, 66),
  3: ("M03_ARQUITECTURA_HEXAGONAL",
      ["3.1-capas-aplicacion","3.2-puertos-adaptadores",
       "3.3-separacion-capas","3.4-implementacion-aspnet-core"], 57, 69)
}
MARKER = re.compile(r"<!-- (M0[23]_(?:ARCHIVO|CODIGO)) (\{[^\n]*\}) -->\s*" +
                    chr(96)*3 + r"([^\n]*)\n([\s\S]*?)\n" + chr(96)*3)


def audit(num):
    directory, stages, markers_expected, blocks_expected = MODULES[num]
    text = (ROOT/directory/"PRACTICAS"/f"M0{num}_PRACTICAS.md").read_text(encoding="utf-8")
    codeblocks = re.findall(r"^" + chr(96)*3, text, re.M)
    assert len(codeblocks)==blocks_expected*2, (num,len(codeblocks))
    ids = re.findall(r"^### PASO ("+str(num)+r"\.\d+\.\d+) — ",text,re.M)
    expected = [f"{num}.{i}.{j}" for i in range(1,5) for j in range(1,25)]
    assert ids==expected, f"M0{num}: falta o se repite un paso"
    records=[]
    matches=list(MARKER.finditer(text))
    assert len(matches)==markers_expected, (num,len(matches),markers_expected)
    for match in matches:
        meta=json.loads(match.group(2))
        step=meta["paso"]
        assert step in expected
        point=int(step.split(".")[1])
        target=ROOT/directory/"PROYECTO"/stages[point-1]/meta["ruta"]
        assert target.is_file(), f"M0{num} {step}: falta {target}"
        records.append((step,meta["ruta"],meta.get("modo","referencia")))
    assert "**Resultado de aprendizaje.**" not in text
    assert "**Por qué funciona así.**" not in text
    print(f"M0{num} AUDITORÍA: 96/96 pasos, {len(records)} archivos trazables, "
          f"{blocks_expected} bloques de código",flush=True)
    return stages,records


def run(cmd,cwd,env,timeout=650):
    print("$ "+" ".join(map(str,cmd)),flush=True)
    p=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,text=True,
                     encoding="utf-8",errors="replace",timeout=timeout)
    print(p.stdout[-8500:],flush=True)
    if p.returncode: raise RuntimeError(f"Exit {p.returncode}: "+ " ".join(map(str,cmd)))
    return p.stdout


def count_trx(path):
    found=list(path.glob("*.trx"))
    assert found, f"Sin archivos TRX: {path}"
    passed=failed=total=skipped=0
    for file in found:
        node=ET.parse(file).getroot().find(".//{*}Counters")
        assert node is not None,str(file)
        passed+=int(node.attrib.get("passed",0))
        failed+=int(node.attrib.get("failed",0))
        total+=int(node.attrib.get("total",0))
        skipped+=int(node.attrib.get("notExecuted",0))
    assert passed>0 and failed==0 and passed+skipped==total, (passed,failed,total,skipped)
    return {"passed":passed,"total":total,"failed":failed,"skipped":skipped,
            "test_projects":len(found)}


def tests(num, stages, env, reconstruir_incremental=False):
    root=ROOT/MODULES[num][0]/"PROYECTO"
    workroot=Path(os.getenv("RUNNER_TEMP",tempfile.gettempdir())) / (
        f"m0{num}_validacion_" + uuid.uuid4().hex[:8])
    workroot.mkdir(parents=True,exist_ok=True)
    counts=[]
    for index,slug in enumerate(stages,1):
        stage=workroot/slug
        if reconstruir_incremental and index >= 2:
            from auditar_reconstruccion_practicas import materializar_etapa
            materializar_etapa(num,index,stage)
        else:
            shutil.copytree(root/slug,stage)
        project=("tests/AceriaApp.Api.Tests/AceriaApp.Api.Tests.csproj"
                 if num==2 else "AceriaApp.sln")
        run(["dotnet","restore",project,"--nologo"],stage,env)
        run(["dotnet","build",project,"-c","Release","--no-restore","--nologo"],stage,env)
        output=stage/"_test_results"
        output.mkdir(exist_ok=True)
        run(["dotnet","test",project,"-c","Release","--no-build","--no-restore",
             "--nologo","--logger","trx","--results-directory",str(output)],
            stage,env)
        summary=count_trx(output)
        counts.append({"point":f"{num}.{index}",**summary})
        print(f"M0{num} PUNTO {num}.{index}: "
              f"{summary['passed']}/{summary['total']} pruebas correctas",flush=True)
    return counts,workroot/stages[-1]


def http_call(url, payload=None):
    body=json.dumps(payload).encode() if payload is not None else None
    req=urllib.request.Request(url,data=body,
       headers={"Content-Type":"application/json"} if body else {},
       method="POST" if body else "GET")
    try:
        with urllib.request.urlopen(req,timeout=15) as res:
            data=res.read().decode("utf-8")
            return res.status,json.loads(data) if data.strip() else None,dict(res.headers)
    except urllib.error.HTTPError as e:
        return e.code,None,dict(e.headers)


def smoke(num,stage,env):
    base="http://127.0.0.1:"+str(51180+num)
    endpoint=("/api/v1/ordenes" if num==2 else "/api/v1/hexagonal/ordenes")
    local=env.copy()
    local["ASPNETCORE_ENVIRONMENT"]="Development"
    cs="Server=.\\SQLEXPRESS;Trusted_Connection=True;TrustServerCertificate=True;Encrypt=False;Database="
    suffix=uuid.uuid4().hex[:10]
    local["ConnectionStrings__AceriaApp"]=cs+"AceriaM02_"+suffix
    if num==3:local["ConnectionStrings__AceriaHexagonal"]=cs+"AceriaM03_"+suffix
    import tempfile
    logpath=Path(tempfile.gettempdir())/f"m0{num}_kestrel.log"
    with logpath.open("w",encoding="utf-8") as stream:
        proc=subprocess.Popen(["dotnet","run","-c","Release","--no-build",
            "--no-launch-profile","--project","src/AceriaApp.Api","--urls",base],
            cwd=stage,env=local,stdout=stream,stderr=subprocess.STDOUT)
        try:
            stop=time.monotonic()+110
            while time.monotonic()<stop:
                if proc.poll() is not None:
                    raise RuntimeError("API finalizada: "+logpath.read_text("utf-8")[-5000:])
                try:
                    status,body,_=http_call(base+endpoint)
                    if status==200 and isinstance(body,list):break
                except (urllib.error.URLError,TimeoutError):
                    time.sleep(.8)
            else:raise RuntimeError("No responde Kestrel")
            status,before,_=http_call(base+endpoint)
            assert status==200 and isinstance(before,list)
            name="CURSO_"+suffix
            status,created,headers=http_call(base+endpoint,
                    {"cliente":name,"material":"CHAPA-3MM","cantidad":5})
            assert status==201 and created and created["cliente"]==name,(status,created)
            location=headers.get("Location","")
            assert location.endswith(created["id"]),(location,created)
            status,read,_=http_call(base+endpoint+"/"+created["id"])
            assert status==200 and read["id"]==created["id"]
            status,allrows,_=http_call(base+endpoint)
            assert status==200 and any(x["id"]==created["id"] for x in allrows)
            bad,_,_=http_call(base+endpoint,
                     {"cliente":"","material":"","cantidad":0})
            large,_,_=http_call(base+endpoint,
                     {"cliente":"Prueba","material":"CHAPA","cantidad":501})
            assert bad==400 and large==422,(bad,large)
            status,openapi,_=http_call(base+"/swagger/v1/swagger.json")
            assert status==200 and "paths" in openapi
            print(f"M0{num} E2E REAL: GET 200, POST 201/Location, SQL, "
                  "validación 400, negocio 422, Swagger 200",flush=True)
            return {"GET":200,"POST":201,"SQL":"persistencia comprobada",
                    "validacion":bad,"capacidad":large,"OpenAPI":status}
        finally:
            proc.terminate()
            try:proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                proc.kill();proc.wait(timeout=15)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--module",type=int,choices=[2,3],required=True)
    ap.add_argument("--audit-only",action="store_true")
    ap.add_argument("--reconstruir-incremental",action="store_true")
    ap.add_argument("--report",type=str)
    args=ap.parse_args()
    stages,records=audit(args.module)
    if args.reconstruir_incremental and args.module==2:
        raise RuntimeError("M02 no tiene aún todas las operaciones de reconstrucción marcadas")
    lines=[f"# M0{args.module} — Evidencia de validación", "",
           "**Pasos:** 96/96.",f"**Marcadores con archivos existentes:** {len(records)}.", ""]
    if not args.audit_only:
        env=os.environ.copy()
        assert env.get("ACERIA_TEST_SQLSERVER"),"Falta ACERIA_TEST_SQLSERVER"
        env["DOTNET_CLI_TELEMETRY_OPTOUT"]="1"
        report,final_stage=tests(args.module,stages,env,args.reconstruir_incremental)
        lines.extend(["| Punto | Correctas | Total | Fallidas |",
          "|---|---:|---:|---:|"]+
          [f"| {r['point']} | {r['passed']} | {r['total']} | {r['failed']} |"
           for r in report])
        result=smoke(args.module,final_stage,env)
        lines.extend(["","**E2E SQL/HTTP:** "+json.dumps(result,ensure_ascii=False),
            "","Se han ejecutado los snapshots de referencia y no todas las "
            "acciones gráficas de Visual Studio.",
            "Reconstrucción incremental desde el manual en las etapas 2..N: "
            + str(bool(args.reconstruir_incremental))])
    if args.report:
        destination=Path(args.report);destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_text("\n".join(lines)+"\n",encoding="utf-8")
        print("INFORME: "+str(destination),flush=True)


if __name__=="__main__":
    main()
