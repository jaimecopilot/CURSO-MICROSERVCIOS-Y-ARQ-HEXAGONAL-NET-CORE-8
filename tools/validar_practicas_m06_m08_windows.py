#!/usr/bin/env python3
"""M06-M08: auditoría de trazabilidad y tests .NET 8 en Windows con SQL y RabbitMQ reales.

Los snapshots canónicos permanecen intactos. Todos los builds se ejecutan
sobre copias de ruta corta para evitar errores de carga de SqlClient.SNI.dll.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import tempfile
import time
import uuid
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
    6: {
        "folder": "M06_COMUNICACION_MICROSERVICIOS",
        "steps": 72,
        "blocks": 114,
        "markers": 92,
        "stages": [
            "6.1-comunicacion-sincrona-http",
            "6.2-comunicacion-asincrona-eventos",
            "6.3-cuando-usar-cada-enfoque",
        ],
        "expected": [232, 264, 283],
    },
    7: {
        "folder": "M07_OBSERVABILIDAD_RESILIENCIA",
        "steps": 96,
        "blocks": 137,
        "markers": 93,
        "stages": [
            "7.1-logging",
            "7.2-health-checks",
            "7.3-gestion-excepciones",
            "7.4-retry-circuit-breaker-polly",
        ],
        "expected": [309, 331, 353, 403],
    },
    8: {
        "folder": "M08_API_GATEWAY",
        "steps": 96,
        "blocks": 96,
        "markers": 66,
        "stages": [
            "8.1-introduccion-api-gateway",
            "8.2-configuracion-basica-yarp",
            "8.3-enrutamiento-peticiones",
            "8.4-balanceo-carga",
        ],
        "expected": [415, 451, 476, 491],
    },
}
MARKER = re.compile(
    r"<!-- M0[678]_CODIGO (\{[^\n]*\}) -->\s*"
    + chr(96) * 3 + r"([^\n]*)\n([\s\S]*?)\n" + chr(96) * 3
)


def command(args: list[str], cwd: Path, env: dict[str, str],
            timeout: int = 1350) -> str:
    print("$ " + " ".join(args), flush=True)
    result = subprocess.run(
        args, cwd=cwd, env=env, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, encoding="utf-8", errors="replace",
        text=True, timeout=timeout,
    )
    print(result.stdout[-10500:], flush=True)
    if result.returncode:
        raise RuntimeError(f"Comando fallido ({result.returncode}): {' '.join(args)}")
    return result.stdout


def audit(module: int) -> list[dict]:
    config = MODULES[module]
    directory = ROOT / config["folder"]
    text = (directory / "PRACTICAS" /
            f"M{module:02}_PRACTICAS.md").read_text(encoding="utf-8-sig")
    stepids = re.findall(
        r"^### PASO (" + str(module) + r"\.\d+\.\d+) — ", text, re.M)
    expected = [
        f"{module}.{point}.{step}"
        for point in range(1, len(config["stages"]) + 1)
        for step in range(1, 25)
    ]
    assert stepids == expected, "Pasos no consecutivos o ausentes"
    fences = re.findall(r"^" + chr(96) * 3, text, re.M)
    assert len(fences) == config["blocks"] * 2, "Bloques de código alterados"
    assert "**Resultado de aprendizaje.**" not in text
    assert "**Por qué funciona así.**" not in text
    assert not re.search(r"\*\*Línea \d+:", text)
    markers = list(MARKER.finditer(text))
    assert len(markers) == config["markers"], (
        len(markers), config["markers"]
    )
    items = []
    for match in markers:
        data = json.loads(match.group(1))
        step = data["paso"]
        assert step in expected, f"Marcador fuera de orden: {step}"
        point = int(step.split(".")[1])
        target = directory / "PROYECTO" / config["stages"][point - 1] / data["ruta"]
        assert target.is_file(), f"Falta el archivo didáctico: {target}"
        items.append({
            "step": step, "path": data["ruta"], "mode": data.get("modo"),
        })
    print(f"TRAZABILIDAD M{module:02}: {len(stepids)} pasos, "
          f"{len(markers)} destinos existentes, {len(fences)//2} "
          "bloques de código", flush=True)
    return items


def wait_tcp(port: int, timeout: float = 10.0) -> None:
    stop = time.monotonic() + timeout
    while time.monotonic() < stop:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=2):
                return
        except OSError:
            time.sleep(0.4)
    raise RuntimeError(f"Servicio TCP localhost:{port} no disponible")


def test_counts(folder: Path) -> dict:
    files = list(folder.glob("*.trx"))
    assert files, f"Faltan informes xUnit en {folder}"
    count = {"total": 0, "passed": 0, "failed": 0, "notExecuted": 0}
    for item in files:
        counters = ET.parse(item).getroot().find(".//{*}Counters")
        assert counters is not None, item
        for field in count:
            count[field] += int(counters.attrib.get(field, 0))
    assert count["total"] > 0 and count["failed"] == 0, count
    assert count["passed"] + count["notExecuted"] == count["total"], count
    assert count["notExecuted"] == 0, count
    return {"passed": count["passed"], "total": count["total"],
            "failed": count["failed"], "projects": len(files)}


def run_stages(module: int, env: dict[str, str],
               reconstruir_incremental: bool = False) -> list[dict]:
    cfg = MODULES[module]
    base = Path(os.getenv("RUNNER_TEMP", tempfile.gettempdir())) / (
        f"mx{module}_" + uuid.uuid4().hex[:6]
    )
    base.mkdir(parents=True, exist_ok=True)
    results = []
    for point, stage in enumerate(cfg["stages"], 1):
        print(f"=== M{module:02}, punto {module}.{point}: "
              "copia aislada, restore, build, xUnit ===", flush=True)
        src = ROOT / cfg["folder"] / "PROYECTO" / stage
        dest = base / f"p{point}"
        if reconstruir_incremental and point >= 2:
            from auditar_reconstruccion_practicas import materializar_etapa
            materializar_etapa(module,point,dest)
        else:
            shutil.copytree(src, dest)
        # El archivo global.json heredado mantiene la selección de .NET 8.
        solution = "AceriaApp.sln"
        command(["dotnet", "restore", solution, "--nologo"], dest, env)
        command(["dotnet", "build", solution, "-c", "Release",
                 "--no-restore", "--nologo"], dest, env)
        trxdir = dest / "_trx"
        trxdir.mkdir()
        command(["dotnet", "test", solution, "-c", "Release",
                 "--no-build", "--no-restore", "--nologo",
                 "--logger", "trx", "--results-directory", str(trxdir)],
                dest, env, timeout=1800)
        tally = test_counts(trxdir)
        expected = cfg["expected"][point - 1]
        assert tally["passed"] == expected, (
            f"M{module:02} punto {point}: {tally['passed']} != "
            f"{expected} pruebas que indica el manual"
        )
        results.append({"punto": f"{module}.{point}", **tally})
        print(f"PUNTO {module}.{point} VALIDADO: "
              f"{tally['passed']}/{tally['total']} tests, "
              f"{tally['projects']} proyectos de pruebas", flush=True)
        # Evitar que cinco versiones de bin/obj agoten el espacio del runner.
        if point < len(cfg["stages"]):
            shutil.rmtree(dest, ignore_errors=True)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", type=int, choices=(6, 7, 8), required=True)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--reconstruir-incremental", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    cfg = MODULES[args.module]
    markers = audit(args.module)
    rows = []
    if not args.audit_only:
        env = dict(os.environ)
        assert env.get("ACERIA_TEST_SQLSERVER"), "No hay conexión SQL de pruebas"
        assert env.get("ACERIA_TEST_RABBITMQ"), "No hay URI RabbitMQ de pruebas"
        env["DOTNET_CLI_TELEMETRY_OPTOUT"] = "1"
        env["DOTNET_NOLOGO"] = "1"
        wait_tcp(1433, timeout=2) if env.get("ACERIA_SQL_REQUIRE_TCP") else None
        wait_tcp(5672, timeout=45)
        rows = run_stages(args.module, env, args.reconstruir_incremental)
    if args.report:
        report = [
            f"# M{args.module:02} — Informe automático Windows, SQL y RabbitMQ",
            "",
            f"**Pasos del manual:** {cfg['steps']}.",
            f"**Bloques de código:** {cfg['blocks']}.",
            f"**Marcadores con ruta existente:** {len(markers)}.",
            "",
        ]
        if rows:
            report += [
                "| Punto | Pruebas correctas | Fallidas | Proyectos de pruebas |",
                "|---|---:|---:|---:|",
            ]
            for row in rows:
                report.append(
                    f"| {row['punto']} | {row['passed']} | "
                    f"{row['failed']} | {row['projects']} |"
                )
            report += [
                "",
                f"**Ejecuciones acumuladas:** {sum(x['passed'] for x in rows)}.",
                "**Estado final:** " + str(rows[-1]["passed"]) + " tests.",
                "",
                "Las pruebas ejecutan los snapshots finales de cada etapa en",
                "Windows con SQL Server Express y RabbitMQ reales, incluidas",
                "las pruebas funcionales que los respectivos proyectos contienen.",
                "El total suma varias ejecuciones acumuladas, no tests distintos.",
                "",
                "Límites: la compilación y los E2E de los proyectos de referencia",
                "Reconstrucción incremental desde el manual en las etapas 2..N: "
                + str(bool(args.reconstruir_incremental)),
                "no equivalen a reproducir manualmente todos los clics de",
                "Visual Studio ni a ejecutar los retos optativos.",
            ]
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text("\n".join(report) + "\n", encoding="utf-8")
        print(f"INFORME: {args.report}", flush=True)


if __name__ == "__main__":
    main()
