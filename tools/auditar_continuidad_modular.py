#!/usr/bin/env python3
"""Audita M03.1-M08.1 desde el módulo anterior, sin copiar el punto de destino.

Busca operaciones faltantes entre la etapa final del módulo N-1 y la primera
etapa N.1. Es diagnóstico: no declara PASS si faltan instrucciones o archivos.
"""
from __future__ import annotations
import argparse
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

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="Si hay diferencias en primeros puntos, fallar")
    ap.add_argument("--report",type=Path,default=ROOT/"AUDITORIA_CONTINUIDAD_MODULAR.md")
    args=ap.parse_args()
    results=[inspect(n) for n in range(3,9)]
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
