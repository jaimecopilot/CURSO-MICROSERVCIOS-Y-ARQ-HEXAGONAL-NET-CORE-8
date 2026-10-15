#!/usr/bin/env python3
"""Construye vista docente SIN abreviar la fuente; originales inmutables.

No modifica fuentes ni produce material final sin los cuatro puntos.
--parcial genera únicamente vistas parciales, explícitamente identificadas.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from pedagogia_m02 import aplicar as aplicar_pedagogia

SRC = Path(".github/fuentes-originales/m02")
WORDS_RE = re.compile(r"\b[\wÁÉÍÓÚÜÑáéíóúüñ]+\b", re.UNICODE)
POINTS = ("2.1", "2.2", "2.3", "2.4")
HEAD = {
    "2.1": "Diseño de APIs REST",
    "2.2": "Recursos, verbos HTTP y códigos de respuesta",
    "2.3": "Validación de peticiones",
    "2.4": "Documentación mediante OpenAPI (Swagger)",
}
STRIP_LINES = re.compile(
    r"^(?:Duración:|PARTE TEÓRICA \(|PARTE PRÁCTICA \(|"
    r"Espero confirmación del usuario antes de continuar con el punto )"
)

def grab(point: str):
    path = SRC/f"punto-{point}.md"
    if not path.is_file():
        return None
    raw = path.read_text(encoding="utf-8")
    a = re.search(r"(?m)^PARTE TEÓRICA \([^\n]+\)\s*$", raw)
    b = re.search(r"(?m)^PARTE PRÁCTICA \([^\n]+\)\s*$", raw)
    if a is None or b is None or a.end() >= b.start():
        raise ValueError(f"{path}: delimitadores ausentes o invertidos")
    theory, practical = raw[:b.start()], raw[b.end():]
    blocks = [int(x) for x in re.findall(r"(?m)^Bloque (\d+) —", theory)]
    steps = [int(x) for x in re.findall(r"(?m)^Paso (\d+) —", practical)]
    if blocks != list(range(1,11)) or steps != list(range(1,25)):
        raise ValueError(f"{point}: {blocks=} / {steps=}; falta contenido original")
    return dict(
        point=point, sha256=hashlib.sha256(raw.encode()).hexdigest(),
        original_chars=len(raw), original_words=len(WORDS_RE.findall(raw)),
        theory=theory, practice=practical, blocks=len(blocks), steps=len(steps),
        path=str(path)
    )

def heading_and_items(text: str, point: str, is_practice: bool):
    """Transforma únicamente sintaxis, mantiene las frases originales."""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if STRIP_LINES.match(s):
            continue
        if s == f"Punto {point} — {HEAD[point]}":
            out.append(f"## Punto {point} — {HEAD[point]}")
        elif re.fullmatch(r"Bloque (\d+) — (.+)", s):
            m = re.fullmatch(r"Bloque (\d+) — (.+)", s)
            out.append(f"### Bloque {m.group(1)} — {m.group(2)}")
        elif re.fullmatch(r"Paso (\d+) — (.+)", s) and is_practice:
            m = re.fullmatch(r"Paso (\d+) — (.+)", s)
            out.append(f"### PASO {point}.{m.group(1)} — {m.group(2)}")
        elif s in ("Resumen rápido de la teoría","Errores comunes del ejercicio completo",
                   "Reto resuelto paso a paso", "Resultado esperado",
                   "Conclusión y enlace al siguiente punto"):
            out.append("### "+s)
        elif re.match(r"^Acción \d+:", s):
            m=re.match(r"^Acción (\d+):\s*(.*)", s)
            out.append(f"- **Acción {m.group(1)}:** {m.group(2)}")
        elif re.match(r"^Línea \d+:", s):
            m=re.match(r"^Línea (\d+):\s*(.*)", s)
            out.append(f"- **Línea {m.group(1)}:** {m.group(2)}")
        elif s.startswith("· "):
            out.append("- "+s[2:])
        elif s.startswith("Por qué se hace:"):
            out.append("**Por qué se hace:**"+line.split(":",1)[1])
        elif s.startswith("Errores comunes:"):
            out.append("**Errores comunes:**"+line.split(":",1)[1])
        elif s.startswith("Verificación:"):
            out.append("**Verificación:**"+line.split(":",1)[1])
        elif s == "PARTE TEÓRICA (26 minutos)" or s == "PARTE PRÁCTICA (27 minutos)":
            continue
        else:
            out.append(line)
    return "\n".join(out).strip()+"\n"



def enmarcar_codigo(text: str, practicas: bool):
    """Marcado de ejemplos literales como bloques, sin modificar líneas fuente."""
    lines=text.splitlines()
    out=[]
    in_code=False
    in_existing_fence=False
    for i,line in enumerate(lines):
        s=line.strip()
        if s.startswith("```"):
            # Respeta fences aportados literalmente por el usuario, especialmente 2.4.
            if in_code:
                out.append("```")
                in_code=False
            in_existing_fence=not in_existing_fence
            out.append(line)
            continue
        if in_existing_fence:
            out.append(line)
            continue
        is_action=bool(re.match(r"^- \*\*Acción \d+:\*\*",s))
        is_reto=bool(re.match(r"^Paso \d+:",s))
        if in_code and (is_action or is_reto or (not practicas and s.startswith("- **Línea 1:**"))):
            out.append("```")
            out.append("")
            in_code=False
        opener=None
        if practicas:
            if (is_action and
                    ("Escribir exactamente el siguiente código:" in s or
                     "Escribir exactamente el siguiente contenido:" in s)):
                opener="markdown" if "contenido:" in s else "csharp"
            elif is_reto and any(k in s for k in (
                  "siguiente record", "siguiente método", "siguiente test", "siguiente código")):
                opener="csharp"
        elif not in_code:
            # Ejemplos concretos seguidos de una explicación 'Línea 1'.
            is_code=(s.startswith("public record ") or s.startswith("var builder ") or
                     s.startswith("app.Map") or s.startswith("// El cliente envía:") or
                     (s=="{" and i+1<len(lines) and
                      re.match(r'^\s*"(?:type|items|id)"',lines[i+1])))
            if is_code and any("- **Línea 1:**" in t for t in lines[i+1:i+65]):
                opener="json" if s=="{" else "csharp"
        if opener and not in_code:
            # Si el ejemplo original ya comienza con un fence Markdown, no
            # crear otro bloque vacío encima de él.
            next_nonempty=next((z.strip() for z in lines[i+1:] if z.strip()),"")
            if next_nonempty.startswith("```"):
                out.append(line)
                continue
            if practicas:
                out.append(line)
                out.append("")
                out.append("```"+opener)
            else:
                out.append("```"+opener)
                out.append(line)
            in_code=True
        else:
            out.append(line)
    if in_code:out.append("```")
    return "\n".join(out)+"\n"

def aplicar_erratas(text: str, point: str, tipo: str):
    """Solo erratas aprobadas para la vista docente; no toca fuentes."""
    applied = []
    if tipo == "PRACTICAS":
        cambios = {
            "2.1": [("con ocho proyectos","con siete proyectos")],
            "2.2": [
                ("con nueve proyectos","con ocho proyectos"),
                ("los diez documentos","los once documentos"),
                ("diez documentos","once documentos")
            ]
        }
        for before, after in cambios.get(point,[]):
            n=text.count(before)
            if n:
                text=text.replace(before,after)
                applied.append(dict(antes=before,despues=after,veces=n))
    return text, applied

def canonical_tokens(s: str):
    """No acepta que desaparezcan frases: elimina solo marcas visuales."""
    # Los encabezados PASO pasan de 2.x.n a n, respetando títulos.
    s = re.sub(r"(?m)^### PASO 2\.[1-4]\.(\d+) —",r"Paso \1 —",s)
    s = re.sub(r"(?m)^### Bloque (\d+) —",r"Bloque \1 —",s)
    s = re.sub(r"(?m)^## Punto ", "Punto ",s)
    s = re.sub(r"(?m)^### (Resumen rápido de la teoría|Errores comunes del ejercicio completo|Reto resuelto paso a paso|Resultado esperado|Conclusión y enlace al siguiente punto)",r"\1",s)
    s = re.sub(r"(?m)^- \*\*Acción (\d+):\*\*",r"Acción \1:",s)
    s = re.sub(r"(?m)^- \*\*Línea (\d+):\*\*",r"Línea \1:",s)
    s = re.sub(r"(?m)^- ", "· ",s)  # puede afectar a guiones literales originales
    s = re.sub(r"(?m)^\*\*(Por qué se hace|Errores comunes|Verificación):\*\*",r"\1:",s)
    s = "\n".join(l for l in s.splitlines() if not STRIP_LINES.match(l.strip()))
    # No se aplica comparación de guiones sin contextualizar; se hace por líneas.
    return s

def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("--parcial", action="store_true")
    arg.add_argument("--salida", type=Path, default=Path("previsualizacion_m02"))
    a=arg.parse_args()
    docs=[grab(point) for point in POINTS]
    missing=[point for point,doc in zip(POINTS,docs) if doc is None]
    ready=[doc for doc in docs if doc]
    if missing and not a.parcial:
        raise SystemExit("NO GENERAR MATERIAL FINAL: faltan fuentes completas: "+", ".join(missing))
    if not ready:
        raise SystemExit("No hay fuentes")
    a.salida.mkdir(parents=True,exist_ok=True)
    theory=["# M02 — Teoría de desarrollo de APIs REST\n\n**Autor: JAIME GALLO**\n"]
    practice=["# M02 — Prácticas de desarrollo de APIs REST\n\n**Autor: JAIME GALLO**\n"]
    report={"es_material_final":not missing,"fuentes_presentes":[],"faltan":missing}
    for doc in ready:
        p=doc["point"]
        theory_fragment=enmarcar_codigo(heading_and_items(doc["theory"],p,False),False)
        practice_fragment="## Punto "+p+" — "+HEAD[p]+"\n\n"+enmarcar_codigo(heading_and_items(doc["practice"],p,True),True)
        theory_fragment, ct = aplicar_erratas(theory_fragment,p,"TEORIA")
        practice_fragment, cp = aplicar_erratas(practice_fragment,p,"PRACTICAS")
        practice_fragment, extras = aplicar_pedagogia(practice_fragment,p,"PRACTICAS")
        doc["correcciones_aplicadas"]=ct+cp+extras
        theory.append(theory_fragment)
        practice.append(practice_fragment)
        report["fuentes_presentes"].append({
            k:v for k,v in doc.items() if k not in ("theory","practice")
        })
    theory_text="\n\n---\n\n".join(theory)
    practice_text="\n\n---\n\n".join(practice)
    expected_blocks=10*len(ready)
    expected_steps=24*len(ready)
    actual_blocks=len(re.findall(r"(?m)^### Bloque \d+ —",theory_text))
    actual_steps=len(re.findall(r"(?m)^### PASO 2\.[1-4]\.\d+ —",practice_text))
    if actual_blocks!=expected_blocks or actual_steps!=expected_steps:
        raise ValueError(f"Salida incompleta: {actual_blocks}/{expected_blocks} bloques; {actual_steps}/{expected_steps} pasos")
    label="M02" if not missing else "M02_PREVISUALIZACION_INCOMPLETA"
    for name,contents in [("TEORIA",theory_text),("PRACTICAS",practice_text)]:
        (a.salida/f"{label}_{name}.md").write_text(contents,encoding="utf-8")
    (a.salida/"INFORME.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(dict(complete=not missing, present=[x["point"] for x in ready],
                          missing=missing, blocks=actual_blocks, steps=actual_steps),ensure_ascii=False))
    if missing:
        print("ADVERTENCIA: vistas parciales. No publicarlas como material definitivo.")

if __name__=="__main__":
    main()
