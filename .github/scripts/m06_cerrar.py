import hashlib,json,os
from pathlib import Path
from validar_sqlserver import file_manifest,validate_windows_sources
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'M06_COMUNICACION_MICROSERVICIOS'
read=lambda name:json.loads((BASE/name).read_text())
sql=read('M06_SQLSERVER_RESULTADOS.json');win=read('M06_WINDOWS_RESULTADOS.json');http=read('M06_HTTP_RESULTADOS.json');pdf=read('REPORTE_PDF_M06.json');e2e=read('M06_E2E_RESULTADOS.json')
assert all(r['resultado']=='PASS' for r in (sql,win,http))
assert sql['commit_comprobado']==win['commit_comprobado']==http['commit_comprobado']==os.environ['GITHUB_SHA']
assert sql['tests_por_etapa']==[232,264,283]
assert sql['archivos_proyectos_sha256']==file_manifest(BASE/'PROYECTO')
assert sql['manual_sha256']==hashlib.sha256((BASE/'PRACTICAS/M06_PRACTICAS.md').read_bytes()).hexdigest()
for r in (win,http):validate_windows_sources(r['codigo_normalizado_sha256'],sql['codigo_normalizado_sha256'],'6.3-cuando-usar-cada-enfoque')
assert e2e['retos_optativos']['resultado']=='PASS'
assert http['mensajeria']=='PASS' and win['reinicio_con_persistencia']=='PASS'
assert isinstance(pdf,list) and len(pdf)==2
for kind in ['TEORIA','PRACTICAS']:
 stem=BASE/kind/('M06_'+kind)
 entry=next(r for r in pdf if r['documento']==kind)
 assert not entry['paginas_blancas'] and not entry['desbordamientos'] and entry['bloques_omitidos']==0
 for ext,key in [('.md','markdown_sha256'),('.pdf','pdf_sha256')]:assert entry[key]==hashlib.sha256(stem.with_suffix(ext).read_bytes()).hexdigest()
run=f'https://github.com/{os.environ["GITHUB_REPOSITORY"]}/actions/runs/{os.environ["GITHUB_RUN_ID"]}'
(BASE/'CIERRE_AUTOMATIZADO.md').write_text(f'''# M06: comprobación automatizada\n\nResultado: PASS. Revisión `{os.environ['GITHUB_SHA']}`.\n\nEjecución: {run}\n\nTres etapas reconstruidas desde el Markdown:232, 264 y 283 pruebas; tres retos ejecutados por separado. SQLServer Express real, RabbitMQ real, recorrido entre dos procesos HTTP y persistencia LocalDB en Windows. Los hashes de manual, proyectos y PDF coinciden con sus informes.\n\nLa revisión visual y el cierre editorial se registran por separado antes de integrar main.\n''')
print('M06 cierre automatizado PASS')
