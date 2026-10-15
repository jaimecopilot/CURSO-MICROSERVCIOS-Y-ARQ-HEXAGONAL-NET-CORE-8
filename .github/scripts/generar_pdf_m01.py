#!/usr/bin/env python3
"""Vista previa de PDFs docentes M01 desde los Markdown, sin modificar el repositorio."""
from pathlib import Path
import json
import re
import sys
import markdown
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
import fitz

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "M01_INTRODUCCION_MICROSERVICIOS"
CSS_TEXT = r"""
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
OUT = ROOT / "_revision_m01_pdf"
OUT.mkdir(exist_ok=True)
reports = []
for typ in ("TEORIA", "PRACTICAS"):
    md_file = BASE / typ / ("M01_" + typ + ".md")
    src = md_file.read_text(encoding="utf-8")
    page_html = markdown.markdown(src, extensions=["extra", "sane_lists", "toc"],
                                  output_format="html5")
    soup = BeautifulSoup(page_html, "html.parser")
    if typ == "TEORIA":
        assert len([x for x in soup.find_all("h3") if x.text.startswith("Bloque ")]) == 50
        assert len(soup.find_all("img")) == 5
    else:
        steps = [x for x in soup.find_all("h3") if re.match(r"^Paso \d+ —", x.get_text(" ",strip=True))]
        assert len(steps) == 120, len(steps)
        titles=[x for x in soup.find_all("h2") if x.text == "Errores comunes del ejercicio completo"]
        assert len(titles) == 5, len(titles)
        for title in titles:
            table = title.find_next_sibling("table")
            assert table is not None and len(table.find_all("tr")) == 11, str(title)
    target=OUT / ("M01_" + typ + ".pdf")
    HTML(string="<html lang='es'><meta charset='utf-8'><body>" + page_html + "</body></html>",
         base_url=str(md_file.parent)).write_pdf(str(target),stylesheets=[CSS(string=CSS_TEXT)])
    doc=fitz.open(str(target))
    blank=[];bad_bounds=[]
    for i,page in enumerate(doc):
        words=page.get_text("words")
        if len(words)<2: blank.append(i+1)
        for word in words:
            x0,y0,x1,y1=word[:4]
            if x0 < -1 or y0 < -1 or x1 > page.rect.width+1 or y1 > page.rect.height+1:
                bad_bounds.append({"page":i+1,"word":word[4],"bounds":[x0,y0,x1,y1]})
                if len(bad_bounds)>15:break
    fulltext="\n".join(page.get_text() for page in doc)
    expected=["Punto 1.1","Punto 1.2","Punto 1.3","Punto 1.4","Punto 1.5"]
    assert all(t in fulltext for t in expected), "Falta un punto en el PDF"
    assert len(fulltext)>30000, len(fulltext)
    report={"document":typ,"pages":len(doc),"pdf_bytes":target.stat().st_size,
            "extractable_chars":len(fulltext),"blank_pages":blank,
            "out_of_page_words":bad_bounds,"source_bytes":md_file.stat().st_size,
            "html_tables":len(soup.find_all("table")),"html_images":len(soup.find_all("img"))}
    print(json.dumps(report,ensure_ascii=False));reports.append(report)
    if blank or bad_bounds: raise RuntimeError("PDF no supera comprobación geométrica")
(OUT / "reporte_pdf_m01.json").write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding="utf-8")
