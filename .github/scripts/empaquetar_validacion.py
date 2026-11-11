import argparse
from pathlib import Path
import tarfile
from validar_sqlserver import ROOT, MODULES
p=argparse.ArgumentParser();p.add_argument('--tipo',choices=['sql','windows','pdf'],required=True);p.add_argument('--modulo',type=int,choices=MODULES)
a=p.parse_args(); files=[]
if a.tipo=='sql':
 folder=ROOT/MODULES[a.modulo][0]
 files=[p for p in (folder/'PROYECTO').rglob('*') if p.is_file() and not {'bin','obj','TestResults','__pycache__'}.intersection(p.parts)]
 files += [folder/f'M{a.modulo:02}_E2E_RESULTADOS.json',ROOT/f'docs/validacion-sqlserver/M{a.modulo:02}_SQLSERVER_RESULTADOS.json']
elif a.tipo=='windows':files=[ROOT/f'docs/validacion-sqlserver/M{a.modulo:02}_LOCALDB_RESULTADOS.json']
else:
 for folder,_,_ in MODULES.values():
  for kind in ['TEORIA','PRACTICAS']:files+=list((ROOT/folder/kind).glob('*.pdf'))
  files+=list((ROOT/folder).glob('REPORTE_PDF_*.json'))
 files.append(ROOT/'docs/validacion-sqlserver/PDF_RESULTADOS.json')
out=ROOT/'.qa/empaquetados'/f'{a.tipo}-{a.modulo or "todos"}.tar.gz';out.parent.mkdir(parents=True,exist_ok=True)
with tarfile.open(out,'w:gz') as tar:
 for f in files:tar.add(f,arcname=f.relative_to(ROOT))
print(out)
