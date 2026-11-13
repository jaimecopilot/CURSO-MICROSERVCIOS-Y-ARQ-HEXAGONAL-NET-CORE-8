# Auditoría de paridad — Prácticas M06, M07 y M08

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS  
**Autor:** JAIME GALLO  
**Rama:** `version-corregida`  
**Fecha:** 13 de noviembre de 2026  
**Resultado:** sin divergencias en los fragmentos finales marcados.

La auditoría utiliza `tools/auditar_paridad_m06_m08.py`. Se inspeccionan los marcadores
`M06_CODIGO`, `M07_CODIGO` y `M08_CODIGO` de los tres manuales de prácticas.
Para cada marcador se comprueba que el archivo existe en el proyecto y etapa
indicados. Cuando un mismo archivo se modifica varias veces en una etapa,
se compara su **último fragmento de referencia** con el archivo resultante.

| Módulo | Marcadores con ruta válida | Destinos distintos en su última operación | Contenido idéntico normalizado | Fragmento contenido en el archivo | Divergencias |
|---|---:|---:|---:|---:|---:|
| M06 | 92 | 77 | 71 | 6 | 0 |
| M07 | 93 | 73 | 73 | 0 | 0 |
| M08 | 66 | 47 | 47 | 0 | 0 |
| **Total** | **251** | **197** | **191** | **6** | **0** |

**Cómo se interpreta:** la equivalencia normalizada ignora la indentación y las
líneas vacías, pero no elimina instrucciones del código. Los seis casos de M06
clasificados como «fragmento contenido» son inserciones o referencias parciales
que aparecen dentro de archivos posteriores, no discrepancias detectadas.

**Límite de esta comprobación:** no recrea desde cero todas las etapas mediante
acciones gráficas de Visual Studio. Demuestra correspondencia de los marcadores
comprobados con los proyectos de referencia, mientras las compilaciones, xUnit y
ensayos funcionales pertenecen a la batería de validación Windows separada.

[Ejecución de auditoría de paridad en GitHub Actions](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43493682718).

Los PDF, teorías y proyectos originales no son modificados por la auditoría.
