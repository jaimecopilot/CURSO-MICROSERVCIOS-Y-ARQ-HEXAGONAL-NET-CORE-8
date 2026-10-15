#!/usr/bin/env python3
"""Reproduce Markdown M02 como PDF, con portada individual y autor en todas las páginas."""
from pathlib import Path
import os, json, fitz, mistune, weasyprint
ROOT=Path("M02_APIS_REST_ASPNET_CORE")
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
COURSE="ARQUITECTURA HEXAGONAL Y MICROSERVICIOS AVANZADOS CON .NET 8"
MOD="MÓDULO 02 · DESARROLLO DE APIs REST CON ASP.NET CORE"
AUTHOR="AUTOR: JAIME GALLO"
CSS="""
@page { size: A4; margin: 25mm 17mm 22mm 17mm; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 9.15pt; line-height: 1.44; color:#1b2b36; }
h1 { color:#123d58; font-size:20pt; margin-top:8mm; }
h2 { font-size:14pt; color:#174e6c; margin-top:9mm; padding: 2mm 0; border-bottom: 1px solid #aac5d6; break-after:avoid; }
h3 { font-size:11.5pt; color:#255b78; margin-top:5mm; break-after:avoid; }
p { margin-top:2.5mm; margin-bottom:2.8mm; text-align:justify; orphans:3; widows:3; }
ul, ol { padding-left:6mm; margin-top:2mm; }
li { margin-bottom:1.4mm; }
table { width:100%; border-collapse:collapse; font-size:8.2pt; margin:4mm 0 5mm; break-inside:avoid; }
th,td { padding:1.9mm 2mm; border:0.6px solid #b7cbd7; text-align:left; vertical-align:top; }
th { background:#e5eff4; }
code { font-family:'DejaVu Sans Mono',monospace; font-size:7.65pt; }
pre { white-space:pre-wrap; overflow-wrap:anywhere; background:#f2f5f7; border-left:3px solid #b77e31; padding:3mm; font-size:7.7pt; break-inside:avoid; }
pre code { font-size:7.7pt; }
img { max-width:100%; height:auto; }
blockquote { padding-left:5mm; border-left:2px solid #d7bd8d; color:#385568; }
"""
def font_setup(page):
    if Path(FONT).is_file():page.insert_font(fontname="DejaVu",fontfile=FONT);return "DejaVu"
    return "helv"
def cover(page,kind,pages):
    r=page.rect
    page.draw_rect(r,color=(.08,.18,.27),fill=(.08,.18,.27))
    page.draw_rect(fitz.Rect(45,96,r.width-45,104),color=None,fill=(.78,.52,.22))
    face=font_setup(page)
    for content,y,size,color in [
        ("CURSO · .NET 8",160,14,(.85,.68,.44)),
        ("ARQUITECTURA HEXAGONAL",215,24,(1,1,1)),
        ("Y MICROSERVICIOS AVANZADOS",250,17,(1,1,1)),
        ("MÓDULO 02",356,23,(.85,.68,.44)),
        ("DESARROLLO DE APIs REST",396,21,(1,1,1)),
        ("CON ASP.NET CORE",427,20,(1,1,1)),
        (kind,495,21,(.85,.68,.44)),
        (AUTHOR,695,12,(1,1,1))
    ]:page.insert_text((52,y),content,fontname=face,fontsize=size,color=color)
    page.insert_text((52,744),"ACERIAAPP · MATERIAL FORMATIVO",fontname=face,fontsize=9,color=(.77,.83,.86))
def stamp(page,kind,num,total):
    f=font_setup(page)
    w=page.rect.width
    page.draw_line((38,49),(w-38,49),color=(.77,.82,.84),width=.5)
    page.insert_text((39,19),"CURSO · "+COURSE,fontname=f,fontsize=6.25,color=(.10,.30,.43))
    page.insert_text((39,31),MOD+" · "+kind,fontname=f,fontsize=6.15,color=(.10,.30,.43))
    page.insert_text((w-175,44),AUTHOR,fontname=f,fontsize=7.2,color=(.23,.32,.38))
    page.draw_line((39,page.rect.height-43),(w-39,page.rect.height-43),color=(.77,.82,.84),width=.5)
    page.insert_text((39,page.rect.height-29),AUTHOR,fontname=f,fontsize=7,color=(.18,.34,.45))
    page.insert_text((w-115,page.rect.height-29),f"PÁGINA {num} / {total}",fontname=f,fontsize=7,color=(.18,.34,.45))
def build(kind):
    path=ROOT/kind/("M02_"+kind+".md")
    markdown=path.read_text(encoding="utf-8")
    md=mistune.create_markdown(plugins=["table","strikethrough"])
    body=md(markdown)
    html='<html lang="es"><head><meta charset="utf-8"><style>'+CSS+'</style></head><body>'+body+'</body></html>'
    raw=ROOT/kind/("_M02_"+kind+"_sin_portada.pdf")
    weasyprint.HTML(string=html,base_url=str(path.parent.resolve())).write_pdf(str(raw))
    origin=fitz.open(raw)
    result=fitz.open()
    cover(result.new_page(width=fitz.paper_rect("a4").width,height=fitz.paper_rect("a4").height), "TEORÍA" if kind=="TEORIA" else "PRÁCTICAS",len(origin))
    result.insert_pdf(origin)
    total=len(result)
    for n,page in enumerate(result,1):
        stamp(page,"TEORÍA" if kind=="TEORIA" else "PRÁCTICAS",n,total)
    final=ROOT/kind/("M02_"+kind+".pdf")
    result.save(final,garbage=4,deflate=True)
    result.close();origin.close();raw.unlink()
    check=fitz.open(final)
    for n,p in enumerate(check):
        text=p.get_text()
        assert "JAIME GALLO" in text,(kind,n,"autor")
        assert "MÓDULO 02" in text,(kind,n,"modulo")
        assert "ARQUITECTURA HEXAGONAL" in text,(kind,n,"curso")
    print(json.dumps({"document":kind,"paginas_con_portada":len(check),"tamano_bytes":final.stat().st_size,"paginacion_y_autoria":"PASS"},ensure_ascii=False))
    check.close()
if __name__=="__main__":
    build("TEORIA");build("PRACTICAS")
