#!/usr/bin/env python3
"""Empaqueta únicamente evidencia M07 comprobada y certifica revisión y archivos."""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, sys, tarfile
from pathlib import Path
from validar_sqlserver import file_manifest, source_manifest, validate_windows_sources
ROOT=Path(__file__).resolve().parents[2]
MODULE='M07_OBSERVABILIDAD_RESILIENCIA'
STAGES=['7.1-logging','7.2-health-checks','7.3-gestion-excepciones','7.4-retry-circuit-breaker-polly']
EXPECTED=[309,331,353,403]
CATALOG_TESTS=[12,13,13,18]
FUNCTIONAL_TESTS=[14,9,9,32]
IGNORED={'bin','obj','TestResults','.vs','.git','__pycache__'}
SMOKE_CHECKS=('logging','health_checks','gestion_excepciones','resiliencia','reinicio_con_persistencia')

def require(condition,message):
    if not condition:raise ValueError(message)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def revision_actual(root=ROOT):
    value=os.environ.get('GITHUB_SHA')
    if not value:value=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True,encoding='utf-8').strip()
    require(bool(re.fullmatch(r'[0-9a-f]{40}',value)), 'Falta una revisión Git completa')
    return value

def validate_e2e(report):
    summary=report.get('resumen',{})
    require(summary.get('resultado')=='PASS','E2E no ejecutado o fallido')
    require(summary.get('pasos')==96 and summary.get('tests_por_etapa')==EXPECTED,'E2E incompleto o con conteos incorrectos')
    require(summary.get('base_m06_intacta') is True,'E2E no acredita la conservación de M06')
    stages=report.get('etapas',[])
    require(len(stages)==4,'E2E no contiene cuatro etapas')
    for i,(stage,expected) in enumerate(zip(stages,EXPECTED)):
        require(stage.get('estado')=='PASS' and stage.get('tests_acumulados')==expected,f'E2E etapa 7.{i+1} incompleta')
        require([stage.get(k) for k in ('n_proyectos','n_proyectos_tests','n_documentos')]==[31+i,19+i,36+2*i],f'E2E etapa 7.{i+1}: estructura incorrecta')
    challenges=report.get('retos_optativos',{})
    require(challenges.get('resultado')=='PASS' and challenges.get('etapas_obligatorias_intactas') is True,'Hay un reto fallido o una etapa obligatoria alterada')
    rows=challenges.get('retos',[])
    require(len(rows)==4,'Falta comprobar algún reto')
    for i,(row,expected) in enumerate(zip(rows,EXPECTED)):
        require(row.get('estado')=='PASS' and row.get('test_resumen')=='PASS' and row.get('tests_solucion')==expected+1
                and row.get('tests_proyecto')==CATALOG_TESTS[i]+FUNCTIONAL_TESTS[i]+1,f'Conteo o ejecución incorrecta del reto 7.{i+1}')

def validate_smoke(report,revision,*,windows=False):
    require(report.get('resultado')=='PASS','Smoke HTTP no comprobado')
    require(report.get('commit_comprobado')==revision,'Smoke de otra revisión')
    for name in SMOKE_CHECKS:require(report.get(name)=='PASS',f'Smoke no acredita {name}')
    require(report.get('mensajeria')==('CUBIERTA_EN_LINUX' if windows else 'PASS'),'Smoke no acredita mensajería en Linux')
    require(bool(report.get('codigo_normalizado_sha256')),'Smoke sin hashes de código')

def validate_sql(report,base,revision):
    require(report.get('resultado')=='PASS','SQL Server no comprobado')
    require(report.get('commit_comprobado')==revision,'SQL Server de otra revisión')
    require(report.get('tests_por_etapa')==EXPECTED,'SQL Server: conteos incompletos')
    require(report.get('archivos_proyectos_sha256')==file_manifest(base/'PROYECTO'),'Los archivos publicados difieren de los comprobados en SQL Server')
    require(report.get('codigo_normalizado_sha256')==source_manifest(base/'PROYECTO'),'El código publicado difiere de los hashes SQL Server')
    require(report.get('manual_sha256')==sha(base/'PRACTICAS/M07_PRACTICAS.md'),'El manual difiere del comprobado')
    rows=report.get('evidencias_bd',[])
    require(report.get('proveedor')=='Microsoft.EntityFrameworkCore.SqlServer' and len(rows)>0
            and report.get('bases_verificadas')==len(rows),'Falta evidencia SQL Server real')
    for row in rows:
        require(row.get('provider')=='Microsoft.EntityFrameworkCore.SqlServer' and row.get('engineEdition')==4
                and bool(row.get('version')) and str(row.get('database','')).startswith('AceriaTest_')
                and row.get('modo') in ('conexion_externa','testcontainers'),'Evidencia SQL Server Express inválida')

