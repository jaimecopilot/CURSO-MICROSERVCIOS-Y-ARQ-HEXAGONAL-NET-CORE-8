import argparse,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'M06_COMUNICACION_MICROSERVICIOS'
p=argparse.ArgumentParser();p.add_argument('--tipo',choices=['linux','windows','pdf'],required=True);args=p.parse_args()
paths=[]
if args.tipo=='linux':paths=[BASE/'PROYECTO',*[BASE/name for name in ['M06_E2E_RESULTADOS.json','M06_SQLSERVER_RESULTADOS.json','M06_HTTP_RESULTADOS.json']]]
elif args.tipo=='windows':paths=[BASE/'M06_WINDOWS_RESULTADOS.json']
else:paths=[BASE/'TEORIA/M06_TEORIA.pdf',BASE/'PRACTICAS/M06_PRACTICAS.pdf',BASE/'REPORTE_PDF_M06.json']
out=ROOT/'.qa/m06-artefactos';out.mkdir(parents=True,exist_ok=True)
with tarfile.open(out/(args.tipo+'.tar.gz'),'w:gz') as tar:
 for path in paths:
  assert path.exists(),path
  for file in (path.rglob('*') if path.is_dir() else [path]):
   if file.is_file() and not {'bin','obj','TestResults','.vs','__pycache__'}.intersection(file.relative_to(ROOT).parts):tar.add(file,arcname=file.relative_to(ROOT))
