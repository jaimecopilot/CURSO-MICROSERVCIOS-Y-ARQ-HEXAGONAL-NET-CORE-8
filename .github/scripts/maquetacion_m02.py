"""Maquetación docente reproducible: 8 esquemas, listas y 4 tablas de errores.

No altera las fuentes de la carpeta fuentes-originales. El contrato original
se preserva y se mejora solo la representación Markdown/PDF del alumno.
"""
from __future__ import annotations
import re

FIGURAS = {
 "2.1": [(1, "m02-2-1-rest-restricciones.svg", "Las seis restricciones de REST y su función"),
         (2, "m02-2-1-uris.svg", "De la colección al recurso y sus relaciones")],
 "2.2": [(3, "m02-2-2-verbo-codigo.svg", "Cómo relacionar verbos HTTP con resultados"),
         (8, "m02-2-2-problem-details.svg", "Los campos principales de Problem Details")],
 "2.3": [(1, "m02-2-3-niveles-validacion.svg", "Recorrido de una petición por los tres niveles de validación"),
         (6, "m02-2-3-filtro-validacion.svg", "Ejecución del filtro antes del manejador Minimal API")],
 "2.4": [(2, "m02-2-4-generacion-openapi.svg", "Del endpoint de ASP.NET Core al documento OpenAPI"),
         (3, "m02-2-4-estructura-openapi.svg", "Secciones que componen el contrato OpenAPI")]
}

# Cada par reproduce una causa y su solución TAL CUAL figuran en la fuente.
# Se reconstruye y compara cada fila antes de aceptar la tabla; no se inventa texto.
DESGLOSE = {
 "2.1": [
 ("Falta el flag /E","Ejecutar xcopy origen destino /E /I /H /Y"),
 ("Falta el using System;","Añadir el using al principio del archivo"),
 ("Falta el using System.Collections.Generic;","Añadir el using al principio del archivo"),
 ("Falta el using System.Linq;","Añadir el using al principio del archivo"),
 ("No se inicializa _uris","Inicializar en el constructor"),
 ("Falta la comprobación con StartsWith","Revisar la primera comprobación de Validar"),
 ("Falta StringComparison.OrdinalIgnoreCase","Añadir el parámetro a Contains"),
 ("Falta el paquete FluentAssertions","Ejecutar dotnet add package FluentAssertions"),
 ("Falta la referencia al proyecto monolítico","Ejecutar dotnet add reference"),
 ("La API está en ejecución","Detener la API con Ctrl+C")],
 "2.2": [
 ("Falta el flag /E","Ejecutar xcopy origen destino /E /I /H /Y"),
 ("Falta el using System.Collections.Generic;","Añadir el using al principio del archivo"),
 ("Falta el using System.Linq;","Añadir el using al principio del archivo"),
 ("Falta el using System.Linq;","Añadir el using al principio del archivo"),
 ("No se inicializa _combinaciones","Inicializar en el constructor"),
 ("No se comprueba si el verbo existe","Comprobar ContainsKey antes de acceder"),
 ("Falta la comprobación con Contains","Revisar la segunda comprobación del método"),
 ("Falta el paquete FluentAssertions","Ejecutar dotnet add package FluentAssertions"),
 ("Falta la referencia al proyecto monolítico","Ejecutar dotnet add reference"),
 ("La API está en ejecución","Detener la API con Ctrl+C")],
 "2.3": [
 ("Falta el flag /E","Ejecutar xcopy origen destino /E /I /H /Y"),
 ("Falta el using FluentValidation;","Añadir el using al principio del archivo"),
 ("Falta el using AceriaApp.Monolito.Api.Validacion;","Añadir el using al principio de Program.cs"),
 ("Falta el using System.Linq;","Añadir el using al principio del archivo"),
 ("Falta el paquete FluentValidation.DependencyInjectionExtensions","Ejecutar dotnet add package FluentValidation.DependencyInjectionExtensions"),
 ("No está registrado en el contenedor","Añadir AddValidatorsFromAssemblyContaining"),
 ("Falta el paquete FluentAssertions","Ejecutar dotnet add package FluentAssertions"),
 ("Falta la referencia al proyecto monolítico","Ejecutar dotnet add reference"),
 ("La API está en ejecución","Detener la API con Ctrl+C"),
 ("Falta el .gitignore","Verificar que el .gitignore está presente")],
 "2.4": [
 ("Falta el flag /E","Ejecutar xcopy origen destino /E /I /H /Y"),
 ("Falta el using System;","Añadir el using al principio del archivo"),
 ("Falta el paquete FluentAssertions","Ejecutar dotnet add package FluentAssertions"),
 ("Falta la referencia al proyecto monolítico","Ejecutar dotnet add reference"),
 ("No se inicializa Metadatos con new()","Inicializar con new()"),
 ("No se registró SwaggerDoc con los metadatos","Revisar DocumentacionExtensions"),
 ("Falta la integración en Program.cs","Comprobar AddDocumentacionOpenApi y UseDocumentacionOpenApi"),
 ("La API está en ejecución","Detener la API con Ctrl+C"),
 ("Falta el .gitignore","Verificar que el .gitignore está presente"),
 ("No se ha ejecutado git add .","Ejecutar git add . antes del commit")]
}

