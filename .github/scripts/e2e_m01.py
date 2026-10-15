#!/usr/bin/env python3
"""Pruebas E2E por punto para AceriaApp M01.

El código de trabajo se copia siempre a un directorio temporal; nunca se
sobrescriben los cinco proyectos que recibe el alumno.

Modos:
  static: valida 120 pasos/documentación, marcadores, proyectos y herencia.
  stage : valida cada paso y ejecuta dotnet build/tests tras activar cada bloque.
  sql   : añade migración real + HTTP contra SQL Server con conexión indicada.
  reto  : además activa y verifica el reto del punto.
"""
from __future__ import annotations
import argparse, dataclasses, hashlib, json, os, re, shutil, socket, subprocess, sys, tempfile, time, urllib.error, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

SLUGS = [
    '1.1-monolito-vs-microservicios',
    '1.2-ventajas-inconvenientes',
    '1.3-principios-diseno',
    '1.4-organizacion-solucion',
    '1.5-buenas-practicas',
]
TOTALS = [1, 9, 13, 18, 23]
DOCS = [
    ['ADR-001-monolito-vs-microservicios.md'],
    ['analisis-ventajas-inconvenientes.md', 'ADR-002-metricas-acoplamiento.md'],
    ['principios-diseno.md', 'ADR-003-principios-diseno.md'],
    ['organizacion-solucion.md', 'ADR-004-organizacion-solucion.md'],
    ['buenas-practicas.md', 'ADR-005-buenas-practicas.md'],
]

class CheckError(Exception): pass

