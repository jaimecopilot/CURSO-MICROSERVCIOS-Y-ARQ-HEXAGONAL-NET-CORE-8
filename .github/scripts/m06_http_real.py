#!/usr/bin/env python3
"""Dos procesos Kestrel, dos contextos propietarios y persistencia real."""
import argparse,json,os,socket,subprocess,time,urllib.request,urllib.error,uuid,tempfile,shutil,sys
from pathlib import Path
from validar_sqlserver import source_manifest
ROOT=Path(__file__).resolve().parents[2]
FINAL=ROOT/'M06_COMUNICACION_MICROSERVICIOS/PROYECTO/6.3-cuando-usar-cada-enfoque'

def request(base,path,method='GET',body=None,expected=200):
    req=urllib.request.Request(base+path,data=None if body is None else json.dumps(body).encode(),method=method,
                               headers={'Content-Type':'application/json'})
    try:response=urllib.request.urlopen(req,timeout=12)
    except urllib.error.HTTPError as error:response=error
    with response:
        data=response.read().decode();status=response.status;headers=dict(response.headers)
    if status!=expected:raise AssertionError(f'{method} {path}: {status}, esperado {expected}: {data}')
    return json.loads(data) if data else None,headers

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--windows',action='store_true');args=parser.parse_args()
    if args.windows and sys.platform!='win32':raise RuntimeError('El recorrido LocalDB exige Windows')
    logs=ROOT/'.qa/m06-http';logs.mkdir(parents=True,exist_ok=True)
    report={'resultado':'FAIL','commit_comprobado':os.environ.get('GITHUB_SHA'),
            'plataforma':'Windows LocalDB' if args.windows else 'Linux SQL Server Express y RabbitMQ',
            'codigo_normalizado_sha256':source_manifest(FINAL),'comprobaciones':[]}
    processes={};streams={};ports={};temp=None
    def stop(name):
        p=processes.pop(name,None)
        if p:
            p.terminate()
            try:p.wait(timeout=20)
            except subprocess.TimeoutExpired:p.kill();p.wait()
        if name in streams:streams.pop(name).close()
    try:
        temp=tempfile.TemporaryDirectory(prefix='axia6-',dir=os.environ.get('RUNNER_TEMP'))
        stage=Path(temp.name)/'etapa';shutil.copytree(FINAL,stage,ignore=shutil.ignore_patterns('bin','obj','TestResults','.vs'))
        assert source_manifest(stage)==report['codigo_normalizado_sha256']
        for name in ('AceriaApp.Api','AceriaApp.Inventario.Api'):
            subprocess.run(['dotnet','build',str(stage/'src'/name/(name+'.csproj')),'-c','Release','-m:1','--disable-build-servers','-p:NuGetAudit=false'],check=True)
        for name in ('produccion','inventario'):
            with socket.socket() as s:s.bind(('127.0.0.1',0));ports[name]=s.getsockname()[1]
        urls={k:f'http://127.0.0.1:{v}' for k,v in ports.items()}
        prefix=os.environ['ACERIA_HTTP_SQL_PREFIX'];server=os.environ['ACERIA_TEST_SQLSERVER']
        env=dict(os.environ,ASPNETCORE_ENVIRONMENT='Development',Comunicacion__InventarioUrl=urls['inventario']+'/',
                 Comunicacion__WorkersActivos='false' if args.windows else 'true',Comunicacion__Prefijo='http-'+uuid.uuid4().hex)
        for key in ('AceriaApp','AceriaHexagonal','AceriaProduccion','AceriaInventario'):
            env['ConnectionStrings__'+key]=server+';Database='+prefix+'_'+key
        if not args.windows:env['Comunicacion__RabbitMqUri']=os.environ['ACERIA_TEST_RABBITMQ']
        def start(name):
            project='AceriaApp.Api' if name=='produccion' else 'AceriaApp.Inventario.Api'
            api=stage/'src'/project
            stream=(logs/(name+'-'+uuid.uuid4().hex[:5]+'.log')).open('w',encoding='utf-8');streams[name]=stream
            processes[name]=subprocess.Popen(['dotnet',str(api/'bin/Release/net8.0'/(project+'.dll'))],cwd=api,
                                             env=dict(env,ASPNETCORE_URLS=urls[name]),stdout=stream,stderr=subprocess.STDOUT)
            deadline=time.monotonic()+120
            while time.monotonic()<deadline:
                if processes[name].poll() is not None:raise RuntimeError(name+' terminó al iniciar')
                try:request(urls[name],'/swagger/v1/swagger.json' if name=='produccion' else '/health');return
                except (urllib.error.URLError,TimeoutError,OSError):time.sleep(.3)
            raise TimeoutError(name+' no arrancó')
        start('inventario');start('produccion')
        api=urls['produccion'];inventory=urls['inventario']
        material,_=request(api,'/api/v1/comunicacion/materiales/Acero');assert material['stock']==300
        request(api,'/api/v1/comunicacion/materiales/NoExiste',expected=404)
        order,_=request(api,'/api/v1/produccion/ordenes','POST',{'cliente':'Axia M06','material':'Acero','cantidad':20},201)
        oid=order['id'];request(api,f'/api/v1/produccion/ordenes/{oid}/lineas','POST',{'material':'Inoxidable','cantidad':10})
        request(api,f'/api/v1/comunicacion/ordenes/{oid}/planificar','POST',{},202)
        request(api,f'/api/v1/comunicacion/ordenes/{oid}/planificar','POST',{},409)
        request(api,f'/api/v1/comunicacion/ordenes/{uuid.uuid4()}/planificar','POST',{},404)
        report['comprobaciones']+=['HTTP entre procesos:200/404','Planificar orden y líneas:202','Transición repetida:409','Orden ausente:404']
        if not args.windows:
            deadline=time.monotonic()+45
            while True:
                try:projection,_=request(inventory,f'/api/v1/planificaciones/{oid}');break
                except AssertionError:
                    if time.monotonic()>deadline:raise
                    time.sleep(.25)
            assert projection['cantidadTotal']==30
            report['comprobaciones'].append('SQL Producción -> outbox -> RabbitMQ -> inbox SQL Inventario:30 unidades')
        excessive,_=request(api,'/api/v1/produccion/ordenes','POST',{'cliente':'Axia','material':'Acero','cantidad':450},201)
        request(api,f'/api/v1/comunicacion/ordenes/{excessive["id"]}/planificar','POST',{},409)
        pending,_=request(api,f'/api/v1/produccion/ordenes/{excessive["id"]}');assert pending['estado']=='Borrador'
        stop('inventario')
        request(api,'/api/v1/comunicacion/materiales/Acero',expected=503)
        request(api,f'/api/v1/comunicacion/ordenes/{excessive["id"]}/planificar','POST',{},503)
        start('inventario');stop('produccion');start('produccion')
        saved,_=request(api,f'/api/v1/produccion/ordenes/{oid}');assert saved['estado']=='Planificada' and saved['cantidadTotal']==30
        if not args.windows:
            saved,_=request(inventory,f'/api/v1/planificaciones/{oid}');assert saved['cantidadTotal']==30
        report['comprobaciones']+=['Stock insuficiente:409 sin transición','Servicio caído:503','Reinicio de ambos procesos conserva datos SQL']
        report.update(resultado='PASS',reinicio_con_persistencia='PASS',mensajeria='PASS' if not args.windows else 'CUBIERTA_EN_LINUX')
    except Exception as error:
        report['error']=str(error)
        for stream in streams.values():stream.flush()
        for log in logs.glob('*.log'):print(log.name+'\n'+log.read_text(errors='replace')[-6000:])
    finally:
        for name in list(processes):stop(name)
        if temp:temp.cleanup()
        path=ROOT/'M06_COMUNICACION_MICROSERVICIOS'/('M06_WINDOWS_RESULTADOS.json' if args.windows else 'M06_HTTP_RESULTADOS.json')
        path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='codigo_normalizado_sha256'},ensure_ascii=False))
    return 0 if report['resultado']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
