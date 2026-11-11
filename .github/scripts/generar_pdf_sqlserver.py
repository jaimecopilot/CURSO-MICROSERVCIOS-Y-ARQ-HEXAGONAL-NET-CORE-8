#!/usr/bin/env python3
"""Regenera los ocho PDF y verifica texto completo, límites y correspondencia MD."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import fitz
import markdown
from weasyprint import HTML, CSS
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('pdf_m05', ROOT/'.github/scripts/m05_generar_pdf.py')
shared = importlib.util.module_from_spec(spec); spec.loader.exec_module(shared)

def main():
    # Conserva las comprobaciones específicas de cada manual y su estilo aprobado.
    for script in ['generar_pdf_m02.py', 'm03_generar_pdf.py', 'm04_generar_pdf.py', 'm05_generar_pdf.py']:
        subprocess.run([sys.executable, str(ROOT/'.github/scripts'/script)], cwd=ROOT, check=True)
    m02 = ROOT/'M02_APIS_REST_ASPNET_CORE/TEORIA/M02_TEORIA.md'
    html = markdown.markdown(m02.read_text(), extensions=['extra','sane_lists','toc'])
    HTML(string='<html lang="es"><meta charset="utf-8"><body>'+html+'</body></html>', base_url=str(m02.parent)).write_pdf(str(m02.with_suffix('.pdf')), stylesheets=[CSS(string=shared.CSS_TEXT)])
    results=[]
    for module in range(2,6):
        folder=next(ROOT.glob(f'M{module:02}_*'))
        for kind in ['TEORIA','PRACTICAS']:
            md=folder/kind/f'M{module:02}_{kind}.md';pdf=md.with_suffix('.pdf')
            source=md.read_text(encoding='utf-8')
            if kind=='PRACTICAS' and re.search(r'\b(?:fuente|fuentes|procedencia)\b',source,re.I):
                raise ValueError(f'Referencia editorial en {md}')
            if (folder/'FUENTE').exists():raise ValueError(f'Carpeta FUENTE en {folder}')
            html=markdown.markdown(source,extensions=['extra','sane_lists','toc'])
            with fitz.open(pdf) as doc:
                coverage=shared.verify_text_coverage(html,doc)
                for i,page in enumerate(doc,1):
                    if len(page.get_text().strip())<12:raise ValueError(f'Página vacía {pdf}:{i}')
                    for word in page.get_text('words'):
                        rect=fitz.Rect(word[:4])
                        if rect.x0 < -1 or rect.y0 < -1 or rect.x1>page.rect.width+1 or rect.y1>page.rect.height+1:
                            raise ValueError(f'Texto fuera de página {pdf}:{i}: {word[4]}')
                results.append({'modulo':module,'tipo':kind,'paginas':len(doc),'resultado':'PASS',
                    'md_sha256':hashlib.sha256(md.read_bytes()).hexdigest(),
                    'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),**coverage})
    report={'resultado':'PASS','commit_comprobado':os.environ.get('GITHUB_SHA'),
            'documentos':results,'revision_visual':'La inspección humana/asistida de páginas se registra por separado.'}
    out=ROOT/'docs/validacion-sqlserver/PDF_RESULTADOS.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
