#!/usr/bin/env python3
"""PDF de teoría y prácticas M08 desde los Markdown: base tipográfica M01/M02."""
from __future__ import annotations
from pathlib import Path
import json,re,unicodedata,hashlib,argparse
from bs4 import BeautifulSoup
from weasyprint import HTML,CSS
import fitz
from m08_texto import parse_explanation
try:
 import markdown
 def tohtml(source):return markdown.markdown(source,extensions=['extra','sane_lists','toc'],output_format='html5')
except ImportError:
 import mistune
 parser=mistune.create_markdown(plugins=['table','strikethrough'])
 def tohtml(source):return parser(source)
ROOT=Path(__file__).resolve().parents[2]
M08=ROOT/'M08_API_GATEWAY'
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
li { margin: 0 0 4pt; break-inside: avoid; }
pre { break-inside: avoid; white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word;
  font-family: "DejaVu Sans Mono", monospace; font-size: 7.65pt; line-height: 1.34;
  border-left: 3pt solid #91a9bc; padding: 7pt 8pt; background: #f3f6f9;
  margin: 8pt 0 11pt; }
code { font-family: "DejaVu Sans Mono", monospace; overflow-wrap: anywhere; font-size: .92em; }
pre code { font-size: inherit; }
pre.long-code { break-inside: auto; }
table { width: 100%; border-collapse: collapse; margin: 11pt 0; table-layout: fixed;
  font-size: 8.15pt; line-height: 1.3; }
