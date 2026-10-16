#!/usr/bin/env python3
"""Genera PDF legibles a partir de las vistas Markdown derivadas de fuentes originales."""
from __future__ import annotations
import argparse
import html
import re
from pathlib import Path
import markdown
from weasyprint import HTML
import fitz

STYLE = """
@page {
    size: A4;
    margin: 17mm 17mm 18mm 18mm;
    @bottom-center {
        content: counter(page);
        font-family: 'DejaVu Sans', sans-serif;
        color: #697482;
        font-size: 8pt;
    }
}
html { font-family: 'DejaVu Sans', 'Liberation Sans', sans-serif; }
body { font-size: 9.1pt; line-height: 1.46; color: #24313f; }
h1 { font-size: 17pt; color: #17304b; margin: 0 0 12pt; border-bottom: 2px solid #becfdb; padding-bottom: 9pt; }
h2 { font-size: 13pt; color: #203d58; margin-top: 17pt; border-bottom: 1px solid #d7e2eb; padding-bottom: 3pt; }
h3 { font-size: 10.4pt; color: #234a62; margin-top: 11pt; margin-bottom: 4pt; }
h1, h2, h3, h4 { page-break-after: avoid; break-after: avoid; }
img { display: block; width: 97%; max-width: 100%; height: auto;
      margin: 9pt auto 5pt; page-break-inside: avoid; break-inside: avoid; }
p:has(> img) { margin-top: 8pt; margin-bottom: 3pt; text-align: center; }
p:has(> img) + p { margin-top: 2pt; font-size: 8pt; color: #48697e; text-align: center; }
/* Dejar que el navegador distribuya cada columna según la tabla real.
   Antes las tres primeras sumaban 100%, expulsando una cuarta columna
   fuera del A4. */ 
table { table-layout: fixed; max-width: 100%; }
tr { break-inside: avoid; page-break-inside: avoid; }
p { margin: 5pt 0 6pt; orphans: 3; widows: 3; text-align: justify; }
ul, ol { margin: 4pt 0 6pt 15pt; padding-left: 8pt; }
li { padding-left: 1pt; margin-bottom: 2pt; }
li p { text-align: left; }
strong { color: #1e354a; }
pre, code { font-family: 'DejaVu Sans Mono', monospace; font-size: 7.9pt; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; background: #f4f7f9;
      border: 1px solid #e0e5ea; padding: 7pt; page-break-inside: auto; break-inside: auto; box-decoration-break: clone; }
code { overflow-wrap: anywhere; }
table { border-collapse: collapse; width: 100%; font-size: 8pt; margin: 7pt 0 10pt; }
th, td { border: 1px solid #d5dee5; padding: 4pt 5pt; vertical-align: top; overflow-wrap: anywhere; }
th { background: #edf3f7; color: #243b50; }
thead { display: table-header-group; }
hr { border: none; border-top: 1px solid #cbd6de; margin: 14pt 0; }
"""

def make(src: Path, dst: Path):
    raw=src.read_text(encoding="utf-8")
    body=markdown.markdown(raw,extensions=["extra","fenced_code","tables","sane_lists"])
    h='<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>'+STYLE+'</style></head><body>'+body+'</body></html>'
    HTML(string=h,base_url=str(src.parent.resolve())).write_pdf(str(dst))
    document=fitz.open(str(dst))
    pages=len(document)
    lengths=[len(page.get_text().strip()) for page in document]
    if pages<2 or min(lengths)<12:
        raise RuntimeError(f"PDF incompleto: {dst} ({pages} páginas, mínima longitud {min(lengths)})")
    missing = []
    for marker in ("Punto 2.1","Punto 2.2"):
        if marker not in "".join(page.get_text() for page in document):
            missing.append(marker)
    if missing: raise RuntimeError(f"Faltan encabezados de punto en PDF {dst}: {missing}")
    return dict(pdf=str(dst),pages=pages,bytes=dst.stat().st_size,min_page_chars=min(lengths))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--directorio",type=Path,default=Path("m02_previsualizacion"))
    args=ap.parse_args()
    for path in sorted(args.directorio.glob("*.md")):
        print(make(path,path.with_suffix(".pdf")))

if __name__=="__main__": main()
