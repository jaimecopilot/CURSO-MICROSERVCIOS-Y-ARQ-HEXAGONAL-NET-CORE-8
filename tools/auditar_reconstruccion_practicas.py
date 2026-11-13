#!/usr/bin/env python3
"""Diagnóstico honesto de reconstrucción incremental de M02-M08.

No copia el proyecto del punto de destino para que una etapa aparente reconstruirse.
Usa el punto ANTERIOR como entrada y aplica, en orden, sólo las operaciones de
código explícitas del manual corregido. Detecta archivos modificados sin instrucción
marcada, diferencias y operaciones imposibles; no declara un E2E satisfactorio.
La ejecución real .NET/xUnit/SQL/RabbitMQ se hace con los workflows de cada módulo.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import difflib
import json
from pathlib import Path
import re
import sys
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FENCE = chr(96) * 3
CONFIG = {
    2: ("M02_APIS_REST_ASPNET_CORE", [
        "2.1-diseno-apis-rest", "2.2-recursos-verbos-codigos",
        "2.3-validacion-peticiones", "2.4-documentacion-openapi"]),
    3: ("M03_ARQUITECTURA_HEXAGONAL", [
        "3.1-capas-aplicacion", "3.2-puertos-adaptadores",
        "3.3-separacion-capas", "3.4-implementacion-aspnet-core"]),
    4: ("M04_PATRONES_ARQUITECTURA", [
        "4.1-repository", "4.2-unit-of-work", "4.3-mediator",
        "4.4-result-pattern", "4.5-inyeccion-dependencias"]),
    5: ("M05_DDD_CQRS", [
        "5.1-conceptos-ddd", "5.2-entidades-value-objects", "5.3-casos-de-uso",
        "5.4-commands-queries", "5.5-dominio-aceria"]),
    6: ("M06_COMUNICACION_MICROSERVICIOS", [
        "6.1-comunicacion-sincrona-http", "6.2-comunicacion-asincrona-eventos",
        "6.3-cuando-usar-cada-enfoque"]),
    7: ("M07_OBSERVABILIDAD_RESILIENCIA", [
        "7.1-logging", "7.2-health-checks",
        "7.3-gestion-excepciones", "7.4-retry-circuit-breaker-polly"]),
    8: ("M08_API_GATEWAY", [
        "8.1-introduccion-api-gateway", "8.2-configuracion-basica-yarp",
        "8.3-enrutamiento-peticiones", "8.4-balanceo-carga"]),
}
CODE = re.compile(
    r"<!-- M0[2-8]_(?:ARCHIVO|CODIGO) (\{[^\n]*\}) -->\s*"
    + re.escape(FENCE) + r"([^\n]*)\n([\s\S]*?)\n" + re.escape(FENCE)
)
STEP = re.compile(r"^### PASO (\d+\.\d+\.\d+) — ", re.M)
MODES = {"crear", "reemplazar", "insertar_antes", "referencia"}
SKIP_DIRS = {"bin", "obj", ".vs", ".git", "node_modules", ".qa"}
SKIP_EXT = {".dll", ".pdb", ".exe", ".png", ".jpg", ".jpeg", ".pdf",
            ".zip", ".ico", ".svg", ".lock", ".db", ".sqlite"}
MAX_BYTES = 2_000_000


def norm(text: str) -> str:
    """Normalización editorial: respeta las instrucciones no triviales."""
    return "\n".join(
        line.strip() for line in text.replace("\r\n", "\n").lstrip("\ufeff").splitlines()
        if line.strip()
    )


def safe_relative(path: str) -> str:
    p = Path(path.replace("\\", "/"))
    if p.is_absolute() or ".." in p.parts or not p.parts or ":" in p.parts[0]:
        raise ValueError(f"Ruta insegura: {path}")
    return p.as_posix()


def files(root: Path) -> dict[str, str]:
    result = {}
    if not root.is_dir():
        raise FileNotFoundError(f"Falta el directorio del proyecto: {root}")
    for p in root.rglob("*"):
        if not p.is_file() or any(seg in SKIP_DIRS for seg in p.parts):
            continue
        if p.suffix.lower() in SKIP_EXT or p.stat().st_size > MAX_BYTES:
            continue
        try:
            result[p.relative_to(root).as_posix()] = p.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
    return result


def steps_and_operations(module: int, root: Path, stage_names: list[str]):
    manual = root / "PRACTICAS" / f"M{module:02}_PRACTICAS.md"
    text = manual.read_text(encoding="utf-8-sig")
    expected = [f"{module}.{p}.{s}" for p in range(1, len(stage_names) + 1)
                for s in range(1, 25)]
    observed = [match.group(1) for match in STEP.finditer(text)]
    if observed != expected:
        raise ValueError(f"M{module:02}: lista/orden de pasos divergente; "
                         f"observados {len(observed)}, esperados {len(expected)}")
    by_point: dict[int, list[dict]] = defaultdict(list)
    for m in CODE.finditer(text):
        info = json.loads(m.group(1))
        step = info["paso"]
        if step not in expected:
            raise ValueError(f"M{module:02}: marcador fuera de lugar {step}")
        point = int(step.split(".")[1])
        mode = info.get("modo", "referencia")
        if mode not in MODES:
            raise ValueError(f"M{module:02} {step}: modo no documentado {mode}")
        rel = safe_relative(info["ruta"])
        dest = root / "PROYECTO" / stage_names[point-1] / rel
        if not dest.is_file():
            raise FileNotFoundError(f"M{module:02} {step}: destino ausente {dest}")
        by_point[point].append({
            "paso": step,
            "ruta": rel,
            "modo": mode,
            "ancla": info.get("ancla"),
            "codigo": m.group(3),
            "lenguaje": m.group(2),
        })
    return expected, by_point


def apply_marked_operations(previous: dict[str, str], ops: list[dict]):
    """No consulta nunca el snapshot final para aplicar un cambio."""
    constructed = previous.copy()
    diagnostics = []
    for op in ops:
        rel, mode, code, step = op["ruta"], op["modo"], op["codigo"], op["paso"]
        if mode == "referencia":
            continue  # M02 no declara operaciones de escritura para estas referencias.
        if mode in {"crear", "reemplazar"}:
            constructed[rel] = code + "\n"
            continue
        anchor = op["ancla"]
        if not isinstance(anchor, str) or not anchor.strip():
            diagnostics.append(f"{step} {rel}: insertar_antes carece de ancla")
            continue
        content = constructed.get(rel)
        if content is None:
            diagnostics.append(f"{step} {rel}: falta archivo inicial para insertar")
            continue
        if norm(code) and norm(code) in norm(content):
            continue
        if anchor not in content:
            diagnostics.append(f"{step} {rel}: no aparece ancla declarada {anchor!r}")
            continue
        constructed[rel] = content.replace(anchor, code + "\n" + anchor, 1)
    return constructed, diagnostics


def solution_paths(text: str) -> set[str]:
    """Rutas lógicas de proyectos .csproj; omite GUIDs generados por dotnet sln."""
    results = set()
    for match in re.finditer(
        r'(?m)^Project\("[^"]+"\)\s*=\s*"[^"]+",\s*"([^"]+\.csproj)"',
        text,
    ):
        results.add(match.group(1).replace("\\", "/").casefold())
    return results


def manual_section(manual: str, module: int, point: int) -> str:
    """Selecciona la primera sección del punto; evita coincidencias en bloques de código."""
    pattern = re.compile(r"(?m)^# Punto " + str(module) + r"\.(\d+)\s+")
    headers = list(pattern.finditer(manual))
    indices = [i for i, match in enumerate(headers)
               if int(match.group(1)) == point]
    if not indices:
        return ""
    i = indices[0]
    end = next(
        (h.start() for h in headers[i+1:] if int(h.group(1)) != point),
        len(manual),
    )
    return manual[headers[i].start():end]


def check_generated_solution(previous: dict[str,str], built: dict[str,str],
                             actual: dict[str,str], section: str):
    """La solución se construye mediante dotnet sln add, no copiando GUIDs.

    Un PASS semántico exige que la guía indique agregar proyectos, que los
    nuevos .csproj procedan de operaciones escritas en el manual y que la
    membresía resultante coincida con el proyecto canónico.
    """
    prev = previous.get("AceriaApp.sln")
    wanted = actual.get("AceriaApp.sln")
    if not prev or not wanted:
        return False, "Falta la solución anterior o la esperada"
    if not re.search(r"dotnet\s+sln(?:\s+\S+)?\s+add\b", section, re.I):
        return False, "La práctica no muestra el comando dotnet sln add"
    baseline = solution_paths(prev)
    newly_created = {
        file.casefold()
        for file in built.keys() - previous.keys() if file.endswith(".csproj")
    }
    predicted = baseline | newly_created
    target = solution_paths(wanted)
    if not predicted == target:
        extra = sorted(predicted - target)
        missing = sorted(target - predicted)
        return False, f"Membresía diferente; extra={extra}, ausentes={missing}"
    if any(rel not in {p.casefold() for p in built} for rel in target):
        return False, "Algún proyecto de la solución no se encuentra en el árbol reconstruido"
    return True, (
        f"{len(baseline)} proyectos heredados + {len(newly_created)} "
        f"incorporados mediante comandos; {len(target)} referencias coincidentes"
    )


def audit_module(module: int) -> tuple[list[str], dict]:
    dirname, stages = CONFIG[module]
    root = ROOT / dirname
    expected_steps, by_point = steps_and_operations(module, root, stages)
    manual_text = (root / "PRACTICAS" / f"M{module:02}_PRACTICAS.md").read_text(encoding="utf-8-sig")
    report = [
        f"## M{module:02} — {dirname}",
        "",
        f"- Pasos presentes y ordenados: **{len(expected_steps)}/{len(expected_steps)}**",
        f"- Marcadores de código/ruta: **{sum(map(len,by_point.values()))}**",
        "- El punto inicial se toma como referencia; **no se declara reconstruido desde cero**.",
        "",
    ]
    summary = Counter()
    for p in range(1, len(stages) + 1):
        stage_root = root / "PROYECTO" / stages[p-1]
        actual = files(stage_root)
        ops = by_point[p]
        last_by_file = {op["ruta"]: op for op in ops}
        exact = contained = different = 0
        problems = []
        for rel, op in last_by_file.items():
            snippet = norm(op["codigo"])
            destination = norm(actual[rel])
            if snippet == destination:
                exact += 1
            elif snippet and snippet in destination:
                contained += 1
            else:
                different += 1
                ratio = difflib.SequenceMatcher(
                    None, snippet[:10000], destination[:10000], autojunk=False
                ).ratio()
                problems.append(
                    f"{op['paso']}: {rel}: código marcado no coincide "
                    f"({ratio:.0%} similitud del prefijo)"
                )
        summary.update(markers=len(ops), last_files=len(last_by_file),
                       exact=exact, contained=contained, divergent=different)
        if p == 1:
            report += [
                f"### Punto {module}.{p}",
                f"- Marcadores: {len(ops)}, últimas referencias: {len(last_by_file)}",
                f"- Paridad directa: {exact} idénticos, {contained} contenidos, "
                f"{different} diferentes",
                "- Sin baseline inicial inequívoco para reconstruir esta primera etapa.",
                "",
            ]
            for item in problems[:8]:
                report.append(f"  - **REVISAR:** {item}")
            report.append("")
            continue
        previous = files(root / "PROYECTO" / stages[p-2])
        target_changes = {
            rel for rel in previous.keys() | actual.keys()
            if norm(previous.get(rel, "")) != norm(actual.get(rel, ""))
        }
        constructed, errors = apply_marked_operations(previous, ops)
        marked_changes = target_changes & set(last_by_file)
        untraced = sorted(target_changes - set(last_by_file))
        complete = sorted(rel for rel in target_changes if
                          norm(constructed.get(rel, "")) == norm(actual.get(rel, "")))
        mismatch = sorted(rel for rel in marked_changes if
                          norm(constructed.get(rel, "")) != norm(actual.get(rel, "")))
        deleted = sorted(rel for rel in previous.keys() - actual.keys())
        semantic_solution = False
        semantic_detail = ""
        if "AceriaApp.sln" in untraced:
            semantic_solution, semantic_detail = check_generated_solution(
                previous, constructed, actual,
                manual_section(manual_text, module, p))
            if semantic_solution:
                untraced.remove("AceriaApp.sln")
        summary.update(transitions=1, changed=len(target_changes),
                       marked_changed=len(marked_changes),
                       reconstructed=len(complete), solution_semantic=int(semantic_solution),
                       missing=len(untraced), incorrect=len(mismatch), blocked=len(errors))
        report += [
            f"### Punto {module}.{p}",
            "",
            f"- Archivos cambiados respecto al punto anterior: {len(target_changes)}",
            f"- Cambios con operación de código marcada: {len(marked_changes)}",
            f"- Archivo AceriaApp.sln validado por membresía y comandos: {'sí' if semantic_solution else 'no'} ({semantic_detail})",
            f"- **Resultado idéntico tras aplicar instrucciones marcadas:** "
            f"{len(complete)}/{len(target_changes)}",
            f"- Cambios sin operación marcada: **{len(untraced)}**",
            f"- Cambios marcados todavía distintos: **{len(mismatch)}**",
            f"- Operaciones no aplicables: **{len(errors)}**",
            f"- Eliminaciones de archivos: {len(deleted)}",
            f"- Paridad de últimas referencias: {exact} exactos, "
            f"{contained} contenidos, {different} diferentes",
            "",
        ]
        if untraced:
            report.extend(["**Archivos sin reconstrucción documentada (primeros 20):**", ""])
            report.extend(f"- {FENCE}{x}{FENCE}" for x in untraced[:20])
            report.append("")
        if mismatch:
            report.extend(["**Archivos marcados que no se reconstruyen fielmente (primeros 20):**", ""])
            report.extend(f"- {FENCE}{x}{FENCE}" for x in mismatch[:20])
            report.append("")
        if errors or problems:
            report.extend(["**Otras observaciones:**", ""])
            report.extend(f"- {item}" for item in (errors + problems)[:15])
            report.append("")
    report += [
        f"**Balance M{module:02}:** {summary['transitions']} transiciones comparadas, "
        f"{summary['reconstructed']}/{summary['changed']} archivos reconstruidos "
        f"por código sin consultar su destino, y {summary['solution_semantic']} "
        f"soluciones contrastadas por membresía; {summary['missing']} sin operación marcada, "
        f"{summary['incorrect']} discrepantes con operación marcada.",
        "",
    ]
    return report, dict(summary)


def materializar_etapa(module: int, point: int, destination: Path) -> dict:
    """Construye el punto N.P desde el punto N.(P-1), sin leer código del destino.

    Reutiliza *solo* el snapshot anterior como estado inicial. Aplica las
    operaciones de archivo del manual en su orden y genera la solución .sln
    mediante dotnet sln add. A continuación compara el conjunto de archivos
    contra el punto canónico y se niega a continuar si falta una diferencia.
    Primer punto de cada módulo: aún requiere una reconstrucción inicial aparte.
    """
    if module not in CONFIG or point < 2 or point > len(CONFIG[module][1]):
        raise ValueError("Materialización solo para puntos 2..N de M02-M08")
    dirname, stages = CONFIG[module]
    root = ROOT / dirname
    _, by_point = steps_and_operations(module, root, stages)
    previous_root = root / "PROYECTO" / stages[point - 2]
    target_root = root / "PROYECTO" / stages[point - 1]
    previous = files(previous_root)
    wanted = files(target_root)
    constructed, errors = apply_marked_operations(previous, by_point[point])
    if errors:
        raise RuntimeError(
            f"Operaciones del manual no aplicables en M{module:02}/{point}: "
            + "; ".join(errors)
        )
    differences = set(previous) | set(wanted)
    changed = {rel for rel in differences
               if norm(previous.get(rel, "")) != norm(wanted.get(rel, ""))}
    missing = {rel for rel in changed if
               rel not in {op["ruta"] for op in by_point[point]}
               and rel != "AceriaApp.sln"}
    if missing:
        raise RuntimeError(
            "No se puede reconstruir: el manual no tiene operaciones para "
            + ", ".join(sorted(missing))
        )
    for rel in changed - {"AceriaApp.sln"}:
        if norm(constructed.get(rel, "")) != norm(wanted.get(rel, "")):
            raise RuntimeError(
                f"M{module:02} punto {module}.{point}: el archivo {rel} "
                "no coincide tras aplicar las instrucciones"
            )
    doc = (root / "PRACTICAS" / f"M{module:02}_PRACTICAS.md").read_text(
        encoding="utf-8-sig"
    )
    needs_solution = "AceriaApp.sln" in changed
    if needs_solution:
        ok, explanation = check_generated_solution(
            previous, constructed, wanted, manual_section(doc, module, point)
        )
        if not ok:
            raise RuntimeError("No se puede regenerar AceriaApp.sln: " + explanation)
    if destination.exists():
        raise FileExistsError(f"El destino debe estar vacío: {destination}")
    shutil.copytree(
        previous_root, destination,
        ignore=shutil.ignore_patterns(
            "bin", "obj", "TestResults", "_test_results", "_trx", ".qa"
        ),
    )
    # Sólo las operaciones ya aplicadas al estado anterior se escriben;
    # nunca se usan los bytes del proyecto canónico para crear nuevos archivos.
    for rel in changed - {"AceriaApp.sln"}:
        path = destination / rel
        if rel in constructed:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(constructed[rel], encoding="utf-8")
        elif path.exists():
            path.unlink()

    new_projects = sorted(
        rel for rel in constructed.keys() - previous.keys()
        if rel.casefold().endswith(".csproj")
    )
    if needs_solution and new_projects:
        command = ["dotnet", "sln", "AceriaApp.sln", "add", *new_projects]
        response = subprocess.run(
            command, cwd=destination, text=True, encoding="utf-8",
            errors="replace", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=120,
        )
        print(response.stdout[-4000:], flush=True)
        if response.returncode:
            raise RuntimeError("Error al añadir proyectos a solución: "
                               + response.stdout[-3000:])
    built = files(destination)
    if set(built) != set(wanted):
        raise RuntimeError(
            "Archivos distintos en el árbol reconstruido: "
            f"faltan {sorted(set(wanted)-set(built))}; "
            f"sobran {sorted(set(built)-set(wanted))}"
        )
    for rel, expected in wanted.items():
        actual = built[rel]
        if rel == "AceriaApp.sln":
            if solution_paths(actual) != solution_paths(expected):
                raise RuntimeError("La membresía de AceriaApp.sln no coincide")
        elif norm(actual) != norm(expected):
            raise RuntimeError(
                f"Paridad post-materialización incorrecta: M{module:02}/"
                f"{module}.{point}/{rel}"
            )
    stats = {
        "module": module,
        "point": f"{module}.{point}",
        "files": len(built),
        "changed": len(changed),
        "reconstructed_text": len(changed) - int(needs_solution),
        "solution_membership": "PASS" if needs_solution else "sin cambios",
        "new_projects": new_projects,
        "destination": str(destination),
    }
    print("RECONSTRUCCION VALIDADA " + json.dumps(stats, ensure_ascii=False),
          flush=True)
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", type=int, choices=tuple(CONFIG))
    parser.add_argument("--report", type=Path,
                        default=ROOT / "AUDITORIA_RECONSTRUCCION_PRACTICAS.md")
    parser.add_argument("--strict", action="store_true",
                        help="Fallará si hay algún archivo no reconstruido o sin instrucción")
    args = parser.parse_args()
    numbers = [args.module] if args.module else list(CONFIG)
    lines = [
        "# Diagnóstico de reconstrucción desde prácticas corregidas",
        "",
        "Este informe distingue pruebas E2E sobre proyectos entregados de una "
        "reconstrucción desde las instrucciones. Para cada transición entre "
        "dos puntos, parte del proyecto del punto **anterior** y aplica "
        "exclusivamente los cambios con metadatos de código presentes en "
        "el manual nuevo. **Nunca copia el proyecto de destino para simular un "
        "resultado**. La primera etapa de cada módulo necesita una especificación "
        "de inicio independiente y, por tanto, sigue fuera del alcance de esta "
        "reconstrucción incremental.",
        "",
        "La comparación de código ignora espacios externos y líneas vacías, "
        "pero no elimina instrucciones ni expresiones. Los retos optativos "
        "y los clics de Visual Studio requieren pruebas adicionales.",
        "",
    ]
    aggregate = Counter()
    for n in numbers:
        details, stats = audit_module(n)
        lines.extend(details)
        aggregate.update(stats)
        print(
            f"M{n:02}: {stats.get('reconstructed', 0)}/"
            f"{stats.get('changed', 0)} cambios reconstruidos; "
            f"{stats.get('missing',0)} sin marcador; "
            f"{stats.get('incorrect',0)} no coincidentes; "
            f"paridad divergente {stats.get('divergent',0)}",
            flush=True,
        )
    lines += [
        "## Balance",
        "",
        f"- Transiciones auditadas: **{aggregate['transitions']}**",
        f"- Archivos con cambios: **{aggregate['changed']}**",
        f"- Reconstruidos exactamente desde los pasos marcados: "
        f"**{aggregate['reconstructed']}**",
        f"- Soluciones .sln verificadas por comandos de alta y membresía "
        f"(no igualdad byte a byte): **{aggregate['solution_semantic']}**",
        f"- Sin operación de reconstrucción explícita: **{aggregate['missing']}**",
        f"- Marcados, pero no reproducibles exactamente: "
        f"**{aggregate['incorrect']}**",
        f"- Últimas referencias cuyo contenido no coincide: "
        f"**{aggregate['divergent']}**",
        "",
        "**Estado:** DIAGNÓSTICO; no se declara certificación de reconstrucción "
        "completa mientras haya brechas o falte reconstruir el inicio del módulo.",
        "",
    ]
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines), encoding="utf-8")
    print(f"INFORME: {args.report}", flush=True)
    if args.strict and any(aggregate[k] > 0 for k in
                           ("missing", "incorrect", "blocked", "divergent")):
        sys.exit(1)


if __name__ == "__main__":
    main()
