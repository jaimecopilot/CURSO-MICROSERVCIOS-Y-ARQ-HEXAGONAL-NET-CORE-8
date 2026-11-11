#!/usr/bin/env python3
"""Ejecuta la reconstrucción y exige evidencia del motor SQL Server Express real."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
MODULES = {
    2: ('M02_APIS_REST_ASPNET_CORE', 'e2e_laboratorio_m02.py', [3, 7, 12, 16]),
    3: ('M03_ARQUITECTURA_HEXAGONAL', 'm03_e2e_desde_practicas.py', [23, 31, 38, 50]),
    4: ('M04_PATRONES_ARQUITECTURA', 'm04_e2e_desde_practicas.py', [62, 77, 90, 105, 118]),
    5: ('M05_DDD_CQRS', 'm05_e2e_desde_practicas.py', [134, 153, 172, 190, 208]),
}

def validate_evidence(report, module, directory):
    expected = MODULES[module][2]
    if report.get('resumen', {}).get('resultado') != 'PASS':
        raise ValueError('La reconstrucción no ha terminado en PASS')
    stages = report.get('etapas', [])
    if len(stages) != len(expected):
        raise ValueError('Número de etapas incompleto')
    for stage, count in zip(stages, expected):
        if stage.get('estado', stage.get('resultado')) != 'PASS':
            raise ValueError('Una etapa no ejecutó todas sus pruebas')
        actual = stage.get('tests_acumulados', stage.get('tests'))
        if actual != count:
            raise ValueError(f'Conteo de etapa incorrecto: {actual}, esperado {count}')
    if report.get('resumen', {}).get('tests_por_etapa') != expected:
        raise ValueError('El resumen no coincide con los tests por etapa')
    challenges = report.get('retos_optativos')
    if (module >= 3 and (challenges is None or challenges.get('resultado') != 'PASS')) or (module == 2 and challenges and challenges.get('resultado') not in ('PASS', 'MANUAL_NO_EJECUTADO')):
        raise ValueError('Hay un reto sin comprobar o fallido')
    evidence = [json.loads(p.read_text(encoding='utf-8-sig')) for p in sorted(Path(directory).glob('*.json'))]
    if not evidence:
        raise ValueError('Falta evidencia SQL obtenida al abrir las bases de pruebas')
    for row in evidence:
        if row.get('provider') != 'Microsoft.EntityFrameworkCore.SqlServer':
            raise ValueError('El proveedor de la evidencia no es SQL Server')
        if row.get('engineEdition') != 4 or not row.get('version'):
            raise ValueError('No se ha acreditado SQL Server Express/LocalDB y su versión')
        if not str(row.get('database', '')).startswith('AceriaTest_'):
            raise ValueError('La prueba no identifica su base aislada')
        if row.get('modo') not in ('conexion_externa', 'testcontainers'):
            raise ValueError('Modo de ejecución no reconocido')
    return {'resultado': 'PASS', 'proveedor': 'Microsoft.EntityFrameworkCore.SqlServer',
            'edicion': 'SQL Server Express / LocalDB', 'bases_verificadas': len(evidence),
            'versiones': sorted({r['version'] for r in evidence}),
            'origenes': sorted({r.get('origen', r['modo']) for r in evidence}),
            'tests_por_etapa': expected}

def file_manifest(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob('*')) if p.is_file()
            and not {'bin', 'obj', 'TestResults', '.vs', '.git', '__pycache__'}.intersection(p.relative_to(directory).parts)}

def source_manifest(directory):
    return {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_text(encoding='utf-8-sig').encode('utf-8')).hexdigest()
            for p in sorted(directory.rglob('*')) if p.is_file() and p.suffix in ('.cs', '.csproj', '.json')
            and not {'bin', 'obj', 'TestResults', '.vs', '.git', '__pycache__'}.intersection(p.relative_to(directory).parts)}

def validate_windows_sources(windows, linux, stage):
    expected = {key[len(stage)+1:]: value for key, value in linux.items() if key.startswith(stage+'/')}
    if not expected or windows != expected:
        raise ValueError('Windows no ha ejecutado exactamente el código que se publica')

def reconstruct_through(last_module):
    for module in range(2, last_module+1):
        folder, script, _ = MODULES[module]
        report = ROOT / '.qa/reconstruccion' / f'M{module:02}.json'
        subprocess.run([sys.executable, str(ROOT / '.github/scripts' / script), '--no-tests',
                        '--out', str(report), '--output-dir', str(ROOT / folder / 'PROYECTO')], cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--modulo', type=int, choices=MODULES, required=True)
    args = parser.parse_args()
    folder, script, _ = MODULES[args.modulo]
    evidence_dir = ROOT / '.qa/sqlserver' / f'm{args.modulo:02}' / 'bases'
    evidence_dir.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, ACERIA_SQL_EVIDENCE_DIR=str(evidence_dir.resolve()),
               DOTNET_CLI_UI_LANGUAGE='en', DOTNET_NOLOGO='true', DOTNET_PROCESSOR_COUNT='1')
    report_path = ROOT / folder / f'M{args.modulo:02}_E2E_RESULTADOS.json'
    command = [sys.executable, str(ROOT / '.github/scripts' / script), '--out', str(report_path)]
    if args.modulo == 2:
        command += ['--output-dir', str(ROOT / folder / 'PROYECTO')]
    output = ROOT / 'docs/validacion-sqlserver' / f'M{args.modulo:02}_SQLSERVER_RESULTADOS.json'
    result = {'modulo': args.modulo, 'fecha_utc': datetime.now(timezone.utc).isoformat(),
              'commit_comprobado': os.environ.get('GITHUB_SHA', subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()),
              'run_url': f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}",
              'resultado': 'FAIL'}
    try:
        reconstruct_through(args.modulo-1)
        subprocess.run(command, cwd=ROOT, env=env, check=True)
        report = json.loads(report_path.read_text(encoding='utf-8'))
        result.update(validate_evidence(report, args.modulo, evidence_dir))
        result['manual_sha256'] = hashlib.sha256((ROOT / folder / 'PRACTICAS' / f'M{args.modulo:02}_PRACTICAS.md').read_bytes()).hexdigest()
        result['archivos_proyectos_sha256'] = file_manifest(ROOT / folder / 'PROYECTO')
        result['codigo_normalizado_sha256'] = source_manifest(ROOT / folder / 'PROYECTO')
        result['evidencias_bd'] = [json.loads(p.read_text()) for p in sorted(evidence_dir.glob('*.json'))]
    except Exception as exc:
        result['error'] = str(exc)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('archivos_proyectos_sha256', 'codigo_normalizado_sha256', 'evidencias_bd')}, ensure_ascii=False), flush=True)
    return 0 if result['resultado'] == 'PASS' else 1

if __name__ == '__main__':
    sys.exit(main())
