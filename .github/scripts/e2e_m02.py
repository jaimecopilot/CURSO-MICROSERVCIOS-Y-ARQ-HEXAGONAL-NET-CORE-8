#!/usr/bin/env python3
"""Control M02: 40 bloques, 96 pasos, herencia real y SQL/HTTP opcional."""
import argparse, hashlib, json, re, sys, tempfile
from pathlib import Path
ROOT=Path("M02_APIS_REST_ASPNET_CORE")
STAGES=["2.1-diseno-apis-rest","2.2-recursos-verbos-codigos","2.3-validacion-peticiones","2.4-documentacion-openapi"]
sys.path.insert(0,str(Path(".github/scripts").resolve()))
from e2e_m01 import sql_and_http
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def audit():
    t=(ROOT/"TEORIA/M02_TEORIA.md").read_text(encoding="utf-8")
    p=(ROOT/"PRACTICAS/M02_PRACTICAS.md").read_text(encoding="utf-8")
    blocks=len(re.findall(r"^### Bloque \d+ —",t,re.M))
    steps=re.findall(r"^### PASO (2\.[1-4]\.\d+) —",p,re.M)
    assert blocks==40,(blocks,"bloques esperados 40")
    assert len(steps)==96,(len(steps),"pasos esperados 96")
    assert len(set(steps))==96
    report={"ok":True,"bloques":blocks,"pasos":len(steps),"matriz":[],"docs_heredados":0,"archivos_heredados":0}
    previous=Path("M01_INTRODUCCION_MICROSERVICIOS/PROYECTO/1.5-buenas-practicas")
    for i,slug in enumerate(STAGES):
        cur=ROOT/"PROYECTO"/slug
        assert (cur/"AceriaApp.sln").exists(),cur
        assert len(list(cur.rglob("*.csproj")))==7+i,slug
        for f in (previous/"docs").glob("*.md"):
            dst=cur/"docs"/f.name
            assert dst.exists() and digest(dst)==digest(f),f"{slug}: documento heredado distinto {f.name}"
            report["docs_heredados"]+=1
        if i:
            for f in previous.rglob("*"):
                if not f.is_file() or any(x in ("bin","obj",".vs","TestResults") for x in f.parts):continue
                rel=f.relative_to(previous)
                if rel.as_posix() in ("README.md","AceriaApp.sln","src/AceriaApp.Monolito.Api/Program.cs","src/AceriaApp.Monolito.Api/AceriaApp.Monolito.Api.csproj"):continue
                dst=cur/rel
                assert dst.exists() and digest(dst)==digest(f),f"{slug}: herencia alterada {rel}"
                report["archivos_heredados"]+=1
        text=p.split(f"## Punto 2.{i+1} —",1)[1]
        if i<3:text=text.split(f"## Punto 2.{i+2} —",1)[0]
        headings=list(re.finditer(r"^### PASO 2\.\d+\.(\d+) — (.*)$",text,re.M))
        nums=[int(x.group(1)) for x in headings]
        assert nums==list(range(1,25)),(slug,nums)
        for j,h in enumerate(headings):
            body=text[h.end():headings[j+1].start() if j+1<len(headings) else len(text)]
            matches=re.findall(r"^\*\*Acción (\d+):\*\*",body,re.M)
            assert len(matches)>=4,(slug,j+1,len(matches))
            assert ("**Por qué se hace:**" in body and "**Errores comunes:**" in body and "**Verificación:**" in body)
            refs=re.findall(r"^\*\*Acción 2:\*\* Localizar "+re.escape(chr(96))+r"([^"+re.escape(chr(96))+r"]+)"+re.escape(chr(96)),body,re.M)
            assert len(refs)==1,(slug,j+1,"falta referencia única")
            target=cur/refs[0]
            assert target.exists(),(slug,j+1,"ruta inexistente",refs[0])
            report["matriz"].append({"punto":f"2.{i+1}","paso":j+1,"referencia":refs[0],"existe":True,"tipo":"manual+compilacion"})
        previous=cur
    for banned in ("53 minutos","26 minutos","27 minutos","metaprompt.md","verificacion.md"):
        assert banned not in t and banned not in p,banned
    return report
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("static","sql"),default="static")
    ap.add_argument("--point",choices=STAGES)
    ap.add_argument("--out",default="m02-e2e-evidencia.json")
    args=ap.parse_args()
    results=audit()
    if args.mode=="sql":
        assert args.point,"--point obligatorio en SQL"
        target=ROOT/"PROYECTO"/args.point
        with tempfile.TemporaryDirectory(prefix="aceria-m02-sql-") as work:
            results["sql_http"]=sql_and_http(target,args.point,STAGES.index(args.point),Path(work))
    Path(args.out).write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({k:v for k,v in results.items() if k!="matriz"},ensure_ascii=False))
if __name__=="__main__":main()
