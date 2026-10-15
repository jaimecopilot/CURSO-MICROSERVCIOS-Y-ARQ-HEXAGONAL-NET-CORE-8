#!/usr/bin/env python3
"""Ejecución pedagógica M02 2.1-2.4: 24 estados por punto, en copias temporales.
No altera los proyectos del alumno ni certifica la fidelidad de los Markdown.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import subprocess
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path("M02_APIS_REST_ASPNET_CORE/PROYECTO")
SLUGS = {"2.1": "2.1-diseno-apis-rest", "2.2": "2.2-recursos-verbos-codigos", "2.3": "2.3-validacion-peticiones", "2.4": "2.4-documentacion-openapi"}
TOTAL = {"2.1": 31, "2.2": 36, "2.3": 42, "2.4": 51}
STEPS = {"2.1": {6, 8, 10, 15, 16, 17}, "2.2": {6, 7, 9, 14, 15}, "2.3": {7, 8, 9, 14, 15, 16}, "2.4": {6, 7, 9, 13, 14, 15}}


def shell(args, cwd, timeout=400):
    t = time.monotonic()
    p = subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    result = dict(command=" ".join(args), code=p.returncode,
                  seconds=round(time.monotonic()-t, 3), tail=(p.stdout+p.stderr)[-1800:])
    if p.returncode:
        raise RuntimeError(json.dumps(result, ensure_ascii=False))
    return result


def activate(folder: Path, point: str, step: int):
    key = f"{point}.{step}"
    start = f"// INICIO PASO {key} "
    end = f"// FIN PASO {key}"
    changed = []
    for file in sorted(folder.rglob("*.cs")):
        content = file.read_text(encoding="utf-8")
        lines = content.splitlines(keepends=True)
        out, active, found = [], False, False
        for line in lines:
            if line.startswith(start):
                if active:
                    raise RuntimeError(f"Inicio anidado: {file}")
                active, found = True, True
                out.append(line)
            elif line.strip() == end:
                if not active:
                    raise RuntimeError(f"Fin sin inicio: {file}")
                active = False
                out.append(line)
            elif active:
                if line.startswith("// "):
                    out.append(line[3:])
                elif line.strip() == "//":
                    out.append("\n")
                else:
                    raise RuntimeError(f"Línea no comentada antes de activar: {file}")
            else:
                out.append(line)
        if active:
            raise RuntimeError(f"Marcador sin cerrar: {file}")
        if found:
            file.write_text("".join(out), encoding="utf-8")
            changed.append(str(file.relative_to(folder)))
    return changed



def deactivate_legacy_swagger(folder: Path):
    """El alumno comenta los registros y endpoints anteriores al activar el paso 2.4.9."""
    target = folder/"src/AceriaApp.Monolito.Api/Program.cs"
    lines = target.read_text(encoding="utf-8").splitlines(keepends=True)
    output, inactive, count = [], False, 0
    for line in lines:
        if line.startswith("// INICIO SUSTITUCION PASO 2.4.9"):
            if inactive:
                raise RuntimeError("Sustitución anidada")
            inactive, count = True, count+1
            output.append(line)
        elif line.strip() == "// FIN SUSTITUCION PASO 2.4.9":
            if not inactive:
                raise RuntimeError("Cierre de sustitución sin inicio")
            inactive = False
            output.append(line)
        elif inactive and line.strip():
            output.append("// "+line)
        elif inactive:
            output.append("//\n")
        else:
            output.append(line)
    if inactive or count != 4:
        raise RuntimeError(f"Se esperaban 4 fragmentos heredados a desactivar: {count}")
    target.write_text("".join(output), encoding="utf-8")


def run_tests(folder: Path, expected: int):
    with tempfile.TemporaryDirectory(prefix="m02-trx-") as temp:
        paths = sorted(folder.glob("tests/*/*.csproj"))
        passed = 0
        for file in paths:
            name = file.stem + ".trx"
            shell(["dotnet", "test", str(file), "-c", "Release",
                   "--no-build", "--no-restore", "--logger",
                   f"trx;LogFileName={name}", "--results-directory", temp],
                  folder, timeout=300)
            xml = ET.parse(Path(temp)/name).getroot()
            counters = xml.find(".//{*}ResultSummary/{*}Counters")
            if counters is None:
                raise RuntimeError("TRX sin contadores: "+name)
            p, total, failed = (int(counters.get(k, -1)) for k in ("passed", "total", "failed"))
            if p != total or failed != 0:
                raise RuntimeError(f"{name}: {p}/{total} correctos y {failed} fallos")
            passed += p
        if passed != expected:
            raise RuntimeError(f"Se esperaban {expected} pruebas, encontradas {passed}")
        return {"projects": len(paths), "passed": passed}


def main():
    cli = argparse.ArgumentParser()
    cli.add_argument("--point", required=True, choices=tuple(SLUGS))
    cli.add_argument("--root", type=Path, default=Path("."))
    args = cli.parse_args()
    root = args.root.resolve()
    point = args.point
    source = root/ROOT/SLUGS[point]
    assert (source/"AceriaApp.sln").is_file(), source
    with tempfile.TemporaryDirectory(prefix="aceria-m02-stages-") as tmp:
        folder = Path(tmp)/SLUGS[point]
        shutil.copytree(source, folder, ignore=shutil.ignore_patterns("bin","obj",".vs","TestResults"))
        tests_before = TOTAL[point] - {"2.1":8,"2.2":5,"2.3":6,"2.4":9}[point]
        report = {"point":point,"steps":[],"expected_initial_tests":tests_before,
                  "expected_final_tests":TOTAL[point]}
        shell(["dotnet","restore","AceriaApp.sln"],folder)
        # Estado de partida, antes de descomentar ningún archivo de este punto.
        shell(["dotnet","build","AceriaApp.sln","-c","Release","--no-restore"],folder)
        report["base_tests"]=run_tests(folder, tests_before)
        activated = set()
        for step in range(1,25):
            changed=activate(folder,point,step)
            if point=="2.4" and step==9:
                deactivate_legacy_swagger(folder)
            if changed:
                activated.add(step)
            # Se comprueba la compilación en cada uno de los 24 estados, incluso
            # cuando el paso es documental y no cambia ningún archivo C#.
            build=shell(["dotnet","build","AceriaApp.sln","-c","Release","--no-restore"],folder)
            row={"step":step,"changed":changed,"build_seconds":build["seconds"]}
            if step=={"2.1":20,"2.2":18,"2.3":19,"2.4":18}[point]:
                row["tests"]=run_tests(folder,TOTAL[point])
            report["steps"].append(row)
        assert activated == STEPS[point], (activated,STEPS[point])
        report["final_tests"]=run_tests(folder,TOTAL[point])
    report["success"]=True
    path=root/f"m02-stages-{point}.json"
    path.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({"ok":True,"point":point,"compiled_states":25,
                      "activated_steps":sorted(activated),"tests":report["final_tests"]},
                     ensure_ascii=False))


if __name__=="__main__":
    main()
