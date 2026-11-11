#!/usr/bin/env python3
"""Acredita observabilidad, fallos y recuperación en dos procesos Kestrel reales."""
import argparse,json,os,re,socket,subprocess,time,urllib.request,urllib.error,uuid,tempfile,shutil,sys
from pathlib import Path
from validar_sqlserver import source_manifest
ROOT=Path(__file__).resolve().parents[2]
FINAL=ROOT/'M07_OBSERVABILIDAD_RESILIENCIA/PROYECTO/7.4-retry-circuit-breaker-polly'

def request(base,path,method='GET',body=None,expected=200,headers=None):
    req=urllib.request.Request(base+path,data=None if body is None else json.dumps(body).encode('utf-8'),method=method,
                               headers={'Content-Type':'application/json',**(headers or {})})
    try:response=urllib.request.urlopen(req,timeout=12)
    except urllib.error.HTTPError as error:response=error
    with response:
        data=response.read().decode('utf-8');status=response.status;response_headers={k.lower():v for k,v in response.headers.items()}
    if status!=expected:raise AssertionError(f'{method} {path}: {status}, esperado {expected}: {data}')
    return json.loads(data) if data else None,response_headers

def own(events):
    return [e for e in events if e.get('Properties',{}).get('SourceContext','').startswith(('AceriaApp.Observabilidad.','AceriaApp.Resiliencia'))]

def verify_correlation(events,correlation,secrets):
    selected=[e['Properties'] for e in own(events) if e['Properties'].get('CorrelationId')==correlation and 'Ruta' in e['Properties']]
    assert {p.get('Servicio') for p in selected}=={'Produccion','Inventario'},'Falta correlación entre servicios'
    assert all('{' in p['Ruta'] and '?' not in p['Ruta'] for p in selected),'Debe registrarse la plantilla de ruta'
    payload=json.dumps(own(events),ensure_ascii=False)
    assert all(secret not in payload for secret in secrets),'Dato sensible en eventos propios'

def verify_health(data,*,healthy):
    assert set(data)=={'estado','componentes'}
    assert data['estado']==('Healthy' if healthy else 'Unhealthy')
    assert data['componentes'],'Readiness debe acreditar dependencias'
    for component in data['componentes']:
        assert set(component)=={'nombre','estado','milisegundos'}
        assert isinstance(component['milisegundos'],(int,float))
    states=[p['estado'] for p in data['componentes']]
    assert all(s=='Healthy' for s in states) if healthy else 'Unhealthy' in states

def verify_problem(data,headers,correlation):
    assert headers['content-type'].split(';')[0]=='application/problem+json'
    assert headers['x-correlation-id']==correlation and data['correlationId']==correlation
    assert data['status']==500 and data['type']=='about:blank' and data['traceId']
    assert data['title']=='Se ha producido un error interno.' and not data.get('detail')
    assert 'Detalle interno' not in json.dumps(data)

def broker_action(action):
    identifier=os.environ.get('ACERIA_RABBIT_CONTAINER_ID','')
    if not re.fullmatch(r'[a-f0-9]{64}',identifier):raise ValueError('Falta el ID exacto del contenedor RabbitMQ creado por el host')
    if action not in ('stop','start'):raise ValueError('Acción de contenedor no permitida')
    subprocess.run(['docker',action,*(['--time','3'] if action=='stop' else []),identifier],check=True,timeout=25)

