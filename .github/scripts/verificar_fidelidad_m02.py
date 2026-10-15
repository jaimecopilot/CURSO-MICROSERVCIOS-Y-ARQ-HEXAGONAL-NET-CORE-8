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
def fences_no_alterados(parts, category, index):
    text=parts[0 if category=="TEORIA" else 1]
    if category!="PRACTICAS" or index!=3:
        return fences(text)
    # 2.4: se reescribieron SOLO estos pasos, sus bloques de
    # documentación asociados y el reto, según las correcciones aprobadas.
    approved={4,6,9,13,15,19,20}
    result=[]
    for m in re.finditer(r"```[^\n]*\n(.*?)\n```",text,flags=re.S):
        previous=text[:m.start()]
        positions=re.findall(r"(?m)^Paso (\d+) —",previous)
        n=int(positions[-1]) if positions else None
        if "Reto resuelto paso a paso" in previous and previous.rfind("Reto resuelto paso a paso")>previous.rfind("Paso 24 —"):
            continue
        if n not in approved:
            result.append(m.group(1).strip())
    return result

def primeros_parrafos(teoria):
    # Cada uno de los diez bloques tiene un primer párrafo didáctico
    # cuya redacción NO puede perderse ni sustituirse por síntesis.
    for match in re.finditer(r"(?m)^Bloque \d+ —[^\n]+\s*\n\s*\n([^\n]{80,})",teoria):
        yield match.group(1).strip()

def sections(raw):
    a=re.search(r"(?im)^\s*PARTE TE[ÓO]RICA\b",raw)
    b=re.search(r"(?im)^\s*PARTE PR[ÁA]CTICA\b",raw)
    if a is None or b is None or b.start()<=a.start(): raise ValueError("falta separación teoría/práctica")
    return raw[a.end():b.start()],raw[b.end():]
def activar_codigo_heredado(source):
    """El estado siguiente DESCOMENTA el código del punto anterior.
    Es una transición didáctica intencionada, no una mutación arbitraria."""
    out=[]
    inside=False
    for line in source.splitlines():
        if re.match(r"^// INICIO PASO \d+\.\d+",line):
            inside=True
            continue
        if inside and re.match(r"^// FIN PASO \d+\.\d+",line):
            inside=False
            continue
        if inside:
            if line.startswith("// "):
                line=line[3:]
            elif line=="//":
                line=""
        out.append(line)
    return "\n".join(out)

def normalize_code(source):
    return "\n".join(x.strip() for x in source.splitlines() if x.strip())

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
            if old.is_file():
                if old.read_bytes()==cs.read_bytes():
                    continue
                original=old.read_text(encoding="utf-8")
                # Cada copia autónoma hereda el código ACTIVADO del estado anterior.
                if normalize_code(activar_codigo_heredado(original)) == normalize_code(cs.read_text(encoding="utf-8")):
                    continue
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
            original_code=[code for i,parts in enumerate(sections_all) for code in fences_no_alterados(parts,category,i)]
            result=normalise(content)
            missing=[i for i,c in enumerate(original_code,1) if normalise(c) not in result]
            if missing:
                problems.append(f"{name}: {len(missing)} ejemplos originales no afectados por las correcciones están ausentes. Índices: {missing[:15]}")
            if category=="TEORIA":
                for i,parts in enumerate(sections_all,1):
                    first=list(primeros_parrafos(parts[0]))
                    if len(first)!=10:
                        problems.append(f"2.{i}: solo se detectan {len(first)} primeros párrafos teóricos")
                    elif any(normalise(p) not in result for p in first):
                        problems.append(f"2.{i}: han desaparecido párrafos originales de teoría")
            if category=="PRACTICAS":
                for term in ("DocumentacionExtensionsTests", "EsEntornoDeProduccion",
                             "ValidacionExtensions", "Cincuenta y una pruebas",
                             "equipo@acerialocal", "FluentValidation.DependencyInjectionExtensions"):
                    if term.casefold() not in content.casefold():
                        problems.append(f"{name}: falta corrección técnica aprobada: {term}")
                if content.count("for %f in")!=3:
                    problems.append(f"{name}: no se compara todo docs en 2.2, 2.3 y 2.4")
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
