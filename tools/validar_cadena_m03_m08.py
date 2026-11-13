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
from reconstruir_m02_incremental import materialize as construir_m02

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--report",type=Path,
        default=ROOT/"AUDITORIA_CADENA_M03_M08.md")
    parser.add_argument("--desde-m02-vacio",action="store_true",
        help="Iniciar M02.1 desde vacío, reconstruir 4 puntos, luego los 25 M03-M08")
    args=parser.parse_args()
    previous=ROOT/CONFIG[2][0]/"PROYECTO"/CONFIG[2][1][-1]
    results=[]
    with tempfile.TemporaryDirectory(prefix="aceria-cadena-completa_") as tmp:
        if args.desde_m02_vacio:
            previous=Path(tmp)/"M02_4"
            proofs=construir_m02(previous,stage=4,desde_cero=True)
            if len(proofs)!=4 or not all(p["pass"] for p in proofs):
                raise RuntimeError("Faltan etapas de M02 o existe discrepancia con su proyecto")
            print("CADENA 04/29: M02.1–M02.4 desde carpeta vacía PASS",flush=True)
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
                print(f"CADENA {len(results)+(4 if args.desde_m02_vacio else 0):02d}/"
                      f"{29 if args.desde_m02_vacio else 25}: M{module:02}.{point} PASS",flush=True)
    assert len(results)==25,results
    report=[
        "# Reconstrucción acumulativa M02–M08" if args.desde_m02_vacio else "# Reconstrucción acumulativa M03–M08",
        "",
        ("Se ha reconstruido M02.1 desde una carpeta vacía y se han aplicado "
         "sus instrucciones para obtener M02.2, M02.3 y M02.4. " if args.desde_m02_vacio
         else "Se ha partido del proyecto de referencia final de M02. ")
        + "Cada etapa desde M03.1 hasta M08.4 utiliza los archivos obtenidos "
        "en la etapa anterior de esta misma ejecución, sin copiar destinos.",
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
    if args.desde_m02_vacio:
        report.extend(f"| M02.{p} | PASS |" for p in range(1,5))
    report.extend(f"| M{m:02}.{p} | PASS |" for m,p in results)
    report.extend(["",f"**Resultado:** {29 if args.desde_m02_vacio else 25} de "
                   f"{29 if args.desde_m02_vacio else 25} puntos reconstruidos "
                   "acumulativamente sin copiar destinos, sin divergencias.",
                   "",
                   "**Limitaciones:** M01 y la entrada desde M01 a M02 aún no "
                   "están integradas en esta prueba; M09 en Docker Desktop "
                   "físico Windows sigue pendiente. No reproduce "
                   "interacciones gráficas de Visual Studio ni retos optativos.",
                   ""])
    args.report.write_text("\n".join(report),encoding="utf-8")
    print("PASS CADENA ACUMULATIVA: M02.1→M08.4 (29/29)" if args.desde_m02_vacio
          else "PASS CADENA ACUMULATIVA: M03.1→M08.4 (25/25)",flush=True)
    print(f"INFORME: {args.report}",flush=True)

if __name__=="__main__":
    main()