def check(assertion, message):
    if not assertion: raise CheckError(message)

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def exec_cmd(args, *, cwd, env=None, timeout=250, check_result=True):
    start = time.monotonic()
    try:
        p = subprocess.run(args, cwd=str(cwd), env=env, text=True, errors='replace',
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise CheckError('TIMEOUT: ' + ' '.join(map(str,args)) + '\n' + str(e)) from e
    res={'cmd':' '.join(map(str,args)),'returncode':p.returncode,
         'seconds':round(time.monotonic()-start,2),'tail':p.stdout[-3800:]}
    if check_result and p.returncode != 0: raise CheckError('ERROR '+json.dumps(res,ensure_ascii=False))
    return res

def sections(practice):
    matches = list(re.finditer(r'^# Punto (1\.[1-5]) —', practice, re.M))
    # El README incluido como ejemplo también tiene este encabezado. Tomamos
    # la primera aparición por punto y restringimos por la siguiente.
    unique={}
    for m in matches: unique.setdefault(m.group(1),m.start())
    check(len(unique)==5,f'Se esperaban cinco puntos: {list(unique)}')
    out={}
    for i in range(5):
        point=f'1.{i+1}'; end=f'1.{i+2}'
        block=practice[unique[point]:unique.get(end,len(practice))]
        stepmatches=list(re.finditer(r'^### Paso (\d+) — (.*)$',block,re.M))
        # Evita títulos de paso dentro de README/código: comprobar 1..24.
        nums=[int(m.group(1)) for m in stepmatches]
        check(nums==list(range(1,25)),f'{point}: pasos encontrados {nums}')
        out[point]=[(int(m.group(1)),m.group(2),block[m.end():stepmatches[j+1].start() if j+1<len(stepmatches) else len(block)]) for j,m in enumerate(stepmatches)]
    return out

def marker_index(directory, point):
    matches={}
    for path in directory.rglob('*.cs'):
        lines=path.read_text(encoding='utf-8').splitlines()
        starts=[]
        for i,line in enumerate(lines):
            match=re.match(r'^// INICIO PASO (1\.\d+\.\d+)\b',line)
            if match: starts.append((i,match.group(1)))
            match_end=re.match(r'^// FIN PASO (1\.\d+\.\d+)\s*$',line)
            if match_end:
                check(starts and starts[-1][1]==match_end.group(1),f'Marcador descompensado en {path}:{i+1}')
                j,key=starts.pop()
                if key.startswith(point+'.'): matches.setdefault(int(key.split('.')[-1]),[]).append((path,j,i))
        check(not starts,f'Sin FIN PASO en {path}: {starts}')
    return matches

def activate_step(directory, point, step):
    key=f'{point}.{step}'
    changed=[]
    for f in directory.rglob('*.cs'):
        lines=f.read_text(encoding='utf-8').splitlines(keepends=True)
        out=[];active=False;found=0
        for line in lines:
            if line.startswith('// INICIO PASO '+key+' '):
                check(not active,f'Inicio anidado: {f} {key}')
                active=True;found+=1;continue
            if active and line.startswith('// FIN PASO '+key):
                active=False;continue
            if active and line.startswith('// '):out.append(line[3:])
            elif active and line.rstrip('\r\n')=='//':out.append('\n')
            else:out.append(line)
        check(not active,f'Fin ausente: {f} {key}')
        if found:
            f.write_text(''.join(out),encoding='utf-8')
            changed.append(str(f.relative_to(directory)))
    if point=='1.1' and step==14:
        mig=directory/'src/AceriaApp.Monolito.Api/Infraestructura/Migraciones'
        for name in ['202610140001_Inicial.cs.txt','AceriaDbContextModelSnapshot.cs.txt']:
            f=mig/name
            check(f.exists(),f'Migración plantilla ausente: {f}')
            f.rename(f.with_suffix(''))
            changed.append(str(f.relative_to(directory)))
    return changed

def static_audit(root, *, strict=True):
    base=root/'M01_INTRODUCCION_MICROSERVICIOS'
    proj=base/'PROYECTO'
    practice=(base/'PRACTICAS/M01_PRACTICAS.md').read_text(encoding='utf-8')
    theory=(base/'TEORIA/M01_TEORIA.md').read_text(encoding='utf-8')
    blocks=len(re.findall(r'^### Bloque \d+ —',theory,re.M))
    check(blocks==50,f'Bloques teóricos: {blocks}, deberían ser 50')
    blocks_by_point=[theory.split(f'# Punto 1.{i} —',1)[1].split(f'# Punto 1.{i+1} —',1)[0] if i<5 else theory.split('# Punto 1.5 —',1)[1] for i in range(1,6)]
    for n,b in enumerate(blocks_by_point,1):
        check(len(re.findall(r'^### Bloque \d+ —',b,re.M))==10,f'Teoría punto 1.{n} incompleta')
    sections_by_point=sections(practice)
    rows=[];count_markers=0;inherited=0
    for i,slug in enumerate(SLUGS):
        point=f'1.{i+1}';directory=proj/slug
        check((directory/'AceriaApp.sln').exists(),f'Sin solución {point}')
        csprojs=list(directory.rglob('*.csproj'))
        check(len(csprojs)==i+2,f'{point}: {len(csprojs)} proyectos, esperado {i+2}')
        for d in DOCS[i]:check((directory/'docs'/d).is_file(),f'{point}: falta docs/{d}')
        if i:
            prev=proj/SLUGS[i-1]
            for f in (prev/'docs').iterdir():
                check((directory/'docs'/f.name).is_file(),f'{point}: documentación heredada {f.name} perdida')
                check(digest(f)==digest(directory/'docs'/f.name),f'{point}: documento heredado alterado {f.name}')
                inherited+=1
        mi=marker_index(directory,point)
        count_markers+=sum(len(v) for v in mi.values())
        for n,title,body in sections_by_point[point]:
            actions=re.findall(r'^\*\*Acción \d+:\*\*',body,re.M)
            check(3<=len(actions)<=8,f'Acciones fuera de rango: {point}.{n}: {len(actions)}')
            for term in ['**Por qué se hace:**','**Errores comunes:**','**Verificación:**']:
                check(term in body,f'{point}.{n} sin {term}')
            refs=re.findall(r'\*\*Archivo preparado en este punto:\*\* `([^`]+)`',body)
            mode='marcador C#' if n in mi else ('SQL Server' if point=='1.1' and n==15 else 'archivo/operación/manual')
            if refs:
                for rel in refs:
                    check((directory/rel).is_file(),f'{point}.{n} referencia inexistente: {rel}')
                    check(n in mi,f'{point}.{n}: no hay marcador C# para archivo {rel}')
            rows.append({'punto':point,'paso':n,'titulo':title,'modo':mode,
                         'marcadores':len(mi.get(n,[])),'archivos':refs,
                         'automatizable':mode in ('marcador C#','SQL Server') or n in (16,17,18,21,22)})
        for step,entries in mi.items():
            check(1<=step<=24,f'{point}: marcador fuera de 1..24: {step}')
    return {'ok':True,'puntos':len(SLUGS),'bloques_teoricos':blocks,'pasos':len(rows),
            'marcadores':count_markers,'documentos_heredados_iguales':inherited,
            'proyectos_por_punto':[2,3,4,5,6], 'tests_esperados':TOTALS,'matriz':rows}

def run_tests(directory, expected, logdir):
    tests=sorted(directory.glob('tests/*/*.csproj'))
    check(len(tests)>0,'No hay proyectos xUnit')
    passed=0; logs=[]
    for p in tests:
        logfile=p.stem+'.trx'
        result=exec_cmd(['dotnet','test',str(p),'--configuration','Release','--no-build',
                         '--logger','trx;LogFileName='+logfile,'--results-directory',str(logdir)],cwd=directory,timeout=240)
        trx=logdir/logfile
        check(trx.exists(),f'No se generó TRX de {p.name}: {result["tail"]}')
        doc=ET.parse(trx).getroot()
        counters=doc.find('.//{*}ResultSummary/{*}Counters')
        check(counters is not None,f'TRX sin resultados: {trx}')
        failed=int(counters.get('failed',-1)); total=int(counters.get('total',-1)); passed_now=int(counters.get('passed',-1))
        check(failed==0 and total==passed_now,f'{p.stem}: {total} totales, {passed_now} pasados, {failed} fallos')
        passed+=passed_now;logs.append({'project':p.stem,'passed':passed_now,'trx':str(trx)})
    check(passed==expected,f'Esperados {expected} tests, ejecutados {passed}')
    return logs

def build_and_test_stages(root, index, work, *, reto=False, sql=False):
    point=f'1.{index+1}'; slug=SLUGS[index]
    source=root/'M01_INTRODUCCION_MICROSERVICIOS/PROYECTO'/slug
    target=work/slug
    shutil.copytree(source,target)
    evidence=[];last_test=None
    # Compilación base: el nuevo punto ya viene con proyectos heredados activos y nuevos comentados.
    evidence.append({'paso':0,'tipo':'compilación base',
                     'run':exec_cmd(['dotnet','build','AceriaApp.sln','-c','Release'],cwd=target)})
    for step in range(1,25):
        changed=activate_step(target,point,step)
        row={'paso':step,'tipo':'activación' if changed else 'comprobación documental/estructura','archivos':changed}
        if changed:
            row['build']=exec_cmd(['dotnet','build','AceriaApp.sln','-c','Release'],cwd=target)
        # La última activación de los tests está en paso 17 (punto 1.1)
        # o paso 15 (puntos 1.2..1.5). Comprobamos al final del ejercicio.
        if step==18:
            logdir=work/f'{point}-trx';logdir.mkdir(parents=True,exist_ok=True)
            row['unit_tests']=run_tests(target,TOTALS[index],logdir)
            last_test=sum(z['passed'] for z in row['unit_tests'])
        evidence.append(row)
    check(last_test==TOTALS[index],f'{point}: pruebas básicas no ejecutadas')
    if sql:
        evidence.append({'paso':'E2E SQL/HTTP','resultado':sql_and_http(target,point,index,work)})
    if reto:
        challenge_files=activate_challenge(target,point)
        check(challenge_files,point+': no se han activado ficheros de reto')
        evidence.append({'paso':'RETO','tipo':'activación reto','archivos':challenge_files,
                         'build':exec_cmd(['dotnet','build','AceriaApp.sln','-c','Release'],cwd=target)})
        logdir=work/f'{point}-reto-trx';logdir.mkdir(parents=True,exist_ok=True)
        evidence.append({'paso':'RETO test','unit_tests':run_tests(target,TOTALS[index]+1,logdir)})
        if sql and index==0:
            evidence.append({'paso':'RETO 404 HTTP','resultado':sql_and_http(target,point,index,work,reto=True)})
    return {'punto':point,'total_tests_basicos':last_test,'retos':reto,
            'sql_http_ejecutado':sql,'evidencias':evidence}

def activate_challenge(target,point):
    """Activa solamente el reto actual, no los heredados.

    Las líneas del reto siguen comentadas tras activar el bloque del PASO.
    Se activan hasta la primera línea de código ya activa. Es un segundo nivel
    de descomentado, igual que efectuar Ctrl+K/Ctrl+U de nuevo sobre el reto.
    """
    changed=[]
    for path in target.rglob('*.cs'):
        lines=path.read_text().splitlines(keepends=True)
        out=[];challenge=False;found=False
        for line in lines:
            if re.match(r'^\s*// RETO '+re.escape(point)+r'\b',line):
                challenge=True;found=True;continue
            if challenge:
                m=re.match(r'^(\s*)// ?(.*?)(\r?\n)?$',line)
                if m and not re.match(r'^\s*// (?:RETO |PASO )',line):
                    out.append(m.group(1)+m.group(2)+(m.group(3) or ''))
                    continue
                challenge=False
            out.append(line)
        if found:
            path.write_text(''.join(out));changed.append(str(path.relative_to(target)))
    if point in ('1.3','1.4'):
        record={'1.3':'ResumenLimites','1.4':'ResumenProyectos'}[point]
        path=(target/'src/AceriaApp.Monolito.Api'/('Diseno' if point=='1.3' else 'Organizacion')/('CatalogoLimites.cs' if point=='1.3' else 'CatalogoProyectos.cs'))
        data=path.read_text()
        pattern='// public record '+record+'('
        check(data.count(pattern)==1,point+': el record de reto no está presente o se duplicó')
        path.write_text(data.replace(pattern,'public record '+record+'('))
        changed.append(str(path.relative_to(target)))
    if point=='1.1':
        f=target/'tests/AceriaApp.Monolito.Tests/OrdenEndpointsTests.RETO.cs.txt'
        check(f.exists(),'No se encuentra reto 1.1 test')
        lines=f.read_text().splitlines()
        # El encabezado introductorio ocupa varias líneas; empezar en el primer using.
        start=next((i for i,line in enumerate(lines) if line.startswith('// using ')), None)
        check(start is not None,'RETO 1.1: plantilla sin usings')
        code='\n'.join(line[3:] if line.startswith('// ') else line for line in lines[start:])+'\n'
        check('public class OrdenEndpointsTests' in code,'Plantilla RETO 1.1 inválida')
        dest=f.with_name('OrdenEndpointsTests.cs')
        dest.write_text(code)
        f.unlink()
        csproj=target/'tests/AceriaApp.Monolito.Tests/AceriaApp.Monolito.Tests.csproj'
        contents=csproj.read_text()
        check('</ItemGroup>' in contents,'csproj inesperado')
        # EF InMemory 8.0.0 solo pertenece al reto, no contamina los tests básicos.
        contents=contents.replace('</ItemGroup>','  <PackageReference Include="Microsoft.EntityFrameworkCore.InMemory" Version="8.0.0" />\n  </ItemGroup>',1)
        csproj.write_text(contents)
        changed.extend([str(dest.relative_to(target)),str(csproj.relative_to(target))])
    return changed

def request_json(url, *, data=None):
    raw=None if data is None else json.dumps(data).encode('utf-8')
    req=urllib.request.Request(url,data=raw,headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=6) as resp:
            b=resp.read().decode('utf-8')
            return resp.status, json.loads(b) if b else None
    except urllib.error.HTTPError as e:
        return e.code,e.read().decode('utf-8',errors='replace')

def sql_and_http(target,point,index,work,reto=False):
    cs=os.environ.get('M01_SQL_CONNECTION_STRING')
    check(cs is not None,'M01_SQL_CONNECTION_STRING no configurada. SQL/HTTP NO ejecutado')
    env=os.environ.copy();env['ConnectionStrings__AceriaDb']=cs
    env['ASPNETCORE_ENVIRONMENT']='Development';env['DOTNET_NOLOGO']='1'
    api=target/'src/AceriaApp.Monolito.Api'
    # dotnet-ef 8 debe estar instalado en el runner/estación.
    migration=None
    for attempt in range(1,9):
        migration=exec_cmd(['dotnet','ef','database','update','--project',str(api),'--startup-project',str(api),
                            '--no-build','--configuration','Release'],cwd=target,env=env,timeout=100,check_result=False)
        if migration['returncode']==0:break
        time.sleep(4)
    check(migration is not None and migration['returncode']==0,'No se pudo aplicar la migración SQL Server tras reintentos: '+str(migration))
    with socket.socket() as s:
        s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    host=f'http://127.0.0.1:{port}'
    env['ASPNETCORE_URLS']=host
    app=subprocess.Popen(['dotnet','run','--no-build','--no-launch-profile','--configuration','Release',
                          '--project',str(api)],cwd=str(target),env=env,
                         stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    try:
        ready=False
        for _ in range(50):
            if app.poll() is not None: raise CheckError(f'API terminada antes de escuchar: {app.returncode}')
            try:
                status,doc=request_json(host+'/swagger/v1/swagger.json')
                if status==200:
                    check('/api/v1/ordenes' in doc['paths'],'Swagger sin endpoint de órdenes')
                    ready=True;break
            except (ConnectionError,TimeoutError,urllib.error.URLError,ValueError):pass
            time.sleep(.4)
        check(ready,'La API no publicó Swagger a tiempo')
        status,lst=request_json(host+'/api/v1/ordenes')
        check(status==200 and isinstance(lst,list),f'GET lista falló: {status}, {lst}')
        if not reto:
            check(lst==[],f'La base de datos E2E debe estar vacía antes de POST: {lst}')
        status,obj=request_json(host+'/api/v1/ordenes',data={'cliente':'ACX-001','material':'CHAPA-3MM','cantidad':10})
        check(status==201 and obj['cliente']=='ACX-001',f'POST orden incorrecto {status} {obj}')
        oid=obj['id'];status,lst=request_json(host+'/api/v1/ordenes')
        check(status==200 and any(x['id']==oid for x in lst),'GET lista no incluye orden creada')
        outcome={'migracion':'OK','swagger':'OK','get_200':'OK','post_201':'OK','get_post':'OK','id':oid,'reto':reto}
        if reto:
            status,detail=request_json(host+'/api/v1/ordenes/'+oid)
            check(status==200 and detail['id']==oid,f'RETO GET detalle {status} {detail}')
            import uuid
            status,_=request_json(host+'/api/v1/ordenes/'+str(uuid.uuid4()))
            check(status==404,f'RETO GET inexistente devolvió {status}, esperado 404')
            outcome['detalle_200_y_404']='OK'
        else:
            check('/api/v1/ordenes/{id}' not in doc['paths'],'GET de reto activo en escenario básico')
        return outcome
    finally:
        app.terminate()
        try:app.communicate(timeout=12)
        except subprocess.TimeoutExpired:app.kill();app.communicate()

def main():
    ap=argparse.ArgumentParser(description='Validador M01: 120 pasos + .NET + SQL Server + HTTP')
    ap.add_argument('--root',type=Path,default=Path('.'))
    ap.add_argument('--point',choices=[f'1.{i}' for i in range(1,6)])
    ap.add_argument('--mode',choices=['static','stage','sql'],default='static')
    ap.add_argument('--reto',action='store_true')
    ap.add_argument('--out',type=Path,default=Path('M01_E2E_RESULTADOS.json'))
    args=ap.parse_args()
    result={'fecha_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
            'modo':args.mode,'repo_root':str(args.root.resolve()),'puntos':[]}
    try:
        static=static_audit(args.root)
        result['validacion_documental']={k:v for k,v in static.items() if k!='matriz'}
        result['matriz_120_pasos']=static['matriz']
        if args.mode in ('stage','sql'):
            check(args.point is not None,'Indique --point 1.1..1.5 para pruebas con SDK')
            ix=int(args.point.split('.')[1])-1
            with tempfile.TemporaryDirectory(prefix='aceria-m01-e2e-') as tmp:
                result['puntos'].append(build_and_test_stages(args.root,ix,Path(tmp),reto=args.reto,sql=args.mode=='sql'))
                # Conservar evidencias TRX antes de destruir las copias temporales.
                for folder in Path(tmp).glob(args.point+'*-trx'):
                    shutil.copytree(folder,args.out.parent/f'e2e-trx-{args.point}'/folder.name,dirs_exist_ok=True)
        result['resultado']='PASS'
    except Exception as exc:
        result['resultado']='FAIL';result['error']=str(exc)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='matriz_120_pasos' and k!='puntos'},ensure_ascii=False,indent=2))
    if result['resultado']!='PASS':sys.exit(1)

if __name__=='__main__':main()
