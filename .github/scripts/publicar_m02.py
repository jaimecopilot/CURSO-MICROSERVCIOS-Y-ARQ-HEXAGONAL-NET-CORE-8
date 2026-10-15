#!/usr/bin/env python3
"""Publica dos Markdown completos y PDF reproducibles de M02, solo en rama de desarrollo.

Contrato: 4 fuentes íntegras (10 bloques/24 pasos por punto);
nunca modificar .github/fuentes-originales ni inventar texto.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path.cwd()
SCRIPT_DIR=Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from construir_m02_desde_fuentes import grab, POINTS, main as generate
from pdf_m02_previsualizacion import make

TARGET=Path("M02_APIS_REST_ASPNET_CORE")
DOCFILES={
 "TEORIA":TARGET/"TEORIA"/"M02_TEORIA.md",
 "PRACTICAS":TARGET/"PRACTICAS"/"M02_PRACTICAS.md",
}
ARTIFACT=Path("m02_publicacion")
TMP=ARTIFACT/"fuentes_generadas"

def validate_sections(originals: list[dict], docs: dict[str,str]):
    assert len(originals)==4 and all(x for x in originals)
    theory=docs["TEORIA"]
    pract=docs["PRACTICAS"]
    blocks=re.findall(r"(?m)^### Bloque (\d+) —",theory)
    steps=re.findall(r"(?m)^### PASO (2\.[1-4]\.\d+) —",pract)
    assert len(blocks)==40,(len(blocks),blocks)
    assert len(steps)==96,(len(steps),steps)
    for point in POINTS:
        assert steps.count(point+".1")==1
        assert steps.count(point+".24")==1
        for i in range(1,25):
            assert f"{point}.{i}" in steps, f"falta paso {point}.{i}"
        for heading in (f"## Punto {point} —",):
            assert heading in theory and heading in pract, heading
        for sub in ("### Reto resuelto paso a paso",
                    "### Resultado esperado",
                    "### Conclusión y enlace al siguiente punto"):
            # Estos apartados no deben desaparecer del ejercicio por correcciones.
            assert sub in pract,sub
    for v in docs.values():
        assert "Duración:" not in v
        assert "PARTE TEÓRICA (" not in v
        assert "PARTE PRÁCTICA (" not in v
        assert "Espero confirmación del usuario" not in v
        assert v.count("```")==0
    # En los ejemplos ya delimitados 2.4, fences completos y no anidados
    assert len(re.findall(r"(?m)^```",theory))%2==0
    assert len(re.findall(r"(?m)^```",pract))%2==0

    expected={
      "2.3": [
        "### PASO 2.3.15 — Crear CrearOrdenRequestTests.cs",
        "### PASO 2.3.16 — Crear ValidacionExtensions",
        "AddValidatorsFromAssemblyContaining<CrearOrdenRequestValidator>()",
        "builder.Services.AddValidacion();",
        "FluentValidation.DependencyInjectionExtensions",
      ],
      "2.4":[
        "### PASO 2.4.9 — Crear DocumentacionExtensions",
        "### PASO 2.4.15 — Crear DocumentacionExtensionsTests",
        "WebApplicationFactory<Program>",
        "EsEntornoDeProduccion",
        "equipo@acerialocal",
        "Cincuenta y una pruebas unitarias",
      ]
    }
    for point,phrases in expected.items():
        for phrase in phrases:
            assert phrase in pract,f"{point} falta corrección: {phrase}"
    for unacceptable in (
        "equipo@acería.local",
        "Cuarenta y cuatro pruebas unitarias acumuladas en diez proyectos de tests",
        "### PASO 2.4.9 — Crear la clase ConstructorDocumentoOpenApi",
        "### PASO 2.3.15 — Crear el archivo ValidationFilterTests.cs",
    ):
        assert unacceptable not in pract,unacceptable
    # 2.4 fuente original usa fences; preservar integralmente toda su teoría.
    text_original = originals[3]["theory"]
    snippets = [
        "La aplicación de la documentación cierra el módulo 2",
        "Línea 26: type: string → tipo de la propiedad.",
        "Swagger UI lee el documento OpenAPI generado por el servidor",
        "Versionado       → v1 en URL y en documentación.",
    ]
    for phrase in snippets:
        assert phrase in text_original and phrase in theory, f"2.4 teoría perdida: {phrase}"
    return dict(blocks=len(blocks),steps=len(steps),
                points=[x["point"] for x in originals],
                word_counts={key:len(re.findall(r"\w+",contents)) for key,contents in docs.items()})

def main():
    originals=[grab(point) for point in POINTS]
    if not all(originals):raise SystemExit("BLOQUEADO: falta fuente original")
    ARTIFACT.mkdir(parents=True, exist_ok=True)
    # Siempre regenerar Markdown desde originales, no desde vistas previas sintéticas.
    orig_argv=sys.argv[:]
    try:
        sys.argv=[sys.argv[0],"--salida",str(TMP)]
        generate()
    finally: sys.argv=orig_argv
    docs={key:(TMP/f"M02_{key}.md").read_text(encoding="utf-8") for key in DOCFILES}
    report=validate_sections(originals,docs)
    for key,dst in DOCFILES.items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(docs[key],encoding="utf-8")
        pdf=dst.with_suffix(".pdf")
        result=make(dst,pdf)
        shutil.copy2(dst, ARTIFACT/dst.name)
        shutil.copy2(pdf, ARTIFACT/pdf.name)
        report[key]=dict(markdown=str(dst),sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),
                         pdf=result,pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest())
        # Están los 4 puntos y se puede extraer texto de todas las páginas;
        # el texto PDF se deriva del mismo archivo Markdown.
    report["fuentes_sha256"]={x["point"]:x["sha256"] for x in originals}
    (ARTIFACT/"INFORME_DE_GENERACION.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print("M02 VALIDADO, dos Markdown y dos PDF generados")
    print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
