#!/usr/bin/env python3
"""Reconstruye las cinco etapas M05 exclusivamente desde el manual del alumno.

Copia M04 4.5 y aplica los bloques tipados en orden. Nunca lee el código
final M05 para construirlo. Verifica compilaciones intermedias, toda la suite,
los cinco retos aislados y la conservación de documentos y etapas anteriores.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, textwrap
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'M05_DDD_CQRS'
PRACTICAS=BASE/'PRACTICAS/M05_PRACTICAS.md'
M04=ROOT/'M04_PATRONES_ARQUITECTURA/PROYECTO/4.5-inyeccion-dependencias'
STAGES=['5.1-conceptos-ddd','5.2-entidades-value-objects','5.3-casos-de-uso','5.4-commands-queries','5.5-dominio-aceria']
PROJECT_NAMES=['Ddd','ModeloDominio','CasosDeUso','Cqrs','DominioAceria']
CATALOG_TESTS=[11,12,12,12,10]
FUNCTIONAL_TESTS=[5,7,7,6,8]
EXPECTED=[118+sum(CATALOG_TESTS[:i+1])+sum(FUNCTIONAL_TESTS[:i+1]) for i in range(5)]
PROJECT_COUNTS=[16,17,20,21,22]
CHECKPOINTS={f'5.{i}':{2,6,7,8,9,10,11,12,13,14,15,16} for i in range(1,6)}
IGNORED={'bin','obj','TestResults','.vs','.git','__pycache__'}
NS={'t':'http://microsoft.com/schemas/VisualStudio/TeamTest/2010'}

class LabError(RuntimeError): pass

def check(ok,msg):
 if not ok: raise LabError(msg)

def command(*args,cwd:Path,timeout=600):
 env={**os.environ,'DOTNET_CLI_UI_LANGUAGE':'en','DOTNET_NOLOGO':'true',
      'DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1','DOTNET_PROCESSOR_COUNT':'1'}
 p=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                  text=True,errors='replace',timeout=timeout)
 if p.returncode: raise LabError('Comando fallido '+repr(args)+'\n'+p.stdout[-10000:])
 return p.stdout

def text_sha(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def disk_sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(directory):
 return {str(p.relative_to(directory)):disk_sha(p) for p in sorted(directory.rglob('*'))
         if p.is_file() and not any(x in IGNORED for x in p.relative_to(directory).parts)}
def manifest_sha(values):return text_sha(json.dumps(values,sort_keys=True,ensure_ascii=False))
def copy_project(previous,destination):
 check(previous.is_dir(),f'No existe la etapa anterior: {previous}')
 shutil.copytree(previous,destination,ignore=shutil.ignore_patterns(*IGNORED))

def read_markdown():
 content=PRACTICAS.read_text(encoding='utf-8')
 expected=[f'5.{i}.{n}' for i in range(1,6) for n in range(1,25)]
 positions=list(re.finditer(r'^### PASO (5\.[1-5]\.\d+) —',content,re.M))
 check([m.group(1) for m in positions]==expected,'Los 120 pasos no están completos o en orden')
 check(not re.search(r'(?i)\b(?:fuente|procedencia)\b',content),'Texto editorial no permitido en el manual')
 check(not re.search(r'^##?\s+Errores comunes del ejercicio completo',content,re.M|re.I),'Hay un bloque global de errores repetido')
 for i,m in enumerate(positions):
  body=content[m.end():positions[i+1].start() if i+1<len(positions) else len(content)]
  match=re.search(r'\*\*Procedimiento guiado\.\*\*\n\n((?:[1-9]\. [^\n]+\n){4,})',body)
  check(match is not None,m.group(1)+': falta procedimiento guiado')
  check(re.findall(r'^([1-9])\. ',match.group(1),re.M)==['1','2','3','4'],m.group(1)+': debe haber cuatro acciones')
  check('**Por qué funciona así.**' in body and '**Verificación concreta.**' in body,m.group(1)+': faltan explicaciones o verificación')
 patterns={kind:re.compile(r'<!-- '+kind+r' (\{[^\n]+\}) -->\n```(csharp|xml|markdown|json|text)\n([\s\S]*?)\n```') for kind in ('M05_CODIGO','M05_RETO')}
 records={kind:[] for kind in patterns}
 for kind,pat in patterns.items():
  for m in pat.finditer(content):
   info=json.loads(m.group(1));info.update(tipo=m.group(2),codigo=m.group(3)+'\n')
   check(info.get('modo') in ('crear','reemplazar','insertar_antes','insertar_despues'),'Operación no válida: '+str(info))
   path=Path(info.get('ruta',''))
   check(str(path)!='.' and not path.is_absolute() and '..' not in path.parts,'Ruta insegura: '+str(path))
   check(info['paso'] in expected if kind=='M05_CODIGO' else re.fullmatch(r'5\.[1-5]\.reto\.(1|3|6)',info['paso']), 'Paso de bloque no válido')
   current=[p for p in positions if p.start()<m.start()][-1].group(1)
   check(info['paso']==current if kind=='M05_CODIGO' else info['paso'][:3]==current[:3],f'Bloque de {info["paso"]} fuera de su paso')
   records[kind].append(info)
 check(len(records['M05_CODIGO'])>=65,'Faltan operaciones obligatorias')
 check(len(records['M05_RETO'])==15,'Deben existir tres fragmentos por cada uno de cinco retos')
 check(content.count('## Reto de ampliación (optativo)')==5,'Faltan los cinco retos completos')
 # Verify quoted explanations against their displayed code, counting blank lines.
 in_fence=False;block=[];last=[]
 for line_number,line in enumerate(content.splitlines(),1):
  if line.startswith('```'):
   if in_fence:last=block;block=[]
   in_fence=not in_fence
  elif in_fence:block.append(line)
  else:
   explanation=re.match(r'- \*\*Línea (\d+):\*\* `([^`]+)`',line)
   if explanation:
    number=int(explanation.group(1));quote=explanation.group(2)
    check(1<=number<=len(last) and quote.strip() in last[number-1].strip(),f'Explicación desalineada en línea Markdown {line_number}: {quote}')
 for record in records['M05_CODIGO']:
  if record['tipo']=='markdown':
   for line in record['codigo'].splitlines():
    check(not any(re.search(r'\b\w+<[^>]+>',part) for part in re.split(r'`[^`]*`',line)),f'Genérico sin formato de código en {record["ruta"]}: {line}')
 return content,records['M05_CODIGO'],records['M05_RETO']

def apply_one(stage,record):
 path=stage/record['ruta'];path.parent.mkdir(parents=True,exist_ok=True)
 mode=record['modo'];code=record['codigo']
 if record.get('sangria'):code='\n\n'+textwrap.indent(code,' '*record['sangria'])
 if mode=='crear':
  check(not path.exists(),f'Archivo ya existente al crearlo: {path}')
  path.write_text(code,encoding='utf-8')
 elif mode=='reemplazar':
  check(path.is_file(),f'Archivo ausente para reemplazar: {path}')
  path.write_text(code,encoding='utf-8')
 else:
  check(path.is_file(),f'Archivo ausente para insertar: {path}')
  original=path.read_text(encoding='utf-8');anchor=record.get('ancla')
  check(anchor is not None and original.count(anchor)==1,f'Ancla no única en {path}: {anchor!r}')
  replacement=code+anchor if mode=='insertar_antes' else anchor+'\n'+code
  path.write_text(original.replace(anchor,replacement,1),encoding='utf-8')
 return path

def projects(stage):return sorted(p for p in stage.rglob('*.csproj') if not any(x in IGNORED for x in p.parts))
def ensure_solution(stage):
 sln=stage/'AceriaApp.sln'
 if not sln.exists():command('dotnet','new','sln','--name','AceriaApp',cwd=stage)
 files=projects(stage);check(files,'La etapa no contiene proyectos')
 # Always add all projects, including when the copied solution already exists.
 for project in files:command('dotnet','sln','AceriaApp.sln','add',str(project.relative_to(stage)),cwd=stage)
 listing=command('dotnet','sln','AceriaApp.sln','list',cwd=stage).replace('\\','/')
 for p in files:check(p.relative_to(stage).as_posix() in listing,f'La solución omite {p}')
 return len(files)

def compare_inherited(previous,current):
 before=manifest(previous/'docs');after=manifest(current/'docs')
 for path,sha in before.items():check(after.get(path)==sha,f'Documento heredado alterado: {current/path}')
 return len(before)

def compare_inherited_tests(previous,current):
 before={path:sha for path,sha in manifest(previous/'tests').items() if path.endswith('.cs')}
 after=manifest(current/'tests')
 for path,sha in before.items():check(after.get(path)==sha,f'Prueba heredada alterada o eliminada: {current / "tests" / path}')
 return len(before)

def build_and_test(stage,expected):
 command('dotnet','restore','AceriaApp.sln','-p:NuGetAudit=false',cwd=stage)
 build=command('dotnet','build','AceriaApp.sln','-c','Release','--no-restore',cwd=stage)
 resultdir=stage/'TestResults'
 if resultdir.exists():shutil.rmtree(resultdir)
 command('dotnet','test','AceriaApp.sln','-c','Release','--no-build','--no-restore',
         '--logger','trx','--results-directory',str(resultdir),cwd=stage)
 results=[];total=0
 for trx in sorted(resultdir.glob('*.trx')):
  xml=ET.parse(trx);tests=xml.findall('.//t:UnitTestResult',NS)
  check(tests,f'Archivo TRX sin resultados: {trx}')
  check(all(t.get('outcome')=='Passed' for t in tests),'Hay fallos u omisiones en '+trx.name+': '+str([(t.get('testName'),t.get('outcome')) for t in tests if t.get('outcome')!='Passed']))
  summary=xml.find('.//t:Counters',NS)
  check(summary is not None and int(summary.get('total','0'))==len(tests) and int(summary.get('passed','0'))==len(tests),'Contadores TRX no coinciden: '+trx.name)
  total+=len(tests)
  results.append({'proyecto':trx.stem,'tests':len(tests),'metodos':[t.get('testName') for t in tests]})
 check(total==expected,f'Esperadas {expected} pruebas; ejecutadas {total}')
 return {'tests':total,'test_projects':len(results),'proyectos':results,'compilacion':'PASS','build_tail':build[-300:]}

def verify_sql_server(stage):
 helper=stage/'tests/Compartido/SqlServerPruebas.cs'
 check(helper.is_file(),'Falta el helper SQL Server heredado de la etapa anterior')
 forbidden=re.compile(r'\bUse(?:Sqlite|InMemoryDatabase)\s*\(|Microsoft\.EntityFrameworkCore\.(?:Sqlite|InMemory)|Microsoft\.Data\.Sqlite')
 for path in stage.rglob('*'):
  if path.suffix in ('.cs','.csproj') and not any(part in IGNORED for part in path.parts):
   check(not forbidden.search(path.read_text(encoding='utf-8')),f'Proveedor de integración no permitido: {path}')
 relational=[]
 for project in projects(stage):
  if 'tests' not in project.relative_to(stage).parts:continue
  xml=ET.parse(project);includes=[element.get('Include','') for element in xml.findall('.//Compile')]
  files=list(project.parent.glob('*.cs'))+[project.parent/include for include in includes]
  uses_database=any(path.is_file() and ('BaseSqlServer.Crear()' in path.read_text(encoding='utf-8'))
                    for path in files if path.name!='SqlServerPruebas.cs')
  if not uses_database:continue
  check('../Compartido/SqlServerPruebas.cs' in includes,f'Falta vincular el helper SQL Server: {project}')
  packages={element.get('Include'):element.get('Version') for element in xml.findall('.//PackageReference')}
  check(packages.get('Testcontainers.MsSql')=='3.10.0',f'Falta Testcontainers.MsSql 3.10.0: {project}')
  relational.append(str(project.relative_to(stage)))
 check(relational,'No se han encontrado proyectos de integración SQL Server')
 return relational

def verify_architecture(stage,number):
 domain=stage/'src/AceriaApp.Produccion.Dominio/AceriaApp.Produccion.Dominio.csproj'
 check(domain.exists(),'Falta el dominio independiente de Producción')
 contents=domain.read_text()
 check('ProjectReference' not in contents and 'PackageReference' not in contents,'Producción.Dominio depende de una capa o biblioteca exterior')
 sources='\n'.join(p.read_text() for p in domain.parent.rglob('*.cs') if not any(x in IGNORED for x in p.parts))
 check(not re.search(r'using (?:Microsoft\.EntityFrameworkCore|Microsoft\.AspNetCore|AceriaApp\.Hexagonal)',sources),'El dominio de Producción importa infraestructura o el modelo heredado')
 if number>=3:
  app=stage/'src/AceriaApp.Produccion.Aplicacion/AceriaApp.Produccion.Aplicacion.csproj'
  infra=stage/'src/AceriaApp.Produccion.Infraestructura/AceriaApp.Produccion.Infraestructura.csproj'
  check('AceriaApp.Produccion.Dominio.csproj' in app.read_text(),'La aplicación no depende del modelo de Producción')
  check('AceriaApp.Produccion.Infraestructura' not in app.read_text() and 'EntityFrameworkCore' not in app.read_text(),'La aplicación de Producción depende de persistencia')
  check('AceriaApp.Produccion.Aplicacion.csproj' in infra.read_text(),'Infraestructura no implementa los puertos de Producción')
  if number>=4:check('MediatR' in app.read_text() and '12.4.1' in app.read_text(),'MediatR no tiene versión reproducible')

def verify_challenges(output,records):
 before=manifest(output);results=[]
 for i,slug in enumerate(STAGES,1):
  entry={'punto':f'5.{i}','estado':'FAIL'}
  try:
   batch=[r for r in records if r['paso'].startswith(f'5.{i}.reto.')]
   check(len(batch)==3,f'Reto 5.{i}: faltan fragmentos')
   with tempfile.TemporaryDirectory(prefix=f'm05-reto-{i}-') as temp:
    stage=Path(temp)/slug;copy_project(output/slug,stage)
    for r in batch:apply_one(stage,r)
    ensure_solution(stage)
    outcome=build_and_test(stage,EXPECTED[i-1]+1)
    project='AceriaApp.'+PROJECT_NAMES[i-1]+'.Tests'
    target=[p for p in outcome['proyectos'] if any(t.startswith(project+'.') for t in p['metodos'])]
    check(len(target)==1,'No se identifica el proyecto de tests del reto '+project)
    expected=CATALOG_TESTS[i-1]+FUNCTIONAL_TESTS[i-1]+1
    check(target[0]['tests']==expected,f'Reto {project}: resultado inesperado')
    check(any('.Resumen_ConCatalogoPorDefecto_' in t for t in target[0]['metodos']),'No se ejecutó la prueba del resumen')
    entry.update(estado='PASS',tests_proyecto=expected,tests_solucion=outcome['tests'],fragmentos_csharp=3,
                 archivos=sorted(set(r['ruta'] for r in batch)),test_resumen='PASS')
  except Exception as exc:entry['error']=str(exc)
  results.append(entry);print(json.dumps(entry,ensure_ascii=False),flush=True)
 check(manifest(output)==before,'Los retos han modificado las etapas obligatorias')
 return {'resultado':'PASS' if all(r['estado']=='PASS' for r in results) else 'FAIL',
         'etapas_obligatorias_intactas':True,'retos':results}

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--out',type=Path,default=BASE/'M05_E2E_RESULTADOS.json')
 parser.add_argument('--output-dir',type=Path,default=BASE/'PROYECTO')
 parser.add_argument('--no-tests',action='store_true',help='Reconstrucción e inspección sin afirmar ejecución de tests')
 args=parser.parse_args()
 report={'fecha':datetime.now(timezone.utc).isoformat(),'manual':'PRACTICAS/M05_PRACTICAS.md',
         'construccion':'base M04 4.5 más bloques del manual, sin copiar una etapa final M05',
         'etapas':[],'pasos':[]}
 try:
  content,codes,challenges=read_markdown();report['manual_sha256']=text_sha(content)
  base_manifest=manifest(M04);report['base_m04']={'etapa':str(M04.relative_to(ROOT)),'proyectos':14,'tests':118,'proyectos_tests':10,
      'sha256':manifest_sha(base_manifest),'archivos':base_manifest}
  check(len(projects(M04))==14,'La base debe contener catorce proyectos')
  check(len([p for p in projects(M04) if p.is_relative_to(M04/'tests')])==10,'La base debe contener diez proyectos de tests')
  output=args.output_dir.resolve()
  check(output!=M04.resolve() and M04.resolve() not in output.parents and output not in M04.resolve().parents,
        'El directorio de salida se solapa con la base de M04')
  output.mkdir(parents=True,exist_ok=True);previous=M04
  for i,slug in enumerate(STAGES,1):
   stage=output/slug
   if stage.exists():shutil.rmtree(stage)
   previous_manifest=manifest(previous);copy_project(previous,stage)
   builds=[];actions=0
   for step in range(1,25):
    identifier=f'5.{i}.{step}';batch=[r for r in codes if r['paso']==identifier]
    for record in batch:apply_one(stage,record);actions+=1
    if not args.no_tests and step in CHECKPOINTS[f'5.{i}']:
     target='AceriaApp.sln' if step in (2,16) else f'tests/AceriaApp.{PROJECT_NAMES[i-1]}.Tests/AceriaApp.{PROJECT_NAMES[i-1]}.Tests.csproj' if step in (11,12,13,14,15) else 'src/AceriaApp.Api/AceriaApp.Api.csproj'
     if target=='AceriaApp.sln':ensure_solution(stage)
     command('dotnet','build',target,'-c','Release','-p:NuGetAudit=false',cwd=stage)
     builds.append({'paso':identifier,'objetivo':target,'resultado':'PASS'})
    report['pasos'].append({'paso':identifier,'codigo_escrito':len(batch),'archivos':[r['ruta'] for r in batch],
        'resultado':'codigo_aplicado_y_verificado' if batch and not args.no_tests else 'codigo_aplicado' if batch else 'guia_manual_no_simulada'})
   total_projects=ensure_solution(stage)
   check(total_projects==PROJECT_COUNTS[i-1],f'Etapa {slug}: se esperaban {PROJECT_COUNTS[i-1]} proyectos')
   verify_architecture(stage,i);sql_projects=verify_sql_server(stage);inherited=compare_inherited(previous,stage);inherited_tests=compare_inherited_tests(previous,stage)
   check(manifest(previous)==previous_manifest,'La etapa anterior se ha alterado')
   outcome=build_and_test(stage,EXPECTED[i-1]) if not args.no_tests else {'tests':None,'test_projects':None,'proyectos':[]}
   check(args.no_tests or outcome['test_projects']==10+i,'Falta un proyecto de tests en la solución')
   current_manifest=manifest(stage)
   report['etapas'].append({'punto':f'5.{i}','carpeta':slug,'pasos':24,'operaciones_codigo':actions,
       'n_proyectos':total_projects,'documentos_heredados_identicos':inherited,
       'proveedor_configurado':'Microsoft.EntityFrameworkCore.SqlServer','proyectos_sql_server':sql_projects,'archivos_tests_heredados_identicos':inherited_tests,
       'builds_intermedios':len(builds),'compilaciones':builds,'tests_acumulados':outcome['tests'],
       'tests_catalogo_nuevos':CATALOG_TESTS[i-1],'tests_funcionales_nuevos':FUNCTIONAL_TESTS[i-1],
       'expected':EXPECTED[i-1],'tests_proyectos':outcome['proyectos'],
       'estado':'PASS' if not args.no_tests else 'SIN_EJECUTAR_TESTS',
       'sha256':manifest_sha(current_manifest),'archivos':current_manifest})
   print(f'M05 5.{i}: {actions} operaciones desde manual; {len(builds)} compilaciones intermedias; {outcome["tests"]} tests; {total_projects} proyectos',flush=True)
   previous=stage
  check(len(report['pasos'])==120,'No se han recorrido los 120 pasos')
  check(manifest(M04)==base_manifest,'La base de M04 ha cambiado')
  if not args.no_tests:
   report['retos_optativos']=verify_challenges(output,challenges)
   check(report['retos_optativos']['resultado']=='PASS','Hay retos optativos sin superar')
  report['resumen']={'resultado':'PASS' if not args.no_tests else 'SIN_TESTS','pasos':120,
      'operaciones_codigo':len(codes),'archivos_distintos':len(set(r['ruta'] for r in codes)),
      'builds_intermedios':sum(e['builds_intermedios'] for e in report['etapas']),
      'tests_por_etapa':EXPECTED,'base_m04_intacta':True}
 except Exception as exc:report['resumen']={'resultado':'FAIL','error':str(exc)}
 args.out.parent.mkdir(parents=True,exist_ok=True)
 args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report['resumen'],ensure_ascii=False),flush=True)
 if report['resumen']['resultado']=='FAIL':sys.exit(1)
if __name__=='__main__':main()
