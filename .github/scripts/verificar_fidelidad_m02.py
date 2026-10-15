#!/usr/bin/env python3
"""Puerta de fidelidad M02: no modifica los materiales ni certifica la progresión."""
from __future__ import annotations
import argparse,json,re,sys,unicodedata
from pathlib import Path
ROOT=Path("M02_APIS_REST_ASPNET_CORE")
SOURCES=Path(".github/fuentes-originales/m02")
SLUGS=["2.1-diseno-apis-rest","2.2-recursos-verbos-codigos","2.3-validacion-peticiones","2.4-documentacion-openapi"]
def normalise(s):
    s=unicodedata.normalize("NFC",s).casefold()
    s=re.sub(r"(?m)^\s*(duraci[oó]n:.*|parte te[oó]rica \(.*minutos\)|parte pr[aá]ctica \(.*minutos\))$","",s)
    s=re.sub(r"[`*_#|]"," ",s)
    return re.sub(r"\s+"," ",s).strip()
def fences(s):
    return [m.strip() for m in re.findall(r"```[^\n]*\n(.*?)\n```",s,flags=re.S)]
def sections(raw):
    a=re.search(r"(?im)^\s*PARTE TE[ÓO]RICA\b",raw)
    b=re.search(r"(?im)^\s*PARTE PR[ÁA]CTICA\b",raw)
    if a is None or b is None or b.start()<=a.start(): raise ValueError("falta separación teoría/práctica")
    return raw[a.end():b.start()],raw[b.end():]
def check_markers(root):
    errors=[]
    for i,slug in enumerate(SLUGS):
        dest=root/ROOT/"PROYECTO"/slug
        previous=root/(ROOT/"PROYECTO"/SLUGS[i-1] if i else Path("M01_INTRODUCCION_MICROSERVICIOS/PROYECTO/1.5-buenas-practicas"))
        if not dest.is_dir() or not previous.is_dir():
            errors.append(f"{slug}: falta carpeta actual o anterior");continue
        for cs in dest.rglob("*.cs"):
            if any(p in ("obj","bin",".vs") for p in cs.parts):continue
            rel=cs.relative_to(dest);old=previous/rel
            if old.is_file() and old.read_bytes()==cs.read_bytes():continue
            s=cs.read_text(encoding="utf-8")
            starts=re.findall(r"(?m)^// INICIO PASO (2\.[1-4]\.\d+)",s)
            ends=re.findall(r"(?m)^// FIN PASO (2\.[1-4]\.\d+)",s)
            if not starts or sorted(starts)!=sorted(ends):
                errors.append(f"{slug}: {rel}: código nuevo/modificado sin INICIO/FIN PASO equilibrados")
            elif any(not x.startswith(f"2.{i+1}.") for x in starts):
                errors.append(f"{slug}: {rel}: etiquetas de otros puntos")
    return errors
def run(root):
    problems=[]
    originals=[root/SOURCES/f"punto-2.{i}.md" for i in range(1,5)]
    for p in originals:
        if not p.is_file():problems.append(f"Falta copia LITERAL de la fuente: {p.relative_to(root)}")
    sections_all=[]
    for p in originals:
        if not p.is_file():continue
        try:
            theory,practice=sections(p.read_text(encoding="utf-8"))
            b=len(re.findall(r"(?im)^\s*Bloque\s+\d+\s+[—-]",theory))
            n=len(re.findall(r"(?im)^\s*Paso\s+\d+\s+[—-]",practice))
            if b!=10 or n!=24:problems.append(f"{p.name}: {b} bloques / {n} pasos; se esperan 10 / 24")
            sections_all.append((theory,practice))
        except ValueError as e:problems.append(f"{p.name}: {e}")
    for category,name,expected in [("TEORIA","M02_TEORIA.md",40),("PRACTICAS","M02_PRACTICAS.md",96)]:
        p=root/ROOT/category/name
        if not p.is_file():problems.append(f"Falta {p.relative_to(root)}");continue
        content=p.read_text(encoding="utf-8")
        header=r"(?m)^### Bloque \d+\s+[—-]" if category=="TEORIA" else r"(?m)^### PASO 2\.[1-4]\.\d+\s+[—-]"
        n=len(re.findall(header,content))
        if n!=expected:problems.append(f"{name}: {n} apartados, esperados {expected}")
        if len(sections_all)==4:
            original_code=[code for parts in sections_all for code in fences(parts[0 if category=="TEORIA" else 1])]
            result=normalise(content)
            missing=[i for i,c in enumerate(original_code,1) if normalise(c) not in result]
            if missing:
                problems.append(f"{name}: {len(missing)} ejemplos originales ausentes/alterados; comprobar correcciones aprobadas. Índices: {missing[:15]}")
    problems.extend(check_markers(root))
    return {"ok":not problems,"fuentes_originales":sum(p.is_file() for p in originals),
            "fuentes_requeridas":4,"errores":problems,
            "pendiente":"E2E 96 pasos: activar bloque comentado, compilar, probar cada estado en copia temporal"}
def main():
    a=argparse.ArgumentParser();a.add_argument("--root",type=Path,default=Path("."))
    a.add_argument("--out",type=Path,default=Path("m02-fidelidad.json"));args=a.parse_args()
    result=run(args.root.resolve())
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="errores"},ensure_ascii=False))
    for x in result["errores"][:25]:print("NO CERTIFICADO:",x)
    if len(result["errores"])>25:print("Más hallazgos en",args.out)
    return 0 if result["ok"] else 1
if __name__=="__main__":sys.exit(main())
