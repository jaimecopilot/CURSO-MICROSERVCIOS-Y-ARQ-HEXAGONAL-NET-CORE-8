#!/usr/bin/env python3
"""PDF de teoría y prácticas M03 desde los Markdown: base tipográfica M01/M02."""
from __future__ import annotations
from pathlib import Path
import json,re
from weasyprint import HTML,CSS
import fitz
try:
 import markdown
 def tohtml(source):return markdown.markdown(source,extensions=['extra','sane_lists','toc'],output_format='html5')
except ImportError:
 import mistune
 parser=mistune.create_markdown(plugins=['table','strikethrough'])
 def tohtml(source):return parser(source)
ROOT=Path(__file__).resolve().parents[2]
M03=ROOT/'M03_ARQUITECTURA_HEXAGONAL'
CSS_TEXT=r"""
@page { size: A4; margin: 17mm 17mm 19mm 17mm;
  @bottom-center { content: counter(page); font-size: 8pt; color: #667085; } }
html { font-family: "DejaVu Sans", sans-serif; color: #18202a; font-size: 9.4pt; }
body { line-height: 1.39; }
h1,h2,h3,h4 { color: #142b43; line-height: 1.22; break-after: avoid; }
h1 { font-size: 20pt; margin: 14pt 0 13pt; }
h2 { font-size: 15pt; margin: 17pt 0 9pt; }
h3 { font-size: 12pt; margin: 13pt 0 6pt; }
h4 { font-size: 10.5pt; margin: 11pt 0 5pt; }
p { margin: 5pt 0 8pt; orphans: 2; widows: 2; }
ul,ol { margin: 4pt 0 9pt; padding-left: 15pt; }
li { margin: 0 0 4pt; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word;
  font-family: "DejaVu Sans Mono", monospace; font-size: 7.65pt; line-height: 1.34;
  border-left: 3pt solid #91a9bc; padding: 7pt 8pt; background: #f3f6f9;
  margin: 8pt 0 11pt; }
code { font-family: "DejaVu Sans Mono", monospace; overflow-wrap: anywhere; font-size: .92em; }
pre code { font-size: inherit; }
table { width: 100%; border-collapse: collapse; margin: 11pt 0; table-layout: fixed;
  font-size: 8.15pt; line-height: 1.3; }
thead { display: table-header-group; }
th { background: #eaf1f7; color: #10283e; font-weight: bold; }
td,th { border: .55pt solid #aebfce; vertical-align: top; padding: 5pt 6pt;
  overflow-wrap: anywhere; word-break: break-word; }
tr { break-inside: avoid; }
img { max-width: 100%; height: auto; object-fit: contain; }
blockquote { border-left: 3pt solid #bacbd9; margin: 9pt 0; padding-left: 9pt; }
hr { border: none; border-top: 1pt solid #d0d9e2; margin: 14pt 0; }
"""

def main():
 reports=[]
 for typ in ('TEORIA','PRACTICAS'):
  doc=M03/typ/f'M03_{typ}.md'
  source=doc.read_text(encoding='utf-8')
  if typ=='TEORIA':
   assert len(re.findall(r'^### Bloque \d+ —',source,re.M))==40
   assert all(f'# Punto 3.{i}' in source for i in range(1,5))
  else:
   steps=re.findall(r'^### PASO (3\.[1-4]\.\d+) —',source,re.M)
   assert steps == [f'3.{i}.{j}' for i in range(1,5) for j in range(1,25)]
   assert source.count('**Procedimiento guiado.**')==96
  if re.search(r'^## Errores\s+comunes\s+del\s+ejercicio\s+completo\s*$',source,re.I|re.M):
   raise ValueError(f'La seccion global de errores no debe aparecer en M03_{typ}.md')
  html=tohtml(source)
  pdf=doc.with_suffix('.pdf')
  HTML(string="<html lang='es'><meta charset='utf-8'><body>"+html+'</body></html>',
       base_url=str(doc.parent.resolve())).write_pdf(str(pdf),stylesheets=[CSS(string=CSS_TEXT)])
  document=fitz.open(pdf)
  minpages=20 if typ=='TEORIA' else 40
  if len(document)<minpages:raise ValueError(f'PDF corto {typ}: {len(document)} páginas')
  text='\n'.join(page.get_text() for page in document)
  for i in range(1,5):
   if f'Punto 3.{i}' not in text:raise ValueError(f'Sin punto 3.{i} en {typ}')
  blank=[];bounds=[]
  for i,page in enumerate(document,1):
   if len(page.get_text().strip())<12:blank.append(i)
   for w in page.get_text('words'):
    x0,y0,x1,y1=w[:4]
    if x0< -1 or y0< -1 or x1>page.rect.width+1 or y1>page.rect.height+1:
     bounds.append(dict(pagina=i,palabra=w[4],bounds=[x0,y0,x1,y1]))
     if len(bounds)>20:break
   if len(bounds)>20:break
  if blank or bounds:raise RuntimeError(f'Geometria PDF {typ}: vacias {blank}, fuera {bounds}')
  reports.append(dict(documento=typ,paginas=len(document),bytes=pdf.stat().st_size,
                      palabras=len(source.split()),pdf=str(pdf.relative_to(ROOT)),
                      paginas_blancas=blank,desbordamientos=bounds))
  print(json.dumps(reports[-1],ensure_ascii=False),flush=True)
 (M03/'REPORTE_PDF_M03.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
