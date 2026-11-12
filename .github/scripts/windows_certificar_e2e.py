#!/usr/bin/env python3
"""Certificación Windows: reconstrucción y pruebas reales, nunca --no-tests.

M02–M05: SQL Server LocalDB; M06–M08: LocalDB + RabbitMQ real instalado en Windows.
No acredita Docker Desktop sobre un runner alojado (se comprueba por separado).
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    2: [3, 7, 12, 16],
    3: [23, 31, 38, 50],
    4: [62, 77, 90, 105, 118],
    5: [134, 153, 172, 190, 208],
    6: [232, 264, 283],
    7: [309, 331, 353, 403],
    8: [415, 451, 476, 491],
}
FOLDERS = {
    2: "M02_APIS_REST_ASPNET_CORE",
    3: "M03_ARQUITECTURA_HEXAGONAL",
    4: "M04_PATRONES_ARQUITECTURA",
    5: "M05_DDD_CQRS",
    6: "M06_COMUNICACION_MICROSERVICIOS",
    7: "M07_OBSERVABILIDAD_RESILIENCIA",
    8: "M08_API_GATEWAY",
}
LOCALDB = r"Server=(localdb)\MSSQLLocalDB;Database=master;Integrated Security=True;TrustServerCertificate=True"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def call(*command: str, env: dict[str, str]) -> None:
    print("Ejecutando:", " ".join(command), flush=True)
    subprocess.run([str(x) for x in command], cwd=ROOT, env=env, check=True)


def read_json(path: Path) -> dict:
    check(path.is_file(), f"Falta evidencia: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def report_for(module: int, env: dict[str, str], temp: Path) -> dict:
    source = FOLDERS[module]
    if module <= 5:
        # Windows SqlClient.SNI requiere ruta corta para los ensamblados nativos.
        # Los proyectos se reconstruyen desde Markdown; no se copia una etapa final.
        sys.path.insert(0, str(ROOT / ".github" / "scripts"))
        from validar_sqlserver import MODULES, reconstruct_through, validate_evidence
        reconstruct_through(module - 1)
        out = ROOT / ".qa" / "windows" / f"M{module:02}_E2E_RESULTADOS.json"
        short_stage = temp / f"m{module:02}-etapas"
        script_name = MODULES[module][1]
        call(sys.executable, f".github/scripts/{script_name}",
             "--out", str(out), "--output-dir", str(short_stage), env=env)
        e2e = read_json(out)
        result = validate_evidence(e2e, module, temp / f"m{module:02}-bases")
        check(result.get("resultado") == "PASS", "La reconstrucción SQL+tests no ha pasado")
        bases = [read_json(path) for path in sorted((temp / f"m{module:02}-bases").glob("*.json"))]
        check(bases, "No se han creado bases SQL Server reales")
        for evidence in bases:
            check(evidence.get("engineEdition") == 4, "El motor SQL no es Express/LocalDB")
            check(evidence.get("modo") == "conexion_externa", "Se ha usado Docker en lugar de LocalDB")
        bases_count = len(bases)
    else:
        check(env.get("ACERIA_TEST_RABBITMQ"), "Falta URI al RabbitMQ Windows")
        with socket.create_connection(("127.0.0.1", 5672), timeout=10):
            pass
        output_dir = temp / f"m{module:02}-etapas"
        out = ROOT / ".qa" / "windows" / f"M{module:02}_E2E_RESULTADOS.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        call(
            sys.executable, f".github/scripts/m{module:02}_e2e_desde_practicas.py",
            "--out", str(out), "--output-dir", str(output_dir), env=env,
        )
        e2e = read_json(out)
        bases = list((temp / f"m{module:02}-bases").glob("*.json"))
        check(bases, "No hay evidencia de bases SQL Server reales")
        for path in bases:
            evidence = read_json(path)
            check(evidence.get("engineEdition") == 4, f"Motor SQL no LocalDB en {path.name}")
            check(evidence.get("modo") == "conexion_externa", "SQL Server no se conectó a LocalDB")
        bases_count = len(bases)

    summary = e2e.get("resumen", {})
    check(summary.get("resultado") == "PASS", "El E2E no devolvió PASS (SIN_TESTS no basta)")
    check(summary.get("tests_por_etapa") == EXPECTED[module], "Recuento de pruebas erróneo")
    if module >= 3:
        check(e2e.get("retos_optativos", {}).get("resultado") == "PASS",
              "Faltan retos ejecutados con Windows")
    return {
        "resultado": "PASS",
        "tests_por_etapa": EXPECTED[module],
        "retos": e2e.get("retos_optativos", {}).get("resultado"),
        "proveedor": "SQL Server Express LocalDB",
        "bases_sql_verificadas": bases_count,
        "broker": "RabbitMQ nativo Windows real" if module >= 6 else "No requerido",
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--modulo", type=int, choices=sorted(EXPECTED), required=True)
    args = p.parse_args()
    module = args.modulo
    output = ROOT / ".qa" / "windows" / f"M{module:02}_CERTIFICACION_WINDOWS.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    evidence = {
        "modulo": module,
        "plataforma": "Windows 2022 GitHub Actions y SQL Server LocalDB",
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "commit_comprobado": os.environ.get("GITHUB_SHA"),
        "resultado": "FAIL",
        "alcance": "El broker se instala como servicio nativo; Docker Desktop se valida en un equipo Windows.",
    }
    try:
        check(sys.platform == "win32", "Esta certificación requiere Windows real")
        env = dict(
            os.environ,
            ACERIA_TEST_SQLSERVER=LOCALDB,
            ACERIA_SQL_ORIGIN="Windows LocalDB",
            DOTNET_CLI_UI_LANGUAGE="en",
            DOTNET_NOLOGO="true",
            DOTNET_PROCESSOR_COUNT="1",
            PYTHONUTF8="1",
        )
        with tempfile.TemporaryDirectory(prefix=f"axia-win-{module}-") as temp_name:
            temp = Path(temp_name)
            folder = temp / f"m{module:02}-bases"
            folder.mkdir(parents=True, exist_ok=True)
            env["ACERIA_SQL_EVIDENCE_DIR"] = str(folder)
            if module >= 6:
                env["ACERIA_TEST_RABBITMQ"] = "amqp://curso:curso-local@127.0.0.1:5672/"
            evidence.update(report_for(module, env, temp))
    except Exception as exc:
        evidence.update(resultado="FAIL", error=f"{type(exc).__name__}: {exc}")
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2), flush=True)
    return 0 if evidence["resultado"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
