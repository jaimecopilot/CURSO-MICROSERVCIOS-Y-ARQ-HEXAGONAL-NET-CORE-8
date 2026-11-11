#!/usr/bin/env python3
"""Reconstruye y comprueba M07 contra SQL Server y RabbitMQ reales del host."""
from __future__ import annotations
import json, os, re, subprocess, sys, uuid
from pathlib import Path
from validar_sqlserver import validate_evidence, MODULES, file_manifest, source_manifest
from m07_empaquetar import EXPECTED, ROOT, MODULE, read, revision_actual, sha, validate_e2e, validate_smoke
BASE=ROOT/MODULE
MODULES[7]=(MODULE,'m07_e2e_desde_practicas.py',EXPECTED)

def main():
    report={'resultado':'FAIL','commit_comprobado':os.environ.get('GITHUB_SHA'),
            'run_url':f'https://github.com/{os.environ.get("GITHUB_REPOSITORY","")}/actions/runs/{os.environ.get("GITHUB_RUN_ID","")}'}
    try:
        revision=revision_actual(ROOT);report['commit_comprobado']=revision
        env=dict(os.environ,DOTNET_CLI_UI_LANGUAGE='en',DOTNET_PROCESSOR_COUNT='1',PYTHONUTF8='1')
        if not env.get('ACERIA_TEST_SQLSERVER'):raise RuntimeError('Falta la conexión al SQL Server real iniciado por el host')
        if not env.get('ACERIA_TEST_RABBITMQ'):raise RuntimeError('Falta la conexión al broker real iniciado por el host')
        if not re.fullmatch(r'[0-9a-f]{64}',env.get('ACERIA_RABBIT_CONTAINER_ID','')):raise RuntimeError('Falta el identificador del contenedor RabbitMQ creado por el host')
        folder=ROOT/'.qa/m07-sql'/('bases-'+uuid.uuid4().hex);folder.mkdir(parents=True,exist_ok=False)
        env['ACERIA_SQL_EVIDENCE_DIR']=str(folder.resolve());env['GITHUB_SHA']=revision
        subprocess.run([sys.executable,str(ROOT/'.github/scripts/m07_e2e_desde_practicas.py')],env=env,cwd=ROOT,check=True)
        e2e=read(BASE/'M07_E2E_RESULTADOS.json');validate_e2e(e2e)
        report.update(validate_evidence(e2e,7,folder))
        # validate_evidence puede devolver PASS; no se publica hasta completar HTTP.
        report['resultado']='FAIL'
        subprocess.run([sys.executable,str(ROOT/'.github/scripts/m07_http_real.py')],env=env,cwd=ROOT,check=True)
        smoke=read(BASE/'M07_HTTP_RESULTADOS.json');validate_smoke(smoke,revision)
        report.update(resultado='PASS',broker='RabbitMQ 4.1.5 real con cliente 7.1.2',
                      manual_sha256=sha(BASE/'PRACTICAS/M07_PRACTICAS.md'),
                      archivos_proyectos_sha256=file_manifest(BASE/'PROYECTO'),
                      codigo_normalizado_sha256=source_manifest(BASE/'PROYECTO'),
                      evidencias_bd=[read(p) for p in sorted(folder.glob('*.json'))])
    except Exception as exc:report.update(resultado='FAIL',error=str(exc))
    BASE.mkdir(parents=True,exist_ok=True)
    (BASE/'M07_SQLSERVER_RESULTADOS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('archivos_proyectos_sha256','codigo_normalizado_sha256','evidencias_bd')},ensure_ascii=False),flush=True)
    return 0 if report['resultado']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
