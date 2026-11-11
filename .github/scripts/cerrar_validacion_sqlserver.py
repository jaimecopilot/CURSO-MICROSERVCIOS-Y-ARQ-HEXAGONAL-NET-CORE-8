#!/usr/bin/env python3
"""Solo cierra las tareas tras contrastar artefactos, revisión y ambas plataformas."""
import hashlib
import json
import os
from pathlib import Path
import re
from validar_sqlserver import ROOT, MODULES, file_manifest, validate_windows_sources

def main():
    folder=ROOT/'docs/validacion-sqlserver';sha=os.environ['GITHUB_SHA'];rows=[]
    for module,(name,_,counts) in MODULES.items():
        sql=json.loads((folder/f'M{module:02}_SQLSERVER_RESULTADOS.json').read_text())
        win=json.loads((folder/f'M{module:02}_LOCALDB_RESULTADOS.json').read_text())
        assert sql['resultado']==win['resultado']=='PASS',f'M{module:02}: comprobaciones incompletas'
        assert sql['commit_comprobado']==win['commit_comprobado']==sha,'Evidencia de otra revisión'
        assert sql['tests_por_etapa']==counts,'Conteos inconsistentes'
        assert sql['archivos_proyectos_sha256']==file_manifest(ROOT/name/'PROYECTO'),'Proyectos distintos de los comprobados'
        manual=ROOT/name/'PRACTICAS'/f'M{module:02}_PRACTICAS.md'
        assert sql['manual_sha256']==hashlib.sha256(manual.read_bytes()).hexdigest(),'Manual distinto del probado'
        final_stage = sorted((ROOT/name/'PROYECTO').iterdir())[-1].name
        validate_windows_sources(win['codigo_normalizado_sha256'], sql['codigo_normalizado_sha256'], final_stage)
        assert win['reinicio_con_persistencia']==win['limpieza']=='PASS','Windows incompleto'
        rows.append(f'| M{module:02} | {len(counts)} | '+', '.join(map(str,counts))+f" | {sql['bases_verificadas']} | PASS |")
    pdf=json.loads((folder/'PDF_RESULTADOS.json').read_text())
    assert pdf['resultado']=='PASS' and len(pdf['documentos'])==8,'PDF incompletos'
    for item in pdf['documentos']:
        name=MODULES[item['modulo']][0];stem=ROOT/name/item['tipo']/f"M{item['modulo']:02}_{item['tipo']}"
        for ext,key in [('.md','md_sha256'),('.pdf','pdf_sha256')]:
            assert hashlib.sha256(stem.with_suffix(ext).read_bytes()).hexdigest()==item[key],'PDF/Markdown desincronizado'
    run=f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
    text=f'''# Validación SQL Server M02–M05

Resultado automatizado: **PASS**. Revisión comprobada: `{sha}`.

Ejecución: {run}

| Módulo | Etapas reconstruidas | Pruebas por etapa | Bases SQL verificadas | Windows LocalDB y reinicio HTTP |
|---|---:|---|---:|---|
'''+ '\n'.join(rows)+'''

Las pruebas de integración utilizaron SQL Server Express real iniciado con Testcontainers. Cada prueba dispone de una base aislada. Las pruebas de dominio puro conservan su independencia de infraestructura. Windows comprueba los cuatro proyectos finales, peticiones HTTP, validación, conflictos y conservación de los datos después de reiniciar el proceso.

Los retos programados de M03, M04 y M05 se ejecutan aisladamente. M02 contiene propuestas abiertas de ampliación manual; su informe las identifica como MANUAL_NO_EJECUTADO y no las cuenta como pruebas aprobadas.

M01 conserva la evidencia SQL Server Docker 1.1–1.5 y LocalDB Windows 1.1/1.5 de la ejecución 42862047382; no se modificó su código.

Los ocho PDF fueron regenerados desde sus Markdown; se comprobaron cobertura íntegra de texto y límites de página. La revisión visual y la revisión independiente del cambio se registran en REVISION_FINAL.md antes de integrar en main.
'''
    (folder/'CIERRE_AUTOMATIZADO.md').write_text(text,encoding='utf-8')
    plan=folder/'PLAN_Y_ESTADO.md'
    content=plan.read_text();content=re.sub(r'- \[ \] (0[2-9]|1[01]) ',r'- [x] \1 ',content)
    content+='\nComprobaciones automáticas completadas en '+run+'; las tareas 12 y 13 requieren además revisión visual y revisión final documentadas.\n'
    plan.write_text(content)
    print(text)
if __name__=='__main__':main()