thead { display: table-header-group; }
th { background: #eaf1f7; color: #10283e; font-weight: bold; }
td,th { border: .55pt solid #aebfce; vertical-align: top; padding: 5pt 6pt;
  overflow-wrap: anywhere; word-break: break-word; }
tr { break-inside: avoid; }
table.inventory { table-layout: auto; }
table.inventory th { overflow-wrap: normal; word-break: normal; }
img { max-width: 100%; height: auto; object-fit: contain; }
blockquote { border-left: 3pt solid #bacbd9; margin: 9pt 0; padding-left: 9pt; }
.references, .point-intro { break-inside: avoid; }
.illustration { break-inside: avoid; }
hr { border: none; border-top: 1pt solid #d0d9e2; margin: 14pt 0; }
"""

def verify_text_coverage(html,document):
 def norm(text):
  return re.sub(r'\s+','',unicodedata.normalize('NFKC',text).replace('\u00ad',''))
 texts=[norm(''.join(page.get_text(clip=fitz.Rect(0,0,page.rect.width,790),sort=order)
                     for page in document)) for order in (True,False)]
 soup=BeautifulSoup(html,'html.parser')
 blocks=[]
 for tag in soup.find_all(['h1','h2','h3','h4','p','pre','li','td','th']):
  if tag.find_parent(['pre','li','td','th']):continue
  content=norm(tag.get_text())
  if content:blocks.append(content)
 missing=[(i,text[:120]) for i,text in enumerate(blocks) if all(text not in full for full in texts)]
 if missing:raise ValueError(f'Texto del Markdown no localizado en PDF: {missing[:12]}')
 return {'bloques_html':len(blocks),'bloques_pdf_verificados':len(blocks),'bloques_omitidos':0}

def verify_explanation_lines(source):
 """Cada cita Línea N debe pertenecer a la línea física N del bloque anterior."""
 in_fence=False;current=[];previous=[];verified=0
 for number,line in enumerate(source.splitlines(),1):
  if line.startswith('```'):
   if in_fence:previous=current;current=[]
   in_fence=not in_fence
   continue
  if in_fence:
   current.append(line);continue
  match=parse_explanation(line)
  if match:
   index=match[0]
   if not 1<=index<=len(previous):
    raise ValueError(f'Explicación fuera del ejemplo: línea Markdown {number}, Línea {index}')
   actual=previous[index-1].strip()
   if match[1]!=actual:
    raise ValueError(f'Explicación no corresponde al código: línea Markdown {number}, Línea {index}')
   verified+=1
 return verified

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--solo', choices=['TEORIA','PRACTICAS'], help='Renderiza solo el documento indicado')
 args=parser.parse_args()
 if (M08/'FUENTE').exists():
  raise ValueError('La carpeta FUENTE no forma parte del material docente M08')
 reports=[]
 for typ in ([args.solo] if args.solo else ('TEORIA','PRACTICAS')):
  doc=M08/typ/f'M08_{typ}.md'
  source=doc.read_text(encoding='utf-8')
  if re.search(r'^\*\*Líneas? \d+',source,re.M):
   raise ValueError(f'Explicaciones de código sin separar en M08_{typ}.md')
  explanations=len(re.findall(r'^- \*\*Líneas? \d+',source,re.M))
  assert explanations > 0, f'Sin explicaciones de código: {typ}'
  verified_lines=verify_explanation_lines(source)
  assert verified_lines==explanations, f'Explicaciones sin verificación física: {verified_lines}/{explanations}'
  if typ=='TEORIA':
   assert len(re.findall(r'^### Bloque \d+ —',source,re.M))==40
   assert all(f'# Punto 8.{i}' in source for i in range(1,5))
   assert source.count('#### Ampliación didáctica aplicada a AceriaApp')==40
   sections=re.split(r'^# Punto 8\.[1-4] —',source,flags=re.M)[1:]
   assert len(sections)==4
   for point,section in enumerate(sections,1):
    assert re.findall(r'^### Bloque (\d+) —',section,re.M)==[str(n) for n in range(1,11)], f'Bloques fuera de orden en 8.{point}'
    assert section.count('#### Ampliación didáctica aplicada a AceriaApp')==10, f'Ampliaciones incompletas en 8.{point}'
    assert len(re.findall(r'!\[[^\]]+\]\(IMAGENES/8-'+str(point)+r'-[^)]+\.svg\)',section))==3, f'Figuras incompletas en 8.{point}'
  else:
   steps=re.findall(r'^### PASO (8\.[1-4]\.\d+) —',source,re.M)
   assert steps == [f'8.{i}.{j}' for i in range(1,5) for j in range(1,25)]
   assert source.count('**Procedimiento guiado.**')==96
   assert len(re.findall(r'^#{2,3} (?:RETO 8\.[1-4] —|Reto de ampliación \(optativo\))',source,re.M))==4, 'Deben existir cuatro retos con solución'
  if re.search(r'^## Errores\s+comunes\s+del\s+ejercicio\s+completo\s*$',source,re.I|re.M):
   raise ValueError(f'La seccion global de errores no debe aparecer en M08_{typ}.md')
  html=tohtml(source)
  allowed={'h1','h2','h3','h4','h5','h6','p','pre','code','strong','em','ul','ol','li','blockquote','hr','a','img','table','thead','tbody','tr','th','td','del','br','div'}
  invalid=sorted({tag.name for tag in BeautifulSoup(html,'html.parser').find_all() if tag.name not in allowed})
  if invalid:raise ValueError(f'HTML inesperado en {typ}; protege los tipos genéricos con comillas de código: {invalid}')
  soup=BeautifulSoup(html,'html.parser')
  if typ=='PRACTICAS':
   for table in soup.find_all('table'):
    if len(table.find_all('th'))==7:
     table['class']=table.get('class',[])+['inventory']
  # A long listing must flow from the available space instead of moving in full
  # to the next page and then splitting there anyway. Short examples stay united.
  for listing in soup.find_all('pre'):
   estimated_lines=sum(max(1,(len(line.expandtabs(4))+101)//102)
                       for line in listing.get_text().splitlines())
   if estimated_lines>65:
    listing['class']=listing.get('class',[])+['long-code']
  for example in soup.select('pre > code.language-markdown'):
   inner=BeautifulSoup(tohtml(example.get_text()),'html.parser')
   invalid=sorted({tag.name for tag in inner.find_all() if tag.name not in allowed})
   if invalid:raise ValueError(f'HTML inesperado en un documento Markdown del laboratorio: {invalid}')
  for heading in list(soup.find_all('h1')):
   if heading.get_text().startswith('Punto '):
    members=[heading]
    sibling=heading.find_next_sibling()
    while sibling is not None and sibling.name not in ('hr','h1','h2','h3'):
     members.append(sibling)
     sibling=sibling.find_next_sibling()
    group=soup.new_tag('div',attrs={'class':'point-intro'})
    heading.insert_before(group)
    for member in members:group.append(member.extract())
  for heading in soup.find_all('h2'):
   if typ=='PRACTICAS' and heading.get_text()=='Cierre del curso':
    closing=heading.find_next_sibling('p')
    if closing is not None:
     section=soup.new_tag('div',attrs={'class':'point-intro'})
     heading.insert_before(section)
     section.append(heading.extract());section.append(closing.extract())
   if heading.get_text() in ('Documentación técnica de consulta','Bibliografía oficial y lecturas de ampliación'):
    listing=heading.find_next_sibling('ul')
    if listing is not None:
     section=soup.new_tag('section',attrs={'class':'references'})
     heading.insert_before(section)
     section.append(heading.extract());section.append(listing.extract())
  for picture in list(soup.find_all('img')):
   paragraph=picture.parent
   caption=paragraph.find_next_sibling('p') if paragraph.name=='p' else None
   if caption is not None and caption.get_text().startswith(('Interpretación del gráfico:','Interpretación del mapa:')):
    group=soup.new_tag('div',attrs={'class':'illustration'})
    paragraph.insert_before(group)
    group.append(paragraph.extract());group.append(caption.extract())
  html=str(soup)
  separated=len(re.findall(r'<li>\s*(?:<p>)?\s*<strong>Líneas? \d+',html))
  if separated!=explanations:
   raise ValueError(f'Explicaciones unidas al convertir {typ}: {separated}/{explanations}')
  figures=BeautifulSoup(html,'html.parser').find_all('img')
  if typ=='TEORIA':
   assert len(figures)==12 and len({im.get('src') for im in figures})==12, 'Deben aparecer los 12 diagramas distintos'
  for image in figures:
   image_path=(doc.parent/image.get('src','')).resolve()
   if not image_path.is_file():raise ValueError(f'Imagen inexistente: {image_path}')
   if image_path.suffix=='.svg' and not image_path.with_suffix('.png').is_file():
    raise ValueError(f'SVG sin PNG correspondiente: {image_path}')
  pdf=doc.with_suffix('.pdf')
  HTML(string="<html lang='es'><meta charset='utf-8'><body>"+html+'</body></html>',
       base_url=str(doc.parent.resolve())).write_pdf(str(pdf),stylesheets=[CSS(string=CSS_TEXT)])
  document=fitz.open(pdf)
  minpages=20 if typ=='TEORIA' else 40
  if len(document)<minpages:raise ValueError(f'PDF corto {typ}: {len(document)} páginas')
  text='\n'.join(page.get_text() for page in document)
  if len(re.findall(r'Líneas? \d+(?:-\d+)?:',text))!=explanations:
   raise ValueError(f'Explicaciones omitidas al generar el PDF {typ}')
  for i in range(1,5):
   if f'Punto 8.{i}' not in text:raise ValueError(f'Sin punto 8.{i} en {typ}')
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
  coverage=verify_text_coverage(html,document)
  reports.append(dict(documento=typ,paginas=len(document),bytes=pdf.stat().st_size,
                      palabras=len(source.split()),pdf=str(pdf.relative_to(ROOT)),
                      explicaciones_separadas=explanations,
                      citas_de_linea_comprobadas=verified_lines,
                      ampliaciones=40 if typ=='TEORIA' else 0,
                      figuras=len(figures),
                      markdown_sha256=hashlib.sha256(source.encode()).hexdigest(),
                      pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
                      **coverage,
                      paginas_blancas=blank,desbordamientos=bounds))
  print(json.dumps(reports[-1],ensure_ascii=False),flush=True)
 report_path=M08/'REPORTE_PDF_M08.json'
 if args.solo and report_path.exists():
  previous=json.loads(report_path.read_text(encoding='utf-8'))
  reports=[r for r in previous if r['documento']!=args.solo]+reports
 reports.sort(key=lambda r: 0 if r['documento']=='TEORIA' else 1)
 report_path.write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