def imagenes_en_teoria(markdown: str):
    """Inserta 8 figuras en bloques concretos sin suprimir contenido original."""
    result=markdown
    for point,fs in FIGURAS.items():
        for num,file,desc in fs:
            header=f"### Bloque {num} —"
            section=result.index(f"## Punto {point} —")
            block=result.index(header,section)
            title_end=result.index("\n",block)
            paragraph_start=result.index("\n\n",title_end)+2
            paragraph_end=result.index("\n\n",paragraph_start)
            figure=(f"\n\n![Figura del punto {point}: {desc}](IMAGENES/{file})\n\n"
                    f"*Figura M02.{point}.{num} — {desc}.*")
            result=result[:paragraph_end]+figure+result[paragraph_end:]
    if result.count("](IMAGENES/")!=8:
        raise ValueError("La teoría debe incluir exactamente ocho gráficos vectoriales")
    return result

def listar_ejemplos(text: str):
    """Convierte en ítems los ejemplos con '→' que estaban seguidos sin formato.
    Respeta los bloques C#/JSON/YAML originales.
    """
    lines=text.splitlines()
    result=[]
    fenced=False
    count=0
    for i,line in enumerate(lines):
        s=line.strip()
        if s.startswith("~~~") or s.startswith("```"):
            fenced=not fenced
            result.append(line)
            continue
        if not fenced and "→" in s and not s.startswith(("- ","|","Línea ","> ","<!--")):
            # Solo se reformatean líneas de ejemplo seguidas de anotaciones
            # "Línea n", nunca párrafos explicativos o código.
            if (i+1<len(lines) and (lines[i+1].strip().startswith("- **Línea ")
                  or "→" in lines[i+1] or not lines[i+1].strip())):
                if len(s)<165 and not s.startswith(("El ","La ","Las ","Los ","Un ","Una ","Cada ","La primera","Acción")):
                    left,right=s.split("→",1)
                    left=left.strip();right=right.strip()
                    if left and right and len(left)<95:
                        result.append(f"- **{left}** → {right}")
                        count+=1
                        continue
        result.append(line)
    if count<30:
        raise ValueError(f"Se esperaban ejemplos por ítems, solo convertidos {count}")
    return "\n".join(result),count

def tabla_errores(text: str,point: str):
    """Divide exactamente diez líneas originales en tres columnas verificadas."""
    pattern=(r"(?m)^### Errores comunes del ejercicio completo\s*\n\s*"
             r"Error Causa Solución\s*\n(?P<rows>(?:[^\n]+\n){10})")
    m=re.search(pattern,text)
    if not m:
        raise ValueError(f"{point}: no se encontró la tabla de errores fuente con diez filas")
    lines=m.group("rows").rstrip("\n").splitlines()
    if len(lines)!=10:raise ValueError(f"{point}: filas={len(lines)}")
    hints=DESGLOSE[point]
    rows=[]
    for n,(line,(cause,fix)) in enumerate(zip(lines,hints),1):
        if not line.endswith(fix):
            raise ValueError(f"{point} fila {n}: solución distinta: {line}")
        before=line[:-len(fix)].strip()
        if not before.endswith(cause):
            raise ValueError(f"{point} fila {n}: causa distinta: {line}")
        error=before[:-len(cause)].strip()
        if not error:raise ValueError(f"{point} fila {n}: error vacío")
        if f"{error} {cause} {fix}"!=line.strip():
            raise ValueError(f"{point} fila {n}: se alteraron palabras")
        rows.append(f"| {error} | {cause} | {fix} |")
    table=("| Error observado | Causa | Solución guiada |\n"
           "|:---|:---|:---|\n"+"\n".join(rows)+"\n")
    return text[:m.start()]+ "### Errores comunes del ejercicio completo\n\n"+table+text[m.end():]

def ejecutar(markdown: str, tipo: str):
    if tipo=="TEORIA":
        markdown=imagenes_en_teoria(markdown)
        markdown,num=listar_ejemplos(markdown.replace("```","```"))
        return markdown
    if tipo=="PRACTICAS":
        for point in DESGLOSE:
            markdown=tabla_errores(markdown,point)
        assert markdown.count("| Error observado | Causa | Solución guiada |")==4
        assert "Error Causa Solución" not in markdown
        return markdown
    raise ValueError(tipo)
