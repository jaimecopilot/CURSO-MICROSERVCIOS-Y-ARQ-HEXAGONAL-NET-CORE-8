#!/usr/bin/env python3
"""Prueba Windows: proceso HTTP real, SQL LocalDB y datos conservados tras reiniciar."""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from validar_sqlserver import reconstruct_through, source_manifest
ROOT = Path(__file__).resolve().parents[2]
FINAL = {2: 'M02_APIS_REST_ASPNET_CORE/PROYECTO/2.4-documentacion-openapi',
         3: 'M03_ARQUITECTURA_HEXAGONAL/PROYECTO/3.4-implementacion-aspnet-core',
         4: 'M04_PATRONES_ARQUITECTURA/PROYECTO/4.5-inyeccion-dependencias',
         5: 'M05_DDD_CQRS/PROYECTO/5.5-dominio-aceria'}

def request(base, path, method='GET', body=None, expected=200):
    data = json.dumps(body).encode() if body is not None else (b'' if method == 'POST' else None)
    req = urllib.request.Request(base + path, data=data, method=method, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            status, text, headers = response.status, response.read().decode(), dict(response.headers)
    except urllib.error.HTTPError as exc:
        status, text, headers = exc.code, exc.read().decode(), dict(exc.headers)
    if status != expected:
        raise AssertionError(f'{method} {path}: HTTP {status}, esperado {expected}: {text[:1500]}')
    return json.loads(text) if text else None, headers

def sql(action, databases=''):
    command = ['powershell', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File',
               str(ROOT / '.github/scripts/localdb_sql.ps1'), '-Action', action]
    if databases: command += ['-Databases', databases]
    return subprocess.check_output(command, text=True, encoding='utf-8').strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--modulo', type=int, choices=FINAL, required=True)
    module = parser.parse_args().modulo
    result = {'modulo': module, 'resultado': 'FAIL', 'fecha_utc': datetime.now(timezone.utc).isoformat(),
              'commit_comprobado': os.environ.get('GITHUB_SHA'), 'comprobaciones': []}
    prefix = 'AceriaTest_' + uuid.uuid4().hex
    databases = {key: prefix + '_' + key for key in ['AceriaApp', 'AceriaHexagonal', 'AceriaProduccion']}
    api = ROOT / FINAL[module] / 'src/AceriaApp.Api'
    logs = ROOT / '.qa/localdb' / f'm{module:02}'
    logs.mkdir(parents=True, exist_ok=True)
    process = None
    stream = None
    env = dict(os.environ, ASPNETCORE_ENVIRONMENT='Development', DOTNET_NOLOGO='true', DOTNET_PROCESSOR_COUNT='1')
    for key, database in databases.items():
        env['ConnectionStrings__' + key] = f'Server=(localdb)\\MSSQLLocalDB;Database={database};Trusted_Connection=True;TrustServerCertificate=True'
    def stop():
        nonlocal process, stream
        if process:
            process.terminate()
            try: process.wait(timeout=20)
            except subprocess.TimeoutExpired: process.kill(); process.wait()
            process = None
        if stream: stream.close(); stream = None
    def start(round_number):
        nonlocal process, stream
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
        base = f'http://127.0.0.1:{port}'
        env['ASPNETCORE_URLS'] = base
        stream = (logs / f'api-{round_number}.log').open('w', encoding='utf-8')
        process = subprocess.Popen(['dotnet', str(api / 'bin/Release/net8.0/AceriaApp.Api.dll')],
                                   cwd=api, env=env, stdout=stream, stderr=subprocess.STDOUT)
        deadline = time.monotonic() + 100
        while time.monotonic() < deadline:
            if process.poll() is not None: raise RuntimeError('La API termino al iniciar; consultar log')
            try: request(base, '/swagger/v1/swagger.json'); return base
            except (urllib.error.URLError, TimeoutError, OSError): time.sleep(.4)
        raise RuntimeError('La API no estuvo disponible a tiempo')
    try:
        if sys.platform != 'win32': raise RuntimeError('Esta comprobacion exige Windows y LocalDB')
        result['motor'] = json.loads(sql('info'))
        reconstruct_through(module)
        result['codigo_normalizado_sha256'] = source_manifest(ROOT / FINAL[module])
        subprocess.run(['dotnet', 'build', str(api / 'AceriaApp.Api.csproj'), '-c', 'Release', '-m:1'], cwd=api, env=env, check=True)
        base = start(1)
        routes = ['/api/v1/ordenes']
        if module >= 3: routes.append('/api/v1/hexagonal/ordenes')
        if module >= 4: routes.append('/api/v1/patrones/ordenes')
        if module >= 5: routes.append('/api/v1/produccion/ordenes')
        saved = []
        for route in routes:
            order, headers = request(base, route, 'POST', {'cliente': 'Axia SQL', 'material': 'Acero', 'cantidad': 20}, 201)
            location = next((v for k, v in headers.items() if k.lower() == 'location'), None)
            if not location or not order.get('id'): raise AssertionError('POST sin Location/id')
            path = route + '/' + order['id']
            request(base, path)
            request(base, route + '/' + str(uuid.uuid4()), expected=404)
            request(base, route, 'POST', {'cliente': '', 'material': 'Acero', 'cantidad': 0}, 400)
            if 'produccion' in route:
                request(base, path + '/lineas', 'POST', {'material': 'Inoxidable', 'cantidad': 10})
                request(base, path + '/planificar', 'POST')
            request(base, path + '/finalizar', 'POST')
            request(base, path + '/finalizar', 'POST', expected=409)
            saved.append(path)
            result['comprobaciones'].append({'ruta': route, 'post_201_location': 'PASS', 'get_200_404': 'PASS',
                                             'validacion_400': 'PASS', 'finalizar_200_409': 'PASS'})
        stop()
        base = start(2)
        for path in saved:
            order, _ = request(base, path)
            if order.get('estado') != 'Finalizada': raise AssertionError('Estado perdido tras reiniciar la API')
            if 'produccion' in path and (order.get('cantidadTotal') != 30 or len(order.get('lineas', [])) != 2):
                raise AssertionError('Agregado incompleto tras reiniciar')
        result.update(resultado='PASS', reinicio_con_persistencia='PASS', bases=list(databases.values()))
    except Exception as exc:
        result['error'] = str(exc)
    finally:
        stop()
        if sys.platform == 'win32':
            try: sql('drop', ','.join(databases.values())); result['limpieza'] = 'PASS'
            except Exception as exc: result.update(resultado='FAIL', error_limpieza=str(exc))
        out = ROOT / 'docs/validacion-sqlserver' / f'M{module:02}_LOCALDB_RESULTADOS.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if result['resultado'] == 'PASS' else 1
if __name__ == '__main__': sys.exit(main())
