#!/usr/bin/env python3
"""Comprueba correspondencia de fragmentos marcados de prácticas M06-M08."""
from collections import Counter
import difflib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CONFIG = {
  6: ("M06_COMUNICACION_MICROSERVICIOS",
      ["6.1-comunicacion-sincrona-http","6.2-comunicacion-asincrona-eventos",
       "6.3-cuando-usar-cada-enfoque"], 92),
  7: ("M07_OBSERVABILIDAD_RESILIENCIA",
      ["7.1-logging","7.2-health-checks","7.3-gestion-excepciones",
       "7.4-retry-circuit-breaker-polly"], 93),
  8: ("M08_API_GATEWAY",
      ["8.1-introduccion-api-gateway","8.2-configuracion-basica-yarp",
       "8.3-enrutamiento-peticiones","8.4-balanceo-carga"], 66),
}
CODE = re.compile(
    r"<!-- M0[678]_CODIGO (\{[^\n]*\}) -->\s*"
    + chr(96)*3 + r"([^\n]*)\n([\s\S]*?)\n" + chr(96)*3
)


def normalized(data):
    return "\n".join(line.strip() for line in data.replace("\r\n","\n")
                     .lstrip("\ufeff").splitlines() if line.strip())


def main():
    report=["# M06–M08 — Paridad de fragmentos frente a proyectos canónicos",""]
    divergencias = 0
    for number, (dirname,stages,expected) in CONFIG.items():
        md=(ROOT/dirname/"PRACTICAS"/f"M{number:02}_PRACTICAS.md").read_text("utf-8")
        matches=[]
        for m in CODE.finditer(md):
            info=json.loads(m.group(1))
            index=int(info["paso"].split(".")[1])-1
            file=ROOT/dirname/"PROYECTO"/stages[index]/info["ruta"]
            assert file.is_file(),f"Falta {file}"
            matches.append((info,m.group(3),file))
        assert len(matches)==expected
        last={}
        for info,code,file in matches:
            last[(info["paso"].split(".")[1],str(file))]=(info,code,file)
        scores=[]
        for info,code,file in last.values():
            target=normalized(file.read_text("utf-8-sig"))
            snippet=normalized(code)
            same=target==snippet
            contains=snippet in target or target in snippet
            ratio=difflib.SequenceMatcher(None,snippet,target,autojunk=False).ratio() if len(snippet)<30000 and len(target)<30000 else 0
            scores.append((info["paso"],info["ruta"],same,contains,ratio,info["modo"]))
        counts=Counter("exacto" if e else "contenido" if inc else "divergente" for _,_,e,inc,_,_ in scores)
        divergencias += counts["divergente"]
        report.extend([
            f"## M{number:02}",
            "",
            f"- Marcadores de archivo válidos: {len(matches)}/{expected}",
            f"- Archivos distintos en la última operación de su etapa: {len(last)}",
            f"- Coincidencia normalizada exacta: {counts['exacto']}",
            f"- Coincidencia de fragmento contenido: {counts['contenido']}",
            f"- Diferencias que requieren revisión semántica: {counts['divergente']}",
            "",
        ])
        problematic=sorted((x for x in scores if not x[2] and not x[3]),
                           key=lambda x:x[4])
        if problematic:
            report += ["| Paso | Archivo | Operación | Similitud |",
                       "|---|---|---|---:|"]
            for step,file,exact,contains,ratio,mode in problematic[:30]:
                report.append(f"| {step} | {file} | {mode} | {ratio:.1%} |")
            report.append("")
        print(f"M{number:02}: {len(matches)} marcadores, {len(last)} destinos "
              f"únicos; exactos={counts['exacto']}, contenido={counts['contenido']}, "
              f"revisar={counts['divergente']}")
    output=ROOT/"AUDITORIA_PARIDAD_M06_M08.md"
    output.write_text("\n".join(report)+"\n",encoding="utf-8")
    print("INFORME "+str(output))
    if divergencias:
        raise SystemExit(f"Paridad fallida: {divergencias} destinos del código docente no coinciden con los proyectos")


if __name__=="__main__":
    main()
