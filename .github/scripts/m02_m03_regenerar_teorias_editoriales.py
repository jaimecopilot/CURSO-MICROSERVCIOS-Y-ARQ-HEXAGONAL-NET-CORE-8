#!/usr/bin/env python3
"""Genera y certifica PDF de M02 y M03 desde version-corregida sin tocar prácticas."""
from pathlib import Path
import hashlib
import json
import re
import sys
import fitz
import markdown
from weasyprint import HTML, CSS

ROOT=Path.cwd()
BASE=ROOT / "_base_main"
OUT=Path("/tmp/teorias_m02_m03_auditoria.json")
CSS_TEXT="""
@page {size:A4; margin:18mm 18mm 21mm 18mm; @bottom-right{content:counter(page);font-size:8pt;color:#6b7280}}
html {font-family:"DejaVu Sans",sans-serif;color:#172b42;font-size:9.35pt}
body{line-height:1.48}
h1,h2,h3,h4{color:#173b57;line-height:1.27;break-after:avoid}
h1{font-size:19.5pt;margin:17pt 0 11pt}
h2{font-size:14.1pt;margin:16pt 0 10pt;break-before:auto}
h3{font-size:11.2pt;margin:13pt 0 8pt}
h4{font-size:9.8pt;margin:10pt 0 7pt}
p{margin:5pt 0 9pt;orphans:2;widows:2}
ul,ol{padding-left:19pt;margin:7pt 0 10pt} li{margin:4pt 0}
hr{border:0;border-top:.65pt solid #d1dce7;margin:16pt 0}
img{max-width:100%;max-height:165mm;height:auto;display:block;margin:11pt auto}
code,pre{font-family:"DejaVu Sans Mono",monospace;overflow-wrap:anywhere}
code{font-size:.88em}
pre{font-size:7.2pt;line-height:1.38;white-space:pre-wrap;word-break:break-word;
 background:#f1f5f9;border-left:2.5pt solid #94a3b8;padding:7pt 9pt;margin:9pt 0 12pt}
table{width:100%;table-layout:fixed;border-collapse:collapse;font-size:7.4pt;line-height:1.28;margin:10pt 0 13pt}
thead{display:table-header-group}th{background:#eaf0f5}
td,th{border:.5pt solid #aebfca;padding:5pt 5pt;vertical-align:top;word-break:break-word;overflow-wrap:anywhere}
tr{break-inside:avoid}
blockquote{border-left:2pt solid #cbd5e1;padding-left:12pt;margin:12pt 0}
"""
expected={
 "M02":("M02_APIS_REST_ASPNET_CORE",2,33,10,4),
 "M03":("M03_ARQUITECTURA_HEXAGONAL",3,41,14,4),
}
all_results={}
for mod,(folder,n,codecount,imgcount,pointcount) in expected.items():
    old=(BASE/folder/"TEORIA"/(mod+"_TEORIA.md")).read_text(encoding="utf-8")
    path=ROOT/folder/"TEORIA"/(mod+"_TEORIA.md")
    new=path.read_text(encoding="utf-8")
    pdf=path.with_suffix(".pdf")
    def codeblocks(text):
        return re.findall(r"(?m)^\x60{3}[^\n]*\n[\s\S]*?\n\x60{3}",text)
    def imagetags(text):
        return re.findall(r"!\[[^\]]*\]\(([^)]+)\)",text)
    def tablerows(text):
        return [line for line in text.splitlines() if line.startswith("|")]
    original_code=codeblocks(old)
    corrected_code=codeblocks(new)
    assert original_code==corrected_code,f"{mod}: código de la teoría alterado"
    assert len(original_code)==codecount,(mod,len(original_code))
    original_images=imagetags(old)
    corrected_images=imagetags(new)
    assert original_images==corrected_images,f"{mod}: falta una figura"
    assert len(original_images)==imgcount,(mod,len(original_images))
    for image in corrected_images:
        assert (path.parent/image).is_file(),f"{mod}: no existe {image}"
    assert tablerows(old)==tablerows(new),f"{mod}: tablas alteradas"
    points=re.findall(r"(?m)^#{1,2} Punto "+str(n)+r"\.([1-4]) —",new)
    assert points==list("1234"),(mod,points)
    original_titles=re.findall(r"(?m)^### Bloque \d+ — ([^\n]+)",old)
    assert len(original_titles)==40,mod
    for title in original_titles:
        assert re.search(r"(?m)^### "+re.escape(title)+r"$",new),f"{mod}: concepto perdido: {title}"
    assert not re.search(r"(?m)^- \*\*Línea \d+:|^### Bloque \d+|^#### Ampliación didáctica aplicada a AceriaApp",new),f"{mod}: patrón editorial aún presente"
    assert "Qué debe saber explicar el alumno." not in new
    assert "tiene dos consecuencias prácticas" not in new
    assert "se caracteriza por tres propiedades" not in new
    assert len(new.split())>=14000 if mod=="M02" else len(new.split())>=20000
    html=markdown.markdown(new,extensions=["extra","sane_lists","toc"],output_format="html5")
    HTML(string="<html lang='es'><meta charset='utf-8'><body>"+html+"</body></html>",
         base_url=str(path.parent.resolve())).write_pdf(str(pdf),stylesheets=[CSS(string=CSS_TEXT)])
    with fitz.open(pdf) as document:
        total_pages=len(document)
        text="\n".join(p.get_text() for p in document)
        blank_pages=[]
        out_of_bounds=[]
        vector_elements=0
        raster_images=0
        for i,page in enumerate(document,1):
            raster_images+=len(page.get_images(full=True))
            vector_elements+=len(page.get_drawings())
            if len(page.get_text().strip())<16 and not page.get_images(full=True) and not page.get_drawings():
                blank_pages.append(i)
            for w in page.get_text("words"):
                x0,y0,x1,y1=w[:4]
                if x0<-1 or y0<-1 or x1>page.rect.width+1 or y1>page.rect.height+1:
                    out_of_bounds.append((i,w[4]))
        for i in range(1,pointcount+1):
            assert f"Punto {n}.{i}" in text,(mod,i,"punto no impreso")
        assert total_pages>=20 and total_pages<=180,(mod,total_pages)
        assert not blank_pages and not out_of_bounds,(mod,blank_pages,out_of_bounds[:15])
        assert raster_images+vector_elements>=imgcount,(mod,"figuras PDF no detectadas")
        report=dict(resultado="PASS",module=mod,puntos=pointcount,apartados_conceptuales=len(original_titles),
                    ejemplos_codigo=len(corrected_code),graficos_fuente=len(corrected_images),
                    tablas_lineas=len(tablerows(new)),palabras=len(new.split()),
                    paginas=total_pages,imagenes_raster_pdf=raster_images,elementos_vectoriales_pdf=vector_elements,
                    paginas_blancas=blank_pages,desbordamientos=out_of_bounds,
                    sha_md=hashlib.sha256(new.encode()).hexdigest(),
                    sha_pdf=hashlib.sha256(pdf.read_bytes()).hexdigest())
        all_results[mod]=report
        print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
OUT.write_text(json.dumps(all_results,ensure_ascii=False,indent=2),encoding="utf-8")
