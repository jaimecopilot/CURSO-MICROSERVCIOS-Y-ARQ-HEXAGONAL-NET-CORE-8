#!/usr/bin/env python3
"""Audita M03.1-M08.1 desde el módulo anterior, sin copiar el punto de destino.

Busca operaciones faltantes entre la etapa final del módulo N-1 y la primera
etapa N.1. Es diagnóstico: no declara PASS si faltan instrucciones o archivos.
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
import sys

from auditar_reconstruccion_practicas import (
    CONFIG, ROOT, apply_marked_operations, check_generated_solution, files,
    manual_section, norm, steps_and_operations,
)

def inspect(module: int):
    if module not in CONFIG or module < 3:
        raise ValueError("Solo se audita continuidad M02→M03 ... M07→M08")
    prev_folder, prev_stages = CONFIG[module-1]
    this_folder, this_stages = CONFIG[module]
    previous = files(ROOT / prev_folder / "PROYECTO" / prev_stages[-1])
    actual = files(ROOT / this_folder / "PROYECTO" / this_stages[0])
    doc_path = ROOT / this_folder / "PRACTICAS" / f"M{module:02}_PRACTICAS.md"
    doc = doc_path.read_text(encoding="utf-8-sig")
    _, ops = steps_and_operations(module, ROOT / this_folder, this_stages)
    constructed, errors = apply_marked_operations(previous, ops[1])
    mark_paths = {operation["ruta"] for operation in ops[1]}
    diffs = {rel for rel in previous.keys() | actual.keys()
             if norm(previous.get(rel, "")) != norm(actual.get(rel, ""))}
    unmarked = sorted(diffs - mark_paths - {"AceriaApp.sln"})
    incorrect = sorted(rel for rel in diffs & mark_paths
                       if norm(constructed.get(rel, "")) != norm(actual.get(rel, "")))
    exact = sorted(rel for rel in diffs - {"AceriaApp.sln"}
                   if norm(constructed.get(rel, "")) == norm(actual.get(rel, "")))
    sln_ok = False
    sln_explanation = "sin cambios"
    if "AceriaApp.sln" in diffs:
        sln_ok, sln_explanation = check_generated_solution(
            previous, constructed, actual, manual_section(doc,module,1))
    if unmarked or incorrect or errors or ("AceriaApp.sln" in diffs and not sln_ok):
        state="PENDIENTE DE CORRECCION"
    else:
        state="PARIDAD DE OPERACIONES OK; COMPILACION E2E NO EJECUTADA"
    result = {
        "module":module,"transition":f"M{module-1:02} final → M{module:02}.1",
        "changed_files":len(diffs),"exact_text_reconstruction":len(exact),
        "solution_member_verified":sln_ok,"solution_explanation":sln_explanation,
        "unmarked":unmarked,"marked_but_different":incorrect,"apply_errors":errors,
        "state":state
    }
    print(result,flush=True)
    return result

def materializar_limite(module: int, target: Path) -> dict:
    """Reconstruye Mx.1 desde M(x-1) final usando solo operaciones del nuevo manual.

    Permite el caso M03.1 donde el módulo anterior no tenía AceriaApp.sln:
    ejecuta dotnet new sln y registra los proyectos heredados y creados.
    Nunca utiliza el contenido del proyecto destino para construirlo.
    """
    if module not in CONFIG or module < 3:
        raise ValueError("Solo M03..M08")
    prev_folder, prev_stages = CONFIG[module-1]
    this_folder, this_stages = CONFIG[module]
    prev_root = ROOT / prev_folder / "PROYECTO" / prev_stages[-1]
    canonical_root = ROOT / this_folder / "PROYECTO" / this_stages[0]
    previous = files(prev_root)
    canonical = files(canonical_root)
    _, bypoint = steps_and_operations(module,ROOT / this_folder,this_stages)
    constructed, errors = apply_marked_operations(previous,bypoint[1])
    if errors:
        raise RuntimeError(f"No se pudo aplicar M{module:02}.1: {errors}")
    changed = {key for key in previous.keys() | canonical.keys()
               if norm(previous.get(key,"")) != norm(canonical.get(key,""))}
    marked={operation["ruta"] for operation in bypoint[1]}
    unexpected=sorted(changed - marked - {"AceriaApp.sln"})
    if unexpected:
        raise RuntimeError(f"M{module:02}.1 tiene cambios no documentados: {unexpected}")
    inconsistent=sorted(key for key in changed - {"AceriaApp.sln"}
                        if norm(constructed.get(key,"")) != norm(canonical.get(key,"")))
    if inconsistent:
        raise RuntimeError(f"M{module:02}.1 difiere del manual: {inconsistent}")
    manual=(ROOT/this_folder/"PRACTICAS"/f"M{module:02}_PRACTICAS.md").read_text(
        encoding="utf-8-sig")
    if "AceriaApp.sln" in changed:
        valid,why=check_generated_solution(
            previous,constructed,canonical,manual_section(manual,module,1))
        if not valid:
            raise RuntimeError(f"Solución M{module:02}.1 no documentada: {why}")
    if target.exists():
        raise FileExistsError(f"El destino de prueba ya existe: {target}")
    shutil.copytree(prev_root,target,ignore=shutil.ignore_patterns(
        "bin","obj","TestResults","_test_results","_trx",".qa"
    ))
    for rel in changed - {"AceriaApp.sln"}:
        dest=target/rel
        if rel not in constructed:
            dest.unlink(missing_ok=True)
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(constructed[rel],encoding="utf-8")
    previous_projects={p for p in previous if p.endswith(".csproj")}
    current_projects={p for p in constructed if p.endswith(".csproj")}
    if "AceriaApp.sln" in changed:
        if "AceriaApp.sln" not in previous:
            result=subprocess.run(
                ["dotnet","new","sln","-n","AceriaApp"],
                cwd=target,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                text=True,encoding="utf-8",errors="replace",timeout=150
            )
            if result.returncode:
                raise RuntimeError("No pudo crearse la solución: "+result.stdout[-1500:])
            projects=sorted(current_projects)
        else:
            projects=sorted(current_projects - previous_projects)
        if projects:
            result=subprocess.run(
                ["dotnet","sln","AceriaApp.sln","add",*projects],
                cwd=target,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                text=True,encoding="utf-8",errors="replace",timeout=150
            )
            if result.returncode:
                raise RuntimeError("No pudo completarse .sln: "+result.stdout[-2000:])
    built=files(target)
    if set(built)!=set(canonical):
        raise RuntimeError(
            f"M{module:02}.1: faltan {sorted(set(canonical)-set(built))}, "
            f"sobran {sorted(set(built)-set(canonical))}"
        )
    from auditar_reconstruccion_practicas import solution_paths
    for rel in built:
        if rel=="AceriaApp.sln":
            if solution_paths(built[rel]) != solution_paths(canonical[rel]):
                raise RuntimeError(f"M{module:02}.1: membresía .sln distinta")
        elif norm(built[rel])!=norm(canonical[rel]):
            raise RuntimeError(f"M{module:02}.1: archivo no coincide {rel}")
    report={"module":module,"transition":f"M{module-1:02} final → M{module:02}.1",
            "files":len(built),"updated":len(changed),"new_projects":
            sorted(current_projects-previous_projects),"state":"PASS"}
    print("LIMITE RECONSTRUIDO "+json.dumps(report,ensure_ascii=False),flush=True)
    return report


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--materializar", action="store_true",
                    help="Reconstruye físicamente todos los primeros puntos, sin usar destinos")
    ap.add_argument("--strict", action="store_true",
                    help="Si hay diferencias en primeros puntos, fallar")
    ap.add_argument("--report",type=Path,default=ROOT/"AUDITORIA_CONTINUIDAD_MODULAR.md")
    args=ap.parse_args()
    results=[inspect(n) for n in range(3,9)]
    if args.materializar:
        for n in range(3,9):
            with tempfile.TemporaryDirectory(prefix=f"limite_m{n:02}_") as temp:
                materializar_limite(n, Path(temp)/f"M{n:02}_1")
        print("PASS: 6/6 primeras etapas reconstruidas desde el módulo anterior",flush=True)
    lines=[
        "# Continuidad entre módulos — M02→M03 hasta M07→M08",
        "",
        "Este informe parte del **proyecto canónico final anterior**, aplica únicamente "
        "operaciones marcadas en el primer punto de las nuevas prácticas, compara "
        "con el proyecto de referencia y detecta diferencias. No reconstruye M01 "
        "desde vacío, no modifica código C#, no realiza E2E y no prueba clics de Visual Studio.",
        "",
        "| Transición | Cambios de archivo | Reconstruidos | Solución .sln | Estado |",
        "|---|---:|---:|---|---|"
    ]
    for r in results:
        lines.append(
            f"| {r['transition']} | {r['changed_files']} | "
            f"{r['exact_text_reconstruction']} | "
            f"{'Paridad' if r['solution_member_verified'] else r['solution_explanation']} | "
            f"{r['state']} |"
        )
    for r in results:
        lines+=["",f"## {r['transition']}","",
                f"**Estado:** {r['state']}.",
                f"**Solución:** {r['solution_explanation']}.",""]
        for field,subtitle in [
            ("unmarked","Cambios sin instrucción de escritura marcada"),
            ("marked_but_different","Operaciones marcadas con resultado distinto"),
            ("apply_errors","Instrucciones que no se pudieron aplicar"),
        ]:
            values=r[field]
            lines.extend([f"### {subtitle} ({len(values)})",""])
            if values:lines.extend(f"- {x}" for x in values)
            else:lines.append("Sin diferencias detectadas por este auditor.")
            lines.append("")
    args.report.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"INFORME: {args.report}",flush=True)
    if args.strict and any("OK" not in r["state"] for r in results):
        raise SystemExit("Falta continuidad de primer punto en uno o más módulos")
if __name__=="__main__":
    main()
