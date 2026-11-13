#!/usr/bin/env python3
"""Reconstrucción encadenada sin copiar snapshots canónicos de M03 a M08.

El único punto de partida es M02/PROYECTO/2.4-documentacion-openapi.
Cada uno de los 25 puntos se construye desde el producto reconstruido
en el paso inmediatamente anterior; se contrastan sus archivos y la
solución .sln contra las referencias, pero nunca se copian esas referencias.
No incluye los 4 puntos M02, M01 o Docker M09.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import json
import tempfile

from auditar_reconstruccion_practicas import CONFIG, ROOT, materializar_etapa
from auditar_continuidad_modular import materializar_limite

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--report",type=Path,
        default=ROOT/"AUDITORIA_CADENA_M03_M08.md")
    args=parser.parse_args()
    previous=ROOT/CONFIG[2][0]/"PROYECTO"/CONFIG[2][1][-1]
    results=[]
    with tempfile.TemporaryDirectory(prefix="aceria-cadena-completa_") as tmp:
        for module in range(3,9):
            for point in range(1,len(CONFIG[module][1])+1):
                destination=Path(tmp)/f"M{module:02}_{point}"
                if point==1:
                    evidence=materializar_limite(
                        module,destination,origen_reconstruido=previous)
                else:
                    evidence=materializar_etapa(
                        module,point,destination,origen_reconstruido=previous)
                assert evidence.get("state","PASS")=="PASS"
                previous=destination
                results.append((module,point))
                print(f"CADENA {len(results):02d}/25: M{module:02}.{point} PASS",flush=True)
    assert len(results)==25,results
    report=[
        "# Reconstrucción acumulativa M03–M08",
        "",
        "Se ha partido únicamente del proyecto de referencia final de M02 "
        "(aún sin reconstruir desde su manual). Para cada etapa desde M03.1 "
        "hasta M08.4 se han aplicado las instrucciones del manual a los "
        "**archivos obtenidos en la etapa anterior de esta misma ejecución**, "
        "no a una copia del siguiente proyecto canónico.",
        "",
        "Cada resultado se ha contrastado con el contenido textual normalizado "
        "y con la pertenencia lógica de los proyectos .csproj en la solución "
        ".sln. Las GUIDs generadas automáticamente pueden diferir. Esta "
        "comprobación no ejecuta xUnit ni Docker: los workflows Windows "
        "cubren las pruebas funcionales e integración por separado.",
        "",
        "| Etapa | Reconstrucción encadenada |",
        "|---|---|",
    ]
    report.extend(f"| M{m:02}.{p} | PASS |" for m,p in results)
    report.extend(["","**Resultado:** 25 de 25 puntos reconstruidos "
                   "acumulativamente sin copiar destinos, sin divergencias.",
                   "",
                   "**Limitaciones:** falta construir M02 desde sus instrucciones, "
                   "demostrar M01 desde cero y ejecutar M09 en Docker Desktop "
                   "físico Windows. Este E2E de archivos no reproduce "
                   "interacciones de Visual Studio ni las pruebas optativas.",
                   ""])
    args.report.write_text("\n".join(report),encoding="utf-8")
    print("PASS CADENA ACUMULATIVA: M03.1→M08.4 (25/25)",flush=True)
    print(f"INFORME: {args.report}",flush=True)

if __name__=="__main__":
    main()
