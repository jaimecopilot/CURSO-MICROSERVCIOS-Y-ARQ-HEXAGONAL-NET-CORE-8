#!/usr/bin/env python3
"""Incorpora portada y elementos editoriales a los PDF M01 generados desde Markdown.

No modifica ni elimina ninguna página del material docente: añade una portada
y superpone cabecera y pie en el espacio libre de las páginas originales.
"""
from pathlib import Path
import json
import math
import fitz

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "_revision_m01_pdf"
TITLE = "CURSO DE ARQUITECTURA HEXAGONAL Y MICROSERVICIOS AVANZADOS CON .NET 8"
MODULE = "MÓDULO 01 · INTRODUCCIÓN A LOS MICROSERVICIOS"
AUTHOR = "AUTOR: JAIME GALLO"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
NAVY = (0.070, 0.145, 0.242)
CYAN = (0.29, 0.83, 0.79)
MUTED = (0.39, 0.48, 0.58)
LIGHT = (0.93, 0.95, 0.97)
WHITE = (1, 1, 1)

def add_font(page):
    page.insert_font(fontname="DVREG", fontfile=REGULAR)
    page.insert_font(fontname="DVBOLD", fontfile=BOLD)

def hexagon(page, x, y, radius, color, width=1.0):
    pts = [fitz.Point(x + radius * math.cos(math.pi / 3 * i),
                      y + radius * math.sin(math.pi / 3 * i)) for i in range(6)]
    for i in range(6):
        page.draw_line(pts[i], pts[(i+1) % 6], color=color, width=width)

def cover(page, category):
    w,h = page.rect.width, page.rect.height
    page.draw_rect(page.rect, color=NAVY, fill=NAVY)
    page.draw_rect(fitz.Rect(0, 0, 13, h), color=CYAN, fill=CYAN)
    add_font(page)
    page.insert_text((54, 82), "ACERIAAPP  /  FORMACIÓN .NET 8",
                     fontname="DVBOLD", fontsize=10, color=CYAN)
    page.draw_line((54, 105),(w-54, 105),color=(.29,.44,.53),width=1.0)
    page.insert_text((54, 150), "CURSO DE ARQUITECTURA HEXAGONAL",
                     fontname="DVREG", fontsize=11.8, color=WHITE)
    page.insert_text((54, 172), "Y MICROSERVICIOS AVANZADOS CON .NET 8",
                     fontname="DVREG", fontsize=11.8, color=WHITE)
    page.insert_text((54, 260), "MÓDULO 01", fontname="DVBOLD", fontsize=15, color=CYAN)
    page.insert_text((54, 316), "INTRODUCCIÓN A LOS",
                     fontname="DVBOLD", fontsize=26, color=WHITE)
    page.insert_text((54, 358), "MICROSERVICIOS",
                     fontname="DVBOLD", fontsize=28, color=WHITE)
    page.draw_rect(fitz.Rect(54, 398, 265, 443), color=CYAN, fill=CYAN)
    page.insert_text((69, 428), category.upper(),
                     fontname="DVBOLD", fontsize=18, color=NAVY)
    for x,y,size in [(453,514,46),(506,563,32),(428,593,23),(520,479,18)]:
        hexagon(page, x,y,size, (.22,.47,.53),1.6)
    page.draw_line((54, 742), (w-54,742),color=(.27,.42,.51),width=.9)
    page.insert_text((54, 779),AUTHOR,fontname="DVBOLD",fontsize=11,color=WHITE)
    page.insert_text((54, 807),"ARQUITECTURA  ·  DISEÑO  ·  IMPLEMENTACIÓN",
                     fontname="DVREG",fontsize=8,color=(.67,.78,.82))

def stamp(page, category):
    add_font(page)
    w,h=page.rect.width,page.rect.height
    # El contenido de Markdown empieza a ~49 pt; el encabezado queda a 16–34 pt.
    page.insert_text((49, 16), TITLE + " · ACERIAAPP",
                     fontname="DVBOLD",fontsize=6.8,color=NAVY)
    page.insert_text((49, 30),MODULE,
                     fontname="DVREG",fontsize=7.2,color=MUTED)
    label = category.upper()
    label_width = fitz.get_text_length(label,fontsize=9,fontname="DVBOLD",
                                       fontfile=BOLD)
    page.insert_text((w - 48 - label_width, 30),label,
                     fontname="DVBOLD",fontsize=9,color=NAVY)
    page.draw_line((49, 37),(w-49,37),color=(.76,.81,.85),width=.6)
    # El contador del PDF original queda centrado a 810–820 pt.
    # La línea del autor usa la esquina inferior izquierda sin taparlo.
    page.insert_text((49,h-12),AUTHOR,
                     fontname="DVBOLD",fontsize=7.2,color=MUTED)

def process(category):
    src=OUT / ("M01_"+category+".pdf")
    if not src.is_file():
        raise FileNotFoundError(src)
    original=fitz.open(src)
    original_pages=len(original)
    result=fitz.open()
    first=result.new_page(width=fitz.paper_rect("a4").width,
                          height=fitz.paper_rect("a4").height)
    cover(first,"TEORÍA" if category=="TEORIA" else "PRÁCTICAS")
    result.insert_pdf(original)
    label="TEORÍA" if category=="TEORIA" else "PRÁCTICAS"
    for page in list(result)[1:]:
        stamp(page,label)
    assert len(result)==original_pages+1
    for idx,page in enumerate(result):
        content=page.get_text()
        assert "JAIME GALLO" in content, f"{category}, página {idx+1}: sin autor"
        assert "MÓDULO 01" in content, f"{category}, página {idx+1}: sin módulo"
        assert "ARQUITECTURA HEXAGONAL" in content, f"{category}, página {idx+1}: sin curso"
        assert label in content, f"{category}, página {idx+1}: sin tipo"
        if idx>0:
            assert len(content)>120, f"{category}, página {idx+1}: contenido vacío"
    output=OUT / ("M01_"+category+"_CON_PORTADA.pdf")
    result.save(output,garbage=3,deflate=True)
    summary={"document":category,"source_pages":original_pages,
             "total_pages":len(result),"all_pages_branded":True,
             "page_1_cover":True,"bytes":output.stat().st_size}
    original.close()
    result.close()
    return summary

if __name__=="__main__":
    reports=[process(t) for t in ("TEORIA","PRACTICAS")]
    (OUT/"reporte_portadas_m01.json").write_text(
        json.dumps(reports,ensure_ascii=False,indent=2),encoding="utf-8")
    for entry in reports: print(json.dumps(entry,ensure_ascii=False))
