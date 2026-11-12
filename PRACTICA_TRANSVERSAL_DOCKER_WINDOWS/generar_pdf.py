#!/usr/bin/env python3
"""Genera y audita el PDF de la práctica transversal Docker en formato A4."""
from pathlib import Path
from weasyprint import HTML, CSS
import markdown, fitz, hashlib, json, re
BASE = Path(__file__).resolve().parent
MD = BASE / 'PRACTICAS_DOCKER_WINDOWS.md'
PDF = MD.with_suffix('.pdf')
CSS_TEXT = """
@page {size:A4; margin:17mm 17mm 20mm 17mm; @bottom-center{content:counter(page); color:#667085; font-size:8pt;}}
html {font-family:"DejaVu Sans",sans-serif; color:#172331; font-size:9.3pt;}
body {line-height:1.42;}
h1,h2,h3,h4 {color:#153553;line-height:1.25;break-after:avoid;}
h1{font-size:20pt;} h2{font-size:14.5pt;margin-top:15pt;} h3{font-size:11pt;margin-top:12pt;}
p{margin:5pt 0 8pt;orphans:2;widows:2;} ul,ol{padding-left:16pt;}
li{margin:0 0 4pt;}
code,pre{font-family:"DejaVu Sans Mono",monospace;overflow-wrap:anywhere;}
code{font-size:.9em;}
pre{white-space:pre-wrap;word-break:break-word;font-size:7.4pt;line-height:1.35;
background:#f3f6f9;border-left:3pt solid #91a9bc;padding:7pt 8pt;margin:8pt 0 11pt;}
table{width:100%;table-layout:fixed;border-collapse:collapse;font-size:7.5pt;line-height:1.26;}
thead{display:table-header-group;} th{background:#eaf1f7;}
td,th{border:.55pt solid #aebfce;padding:4.5pt 5pt;vertical-align:top;word-break:break-word;overflow-wrap:anywhere;}
tr{break-inside:avoid;}
hr{border:0;border-top:1pt solid #cbd5df;margin:14pt 0;}
"""
text=MD.read_text(encoding='utf-8')
assert all(x in text for x in ('Laboratorio A','Laboratorio B','Laboratorio C','SQL Server','RabbitMQ'))
steps=re.findall(r'^### Paso (D\.\d+) —',text,flags=re.M)
assert steps==[f'D.{i}' for i in range(1,17)], f'Pasos Docker faltantes o duplicados: {steps}'
body=markdown.markdown(text,extensions=['extra','sane_lists','toc'],output_format='html5')
HTML(string="<html lang='es'><meta charset='utf-8'><body>"+body+"</body></html>",
     base_url=str(BASE)).write_pdf(str(PDF),stylesheets=[CSS(string=CSS_TEXT)])
pdf=fitz.open(PDF)
blank=[];overs=[]
fulltext='\n'.join(page.get_text() for page in pdf)
for step in steps:
    assert f'Paso {step}' in fulltext, f'El PDF ha omitido el {step}'
for i,page in enumerate(pdf,1):
    if len(page.get_text().strip())<12:blank.append(i)
    for w in page.get_text('words'):
        x0,y0,x1,y1=w[:4]
        if x0<-1 or y0<-1 or x1>page.rect.width+1 or y1>page.rect.height+1:
            overs.append((i,w[4]))
            if len(overs)>20:break
assert 5<=len(pdf)<=50 and not blank and not overs, (len(pdf),blank,overs)
report={'resultado':'PASS','pdf':PDF.name,'paginas':len(pdf),
    'palabras':len(text.split()),'pasos_guiados':len(steps),'sha_md':hashlib.sha256(text.encode()).hexdigest(),
    'sha_pdf':hashlib.sha256(PDF.read_bytes()).hexdigest(),
    'paginas_blancas':blank,'desbordamientos':overs}
(BASE/'REPORTE_PDF_DOCKER.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False),flush=True)
