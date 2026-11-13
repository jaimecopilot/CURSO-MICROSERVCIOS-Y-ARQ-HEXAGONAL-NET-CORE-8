#!/usr/bin/env python3
"""Audita material publicable PDF de M01-M09 sin modificar archivos finales.

Comprueba la cabecera en todas las páginas, integridad básica de lectura y
renderiza una muestra de 3 páginas por documento para inspección visual humana.
No afirma que una miniatura o un texto extraíble pruebe toda la maquetación.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
import json
import re
import sys

import fitz
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
NAMES = {
    1: "M01_INTRODUCCION_MICROSERVICIOS",
    2: "M02_APIS_REST_ASPNET_CORE",
    3: "M03_ARQUITECTURA_HEXAGONAL",
    4: "M04_PATRONES_ARQUITECTURA",
    5: "M05_DDD_CQRS",
    6: "M06_COMUNICACION_MICROSERVICIOS",
    7: "M07_OBSERVABILIDAD_RESILIENCIA",
    8: "M08_API_GATEWAY",
    9: "M09_DESPLIEGUE_DOCKER",
}
EXPECTED_POINTS = {1: 5, 2: 4, 3: 4, 4: 5, 5: 5, 6: 3, 7: 4, 8: 4, 9: 16}

sys.path.insert(0, str(ROOT / "tools"))
from pdf_running_headers import header_present  # noqa: E402


@dataclass
class Result:
    module: int
    kind: str
    pages: int
    headers: int
    text_chars: int
    empty_pages: list[int]
    bounding_boxes_outside: list[int]
    expected_points_present: bool
    preview: str


def all_docs():
    for num, folder in NAMES.items():
        kinds = ["PRACTICAS"] if num == 9 else ["TEORIA", "PRACTICAS"]
        for kind in kinds:
            stem = f"M{num:02}_{kind}"
            yield num, kind, ROOT / folder / kind / (stem + ".md"), ROOT / folder / kind / (stem + ".pdf")


def convert_thumbnail(page, max_width: int = 370):
    pix = page.get_pixmap(matrix=fitz.Matrix(0.72, 0.72), alpha=False)
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    ratio = min(1.0, max_width / image.width)
    return image.resize(
        (round(image.width * ratio), round(image.height * ratio)),
        Image.Resampling.LANCZOS,
    )


def gallery(document, outfile: Path):
    indices = sorted({0, len(document) // 2, len(document) - 1})
    images = [convert_thumbnail(document[index]) for index in indices]
    padding, caption_h = 16, 26
    height = max(im.height for im in images) + caption_h + 2 * padding
    width = sum(im.width for im in images) + (len(images) + 1) * padding
    canvas = Image.new("RGB", (width, height), (244, 246, 249))
    draw = ImageDraw.Draw(canvas)
    x = padding
    for index, im in zip(indices, images):
        draw.text((x, padding), f"Pagina {index+1}", fill=(29, 50, 75))
        canvas.paste(im, (x, padding + caption_h))
        x += im.width + padding
    outfile.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(outfile, optimize=True)


def main():
    target = ROOT / "QA_PUBLICACION_PDF"
    target.mkdir(exist_ok=True)
    results = []
    errors = []
    for num, kind, md, pdf in all_docs():
        label = f"M{num:02} {kind}"
        if not md.is_file() or not pdf.is_file():
            errors.append(f"{label}: falta Markdown o PDF")
            continue
        if md.stat().st_size < 500 or pdf.stat().st_size < 20000:
            errors.append(f"{label}: tamaño de archivo anómalo")
            continue
        with fitz.open(pdf) as doc:
            if not 2 <= len(doc) <= 240:
                errors.append(f"{label}: número inesperado de páginas: {len(doc)}")
            if doc.needs_pass:
                errors.append(f"{label}: PDF protegido")
                continue
            headers = sum(header_present(page,num,kind=="PRACTICAS") for page in doc)
            if headers != len(doc):
                errors.append(f"{label}: faltan cabeceras en {len(doc)-headers} páginas")
            empty = []
            beyond = []
            text_length = 0
            content = []
            for page_num, page in enumerate(doc, 1):
                all_text = page.get_text("text")
                content.append(all_text)
                text_length += len(all_text)
                body = page.get_text(
                    "text",
                    clip=fitz.Rect(0, 48, page.rect.width, page.rect.height - 24)
                ).strip()
                if len(body) < 12:
                    empty.append(page_num)
                for b in page.get_text("blocks"):
                    x0,y0,x1,y1 = b[:4]
                    if x0 < -3 or y0 < -3 or x1 > page.rect.width+3 or y1 > page.rect.height+3:
                        beyond.append(page_num)
                        break
            if empty:
                errors.append(f"{label}: páginas sin cuerpo legible: {empty}")
            if beyond:
                errors.append(f"{label}: bloques de texto fuera de página: {beyond}")
            joined = " ".join(content).replace("\n", " ")
            if num == 9:
                tokens = [f"Paso 9.{i}" for i in range(1,17)]
            else:
                tokens = [f"Punto {num}.{i}" for i in range(1, EXPECTED_POINTS[num]+1)]
            missing = [t for t in tokens if t.casefold() not in joined.casefold()]
            if missing and kind == "PRACTICAS":
                errors.append(f"{label}: faltan referencias a {missing}")
            preview = target / f"M{num:02}_{kind}_muestra.png"
            gallery(doc,preview)
            results.append(Result(num,kind,len(doc),headers,text_length,empty,beyond,
                                  not bool(missing),str(preview.relative_to(ROOT))))
            print(f"{label}: {len(doc)} páginas, {headers}/{len(doc)} cabeceras, "
                  f"{text_length} caracteres, previas {preview}",flush=True)
    report = {
        "documents_expected":17,
        "documents_checked":len(results),
        "pages_total":sum(r.pages for r in results),
        "headers_total":sum(r.headers for r in results),
        "problems":errors,
        "note":("Verificación técnica de archivos. Las 3 miniaturas por documento "
                "facilitan inspección, pero no acreditan revisión visual de todas "
                "las páginas ni sincronización semántica completa."),
        "documents":[asdict(x) for x in results],
    }
    (target/"informe.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    (target/"informe.md").write_text(
        "# Publicación PDF: auditoría técnica\n\n"
        + f"Documentos: {len(results)}/17. Páginas: {report['pages_total']}. "
        + f"Cabeceras: {report['headers_total']}.\n\n"
        + "\n".join(f"- {problem}" for problem in errors)
        + "\n\n**Nota:** no supone una revisión visual humana íntegra.\n",
        encoding="utf-8")
    if errors:
        print("FALLOS: " + "; ".join(errors), file=sys.stderr)
        sys.exit(1)
    print(f"PASS estructural: {len(results)} documentos, "
          f"{report['pages_total']} páginas con cabeceras",flush=True)


if __name__=="__main__":
    main()
