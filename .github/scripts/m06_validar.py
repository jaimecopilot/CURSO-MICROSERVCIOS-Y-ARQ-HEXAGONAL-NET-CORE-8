#!/usr/bin/env python3
"""La ausencia de SQL Server o RabbitMQ nunca se considera una prueba superada."""
import os,json,sys,subprocess,hashlib
from pathlib import Path
from validar_sqlserver import validate_evidence, MODULES, file_manifest, source_manifest
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'M06_COMUNICACION_MICROSERVICIOS'
MODULES[6]=('M06_COMUNICACION_MICROSERVICIOS','m06_e2e_desde_practicas.py',[232,264,283])

def main():
    folder=ROOT/'.qa/m06-sql/bases';folder.mkdir(parents=True,exist_ok=False)
    env=dict(os.environ,ACERIA_SQL_EVIDENCE_DIR=str(folder),DOTNET_CLI_UI_LANGUAGE='en',DOTNET_PROCESSOR_COUNT='1')
    report={'resultado':'FAIL','commit_comprobado':os.environ.get('GITHUB_SHA'),
            'run_url':f'https://github.com/{os.environ.get("GITHUB_REPOSITORY","")}/actions/runs/{os.environ.get("GITHUB_RUN_ID","")}'}
    try:
        if not env.get('ACERIA_TEST_RABBITMQ'):raise RuntimeError('Falta la conexión al broker real iniciada por el host')
        subprocess.run([sys.executable,str(ROOT/'.github/scripts/m06_e2e_desde_practicas.py')],env=env,cwd=ROOT,check=True)
        e2e=json.loads((BASE/'M06_E2E_RESULTADOS.json').read_text())
        report.update(validate_evidence(e2e,6,folder))
        subprocess.run([sys.executable,str(ROOT/'.github/scripts/m06_http_real.py')],env=env,cwd=ROOT,check=True)
        report.update(resultado='PASS',broker='RabbitMQ 4.1.5 real, cliente 7.1.2, pruebas de entrega/reencolado/DLQ y recorrido HTTP',
                      manual_sha256=hashlib.sha256((BASE/'PRACTICAS/M06_PRACTICAS.md').read_bytes()).hexdigest(),
                      archivos_proyectos_sha256=file_manifest(BASE/'PROYECTO'),codigo_normalizado_sha256=source_manifest(BASE/'PROYECTO'),
                      evidencias_bd=[json.loads(p.read_text()) for p in folder.glob('*.json')])
    except Exception as exc:report.update(resultado='FAIL',error=str(exc))
    (BASE/'M06_SQLSERVER_RESULTADOS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('archivos_proyectos_sha256','codigo_normalizado_sha256','evidencias_bd')},ensure_ascii=False))
    return 0 if report['resultado']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
