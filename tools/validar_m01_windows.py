#!/usr/bin/env python3
"""Valida M01 mediante reconstrucción de los cinco esqueletos y E2E en Windows."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request
import urllib.error
import uuid
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
M01 = ROOT / "M01_INTRODUCCION_MICROSERVICIOS"
STAGES = [
    "1.1-monolito-vs-microservicios", "1.2-ventajas-inconvenientes",
    "1.3-principios-diseno", "1.4-organizacion-solucion", "1.5-buenas-practicas",
]
START = re.compile(r"^\s*//\s*INICIO PASO\s+(1\.[1-5]\.\d+)\b")
END = re.compile(r"^\s*//\s*FIN PASO\s+(1\.[1-5]\.\d+)\b")


def run(args, cwd, env, timeout=450):
    print("$ " + " ".join(map(str, args)), flush=True)
    p = subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout)
    print(p.stdout[-9500:], flush=True)
    if p.returncode:
        raise RuntimeError("Comando fallido: " + " ".join(map(str, args)))
    return p.stdout


def activate(folder, point):
    steps = set()
    fragments = 0
    for file in sorted(folder.rglob("*.cs")):
        lines = file.read_text(encoding="utf-8-sig").splitlines()
        result, current = [], None
        for line in lines:
            start, end = START.match(line), END.match(line)
            if start:
                assert current is None, file
                bits = [int(v) for v in start.group(1).split(".")]
                assert bits[:2] == [1, point], (file, bits)
                current = bits[2]
                steps.add(current)
                fragments += 1
                result.append(line)
            elif end:
                assert current == int(end.group(1).split(".")[2]), file
                current = None
                result.append(line)
            elif current is not None:
                if not line.strip():
                    result.append("")
                else:
                    m = re.match(r"^(\s*)// ?(.*)$", line)
                    assert m, (file, line)
                    result.append(m.group(1) + m.group(2))
            else:
                result.append(line)
        assert current is None, file
        if result != lines:
            file.write_text("\n".join(result) + "\n", encoding="utf-8")
    expected = {11, 12, 13, 17} if point == 1 else (
        {6, 7, 8, 13, 14, 15} if point == 2 else {6, 7, 9, 14, 15})
    assert expected <= steps, (point, sorted(expected - steps))
    return steps, fragments


def check_manual():
    text = (M01 / "PRACTICAS" / "M01_PRACTICAS.md").read_text(encoding="utf-8")
    points = list(re.finditer(r"^# Punto 1\.[1-5] — ", text, re.M))
    assert len(points) == 10, f"Se esperaban 10 títulos de punto, encontrados {len(points)}"
    for i in range(5):
        a = points[2*i].start()
        b = points[2*i+2].start() if i < 4 else len(text)
        n = len(re.findall(r"^### Paso \d+ — ", text[a:b], re.M))
        assert n == 24, (i+1, n)
    assert len(re.findall("^" + chr(96)*3, text, re.M)) == 104
    assert not re.search(r"\*\*Acción \d+:", text)
    assert not re.search(r"^\s*-\s*\*\*Línea \d+ —", text, re.M)
    print("MANUAL OK: 5 puntos, 120 pasos, 52 fragmentos de código")


def results_trx(folder):
    files = list(folder.glob("*.trx"))
    assert files, "No se generaron informes TRX de las pruebas"
    counts = {"total": 0, "passed": 0, "failed": 0}
    for file in files:
        c = ET.parse(file).getroot().find(".//{*}Counters")
        assert c is not None, file
        for name in counts:
            counts[name] += int(c.get(name, 0))
    assert counts["total"] > 0 and counts["failed"] == 0
    assert counts["passed"] == counts["total"], counts
    counts["proyectos"] = len(files)
    return counts


def stage(point, workdir, env):
    folder = workdir / STAGES[point-1]
    shutil.copytree(M01 / "PROYECTO" / STAGES[point-1], folder)
    if point == 1:
        migrations = list(folder.rglob("Migraciones/*.cs.txt"))
        assert len(migrations) == 2, migrations
        for file in migrations:
            file.rename(file.with_suffix(""))
    steps, fragments = activate(folder, point)
    run(["dotnet", "restore", "AceriaApp.sln", "--nologo"], folder, env)
    run(["dotnet", "build", "AceriaApp.sln", "-c", "Release", "--no-restore",
         "--nologo"], folder, env)
    results = folder / "_testresults"
    results.mkdir()
    run(["dotnet", "test", "AceriaApp.sln", "-c", "Release", "--no-build",
         "--no-restore", "--nologo", "--logger", "trx",
         "--results-directory", str(results)], folder, env)
    tally = results_trx(results)
    print(f"PUNTO 1.{point} reconstruido: {fragments} fragmentos, "
          f"{len(steps)} pasos de código, {tally['passed']} tests")
    return folder, {"point": f"1.{point}", "fragments": fragments,
                    "steps": len(steps), "passed": tally["passed"],
                    "test_projects": tally["proyectos"]}


def http_call(url, data=None):
    headers = {"Content-Type": "application/json"} if data is not None else {}
    req = urllib.request.Request(
        url, data=json.dumps(data).encode() if data is not None else None,
        headers=headers, method="POST" if data is not None else "GET")
    with urllib.request.urlopen(req, timeout=12) as res:
        return res.status, json.load(res), dict(res.headers.items())


def e2e_http(folder, env):
    base = "http://127.0.0.1:51081"
    p = subprocess.Popen(["dotnet", "run", "--no-launch-profile", "--no-build",
                          "-c", "Release", "--project",
                          "src/AceriaApp.Monolito.Api", "--urls", base],
                         cwd=folder, env=env, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True,
                         encoding="utf-8", errors="replace")
    try:
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            if p.poll() is not None:
                raise RuntimeError(f"La API terminó inesperadamente, rc={p.returncode}")
            try:
                status, _, _ = http_call(base + "/api/v1/ordenes")
                if status == 200:
                    break
            except (urllib.error.URLError, TimeoutError):
                time.sleep(.8)
        else:
            raise RuntimeError("La API no llegó a escuchar")
        status, before, _ = http_call(base + "/api/v1/ordenes")
        assert status == 200 and isinstance(before, list)
        name = "M01-" + uuid.uuid4().hex[:8]
        status, created, headers = http_call(
            base + "/api/v1/ordenes",
            {"cliente": name, "material": "CHAPA-3MM", "cantidad": 5})
        assert status == 201 and created["cliente"] == name
        assert created["cantidad"] == 5 and created["id"]
        assert (headers.get("Location") or "").endswith(created["id"])
        status, after, _ = http_call(base + "/api/v1/ordenes")
        assert status == 200 and len(after) >= len(before) + 1
        assert any(x["id"] == created["id"] for x in after)
        status, swagger, _ = http_call(base + "/swagger/v1/swagger.json")
        assert status == 200 and "/api/v1/ordenes" in swagger["paths"]
        print("E2E OK: HTTP GET 200, POST 201/Location, persistencia SQL, Swagger")
        return {"GET": 200, "POST": 201, "SQL": "persistencia OK", "OpenAPI": 200}
    finally:
        p.terminate()
        try:
            p.communicate(timeout=12)
        except subprocess.TimeoutExpired:
            p.kill()
            p.communicate(timeout=12)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sql", action="store_true")
    parser.add_argument("--report", default="M01_WINDOWS_VALIDACION.md")
    args = parser.parse_args()
    check_manual()
    workspace = Path(os.getenv("RUNNER_TEMP", tempfile.gettempdir())) / (
        "M01_" + uuid.uuid4().hex[:8])
    workspace.mkdir()
    env = os.environ.copy()
    env.update({"DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1"})
    reports = []
    for point in range(1, 6):
        final, row = stage(point, workspace, env)
        reports.append(row)
    sql_result = {}
    if args.sql:
        env["ConnectionStrings__AceriaDb"] = (
            "Server=.\\SQLEXPRESS;Database=AceriaM01_" + uuid.uuid4().hex[:8]
            + ";Trusted_Connection=True;TrustServerCertificate=True;Encrypt=False")
        env["ASPNETCORE_ENVIRONMENT"] = "Development"
        tools = workspace / "tools"
        run(["dotnet", "tool", "install", "dotnet-ef", "--tool-path",
             str(tools), "--version", "8.0.0"], final, env)
        ef = str(tools / "dotnet-ef.exe")
        options = ["--project", "src/AceriaApp.Monolito.Api", "--startup-project",
                   "src/AceriaApp.Monolito.Api", "--no-build",
                   "--configuration", "Release"]
        try:
            run([ef, "database", "update"] + options, final, env)
            sql_result = e2e_http(final, env)
        finally:
            try:
                run([ef, "database", "drop", "--force"] + options, final, env)
            except Exception as ex:
                print("ADVERTENCIA, limpieza de DB: " + str(ex))
    total = sum(x["passed"] for x in reports)
    lines = [
        "# M01 — Evidencias de validación en Windows",
        "",
        "Se reconstruyen los cinco snapshots desde los bloques comentados,",
        "sin alterar los proyectos originales del curso.",
        "",
        "| Punto | Fragmentos activados | Tests xUnit | Compilación |",
        "|---|---:|---:|---|",
    ]
    lines += [
        f"| {x['point']} | {x['fragments']} | {x['passed']} | OK |"
        for x in reports
    ]
    lines += [
        "", f"**Total pruebas ejecutadas entre etapas:** {total}.",
        "", "**Manual:** 5 puntos, 120 pasos, 52 bloques de código.",
        "", "**E2E SQL Express + HTTP:** "
        + json.dumps(sql_result, ensure_ascii=False),
        "", "Límites: la reconstrucción se automatiza desde los marcadores",
        "descritos en el manual. No se han probado acciones gráficas",
        "de Visual Studio ni los retos optativos.",
    ]
    output = Path(args.report)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"INFORME {output}: {total} pruebas ejecutadas", flush=True)


if __name__ == "__main__":
    main()
