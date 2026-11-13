#!/usr/bin/env python3
from pathlib import Path
import re
import json
import fitz
import markdown
from weasyprint import CSS, HTML

base=Path("M01_INTRODUCCION_MICROSERVICIOS/TEORIA")
md=base / "M01_TEORIA.md"
pdf=base / "M01_TEORIA.pdf"
data=md.read_text(encoding="utf-8")
chapters=re.findall(r"^# Punto 1\.([1-5]) —",data,re.M)
assert chapters==list("12345"),chapters
assert len(re.findall(r"^\x60{3}",data,re.M))==100
figures=re.findall(r"!\[[^\]]*\]\((figuras/[^)]+)\)",data)
assert len(figures)==5 and all((base/img).is_file() for img in figures)
assert len(re.findall(r"^\|",data,re.M))==84
assert "Lectura guiada del ejemplo" not in data
assert "#### Profundización:" not in data
assert len(data.split())>30000
css="""
@page{size:A4;margin:18mm 18mm 20mm 18mm;@bottom-right{content:counter(page);font-size:8pt;color:#6b7280}}
html{font-family:"DejaVu Sans",sans-serif;color:#1e293b;font-size:9.3pt}
body{line-height:1.45}h1,h2,h3{color:#173b57;break-after:avoid}
h1{font-size:19pt;break-before:page}h1:first-of-type{break-before:auto}
h2{font-size:14pt;margin-top:14pt}h3{font-size:11pt;margin-top:11pt}
p{margin:6pt 0 9pt;orphans:2;widows:2}
code,pre{font-family:"DejaVu Sans Mono",monospace;overflow-wrap:anywhere}
pre{font-size:7pt;white-space:pre-wrap;word-break:break-word;background:#f2f5f8;padding:7pt}
img{max-width:100%;max-height:160mm;height:auto;display:block;margin:10pt auto}
table{width:100%;table-layout:fixed;border-collapse:collapse;font-size:7.5pt}
th,td{border:.5pt solid #aebfce;padding:5pt;overflow-wrap:anywhere;word-break:break-word}
th{background:#eaf1f7}tr{break-inside:avoid}
"""
body=markdown.markdown(data,extensions=["extra","sane_lists","toc"],output_format="html5")
HTML(string="<html lang='es'><meta charset='utf-8'><body>"+body+"</body></html>",base_url=str(base.resolve())).write_pdf(str(pdf),stylesheets=[CSS(string=css)])
doc=fitz.open(pdf)
n=len(doc)
images=sum(len(p.get_images(full=True)) for p in doc)
blanks=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<14 and not p.get_images(full=True)]
overflows=[]
for i,p in enumerate(doc):
    for w in p.get_text("words"):
        x0,y0,x1,y1=w[:4]
        if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:overflows.append((i+1,w[4]))
result={"resultado":"PASS" if 40<=n<=180 and images>=5 and not blanks and not overflows else "FAIL",
    "paginas":n,"imagenes":images,"palabras":len(data.split()),
    "puntos":5,"ejemplos":50,"graficos":len(figures),
    "paginas_blancas":blanks,"desbordamientos":overflows[:20]}
print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
Path("/tmp/m01_teoria_editorial_auditoria.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
assert result["resultado"]=="PASS",result