def event_id(event):
    value=event.get('Properties',{}).get('EventId')
    return value.get('Id') if isinstance(value,dict) else value

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--windows',action='store_true');args=parser.parse_args()
    if args.windows and sys.platform!='win32':raise RuntimeError('El recorrido LocalDB exige Windows')
    execution=uuid.uuid4().hex
    logs=ROOT/'.qa/m07-http'/execution;logs.mkdir(parents=True,exist_ok=False)
    report={'resultado':'FAIL','ejecucion':execution,'commit_comprobado':os.environ.get('GITHUB_SHA'),
            'plataforma':'Windows LocalDB' if args.windows else 'Linux SQL Server Express y RabbitMQ',
            'codigo_normalizado_sha256':source_manifest(FINAL),'comprobaciones':[]}
    processes={};streams={};ports={};temp=None;broker_stopped=False
    def stop(name):
        p=processes.pop(name,None)
        if p:
            p.terminate()
            try:p.wait(timeout=20)
            except subprocess.TimeoutExpired:p.kill();p.wait()
        if name in streams:streams.pop(name).close()
    def events():
        for stream in streams.values():stream.flush()
        result=[]
        for log in logs.glob('*.log'):
            for line in log.read_text(encoding='utf-8',errors='replace').splitlines():
                try:
                    event=json.loads(line)
                    if isinstance(event,dict) and 'Timestamp' in event:result.append(event)
                except json.JSONDecodeError:pass
        return result
    def wait_for(check,seconds=30):
        deadline=time.monotonic()+seconds
        while True:
            try:return check()
            except (AssertionError,urllib.error.URLError,TimeoutError,OSError):
                if time.monotonic()>=deadline:raise
                time.sleep(.25)
    try:
        temp=tempfile.TemporaryDirectory(prefix='axia7-',dir=os.environ.get('RUNNER_TEMP'))
        stage=Path(temp.name)/'etapa';shutil.copytree(FINAL,stage,ignore=shutil.ignore_patterns('bin','obj','TestResults','.vs'))
        assert source_manifest(stage)==report['codigo_normalizado_sha256']
        for name in ('AceriaApp.Api','AceriaApp.Inventario.Api'):
            subprocess.run(['dotnet','build',str(stage/'src'/name/(name+'.csproj')),'-c','Release','-m:1','--disable-build-servers','-p:NuGetAudit=false'],check=True)
        for name in ('produccion','inventario','sql-ausente','production'):
            with socket.socket() as s:s.bind(('127.0.0.1',0));ports[name]=s.getsockname()[1]
        urls={k:f'http://127.0.0.1:{v}' for k,v in ports.items()}
        prefix=os.environ['ACERIA_HTTP_SQL_PREFIX'];server=os.environ['ACERIA_TEST_SQLSERVER']
        env=dict(os.environ,ASPNETCORE_ENVIRONMENT='Development',Comunicacion__InventarioUrl=urls['inventario']+'/',
                 Comunicacion__WorkersActivos='false' if args.windows else 'true',Comunicacion__Prefijo='http-'+uuid.uuid4().hex,
                 Observabilidad__DiagnosticoActivo='true',Observabilidad__NivelMinimo='Information')
        for key in ('AceriaApp','AceriaHexagonal','AceriaProduccion','AceriaInventario'):
            env['ConnectionStrings__'+key]=server+';Database='+prefix+'_'+key
        if not args.windows:env['Comunicacion__RabbitMqUri']=os.environ['ACERIA_TEST_RABBITMQ']
        def start(name,extra=None):
            project='AceriaApp.Inventario.Api' if name=='inventario' else 'AceriaApp.Api';api=stage/'src'/project
            stream=(logs/(name+'-'+uuid.uuid4().hex[:6]+'.log')).open('w',encoding='utf-8');streams[name]=stream
            processes[name]=subprocess.Popen(['dotnet',str(api/'bin/Release/net8.0'/(project+'.dll'))],cwd=api,
                env=dict(env,ASPNETCORE_URLS=urls[name],**(extra or {})),stdout=stream,stderr=subprocess.STDOUT)
            def alive():
                if processes[name].poll() is not None:raise RuntimeError(name+' terminó al iniciar')
                data,_=request(urls[name],'/health/live');assert data=={'estado':'Healthy','componentes':[]}
            wait_for(alive,120)
        start('inventario');start('produccion')
        api=urls['produccion'];inventory=urls['inventario'];production_pid=processes['produccion'].pid
        correlation='m07-'+uuid.uuid4().hex;query='sentinela-query-'+uuid.uuid4().hex;token='sentinela-token-'+uuid.uuid4().hex
        material,headers=request(api,'/api/v1/comunicacion/materiales/Acero?secreto='+query,headers={'X-Correlation-ID':correlation,'Authorization':'Bearer '+token})
        assert material['stock']==300 and headers['x-correlation-id']==correlation
        wait_for(lambda:verify_correlation(events(),correlation,[query,token]))
        _,bad=request(api,'/api/v1/comunicacion/materiales/Acero',headers={'X-Correlation-ID':'invalido/con/barra'})
        assert re.fullmatch(r'[a-f0-9]{32}',bad['x-correlation-id'])
        report['logging']='PASS';report['comprobaciones']+=['JSON y correlación entre dos procesos; cabecera inválida regenerada; query y Authorization excluidos de eventos propios']
        for url in (api,inventory):
            ready,_=request(url,'/health/ready');verify_health(ready,healthy=True)
        if not args.windows:
            broker_stopped=True;broker_action('stop')
            for url in (api,inventory):
                live,_=request(url,'/health/live');assert live=={'estado':'Healthy','componentes':[]}
                ready,_=request(url,'/health/ready',expected=503);verify_health(ready,healthy=False)
                assert next(c for c in ready['componentes'] if c['nombre']=='rabbitmq')['estado']=='Unhealthy'
            broker_action('start');broker_stopped=False
            def broker_ready():
                for url in (api,inventory):
                    ready,_=request(url,'/health/ready');verify_health(ready,healthy=True)
            wait_for(broker_ready,60)
            report['comprobaciones'].append('RabbitMQ real detenido y recuperado: live200, ready503 y ready200; procesos API conservados')
        start('sql-ausente',{'SkipDatabaseInitialization':'true','Comunicacion__WorkersActivos':'false',
                            'ConnectionStrings__AceriaApp':server+';Database='+prefix+'_Ausente'})
        ready,_=request(urls['sql-ausente'],'/health/ready',expected=503);verify_health(ready,healthy=False)
        assert next(c for c in ready['componentes'] if c['nombre']=='sql-AceriaApp')['estado']=='Unhealthy'
        stop('sql-ausente');report['health_checks']='PASS'
        for url in (api,inventory):
            corr='error-'+uuid.uuid4().hex
            data,headers=request(url,'/api/diagnostico/fallo',expected=500,headers={'X-Correlation-ID':corr,'Accept':'text/plain'})
            verify_problem(data,headers,corr)
        start('production',{'ASPNETCORE_ENVIRONMENT':'Production','Comunicacion__WorkersActivos':'false','SkipDatabaseInitialization':'true'})
        request(urls['production'],'/api/diagnostico/fallo',expected=404);stop('production')
        report['gestion_excepciones']='PASS';report['comprobaciones']+=['SQL existente/inexistente y liveness independientes','ProblemDetails500 en ambas API; diagnóstico404 en Production aun con flag activo']
        path_secret='secreto-ruta-'+uuid.uuid4().hex
        request(api,'/api/v1/comunicacion/materiales/'+path_secret,expected=404)
        body_secret='cliente-privado-'+uuid.uuid4().hex
        order,_=request(api,'/api/v1/produccion/ordenes','POST',{'cliente':body_secret,'material':'Acero','cantidad':20},201)
        oid=order['id'];request(api,f'/api/v1/produccion/ordenes/{oid}/lineas','POST',{'material':'Inoxidable','cantidad':10})
        request(api,f'/api/v1/comunicacion/ordenes/{oid}/planificar','POST',{},202)
        request(api,f'/api/v1/comunicacion/ordenes/{oid}/planificar','POST',{},409)
        request(api,f'/api/v1/comunicacion/ordenes/{uuid.uuid4()}/planificar','POST',{},404)
        if not args.windows:
            projection,_=wait_for(lambda:request(inventory,f'/api/v1/planificaciones/{oid}'),45)
            assert projection['cantidadTotal']==30
        excessive,_=request(api,'/api/v1/produccion/ordenes','POST',{'cliente':'Axia M07','material':'Acero','cantidad':450},201)
        request(api,f'/api/v1/comunicacion/ordenes/{excessive["id"]}/planificar','POST',{},409)
        pending,_=request(api,f'/api/v1/produccion/ordenes/{excessive["id"]}');assert pending['estado']=='Borrador'
        stop('inventario')
        for attempt in range(16):
            request(api,'/api/v1/comunicacion/materiales/Acero',expected=503)
            if any(event_id(e)==7402 for e in events()):break
        else:raise AssertionError('El circuito no se abrió durante la caída real')
        assert any(event_id(e)==7401 for e in events()),'No se observan reintentos reales'
        failfast='abierto-'+uuid.uuid4().hex;started=time.monotonic()
        request(api,'/api/v1/comunicacion/materiales/Acero',expected=503,headers={'X-Correlation-ID':failfast})
        elapsed=time.monotonic()-started;assert elapsed<1.5,'El circuito abierto no falla inmediatamente'
        assert not any(event_id(e)==7401 and e['Properties'].get('CorrelationId')==failfast for e in events())
        request(api,f'/api/v1/comunicacion/ordenes/{excessive["id"]}/planificar','POST',{},503)
        start('inventario')
        recovered,_=wait_for(lambda:request(api,'/api/v1/comunicacion/materiales/Acero'),20);assert recovered['stock']==300
        assert processes['produccion'].pid==production_pid,'La recuperación no debe reiniciar el dueño del circuito'
        def closed():assert any(event_id(e)==7403 for e in events()),'Falta callback de cierre'
        wait_for(closed)
        report.update(resiliencia='PASS',circuito_abierto_respuesta_segundos=round(elapsed,4))
        report['comprobaciones'].append('Inventario real caído: retry7401, circuito7402, fail-fast503; recuperación7403 sin reiniciar Producción')
        assert all(secret not in json.dumps(own(events()),ensure_ascii=False) for secret in (query,token,body_secret,path_secret,'Detalle interno del fallo controlado.'))
        stop('produccion');start('produccion')
        saved,_=request(api,f'/api/v1/produccion/ordenes/{oid}');assert saved['estado']=='Planificada' and saved['cantidadTotal']==30
        if not args.windows:
            saved,_=request(inventory,f'/api/v1/planificaciones/{oid}');assert saved['cantidadTotal']==30
        report['comprobaciones']+=['Planificación y líneas202, transición409, ausencia404, stock insuficiente409 sin transición','Reinicio conserva orden y proyección SQL; eventos propios sin cuerpo de petición']
        report.update(resultado='PASS',reinicio_con_persistencia='PASS',mensajeria='PASS' if not args.windows else 'CUBIERTA_EN_LINUX')
    except Exception as error:
        report['error']=str(error)
        for stream in streams.values():stream.flush()
        for log in logs.glob('*.log'):print(log.name+'\n'+log.read_text(encoding='utf-8',errors='replace')[-5000:])
    finally:
        for name in list(processes):stop(name)
        if broker_stopped:
            try:broker_action('start')
            except Exception as error:report['limpieza_rabbit_error']=str(error);report['resultado']='FAIL'
        if temp:temp.cleanup()
        path=ROOT/'M07_OBSERVABILIDAD_RESILIENCIA'/('M07_WINDOWS_RESULTADOS.json' if args.windows else 'M07_HTTP_RESULTADOS.json')
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='codigo_normalizado_sha256'},ensure_ascii=False))
    return 0 if report['resultado']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
