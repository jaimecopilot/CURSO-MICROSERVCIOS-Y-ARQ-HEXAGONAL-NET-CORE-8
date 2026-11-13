#!/usr/bin/env python3
"""Añade y verifica la cabecera de todas las páginas de M01 a M08.

La ejecución es idempotente. Conserva los PDF originales, sin regenerar
los contenidos desde los Markdown ni modificar el código del curso.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import fitz

COURSE = "ARQUITECTURA HEXAGONAL Y MICROSERVICIOS"
AUTHOR = "JAIME GALLO"
HEADER_HEIGHT = 46.0
MIN_FREE_TOP = 48.0
ROOT = Path(__file__).resolve().parents[1]
PRACTICE_PDFS = (
    "M01_INTRODUCCION_MICROSERVICIOS/PRACTICAS/M01_PRACTICAS.pdf",
    "M02_APIS_REST_ASPNET_CORE/PRACTICAS/M02_PRACTICAS.pdf",
    "M03_ARQUITECTURA_HEXAGONAL/PRACTICAS/M03_PRACTICAS.pdf",
)

PDFS = (
    "M01_INTRODUCCION_MICROSERVICIOS/TEORIA/M01_TEORIA.pdf",
    "M02_APIS_REST_ASPNET_CORE/TEORIA/M02_TEORIA.pdf",
    "M03_ARQUITECTURA_HEXAGONAL/TEORIA/M03_TEORIA.pdf",
    "M04_PATRONES_ARQUITECTURA/TEORIA/M04_TEORIA.pdf",
    "M05_DDD_CQRS/TEORIA/M05_TEORIA.pdf",
    "M06_COMUNICACION_MICROSERVICIOS/TEORIA/M06_TEORIA.pdf",
    "M07_OBSERVABILIDAD_RESILIENCIA/TEORIA/M07_TEORIA.pdf",
    "M08_API_GATEWAY/TEORIA/M08_TEORIA.pdf",
)


def header_lines(module: int, practice: bool = False) -> tuple[str, str, str]:
    kind = "PRÁCTICAS" if practice else "TEORÍA"
    return (COURSE, f"{kind} MÓDULO {module}", AUTHOR)


def top_text(page: fitz.Page) -> str:
    return page.get_text(
        "text", clip=fitz.Rect(0, 0, page.rect.width, HEADER_HEIGHT + 2)
    )


def header_present(page: fitz.Page, module: int, practice: bool = False) -> bool:
    text = top_text(page).upper()
    return all(line in text for line in header_lines(module, practice))


def free_top(page: fitz.Page) -> float:
    bounds = [
        float(block["bbox"][1])
        for block in page.get_text("dict")["blocks"]
        if block.get("type") in (0, 1)
        and block.get("bbox")
        and float(block["bbox"][3]) > 0
    ]
    return min(bounds, default=float(page.rect.height))


def draw_header(page: fitz.Page, module: int, practice: bool = False) -> None:
    width = page.rect.width
    for value, font, size, baseline in (
        (COURSE, "hebo", 8.5, 13.0),
        (f"{'PRÁCTICAS' if practice else 'TEORÍA'} MÓDULO {module}", "hebo", 8.3, 25.2),
        (AUTHOR, "hebo", 7.9, 37.2),
    ):
        text_width = fitz.get_text_length(value, fontname=font, fontsize=size)
        if text_width > width - 30:
            size *= (width - 30) / text_width
            text_width = fitz.get_text_length(value, fontname=font, fontsize=size)
        page.insert_text(
            fitz.Point((width - text_width) / 2, baseline),
            value, fontname=font, fontsize=size,
            color=(0.12, 0.23, 0.36), overlay=True,
        )
    side = max(26.0, width * 0.092)
    page.draw_line(
        fitz.Point(side, 42), fitz.Point(width - side, 42),
        color=(0.65, 0.73, 0.81), width=0.45, overlay=True,
    )


def copy_uri_links(target: fitz.Page, original: fitz.Page,
                   scale: float, dx: float, dy: float) -> None:
    """Conserva los enlaces web si hay que reducir una página para abrir margen."""
    for link in original.get_links():
        if link.get("kind") != fitz.LINK_URI or not link.get("uri"):
            continue
        old = fitz.Rect(link["from"])
        new = fitz.Rect(
            old.x0 * scale + dx, old.y0 * scale + dy,
            old.x1 * scale + dx, old.y1 * scale + dy,
        )
        target.insert_link({
            "kind": fitz.LINK_URI, "from": new, "uri": link["uri"]
        })


def reframe(source: fitz.Document, module: int,
            colliding: set[int], practice: bool = False) -> fitz.Document:
    """Si hay texto en la zona superior, conserva la página A4 y abre espacio.

    Mantiene texto seleccionable, vectores e imágenes; no recorta el pie.
    """
    output = fitz.open()
    for original in source:
        w, h = original.rect.width, original.rect.height
        target = output.new_page(width=w, height=h)
        if original.number in colliding:
            dest = fitz.Rect(0, HEADER_HEIGHT + 3, w, h)
            scale = min(dest.width / w, dest.height / h)
            dx = dest.x0 + (dest.width - w * scale) / 2
            dy = dest.y0 + (dest.height - h * scale) / 2
            target.show_pdf_page(dest, source, original.number, keep_proportion=True)
        else:
            scale, dx, dy = 1.0, 0.0, 0.0
            target.show_pdf_page(original.rect, source, original.number)
        copy_uri_links(target, original, scale, dx, dy)
        draw_header(target, module, practice)
    if source.metadata:
        output.set_metadata(source.metadata)
    return output


def validate(document: fitz.Document, module: int, name: str,
             practice: bool = False) -> None:
    assert len(document) > 0, f"Documento vacío: {name}"
    for page_number, page in enumerate(document, 1):
        text = top_text(page)
        for line in header_lines(module, practice):
            assert text.count(line) == 1, (
                f"Cabecera ausente o repetida en {name}, página {page_number}: {line}"
            )
        assert page.rect.width >= 350 and page.rect.height >= 500, (
            f"Formato de página inesperado: {name}, página {page_number}"
        )


def process(path: Path, module: int, only_check: bool,
            practice: bool = False) -> tuple[int, int, int]:
    if not path.is_file():
        raise FileNotFoundError(f"Falta el PDF: {path}")
    source = fitz.open(path)
    if source.needs_pass:
        raise ValueError(f"PDF protegido: {path}")
    marked = sum(header_present(p, module, practice) for p in source)
    pages = len(source)
    if only_check or marked == pages:
        validate(source, module, path.name, practice)
        source.close()
        return pages, marked, 0
    if marked:
        raise ValueError(f"PDF parcialmente marcado: {path}, {marked}/{pages}")

    colliding = {p.number for p in source if free_top(p) < MIN_FREE_TOP}
    if colliding:
        output = reframe(source, module, colliding, practice)
    else:
        output = source
        for page in output:
            draw_header(page, module, practice)
    validate(output, module, path.name, practice)

    temp = path.with_name(path.stem + ".cabecera-tmp.pdf")
    output.save(temp, garbage=4, deflate=True)
    if output is not source:
        output.close()
    source.close()
    temp.replace(path)
    with fitz.open(path) as verified:
        validate(verified, module, path.name, practice)
    return pages, marked, len(colliding)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--practicas", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    all_pages = 0
    selected = PRACTICE_PDFS if args.practicas else PDFS
    for module, relative in enumerate(selected, 1):
        pages, previous, adjusted = process(
            args.root / relative, module, args.check, args.practicas
        )
        all_pages += pages
        print(
            f"M{module:02}: {pages} páginas; cabeceras {pages}/{pages}; "
            f"ya marcadas {previous}; páginas adaptadas {adjusted}"
        )
    print(
        f"VALIDADO: {all_pages} páginas de {len(selected)} PDF; "
        "cabecera del curso, módulo y autor presente en todas"
    )


if __name__ == "__main__":
    main()
