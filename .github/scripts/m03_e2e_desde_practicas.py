#!/usr/bin/env python3
"""Reconstruye cuatro etapas M03 a partir del propio Markdown del alumno.

NO copia ningún .cs/.csproj final de M03: copia M02 2.4 como punto de
partida y aplica en orden las operaciones tipadas M03_CODIGO del manual.
Compila en puntos intermedios y ejecuta las pruebas xUnit acumuladas.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, textwrap
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'M03_ARQUITECTURA_HEXAGONAL'
PRACTICAS=BASE/'PRACTICAS/M03_PRACTICAS.md'
TEORIA=BASE/'TEORIA/M03_TEORIA.md'
M02=ROOT/'M02_APIS_REST_ASPNET_CORE/PROYECTO/2.4-documentacion-openapi'
STAGES=['3.1-capas-aplicacion','3.2-puertos-adaptadores','3.3-separacion-capas','3.4-implementacion-aspnet-core']
EXPECTED=[23,31,38,50]
CHECKPOINTS={
 '3.1':{6,7,9,14,15},
 '3.2':{6,7,8,10,14,15},
 '3.3':{6,7,9,12,14,15},
 '3.4':{5,6,7,9,10,12,13,14,15,17},
}

class LabError(RuntimeError):pass
def check(ok,msg):
 if not ok:raise LabError(msg)
def command(*args,cwd:Path,timeout=600):
 env={**os.environ,'DOTNET_CLI_UI_LANGUAGE':'en','DOTNET_NOLOGO':'true','DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1'}
 p=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace',timeout=timeout)
 if p.returncode:
  raise LabError('Comando fallido '+repr(args)+'\n'+p.stdout[-7000:])
 return p.stdout

def text_sha(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()
def disk_sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copy_project(source,destination):
 check(source.exists(),f'No existe base de la etapa: {source}')
 shutil.copytree(source,destination,ignore=shutil.ignore_patterns('bin','obj','TestResults','.vs','.git'),dirs_exist_ok=False)

def read_markdown():
 source=PRACTICAS.read_text(encoding='utf-8')
 theory=TEORIA.read_text(encoding='utf-8')
 h=re.findall(r'^### PASO (3\.[1-4]\.\d+) —',source,re.M)
 expected=[f'3.{i}.{n}' for i in range(1,5) for n in range(1,25)]
 check(h==expected,f'Pasos M03 incompletos: {len(h)}, esperados 96 y orden correcto')
 check(len(re.findall(r'^### Bloque \d+ —',theory,re.M))==40,'No hay 40 bloques en teoría M03')
 positions=list(re.finditer(r'^### PASO (3\.[1-4]\.\d+) —',source,re.M))
 for i,m in enumerate(positions):
  body=source[m.end():positions[i+1].start() if i+1<len(positions) else len(source)]
  steps=re.search(r'\*\*Procedimiento guiado\.\*\*\n\n((?:[1-9]\. [^\n]+\n){4,})',body)
  check(steps is not None,m.group(1)+': faltan 4 acciones guiadas numeradas')
  nums=[int(a) for a in re.findall(r'^([1-9])\. ',steps.group(1),re.M)]
  check(nums==[1,2,3,4],m.group(1)+': las acciones deben ser 1-4')
  check('**Verificación concreta.**' in body,m.group(1)+': falta criterio de resultado')
  check('**Por qué funciona así.**' in body,m.group(1)+': falta justificación')
 check(re.search(r'^## Errores\s+comunes\s+del\s+ejercicio\s+completo\s*$',source,re.I|re.M) is None,'Bloque global de errores repetido en M03')
 codepat=re.compile(r'<!-- M03_CODIGO (\{[^\n]+\}) -->\n```(csharp|xml|markdown|json|text)\n([\s\S]*?)\n```')
 found=[]
 for m in codepat.finditer(source):
  info=json.loads(m.group(1));info['tipo']=m.group(2);info['codigo']=m.group(3)+'\n'
  check(info.get('paso') in expected,'Marcador de código fuera de 96 pasos: '+str(info))
  check(info.get('modo') in ('crear','reemplazar','insertar_antes','insertar_despues'),'Modo desconocido '+str(info))
  check(info.get('ruta') and '..' not in Path(info['ruta']).parts,'Ruta insegura en código M03')
  found.append(info)
 check(len(found)>=50,f'Insuficientes operaciones de código M03: {len(found)}')
 # Every file code block must be inside its declared step, never in a later step.
 for i,m in enumerate(positions):
  body=source[m.end():positions[i+1].start() if i+1<len(positions) else len(source)]
  for tagged in codepat.finditer(body):
   rec=json.loads(tagged.group(1))
   check(rec['paso']==m.group(1),f'Código {rec["paso"]} insertado bajo {m.group(1)}')
 return source,theory,found

def apply_one(stage:Path,record):
 path=stage/record['ruta'];path.parent.mkdir(parents=True,exist_ok=True)
 mode=record['modo'];code=record['codigo']
 if mode=='crear':
  check(not path.exists(),f'No se puede crear dos veces: {path}')
  path.write_text(code,encoding='utf-8')
 elif mode=='reemplazar':
  check(path.exists(),f'Sin archivo para reemplazar: {path}')
  path.write_text(code,encoding='utf-8')
 else:
  check(path.is_file(),f'Sin archivo para insertar: {path}')
  original=path.read_text(encoding='utf-8');anchor=record.get('ancla')
  check(anchor is not None and original.count(anchor)==1,
        f'Ancla ambigua para {path}: {anchor}: {original.count(anchor or "")}')
  replacement=code+anchor if mode=='insertar_antes' else anchor+'\n'+code
  path.write_text(original.replace(anchor,replacement,1),encoding='utf-8')
 return path

def project_files(stage:Path):
 return sorted(x for x in stage.rglob('*.csproj') if 'obj' not in x.parts and 'bin' not in x.parts)

def ensure_solution(stage:Path):
 sln=stage/'AceriaApp.sln'
 if not sln.exists():command('dotnet','new','sln','--name','AceriaApp',cwd=stage)
 files=project_files(stage)
 check(files,'No hay proyectos .csproj')
 # Dotnet sln add reports a success when an existing project is already listed.
 for project in files:
  command('dotnet','sln','AceriaApp.sln','add',str(project.relative_to(stage)),cwd=stage)
 return len(files)

def verify_sql_isolation(stage:Path):
 helper=stage/'tests/Compartido/SqlServerPruebas.cs'
 check(helper.is_file(),'Falta helper SQL Server heredado de M02 2.1.22')
 project=stage/'tests/AceriaApp.Api.Tests/AceriaApp.Api.Tests.csproj'
 xml=project.read_text(encoding='utf-8')
 check('Testcontainers.MsSql' in xml and '3.10.0' in xml,'Falta Testcontainers.MsSql 3.10.0')
 check('../Compartido/SqlServerPruebas.cs' in xml and '<Compile ' in xml,'Falta enlace Compile al helper')
 for path in list(stage.rglob('*.cs'))+list(stage.rglob('*.csproj')):
  if any(x in path.parts for x in ('obj','bin')):continue
  code=path.read_text(encoding='utf-8')
  check('UseInMemoryDatabase' not in code and 'EntityFrameworkCore.InMemory' not in code,
        'Proveedor no relacional en '+str(path))
 return disk_sha(helper)


def verify_architecture(stage:Path,n:int):
 if n<3:return
 domain=stage/'src/AceriaApp.Hexagonal.Dominio/AceriaApp.Hexagonal.Dominio.csproj'
 app=stage/'src/AceriaApp.Hexagonal.Aplicacion/AceriaApp.Hexagonal.Aplicacion.csproj'
 infra=stage/'src/AceriaApp.Hexagonal.Infraestructura/AceriaApp.Hexagonal.Infraestructura.csproj'
 api=stage/'src/AceriaApp.Api/AceriaApp.Api.csproj'
 for f in (domain,app,infra,api):check(f.exists(),f'Falta proyecto de capa: {f}')
 d=domain.read_text();a=app.read_text();i=infra.read_text();api_src=api.read_text()
 check('ProjectReference' not in d and 'EntityFrameworkCore' not in d,'Dominio depende de infraestructura')
 check('AceriaApp.Hexagonal.Dominio.csproj' in a and 'AceriaApp.Hexagonal.Infraestructura' not in a,'Aplicación invierte dependencias')
 check('AceriaApp.Hexagonal.Aplicacion.csproj' in i and 'EntityFrameworkCore.SqlServer' in i,'Adaptador SQL no implementado')
 check('AceriaApp.Hexagonal.Aplicacion.csproj' in api_src and 'AceriaApp.Hexagonal.Infraestructura.csproj' in api_src,'API no compone los adaptadores')
 if n==4:
  endpoints=(stage/'src/AceriaApp.Api/Hexagonal/HexagonalOrdenesEndpoints.cs').read_text()
  check('OrdenesCasoUso' in endpoints and 'HexagonalDbContext' not in endpoints and 'EntityFrameworkCore' not in endpoints,
        'La presentación depende directamente de EF Core')
  program=(stage/'src/AceriaApp.Api/Program.cs').read_text()
  for term in ('AddServiciosHexagonales','MapHexagonalOrdenes','SkipDatabaseInitialization'):
   check(term in program,'No está conectada la API con el puerto real: '+term)


def compare_inherited(prev:Path,current:Path):
 inherited=prev/'docs';now=current/'docs'
 if not inherited.exists():return 0
 count=0
 for f in inherited.rglob('*'):
  if not f.is_file():continue
  other=now/f.relative_to(inherited)
  check(other.exists() and disk_sha(f)==disk_sha(other),f'Documento heredado alterado: {other}')
  count+=1
 return count

def build_and_test(stage:Path,expected:int):
 command('dotnet','restore','AceriaApp.sln',cwd=stage)
 log=command('dotnet','build','AceriaApp.sln','-c','Release','--no-restore',cwd=stage)
 outcome=command('dotnet','test','AceriaApp.sln','-c','Release','--no-build','--no-restore',cwd=stage)
 matches=re.findall(r'Passed:\s*(\d+),\s*Skipped:\s*(\d+),\s*Total:\s*(\d+)',outcome)
 check(matches, 'No se pudieron leer los resultados xUnit: '+outcome[-3000:])
 found=sum(int(k) for k,skip,total in matches)
 totals=sum(int(total) for k,skip,total in matches)
 failed=[(int(total)-int(k)-int(skip)) for k,skip,total in matches]
 check(found==expected and totals==expected and sum(failed)==0,
       f'Pruebas del punto: esperado {expected}, PASS={found}, Total={totals}, fallidas={failed}\n{outcome[-3500:]}')
 return {'tests':found,'test_projects':len(matches),'build_tail':log[-250:]}

def verify_challenges(projects:Path,source:str):
 """Ejecuta los fragmentos optativos del manual en copias de cada etapa."""
 sections=source.split('## Reto de ampliación (optativo)')[1:]
 check(len(sections)==4,'Deben existir cuatro retos optativos')
 before={str(p):disk_sha(p) for p in projects.rglob('*') if p.is_file()
         and not any(x in p.parts for x in ('bin','obj','TestResults'))}
 results=[]
 ns={'t':'http://microsoft.com/schemas/VisualStudio/TeamTest/2010'}
 for n,(slug,section) in enumerate(zip(STAGES,sections),1):
  entry={'punto':f'3.{n}','estado':'FAIL'}
  try:
   section=section.split('## Resultado verificable',1)[0]
   blocks=re.findall(r'```csharp\n([\s\S]*?)\n```',section)
   check(len(blocks)==3,f'Reto 3.{n}: se esperan record, método y test')
   validator=re.search(r'\*\*Paso 1:\*\* En `([^`]+)`',section).group(1)
   testfile=re.search(r'\*\*Paso 6:\*\* En `([^`]+)`',section).group(1)
   testproject=re.search(r'`dotnet test ([^`]+)`',section).group(1).replace('\\','/')
   expected=int(re.search(r'\*\*Verificación:\*\*.*?Passed: (\d+)',section).group(1))
   with tempfile.TemporaryDirectory(prefix=f'm03-reto-{n}-') as temporary:
    stage=Path(temporary)/slug
    copy_project(projects/slug,stage)
    paths=[]
    for folder,name,block in [('src',validator,blocks[1]),('tests',testfile,blocks[2])]:
     candidates=list((stage/folder).rglob(name))
     check(len(candidates)==1,f'Destino ambiguo del reto: {name}')
     dest=candidates[0];content=dest.read_text(encoding='utf-8')
     endings=list(re.finditer(r'^}\s*$',content,re.M))
     check(len(endings)==1,f'Se esperaba una clase con un cierre principal: {name}')
     at=endings[0].start()
     content=content[:at]+'\n'+textwrap.indent(block,'    ')+'\n'+content[at:]
     if folder=='src':content=content.rstrip()+'\n\n'+blocks[0]+'\n'
     dest.write_text(content,encoding='utf-8');paths.append(str(dest.relative_to(stage)))
    command('dotnet','restore','AceriaApp.sln',cwd=stage)
    command('dotnet','build','AceriaApp.sln','-c','Release','--no-restore',cwd=stage)
    command('dotnet','test','AceriaApp.sln','-c','Release','--no-build','--no-restore',
            '--logger','trx','--results-directory','TestResults',cwd=stage)
    total=0;target_count=None;summary_pass=False
    for trx in (stage/'TestResults').glob('*.trx'):
     xml=ET.parse(trx);tests=xml.findall('.//t:UnitTestResult',ns)
     check(tests and all(t.get('outcome')=='Passed' for t in tests),f'Pruebas fallidas u omitidas: {trx.name}')
     total+=len(tests)
     methods=xml.findall('.//t:TestMethod',ns)
     if any(m.get('className','').startswith(Path(testproject).stem+'.') for m in methods):
      check(target_count is None,'Resultados duplicados del proyecto del reto')
      target_count=len(tests)
      summary_pass=any(t.get('testName','').endswith('Resumen_ConCatalogoPorDefecto_CuentaCorrectamente') for t in tests)
    check(total==EXPECTED[n-1]+1,f'Reto 3.{n}: total {total}, esperado {EXPECTED[n-1]+1}')
    check(target_count==expected and summary_pass,f'Reto 3.{n}: no se verificó el resultado del manual')
    entry.update(estado='PASS',tests_proyecto=target_count,tests_solucion=total,
                 fragmentos_csharp=3,archivos=paths,test_resumen='PASS')
  except Exception as exc:
   entry['error']=str(exc)
  results.append(entry)
  print(json.dumps(entry,ensure_ascii=False),flush=True)
 after={str(p):disk_sha(p) for p in projects.rglob('*') if p.is_file()
        and not any(x in p.parts for x in ('bin','obj','TestResults'))}
 check(before==after,'Los retos han alterado las etapas obligatorias')
 return {'resultado':'PASS' if all(r['estado']=='PASS' for r in results) else 'FAIL',
         'etapas_obligatorias_intactas':True,'retos':results}

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--out',type=Path,default=BASE/'M03_E2E_RESULTADOS.json')
 p.add_argument('--no-tests',action='store_true',help='Solo reconstruye; útil para inspección local')
 p.add_argument('--output-dir',type=Path,default=BASE/'PROYECTO')
 p.add_argument('--m02-base',type=Path,default=M02,help='Etapa 2.4 reconstruida desde M02_PRACTICAS.md')
 args=p.parse_args()
 report={'fecha':datetime.now(timezone.utc).isoformat(),'origen':'M03_PRACTICAS.md',
         'etapas':[],'pasos':[],'construccion':'desde texto; nunca desde PROYECTO/M03'}
 try:
  source,theory,codes=read_markdown()
  report['source_sha256']=text_sha(source)
  check(args.m02_base.is_dir(),'No se encuentra M02 etapa 2.4')
  inherited_helper=verify_sql_isolation(args.m02_base)
  report['helper_sqlserver_sha256']=inherited_helper
  output=args.output_dir
  output.mkdir(parents=True,exist_ok=True)
  previous=None
  for num,slug in enumerate(STAGES,1):
   stage=output/slug
   if stage.exists():shutil.rmtree(stage)
   copy_project(args.m02_base if num==1 else previous,stage)
   actions=0;builds=0;files=[]
   if num==1:
    check(not (stage/'AceriaApp.sln').exists(),'La base M02 debía carecer de solución de M03')
   for step in range(1,25):
    codeStep=f'3.{num}.{step}'
    batch=[x for x in codes if x['paso']==codeStep]
    for record in batch:
     files.append(str(apply_one(stage,record).relative_to(stage)))
     actions+=1
    # Checkpoints: build API and independent project when its .csproj exists.
    if not args.no_tests and step in CHECKPOINTS[f'3.{num}']:
     lib=stage/'src/AceriaApp.Hexagonal.Infraestructura/AceriaApp.Hexagonal.Infraestructura.csproj'
     if num>=3 and step>=9 and lib.exists():
      command('dotnet','build',str(lib),'-c','Release',cwd=stage)
     else:
      command('dotnet','build','src/AceriaApp.Api/AceriaApp.Api.csproj','-c','Release',cwd=stage)
     builds+=1
    report['pasos'].append({'paso':codeStep,'codigo_escrito':len(batch),'archivos':[
        x['ruta'] for x in batch],'resultado':'aplicado' if batch else 'guia_manual_verificable'})
   total_projects=ensure_solution(stage) if not args.no_tests else len(project_files(stage))
   verify_architecture(stage,num)
   check(verify_sql_isolation(stage)==inherited_helper,'Se modificó el helper SQL Server heredado')
   inheritance=compare_inherited(previous,stage) if previous else 0
   outcome=build_and_test(stage,EXPECTED[num-1]) if not args.no_tests else {'tests':None,'test_projects':None}
   report['etapas'].append({'punto':f'3.{num}','carpeta':slug,'pasos':24,
           'archivos_creados_o_modificados':actions,'n_proyectos':total_projects,
           'documentos_heredados_identicos':inheritance,'builds_intermedios':builds,
           'tests_acumulados':outcome['tests'],'expected':EXPECTED[num-1],
           'estado':'PASS' if not args.no_tests else 'SIN_EJECUTAR_TESTS'})
   print(f'M03 3.{num}: {actions} operaciones desde MD; {builds} compilaciones intermedias; {outcome["tests"]} tests; {total_projects} proyectos',flush=True)
   previous=stage
  check(len(report['pasos'])==96,'No se han visitado los 96 pasos')
  check(all(x['estado']=='PASS' for x in report['etapas']) or args.no_tests,'Etapa incompleta')
  if not args.no_tests:
   report['retos_optativos']=verify_challenges(output,source)
   check(report['retos_optativos']['resultado']=='PASS','Hay retos optativos sin superar')
  report['resumen']={'resultado':'PASS' if not args.no_tests else 'SIN_TESTS','pasos':96,
      'operaciones_codigo':len(codes),'builds_intermedios':sum(x['builds_intermedios'] for x in report['etapas']),
      'tests_por_etapa':EXPECTED}
 except Exception as exc:
  report['resumen']={'resultado':'FAIL','error':str(exc)}
 args.out.parent.mkdir(parents=True,exist_ok=True)
 args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report['resumen'],ensure_ascii=False),flush=True)
 if report['resumen']['resultado']=='FAIL':sys.exit(1)
if __name__=='__main__':main()