def validate_pdf(report,base):
    require(isinstance(report,list) and len(report)==2 and {r.get('documento') for r in report}=={'TEORIA','PRACTICAS'},'Informe PDF incompleto')
    for row in report:
        kind=row['documento'];stem=base/kind/f'M07_{kind}'
        require(isinstance(row.get('paginas'),int) and row['paginas']>0 and row.get('paginas_blancas')==[]
                and row.get('desbordamientos')==[] and row.get('bloques_omitidos')==0,f'PDF {kind} incompleto o desbordado')
        require(row.get('markdown_sha256')==sha(stem.with_suffix('.md')) and row.get('pdf_sha256')==sha(stem.with_suffix('.pdf')),f'PDF {kind}: hashes diferentes')

def payload_paths(kind,base):
    if kind=='linux':return [base/'PROYECTO',*[base/name for name in ('M07_E2E_RESULTADOS.json','M07_SQLSERVER_RESULTADOS.json','M07_HTTP_RESULTADOS.json')]]
    if kind=='windows':return [base/'M07_WINDOWS_RESULTADOS.json']
    if kind=='pdf':return [base/'TEORIA/M07_TEORIA.pdf',base/'PRACTICAS/M07_PRACTICAS.pdf',base/'REPORTE_PDF_M07.json']
    raise ValueError('Tipo de artefacto no permitido')

def validate_kind(kind,base,revision):
    if kind=='linux':
        e2e=read(base/'M07_E2E_RESULTADOS.json');validate_e2e(e2e)
        require(e2e.get('manual_sha256')==sha(base/'PRACTICAS/M07_PRACTICAS.md'),'E2E corresponde a otro manual')
        sql=read(base/'M07_SQLSERVER_RESULTADOS.json');validate_sql(sql,base,revision)
        smoke=read(base/'M07_HTTP_RESULTADOS.json');validate_smoke(smoke,revision)
        validate_windows_sources(smoke['codigo_normalizado_sha256'],sql['codigo_normalizado_sha256'],STAGES[-1])
    elif kind=='windows':
        smoke=read(base/'M07_WINDOWS_RESULTADOS.json');validate_smoke(smoke,revision,windows=True)
        require(smoke['codigo_normalizado_sha256']==source_manifest(base/'PROYECTO'/STAGES[-1]),'Windows no ha ejecutado el mismo código')
    elif kind=='pdf':validate_pdf(read(base/'REPORTE_PDF_M07.json'),base)
    else:raise ValueError('Tipo de artefacto no permitido')

def payload_files(kind,base,root):
    files=[]
    for path in payload_paths(kind,base):
        require(path.exists(),f'Falta el archivo del artefacto: {path}')
        files.extend(p for p in (path.rglob('*') if path.is_dir() else [path]) if p.is_file()
                     and not IGNORED.intersection(p.relative_to(root).parts))
    for path in files:require(not path.is_symlink() and path.resolve().is_relative_to(root),'Archivo enlazado fuera del artefacto')
    return sorted(set(files))

def package(kind,*,root=ROOT,revision=None):
    root=Path(root).resolve();base=root/MODULE;revision=revision or revision_actual(root)
    require(bool(re.fullmatch(r'[0-9a-f]{40}',revision)),'Revisión Git inválida')
    validate_kind(kind,base,revision)
    files=payload_files(kind,base,root)
    hashes={p.relative_to(root).as_posix():sha(p) for p in sorted(files)}
    certificate={'tipo':kind,'resultado':'PASS','commit_comprobado':revision,'archivos_sha256':hashes}
    certpath=root/'.qa/m07-certificados'/f'{kind}.json';write(certpath,certificate)
    destination=root/'.qa/m07-artefactos'/f'{kind}.tar.gz';destination.parent.mkdir(parents=True,exist_ok=True)
    temporary=destination.with_suffix('.tmp')
    try:
        with tarfile.open(temporary,'w:gz') as tar:
            for path in [*sorted(files),certpath]:tar.add(path,arcname=path.relative_to(root).as_posix(),recursive=False)
        os.replace(temporary,destination)
    finally:
        if temporary.exists():temporary.unlink()
    return destination

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--tipo',choices=['linux','windows','pdf'],required=True);args=parser.parse_args(argv)
    try:print(package(args.tipo));return 0
    except Exception as exc:print('M07 paquete rechazado: '+str(exc),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
