#!/usr/bin/env python3
"""Genera las prácticas de M02 con la base tipográfica utilizada en M01."""
from pathlib import Path
import json
import re
import markdown
from weasyprint import HTML, CSS
import fitz

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "M02_APIS_REST_ASPNET_CORE/PRACTICAS/M02_PRACTICAS.md"
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
    steps = re.findall(r"^### PASO (2\.[1-4]\.\d+) —", source, flags=re.M)
    expected = [f"2.{p}.{n}" for p in range(1, 5) for n in range(1, 25)]
    assert steps == expected, f"Pasos perdidos, duplicados o desordenados: {len(steps)}"
    assert "## Cómo construir las cuatro etapas sin duplicar código" in source
    # Los bloques C# no pueden anunciar como "INICIO PASO" otro ejercicio.
    candidates = list(re.finditer(r"^### PASO (2\.[1-4]\.\d+) —", source, re.M))
    for index, match in enumerate(candidates):
        body = source[match.end():candidates[index+1].start() if index+1 < len(candidates) else len(source)]
        for block in re.finditer(r"\`\`\`csharp\n([\s\S]*?)\n\`\`\`", body):
            for marker in re.findall(r"// INICIO PASO (2\.[1-4]\.\d+)", block.group(1)):
                assert marker == match.group(1), f"Marcador {marker} en paso {match.group(1)}"

    assert source.count("**Procedimiento guiado.**") == 96
    assert source.count("**Verificación concreta.**") == 96
    assert "**Acción.**" not in source
    matches=list(re.finditer(r"\*\*Procedimiento guiado\.\*\*\n\n((?:[1-9]\. [^\n]+\n){4,})",source))
    assert len(matches) == 96, len(matches)
    for match in matches:
        assert len(re.findall(r"^[1-9]\. ",match.group(1),flags=re.M)) == 4
    assert all(f"## Punto 2.{p} —" in source for p in range(1, 5))
    page_html = markdown.markdown(source,
                                  extensions=["extra", "sane_lists", "toc"],
                                  output_format="html5")
    html = "<html lang='es'><meta charset='utf-8'><body>" + page_html + "</body></html>"
    HTML(string=html, base_url=str(MD.parent)).write_pdf(str(PDF),
                                                  stylesheets=[CSS(string=CSS_TEXT)])
    doc = fitz.open(str(PDF))
    if len(doc) < 30:
        raise RuntimeError("El PDF parece incompleto")
    fulltext = "\n".join(pg.get_text() for pg in doc)
    for p in range(1,5):
        if f"Punto 2.{p}" not in fulltext:
            raise RuntimeError(f"Falta punto 2.{p} en PDF")
    bounds = []
    blank = []
    for i, pg in enumerate(doc):
        if len(pg.get_text().strip()) < 12:
            blank.append(i+1)
        for w in pg.get_text("words"):
            x0,y0,x1,y1 = w[:4]
            if x0 < -1 or y0 < -1 or x1 > pg.rect.width+1 or y1 > pg.rect.height+1:
                bounds.append((i+1,w[4]))
                if len(bounds) > 15: break
        for img in pg.get_images(full=True):
            for rec in pg.get_image_rects(img[0]):
                if rec.x0 < -1 or rec.y0 < -1 or rec.x1 > pg.rect.width+1 or rec.y1 > pg.rect.height+1:
                    bounds.append((i+1,"IMAGEN"))
        if len(bounds)>15: break
    if blank or bounds:
        raise RuntimeError(f"PDF incompleto: paginas vacias={blank} elementos fuera A4={bounds}")
    print(json.dumps(dict(pdf=str(PDF.relative_to(ROOT)),pages=len(doc),
                          bytes=PDF.stat().st_size,md_words=len(source.split()),
                          steps=len(steps),blank_pages=blank,out_of_page=bounds),
                     ensure_ascii=False))

if __name__ == "__main__":
    main()
