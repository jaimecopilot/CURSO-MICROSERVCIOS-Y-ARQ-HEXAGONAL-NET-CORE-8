#!/usr/bin/env python3
"""Comprueba YARP y cuatro procesos reales sobre SQL Server/LocalDB y RabbitMQ."""
from __future__ import annotations
import argparse,json,os,re,socket,subprocess,time,urllib.request,urllib.error,uuid,tempfile,shutil,sys
from pathlib import Path
from validar_sqlserver import source_manifest
from m07_http_real import own,verify_health
from m08_e2e_desde_practicas import STAGES
ROOT=Path(__file__).resolve().parents[2]
FINAL=ROOT/'M08_API_GATEWAY/PROYECTO'/STAGES[-1]


class SinRedirecciones(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None


def request(base,path,method='GET',body=None,expected=200,headers=None):
    """Envía exactamente una petición y acepta solo los estados expresamente previstos."""
    req=urllib.request.Request(base+path,data=None if body is None else json.dumps(body).encode('utf-8'),
        method=method,headers={'Content-Type':'application/json',**(headers or {})})
    try:response=urllib.request.build_opener(SinRedirecciones()).open(req,timeout=12)
    except urllib.error.HTTPError as error:response=error
    with response:
        data=response.read().decode('utf-8');status=response.status
        result_headers={key.lower():value for key,value in response.headers.items()}
    expected_statuses=expected if isinstance(expected,tuple) else (expected,)
    if status not in expected_statuses:raise AssertionError(f'{method} {path}: {status}, esperado {expected}: {data}')
    return json.loads(data) if data else None,result_headers


def verify_liveness(name,data):
    expected={'servicio':'Gateway','estado':'vivo'} if name=='gateway' else {'estado':'Healthy','componentes':[]}
    assert data==expected,f'Liveness de {name} no corresponde a su contrato'


def verify_instances(values):
    assert set(values)=={'inventario-1','inventario-2'},f'No se acredita reparto entre dos instancias: {values}'


def verify_projection(data,order_id,total):
    assert data.get('ordenId')==order_id and data.get('cantidadTotal')==total,'La proyección no corresponde a la orden planificada'


def verify_correlation(events,correlation,secrets):
    selected=[e['Properties'] for e in own(events) if e['Properties'].get('CorrelationId')==correlation and 'Ruta' in e['Properties']]
    assert {'Gateway','Produccion','Inventario'} <= {p.get('Servicio') for p in selected},'Falta correlación gateway→Producción→Inventario'
    assert all('{' in p['Ruta'] and '?' not in p['Ruta'] for p in selected),'Falta plantilla de ruta en eventos propios'
    payload=json.dumps(own(events),ensure_ascii=False)
    assert all(secret not in payload for secret in secrets),'Dato sensible en eventos propios'


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--windows',action='store_true');args=parser.parse_args(argv)
    if args.windows and sys.platform!='win32':raise RuntimeError('LocalDB requiere Windows real')
    execution=uuid.uuid4().hex
    logs=ROOT/'.qa/m08-http'/execution;logs.mkdir(parents=True,exist_ok=False)
    report={'resultado':'FAIL','ejecucion':execution,'commit_comprobado':os.environ.get('GITHUB_SHA'),
            'plataforma':'Windows LocalDB' if args.windows else 'Linux SQL Server Express y RabbitMQ',
            'codigo_normalizado_sha256':source_manifest(FINAL),'comprobaciones':[],'casos_http':[]}
    processes={};streams={};temporary=None
    def stop(name):
        process=processes.pop(name,None)
        if process:
            process.terminate()
            try:process.wait(timeout=20)
            except subprocess.TimeoutExpired:process.kill();process.wait()
        stream=streams.pop(name,None)
        if stream:stream.close()
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
        temporary=tempfile.TemporaryDirectory(prefix='axia8-',dir=os.environ.get('RUNNER_TEMP'))
        stage=Path(temporary.name)/'etapa';shutil.copytree(FINAL,stage,ignore=shutil.ignore_patterns('bin','obj','TestResults','.vs'))
        assert source_manifest(stage)==report['codigo_normalizado_sha256']
        for project in ('AceriaApp.Api','AceriaApp.Inventario.Api','AceriaApp.Gateway'):
            subprocess.run(['dotnet','build',str(stage/'src'/project/(project+'.csproj')),'-c','Release','-m:1','--disable-build-servers','-p:NuGetAudit=false'],check=True)
        ports={}
        sockets=[]
        for name in ('gateway','produccion','inventario-1','inventario-2'):
            listener=socket.socket();listener.bind(('127.0.0.1',0));sockets.append(listener);ports[name]=listener.getsockname()[1]
        for listener in sockets:listener.close()
        urls={name:f'http://127.0.0.1:{port}' for name,port in ports.items()}
        prefix=os.environ['ACERIA_HTTP_SQL_PREFIX'];server=os.environ['ACERIA_TEST_SQLSERVER']
        env=dict(os.environ,ASPNETCORE_ENVIRONMENT='Development',Comunicacion__InventarioUrl=urls['inventario-1']+'/',
                 Comunicacion__WorkersActivos='false' if args.windows else 'true',Comunicacion__Prefijo='http8-'+uuid.uuid4().hex,
                 Observabilidad__DiagnosticoActivo='true',Observabilidad__NivelMinimo='Information')
        for key in ('AceriaApp','AceriaHexagonal','AceriaProduccion','AceriaInventario'):
            env['ConnectionStrings__'+key]=server+';Database='+prefix+'_'+key
        if not args.windows:env['Comunicacion__RabbitMqUri']=os.environ['ACERIA_TEST_RABBITMQ']
        env['ReverseProxy__Clusters__produccion-cluster__Destinations__produccion__Address']=urls['produccion']+'/'
        for name in ('inventario-1','inventario-2'):
            env[f'ReverseProxy__Clusters__inventario-cluster__Destinations__{name}__Address']=urls[name]+'/'
        def start(name):
            project='AceriaApp.Gateway' if name=='gateway' else 'AceriaApp.Api' if name=='produccion' else 'AceriaApp.Inventario.Api'
            api=stage/'src'/project
            stream=(logs/(name+'-'+uuid.uuid4().hex[:6]+'.log')).open('w',encoding='utf-8');streams[name]=stream
            extra={'ASPNETCORE_URLS':urls[name]}
            if name.startswith('inventario-'):extra['Inventario__Instancia']=name
            processes[name]=subprocess.Popen(['dotnet',str(api/'bin/Release/net8.0'/(project+'.dll')),'--urls',urls[name]],cwd=api,
                env=dict(env,**extra),stdout=stream,stderr=subprocess.STDOUT)
            def alive():
                if processes[name].poll() is not None:raise RuntimeError(name+' terminó al iniciar')
                data,_=request(urls[name],'/health/live');verify_liveness(name,data)
            wait_for(alive,120)
        # Evita competir al crear y sembrar la misma base de Inventario.
        for name in ('inventario-1','inventario-2','produccion','gateway'):start(name)
        gateway=urls['gateway']
        for name in ('produccion','inventario-1','inventario-2'):
            ready,_=request(urls[name],'/health/ready');verify_health(ready,healthy=True)
        def call(path,method='GET',body=None,status=200,headers=None):
            data,response_headers=request(gateway,path,method,body,expected=status,headers=headers)
            report['casos_http'].append({'metodo':method,'ruta':path,'estado':status})
            return data,response_headers
        material,_=call('/api/v1/materiales/Acero');assert material['stock']==300
        head,head_headers=call('/api/v1/materiales/Acero','HEAD')
        assert head is None and head_headers.get('x-instancia') in ('inventario-1','inventario-2')
        report['head_sin_cuerpo']=True
        report['proxy']='PASS'
        correlation='m08-'+uuid.uuid4().hex;query='query-'+uuid.uuid4().hex;token='token-'+uuid.uuid4().hex
        material,headers=call('/api/v1/comunicacion/materiales/Acero?secreto='+query,headers={'X-Correlation-ID':correlation,'Authorization':'Bearer '+token})
        assert material['stock']==300 and headers['x-correlation-id']==correlation
        wait_for(lambda:verify_correlation(events(),correlation,[query,token]))
        _,headers=call('/api/v1/materiales/Acero',headers={'X-Correlation-ID':'invalido/con/barra'})
        assert re.fullmatch(r'[a-f0-9]{32}',headers['x-correlation-id'])
        report['correlacion']='PASS'
        body={'cliente':'Axia gateway '+execution,'material':'Acero','cantidad':20}
        created,headers=call('/api/v1/ordenes','POST',body,201)
        location=headers['location'];assert location.startswith('/api/v1/ordenes/') or location.startswith(gateway+'/api/v1/ordenes/')
        resource=location.removeprefix(gateway)
        saved,_=call(resource);assert saved['id']==created['id'] and saved['cantidad']==20
        call('/api/v1/ordenes','POST',{'cliente':'','material':'Acero','cantidad':0},400)
        call('/api/v1/ordenes','POST',{**body,'cantidad':501},422)
        call('/api/v1/ordenes/'+str(uuid.uuid4()),status=404)
        call(resource+'/finalizar','POST',{},200);call(resource+'/finalizar','POST',{},409)
        report['contratos_http']='PASS'
        alias,headers=call('/inventario/api/v1/materiales/Acero?origen=smoke');assert alias==material and headers['x-instancia'] in ('inventario-1','inventario-2')
        alias_head,alias_headers=call('/inventario/api/v1/materiales/Acero','HEAD')
        assert alias_head is None and alias_headers.get('x-instancia') in ('inventario-1','inventario-2')
        for path in ('/api/diagnostico/fallo','/inventario/api/diagnostico/fallo','/admin','/api/v1/hexagonal/ordenes'):
            call(path,status=404)
        # Solo GET/HEAD publican Inventario; YARP no envía escrituras a ese cluster.
        call('/api/v1/materiales/Acero','POST',{},405)
        report['rutas_y_transformaciones']='PASS'
        def sample(count=12):
            return [request(gateway,'/api/v1/materiales/Acero')[1].get('x-instancia') for _ in range(count)]
        def balanced():
            values=sample();verify_instances(values);return values
        report['balanceo_instancias']=wait_for(balanced);report['balanceo']='PASS'
        order,_=call('/api/v1/produccion/ordenes','POST',body,201);order_id=order['id']
        call(f'/api/v1/produccion/ordenes/{order_id}/lineas','POST',{'material':'Inoxidable','cantidad':10})
        accepted,_=call(f'/api/v1/comunicacion/ordenes/{order_id}/planificar','POST',{},202);assert accepted['ordenId']==order_id
        call(f'/api/v1/comunicacion/ordenes/{order_id}/planificar','POST',{},409)
        if not args.windows:
            def projected():
                projection,_=request(gateway,f'/api/v1/planificaciones/{order_id}');verify_projection(projection,order_id,30)
                assert projection.get('eventoId');return projection
            projection=wait_for(projected,60)
            head,_=call(f'/api/v1/planificaciones/{order_id}','HEAD');assert head is None
            report['mensajeria_orden_id']=order_id;report['mensajeria_evento_id']=projection['eventoId'];report['mensajeria_total']=30
            report['mensajeria']='PASS'
        else:report['mensajeria']='CUBIERTA_EN_LINUX'
        stop('inventario-1')
        def only_healthy():
            values=sample(6);assert set(values)=={'inventario-2'},'Se sigue enviando a una instancia caída';return values
        report['instancia_caida']=wait_for(only_healthy,20)
        stop('inventario-2')
        def unavailable():
            _,headers=request(gateway,'/api/v1/materiales/Acero',expected=503)
            return 503
        report['todos_caidos_http']=wait_for(unavailable,20)
        for name in ('inventario-1','inventario-2'):start(name)
        report['recuperacion_instancias']=wait_for(balanced,30);report['fallo_y_recuperacion']='PASS'
        stop('produccion');start('produccion')
        saved,_=wait_for(lambda:request(gateway,f'/api/v1/produccion/ordenes/{order_id}'),30)
        assert saved['estado']=='Planificada' and saved['cantidadTotal']==30
        persisted,_=request(gateway,resource);assert persisted['id']==created['id'] and persisted['estado']=='Finalizada'
        if not args.windows:
            projection=wait_for(projected,30);verify_projection(projection,order_id,30)
        report['persistencia_orden_id']=order_id;report['reinicio_con_persistencia']='PASS'
        report['comprobaciones']=['Cuatro procesos reales: YARP, Producción y dos Inventario sobre SQL',
            '201 y Location accesible; validación400, ausencia404, conflicto409 y regla422',
            'Alias de Inventario y rutas internas no publicadas; correlación entre tres servicios',
            'RoundRobin reparte; caída parcial, todos503 y recuperación; reinicio conserva SQL',
            'Outbox/inbox con RabbitMQ y proyección SQL' if not args.windows else 'Mensajería acreditada separadamente por Linux']
        report['resultado']='PASS'
    except Exception as error:
        report['error']=str(error)
        for stream in streams.values():stream.flush()
        for log in logs.glob('*.log'):print(log.name+'\n'+log.read_text(encoding='utf-8',errors='replace')[-5000:])
    finally:
        for name in list(processes):stop(name)
        if temporary:temporary.cleanup()
        path=ROOT/'M08_API_GATEWAY'/('M08_WINDOWS_RESULTADOS.json' if args.windows else 'M08_HTTP_RESULTADOS.json')
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='codigo_normalizado_sha256'},ensure_ascii=False))
    return 0 if report['resultado']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
