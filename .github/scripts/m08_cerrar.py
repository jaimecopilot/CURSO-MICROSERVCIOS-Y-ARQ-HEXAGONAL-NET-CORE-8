#!/usr/bin/env python3
"""Cierra M08 solo cuando los tres artefactos conservan revisión, evidencia y hashes."""
from __future__ import annotations
import json, os, sys
from pathlib import Path
from m08_empaquetar import MODULE, EXPECTED, ROOT, read, require, revision_actual, sha, validate_kind, payload_files

def close_module(*,root=ROOT,revision=None,run_url=None):
    root=Path(root).resolve();base=root/MODULE;revision=revision or revision_actual(root)
    for kind in ('linux','windows','pdf'):
        certificate=read(root/'.qa/m08-certificados'/f'{kind}.json')
        require(certificate.get('tipo')==kind and certificate.get('resultado')=='PASS',f'Certificado {kind} inválido')
        require(certificate.get('commit_comprobado')==revision,f'El artefacto {kind} pertenece a otra revisión')
        hashes=certificate.get('archivos_sha256',{})
        require(isinstance(hashes,dict) and bool(hashes),f'El artefacto {kind} carece de hashes')
        expected_files={p.relative_to(root).as_posix() for p in payload_files(kind,base,root)}
        require(set(hashes)==expected_files,f'El certificado {kind} no cubre todos los archivos del artefacto')
        for relative,expected in hashes.items():
            path=root/relative
            require(path.resolve().is_relative_to(base.resolve()) and path.is_file() and not path.is_symlink(),f'Archivo de certificado inválido: {relative}')
            require(sha(path)==expected,f'El hash del archivo {relative} ha cambiado')
        validate_kind(kind,base,revision)
    # El job de publicación ya ha contrastado HEAD con GITHUB_SHA antes de extraer.
    run_url=run_url or f'https://github.com/{os.environ.get("GITHUB_REPOSITORY","")}/actions/runs/{os.environ.get("GITHUB_RUN_ID","")}'
    content=f'''# M08: comprobación automatizada

Resultado: PASS. Revisión `{revision}`.

Ejecución: {run_url}

Cuatro etapas reconstruidas desde el Markdown: {', '.join(str(n) for n in EXPECTED)} pruebas; cuatro retos ejecutados por separado con {', '.join(str(n+1) for n in EXPECTED)} pruebas. Se comprobaron SQL Server Express real, RabbitMQ real, tráfico YARP hacia Producción e Inventario, contratos HTTP, correlación, transformaciones, balanceo entre dos instancias, pérdida y recuperación de destinos y persistencia LocalDB en Windows. Los hashes del manual, proyectos y PDF coinciden con los tres artefactos certificados para esta revisión.

La revisión visual y el cierre editorial se registran por separado antes de integrar main.
'''
    (base/'CIERRE_AUTOMATIZADO.md').write_text(content,encoding='utf-8')
    return {'resultado':'PASS','commit_comprobado':revision,'tests_por_etapa':EXPECTED}

def main():
    try:print(json.dumps(close_module(),ensure_ascii=False));return 0
    except Exception as exc:print('M08 cierre rechazado: '+str(exc),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
