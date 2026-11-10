#!/usr/bin/env python3
"""Genera solamente M01_PRACTICAS.pdf desde M01_PRACTICAS.md; tipografia comun al curso."""
from pathlib import Path
import json
import re
import markdown
from weasyprint import HTML, CSS
import fitz

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "M01_INTRODUCCION_MICROSERVICIOS/PRACTICAS/M01_PRACTICAS.md"
PDF = MD.with_suffix(".pdf")

# Misma escala tipográfica, márgenes y componentes base de generar_pdf_m01.py.
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

def main():
    source = MD.read_text(encoding="utf-8")
    steps = 0
    for part in range(1, 6):
        begin = source.index(f"# Punto 1.{part} —")
        end = source.index(f"# Punto 1.{part+1} —", begin) if part < 5 else len(source)
        segment = source[begin:end]
        matches = list(re.finditer(r"^### Paso (\d+) — ([^\n]+)$", segment, re.M))
        numbers = [int(m.group(1)) for m in matches]
        if numbers != list(range(1,25)):
            raise RuntimeError(f"Punto 1.{part}: pasos incompletos: {numbers}")
        for i,m in enumerate(matches):
            body = segment[m.end():matches[i+1].start() if i+1 < len(matches) else len(segment)]
            actions = [int(n) for n in re.findall(r"^\*\*Acción (\d+):\*\* [^\n]+", body, re.M)]
            if not (3 <= len(actions) <= 8 and actions == list(range(1,len(actions)+1))):
                raise RuntimeError(f"Acciones mal ordenadas en {part}.{m.group(1)}: {actions}")
            if not all(t in body for t in ["**Por qué se hace:**","**Errores comunes:**","**Verificación:**"]):
                raise RuntimeError(f"Falta justificación o comprobación en {part}.{m.group(1)}")
        steps += len(matches)
    if steps != 120:
        raise RuntimeError(f"Se requieren 120 pasos, encontrados {steps}")
    html_body = markdown.markdown(source,extensions=["extra","sane_lists","toc"],output_format="html5")
    HTML(string="<html lang='es'><meta charset='utf-8'><body>"+html_body+"</body></html>",
         base_url=str(MD.parent)).write_pdf(str(PDF),stylesheets=[CSS(string=CSS_TEXT)])
    doc=fitz.open(str(PDF))
    if len(doc) < 50: raise RuntimeError(f"PDF demasiado corto: {len(doc)} páginas")
    alltext="\n".join(p.get_text() for p in doc)
    for part in range(1,6):
        if f"Punto 1.{part}" not in alltext: raise RuntimeError(f"Falta Punto 1.{part}")
    bounds=[];blank=[]
    for i,p in enumerate(doc,1):
        if len(p.get_text().strip()) < 12: blank.append(i)
        for w in p.get_text("words"):
            x0,y0,x1,y1=w[:4]
            if x0 < -1 or y0 < -1 or x1 > p.rect.width+1 or y1 > p.rect.height+1:
                bounds.append((i,w[4]))
                if len(bounds)>15:break
        if len(bounds)>15:break
    if bounds or blank: raise RuntimeError(f"PDF incorrecto: paginas vacias {blank}, fuera de A4 {bounds}")
    print(json.dumps({"pdf":str(PDF.relative_to(ROOT)),"pages":len(doc),
                      "words":len(source.split()),"steps":steps,
                      "bytes":PDF.stat().st_size,"blank_pages":blank,"out_of_page":bounds},
                     ensure_ascii=False))
if __name__ == "__main__":
    main()
