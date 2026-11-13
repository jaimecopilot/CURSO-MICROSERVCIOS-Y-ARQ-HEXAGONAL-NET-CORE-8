# M02 — Informe de revisión pedagógica y validación técnica

**Curso:** ARQUITECTURA HEXAGONAL Y MICROSERVICIOS  
**Módulo:** M02 — Desarrollo de APIs REST con ASP.NET Core 8  
**Autor:** JAIME GALLO  
**Rama:** `version-corregida`  
**Fecha:** 13 de noviembre de 2026  
**Estado:** CIERRE TÉCNICO DE LA REVISIÓN. La aceptación editorial final corresponde al autor.

## Revisión de las prácticas

- Cuatro puntos: 2.1 a 2.4, con 24 pasos en cada punto (96 pasos).
- Se reescribieron 96 explicaciones para desarrollar en prosa el motivo técnico de cada paso.
- Se redujeron las justificaciones y diagnósticos mecánicamente repetidos, respetando los procedimientos con sus comandos y verificaciones.
- Se conservaron los **66 bloques de código** de la versión original (incluidas las separaciones internas), así como los marcadores de archivos y la continuidad del proyecto.
- PDF `PRACTICAS/M02_PRACTICAS.pdf`: **58 páginas**. Cabeceras presentes y verificadas en las 58.

## Pruebas reales de Windows y SQL Server Express

Las pruebas se ejecutaron en el runner `windows-2022`, con .NET 8, SQL Server 2022 Express y el proveedor real EF Core SQL Server. Cada etapa se compiló y probó en una copia de ruta corta para evitar limitaciones de carga de librerías nativas.

| Etapa | xUnit aprobadas | xUnit fallidas | Compilación |
|---|---:|---:|---|
| 2.1 Diseño REST y GET | 3 | 0 | Release OK |
| 2.2 Verbos, CRUD y estados | 7 | 0 | Release OK |
| 2.3 FluentValidation | 12 | 0 | Release OK |
| 2.4 OpenAPI y Swagger | 16 | 0 | Release OK |
| **Total de ejecuciones sobre las cuatro etapas** | **38** | **0** | **Todas correctas** |

El snapshot final 2.4 superó además el recorrido HTTP con SQL Server Express:

- `GET /api/v1/ordenes`: HTTP 200.
- `POST /api/v1/ordenes`: HTTP 201 con cabecera Location y recurso creado.
- `GET /api/v1/ordenes/{id}`: recuperación de la misma orden persistida en SQL.
- Petición inválida: HTTP 400.
- Cantidad superior a la capacidad didáctica: HTTP 422.
- `/swagger/v1/swagger.json`: HTTP 200.

## Trazabilidad

El auditor comprueba la presencia y el orden de los 96 pasos y verifica que los 12 marcadores explícitos `M02_ARCHIVO` apuntan a rutas existentes en los snapshots correspondientes. Se conservan los 66 bloques de código y los cuatro resultados acumulativos.

**Alcance real:** estos ensayos validan los cuatro proyectos de referencia y el recorrido HTTP final. No son una simulación manual, paso por paso, de las interacciones gráficas del alumno en Visual Studio, ni demuestran la equivalencia textual de todos los fragmentos no marcados frente al código final. Los retos optativos no se incluyen en el recuento. Esta distinción evita atribuir a las pruebas más cobertura de la que tienen.

## Reproducibilidad

- [GitHub Actions: M02/M03 Windows SQL HTTP](https://github.com/jaimecopilot/CURSO-MICROSERVCIOS-Y-ARQ-HEXAGONAL-NET-CORE-8/actions/runs/43470830650).
- Validador: `tools/validar_practicas_m02_m03.py`.
- Workflow: `.github/workflows/m02-m03-windows-e2e.yml`.
- Generador PDF: `.github/workflows/rebuild-corrected-theory-pdfs.yml`.
- Encabezados: `tools/pdf_running_headers.py`.

**Conclusión:** M02 se cierra técnicamente en la revisión de redacción de `version-corregida`. No se ha modificado ni fusionado el código de los proyectos en `main`.
