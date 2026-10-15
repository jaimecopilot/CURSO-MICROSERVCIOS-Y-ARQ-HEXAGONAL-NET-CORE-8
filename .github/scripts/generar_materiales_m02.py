#!/usr/bin/env python3
"""Guías de teoría y prácticas M02: 40 bloques y 96 pasos, enlazados con código del repositorio."""
from pathlib import Path
import json,re
BASE=Path("M02_APIS_REST_ASPNET_CORE")
NAMES=["2.1-diseno-apis-rest","2.2-recursos-verbos-codigos","2.3-validacion-peticiones","2.4-documentacion-openapi"]
LABEL=["Diseño de APIs REST","Recursos, verbos HTTP y códigos de respuesta","Validación de peticiones","Documentación mediante OpenAPI (Swagger)"]
TOPICS=[
["REST y restricciones","Identificación de recursos","Representación y negociación de contenido","Semántica de métodos HTTP","Códigos de estado HTTP","Diseño de URIs","Interfaz uniforme y Minimal API","Relaciones y subrecursos","Paginación y filtrado","Contrato aplicado a AceriaApp"],
["El recurso de negocio","Representaciones y DTO","Verbos HTTP: seguridad e idempotencia","Colecciones y elementos concretos","Matriz de verbos y estados","Códigos 4xx y sus causas","Códigos 5xx e intermediarios","Problem Details y RFC 9457","Catálogo de recursos","Validación automática del catálogo"],
["Validación como contrato de entrada","Análisis sintáctico y enlace","Validación semántica","Invariantes del dominio","FluentValidation y sus reglas","IEndpointFilter en Minimal API","Mensajes de error comprensibles","Distinción entre 400 y 422","ValidationProblem y errores por campo","Registro de validadores con extensión"],
["OpenAPI como contrato procesable","SwaggerGen y Swagger UI","Secciones del documento OpenAPI","Metadatos de endpoints","Esquemas de recursos","Ejemplos de petición y respuesta","Versionado del contrato","Documentación de errores","Herramientas consumidoras del documento","Verificación real con WebApplicationFactory"]]
KEYS=[
["Restricciones separan cliente y servidor y reducen acoplamiento","Las URIs representan recursos y no acciones","JSON es una representación; Accept no habilita XML automáticamente","GET es seguro, PUT/DELETE idempotentes, PATCH depende del diseño","201 incluye la ubicación del creado; el estado no basta para definir caché","Se adopta /api/v1 como convención, no como mandato REST","MapGet y MapPost relacionan método, ruta y manejador","Anidamiento expresa contexto de identificación, sin límite normativo fijo","page y pageSize requieren implementación y pruebas","Un validador de URI verifica una convención, no las seis restricciones REST"],
["El recurso refleja necesidades del consumidor, no una tabla EF","Un DTO público no debe confundirse con la entidad persistida","POST puede ser cacheable bajo condiciones HTTP; PATCH puede ser idempotente","No se implementa DELETE de colección sin requisito explícito","Un catálogo de estados es un subconjunto esperado y documentado","400,401,403,404,405,409 y 422 tienen significados diferentes","502 y 504 suelen proceder de un intermediario","Problem Details es un contrato de error; RFC 9457 actualiza RFC 7807","Rutas, métodos y estados previstos forman un catálogo mantenible","Las aserciones deben probar aceptados y rechazados"],
["Un contrato evita que datos erróneos atraviesen la aplicación","Nullability no garantiza por sí sola required en runtime Minimal API","Reglas sobre Cantidad, Cliente y Material describen el dato aceptado","Stock, existencias y concurrencia requieren servicios reales de negocio","La integración DI usa FluentValidation.DependencyInjectionExtensions","Un filtro solo actúa si se aplica a un endpoint compatible","WithMessage devuelve condiciones concretas al cliente","400 y 422 son una convención de la API y no un mapeo obligatorio universal","Agrupar errores por propiedad ayuda a los consumidores","AddValidacion registra el validador, no activa por sí solo el filtro"],
["OpenAPI genera un contrato JSON desde rutas efectivas","La documentación debe limitarse a Development según configuración","info, paths, components y responses describen contrato; otros campos son opcionales","WithName, WithSummary y WithTags enriquecen metadatos","Los modelos de petición y respuesta informan esquemas concretos","Los ejemplos requieren configuración explícita para aparecer en Swagger","v1 en la URI debe coincidir con info.version","ProducesProblem documenta, pero no genera lógica de errores","Postman, ReDoc y clientes generados consumen el mismo artefacto","WebApplicationFactory solicita el Swagger JSON y comprueba contenido y entorno"]]
CODES=[
["docs/diseno-apis-rest.md","src/AceriaApp.Monolito.Api/DisenoRest/UriRest.cs","docs/diseno-apis-rest.md","docs/diseno-apis-rest.md","docs/diseno-apis-rest.md","src/AceriaApp.Monolito.Api/DisenoRest/ValidadorUriRest.cs","src/AceriaApp.Monolito.Api/Program.cs","docs/diseno-apis-rest.md","docs/diseno-apis-rest.md","src/AceriaApp.Monolito.Api/DisenoRest/CatalogoUris.cs"],
["docs/catalogo-recursos.md","docs/catalogo-recursos.md","docs/catalogo-recursos.md","docs/catalogo-recursos.md","src/AceriaApp.Monolito.Api/CatalogoRecursos/ValidadorCombinacionVerboCodigo.cs","docs/catalogo-recursos.md","docs/catalogo-recursos.md","docs/catalogo-recursos.md","src/AceriaApp.Monolito.Api/CatalogoRecursos/CatalogoCombinaciones.cs","tests/AceriaApp.CatalogoRecursos.Tests/ValidadorCombinacionVerboCodigoTests.cs"],
["src/AceriaApp.Monolito.Api/Validacion/CrearOrdenRequest.cs","src/AceriaApp.Monolito.Api/Validacion/CrearOrdenRequest.cs","src/AceriaApp.Monolito.Api/Validacion/CrearOrdenRequestValidator.cs","docs/validacion-peticiones.md","src/AceriaApp.Monolito.Api/Validacion/CrearOrdenRequestValidator.cs","src/AceriaApp.Monolito.Api/Validacion/ValidationFilter.cs","src/AceriaApp.Monolito.Api/Validacion/CrearOrdenRequestValidator.cs","docs/validacion-peticiones.md","src/AceriaApp.Monolito.Api/Validacion/ValidationFilter.cs","src/AceriaApp.Monolito.Api/Validacion/ValidacionExtensions.cs"],
["docs/documentacion-openapi.md","src/AceriaApp.Monolito.Api/Documentacion/DocumentacionExtensions.cs","docs/documentacion-openapi.md","src/AceriaApp.Monolito.Api/Program.cs","docs/documentacion-openapi.md","docs/documentacion-openapi.md","src/AceriaApp.Monolito.Api/Documentacion/MetadatosApi.cs","docs/documentacion-openapi.md","docs/documentacion-openapi.md","tests/AceriaApp.Documentacion.Tests/DocumentacionExtensionsTests.cs"]]
STEPS=[
["Preparar copia independiente desde 1.5","Abrir solución heredada","Verificar documentos heredados","Definir contrato de diseño REST","Crear carpeta DisenoRest","Crear clase UriRest","Revisar construcción de URIs","Crear ValidadorUriRest","Probar versión y segmentos de acción","Crear CatalogoUris","Comprobar consultas de catálogo","Añadir proyecto de pruebas","Añadir ProjectReference","Revisar paquetes de pruebas","Testear URIs válidas e inválidas","Testear construcción de rutas","Testear partición del catálogo","Compilar solución","Ejecutar ocho tests nuevos","Ejecutar tests acumulados","Actualizar README del punto","Crear ADR-006","Comparar documentos anteriores","Confirmar el estado final"],
["Copiar solución del punto 2.1","Abrir solución 2.2","Revisar documentación recibida","Escribir catálogo de recursos","Crear carpeta CatalogoRecursos","Crear CombinacionVerboCodigo","Crear ValidadorCombinacionVerboCodigo","Inspeccionar matriz de estados","Crear CatalogoCombinaciones","Comprobar filtrado con LINQ","Añadir proyecto de pruebas","Añadir referencia al monolito","Revisar dependencias xUnit","Probar casos de la matriz","Probar catálogo","Compilar solución","Ejecutar cinco tests nuevos","Ejecutar tests de la solución","Actualizar README","Crear ADR-007","Comparar todos los docs recibidos","Examinar árbol de proyecto","Comprobar .gitignore","Confirmar el estado final"],
["Copiar solución del punto 2.2","Abrir solución 2.3","Comprobar documentos heredados","Redactar contrato de validación","Incorporar paquete FluentValidation DI","Crear carpeta Validacion","Crear CrearOrdenRequest","Crear CrearOrdenRequestValidator","Crear ValidationFilter","Revisar errores agrupados","Añadir proyecto de pruebas","Añadir referencia al monolito","Comprobar xUnit y aserciones","Probar reglas del validador","Crear CrearOrdenRequestTests","Crear ValidacionExtensions e integrar Program","Compilar solución","Ejecutar seis tests nuevos","Ejecutar pruebas acumuladas","Explicar cambio aditivo en README","Crear ADR-008","Comparar todos los docs previos","Verificar estructura y dependencias","Confirmar el estado final"],
["Copiar solución del punto 2.3","Abrir solución 2.4","Revisar documentos heredados","Crear guía de documentación","Crear carpeta Documentacion","Crear MetadatosApi","Crear ConfiguracionOpenApi","Comprobar selección del entorno","Crear DocumentacionExtensions e integrar Swagger","Añadir proyecto de pruebas","Añadir referencia al monolito","Añadir Microsoft.AspNetCore.Mvc.Testing","Probar datos de contacto","Probar configuración","Probar Swagger HTTP con WebApplicationFactory","Compilar solución","Ejecutar nueve tests nuevos","Ejecutar tests acumulados","Actualizar README","Crear ADR-009","Comparar documentación previa","Comprobar árbol final","Revisar archivos excluidos","Cerrar módulo 2"]]
FILES=[
["AceriaApp.sln","AceriaApp.sln","docs","docs/diseno-apis-rest.md","src/AceriaApp.Monolito.Api/DisenoRest","src/AceriaApp.Monolito.Api/DisenoRest/UriRest.cs","src/AceriaApp.Monolito.Api/DisenoRest/UriRest.cs","src/AceriaApp.Monolito.Api/DisenoRest/ValidadorUriRest.cs","src/AceriaApp.Monolito.Api/DisenoRest/ValidadorUriRest.cs","src/AceriaApp.Monolito.Api/DisenoRest/CatalogoUris.cs","src/AceriaApp.Monolito.Api/DisenoRest/CatalogoUris.cs","tests/AceriaApp.DisenoRest.Tests","tests/AceriaApp.DisenoRest.Tests/AceriaApp.DisenoRest.Tests.csproj","tests/AceriaApp.DisenoRest.Tests/AceriaApp.DisenoRest.Tests.csproj","tests/AceriaApp.DisenoRest.Tests/ValidadorUriRestTests.cs","tests/AceriaApp.DisenoRest.Tests/UriRestTests.cs","tests/AceriaApp.DisenoRest.Tests/CatalogoUrisTests.cs","AceriaApp.sln","tests/AceriaApp.DisenoRest.Tests","AceriaApp.sln","README.md","docs/ADR-006-diseno-apis-rest.md","docs","AceriaApp.sln"],
["AceriaApp.sln","AceriaApp.sln","docs","docs/catalogo-recursos.md","src/AceriaApp.Monolito.Api/CatalogoRecursos","src/AceriaApp.Monolito.Api/CatalogoRecursos/CombinacionVerboCodigo.cs","src/AceriaApp.Monolito.Api/CatalogoRecursos/ValidadorCombinacionVerboCodigo.cs","src/AceriaApp.Monolito.Api/CatalogoRecursos/ValidadorCombinacionVerboCodigo.cs","src/AceriaApp.Monolito.Api/CatalogoRecursos/CatalogoCombinaciones.cs","src/AceriaApp.Monolito.Api/CatalogoRecursos/CatalogoCombinaciones.cs","tests/AceriaApp.CatalogoRecursos.Tests","tests/AceriaApp.CatalogoRecursos.Tests/AceriaApp.CatalogoRecursos.Tests.csproj","tests/AceriaApp.CatalogoRecursos.Tests/AceriaApp.CatalogoRecursos.Tests.csproj","tests/AceriaApp.CatalogoRecursos.Tests/ValidadorCombinacionVerboCodigoTests.cs","tests/AceriaApp.CatalogoRecursos.Tests/CatalogoCombinacionesTests.cs","AceriaApp.sln","tests/AceriaApp.CatalogoRecursos.Tests","AceriaApp.sln","README.md","docs/ADR-007-catalogo-recursos.md","docs","AceriaApp.sln",".gitignore","AceriaApp.sln"],
["AceriaApp.sln","AceriaApp.sln","docs","docs/validacion-peticiones.md","src/AceriaApp.Monolito.Api/AceriaApp.Monolito.Api.csproj","src/AceriaApp.Monolito.Api/Validacion","src/AceriaApp.Monolito.Api/Validacion/CrearOrdenRequest.cs","src/AceriaApp.Monolito.Api/Validacion/CrearOrdenRequestValidator.cs","src/AceriaApp.Monolito.Api/Validacion/ValidationFilter.cs","src/AceriaApp.Monolito.Api/Validacion/ValidationFilter.cs","tests/AceriaApp.Validacion.Tests","tests/AceriaApp.Validacion.Tests/AceriaApp.Validacion.Tests.csproj","tests/AceriaApp.Validacion.Tests/AceriaApp.Validacion.Tests.csproj","tests/AceriaApp.Validacion.Tests/CrearOrdenRequestValidatorTests.cs","tests/AceriaApp.Validacion.Tests/CrearOrdenRequestTests.cs","src/AceriaApp.Monolito.Api/Validacion/ValidacionExtensions.cs","AceriaApp.sln","tests/AceriaApp.Validacion.Tests","AceriaApp.sln","README.md","docs/ADR-008-validacion-peticiones.md","docs","src/AceriaApp.Monolito.Api/AceriaApp.Monolito.Api.csproj","AceriaApp.sln"],
["AceriaApp.sln","AceriaApp.sln","docs","docs/documentacion-openapi.md","src/AceriaApp.Monolito.Api/Documentacion","src/AceriaApp.Monolito.Api/Documentacion/MetadatosApi.cs","src/AceriaApp.Monolito.Api/Documentacion/ConfiguracionOpenApi.cs","src/AceriaApp.Monolito.Api/Documentacion/ConfiguracionOpenApi.cs","src/AceriaApp.Monolito.Api/Documentacion/DocumentacionExtensions.cs","tests/AceriaApp.Documentacion.Tests","tests/AceriaApp.Documentacion.Tests/AceriaApp.Documentacion.Tests.csproj","tests/AceriaApp.Documentacion.Tests/AceriaApp.Documentacion.Tests.csproj","tests/AceriaApp.Documentacion.Tests/MetadatosApiTests.cs","tests/AceriaApp.Documentacion.Tests/ConfiguracionOpenApiTests.cs","tests/AceriaApp.Documentacion.Tests/DocumentacionExtensionsTests.cs","AceriaApp.sln","tests/AceriaApp.Documentacion.Tests","AceriaApp.sln","README.md","docs/ADR-009-documentacion-openapi.md","docs","AceriaApp.sln",".gitignore","AceriaApp.sln"]]
FENCE=chr(96)*3
def put(path,content):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding="utf-8")
def make_svg(i,folder):
 labels=[["Cliente","URI /api/v1","Representación","Respuesta"],["Recurso","Método HTTP","Resultado","Código"],["Petición","Sintaxis","Reglas de entrada","Aplicación"],["Endpoint","SwaggerGen","OpenAPI JSON","Swagger UI"]][i]
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="760" height="140" viewBox="0 0 760 140">'
 for j,label in enumerate(labels):
  x=16+188*j
  svg+=f'<rect x="{x}" y="24" width="160" height="72" rx="12" fill="#e6f0f6" stroke="#214e69" stroke-width="2"/><text x="{x+80}" y="64" font-size="13" text-anchor="middle" font-family="Arial" fill="#214e69">{label}</text>'
  if j<3:svg+=f'<path d="M{x+162} 60 H{x+184}" stroke="#b77e31" stroke-width="3"/>'
 svg+='</svg>'
 put(folder/f"flujo_2_{i+1}.svg",svg)
def teoria():
 o=["# M02 — Desarrollo de APIs REST con ASP.NET Core","","**CURSO DE ARQUITECTURA HEXAGONAL Y MICROSERVICIOS AVANZADOS CON .NET 8**","","**AUTOR: JAIME GALLO**","","## Propósito del módulo","Diseñar contratos REST coherentes, validar peticiones con FluentValidation y comprobar mediante HTTP real la documentación OpenAPI generada por ASP.NET Core. Los cuatro puntos están vinculados a soluciones acumulativas de AceriaApp con EF Core 8 y SQL Server Express.",""]
 for i in range(4):
  o += [f"## Punto 2.{i+1} — {LABEL[i]}","",f"![Diagrama del punto 2.{i+1}](figuras/flujo_2_{i+1}.svg)",""]
  for j,title in enumerate(TOPICS[i]):
   key=KEYS[i][j];code=CODES[i][j]
   o += [f"### Bloque {j+1} — {title}","",
 f"{key}. Este principio debe describirse desde el comportamiento que observa un consumidor de AceriaApp y no exclusivamente desde la estructura interna del proyecto. En el contrato HTTP se distinguen la identificación del recurso, los datos intercambiados, las condiciones de éxito y los motivos de rechazo. La separación importa porque una migración de EF Core o una reorganización de carpetas no debería obligar a los clientes a conocer nuevas clases internas. Cada decisión del bloque se conecta con un archivo concreto, susceptible de inspección, una operación HTTP o una aserción automatizada. El lenguaje de la especificación debe diferenciar requisitos, convenciones y propiedades garantizadas por los protocolos.",
 "",
 f"En la acería, este conocimiento se aplica al ciclo de órdenes de producción, sus clientes y los materiales solicitados. Las operaciones existentes de la API monolítica permiten estudiar lecturas y altas, mientras los contratos de modificación y recursos anidados forman parte del diseño que podrán desarrollar puntos posteriores. La representación que recibe el consumidor no tiene por qué reproducir una tabla. El alumno examinará rutas, cuerpos JSON, métodos y códigos desde una perspectiva unificada: una acción correctamente nombrada no es suficiente si el servidor devuelve una respuesta contradictoria. Para tomar decisiones consistentes también es necesario considerar fallos, reintentos, versiones, seguridad y límites de tamaño. El bloque delimita exactamente qué se ha implementado y qué permanece como especificación.",
 "",
 f"Como criterio de verificación, consultar el archivo {chr(96)}{code}{chr(96)} dentro del proyecto del punto 2.{i+1}. La explicación no considera válida una afirmación solo por aparecer en la documentación: debe existir una clase real, un test pertinente o una operación reproducible que proporcione evidencia. {key}. Cuando esa capacidad dependa de un middleware, se comprobará su conexión al pipeline; cuando dependa de reglas de negocio, se distinguirá la validez superficial del dato de una comprobación de dominio. Este criterio evita confundir un esquema OpenAPI con lógica de aplicación, o una prueba de inicialización de objetos con un test de validación funcional. La consecuencia formativa es aprender a separar especificar, implementar y demostrar.",
 "",
 "**Aspectos del diseño**","",
 f"- **Principio:** {key}.",f"- **Evidencia real:** {chr(96)}{code}{chr(96)}.", "- **Decisión:** conservar el contrato entre los proyectos sucesivos y justificar las excepciones en el arranque.",""]
   if j in (1,5,9):
    o += ["| Contrato | Implementación | Evidencia |","|---|---|---|",f"| {title} | AceriaApp, punto 2.{i+1} | {chr(96)}{code}{chr(96)} |",""]
  o += [f"### Recapitulación del punto 2.{i+1}","El recorrido conecta los conceptos con una solución reproducible. La práctica debe verificar que las responsabilidades se separan correctamente y que la funcionalidad esperada se encuentra realmente conectada al proyecto.","","---"]
 put(BASE/"TEORIA/M02_TEORIA.md","\n".join(o)+"\n")
def excerpt(project,rel):
 p=project/rel
 if not p.is_file() or p.suffix!=".cs":return ""
 lines=p.read_text(encoding="utf-8").splitlines()
 if len(lines)>65:lines=lines[:45]+["// Continuar con el archivo real del proyecto"]
 return FENCE+"csharp\n"+"\n".join(lines)+"\n"+FENCE+"\n"
def practice():
 o=["# M02 — Prácticas de desarrollo de APIs REST","","**CURSO DE ARQUITECTURA HEXAGONAL Y MICROSERVICIOS AVANZADOS CON .NET 8**","**AUTOR: JAIME GALLO**","","## Contexto de trabajo","Cada punto reproduce una solución autónoma con src, tests, docs y AceriaApp.sln. El alumno dispone de la solución de referencia y reproduce sus decisiones contrastando cada paso con los archivos entregados. Entorno recomendado: Visual Studio 2026, SDK .NET 8 y SQL Server Express. La base de datos LocalDB puede utilizarse en Windows para escenarios compatibles de desarrollo.",""]
 for i,n in enumerate(NAMES):
  project=BASE/"PROYECTO"/n;pre=NAMES[i-1] if i else "M01/1.5"
  o += [f"## Punto 2.{i+1} — {LABEL[i]}","",f"**Solución:** {chr(96)}PROYECTO/{n}/AceriaApp.sln{chr(96)}. **Origen:** {pre}.",""]
  for j,title in enumerate(STEPS[i]):
   rel=FILES[i][j]; target=project/rel; step=f"2.{i+1}.{j+1}"
   cmd=f"dotnet test AceriaApp.sln" if "test" in title.lower() or "prueb" in title.lower() else "dotnet build AceriaApp.sln"
   o += [f"### PASO {step} — {title}","",
    f"**Acción 1:** Abrir en Visual Studio la solución {chr(96)}PROYECTO/{n}/AceriaApp.sln{chr(96)} y verificar que se está trabajando en el punto 2.{i+1}.",
    f"**Acción 2:** Localizar {chr(96)}{rel}{chr(96)} y comprobar su función dentro del proyecto acumulativo. No modificar la solución correspondiente a {pre}.",
    f"**Acción 3:** {title}. Revisar el contenido completo del elemento, las entradas necesarias y el resultado esperado, comparándolos con la explicación teórica del punto.",
    f"**Acción 4:** Desde la carpeta de la solución ejecutar {chr(96)}{cmd}{chr(96)} y comprobar la salida antes de continuar.",
    "",
    "**Por qué se hace:**",f"La actividad proporciona evidencia comprobable del elemento {chr(96)}{rel}{chr(96)} y mantiene la trazabilidad desde la teoría hasta el proyecto reproducible. El alumno debe distinguir un archivo preparado de un comportamiento conectado al servidor.","",
    "**Errores comunes:**",
    "- Editar el mismo archivo en la solución del punto previo y perder el estado acumulado.",
    "- Suponer que un método de extensión se ejecuta solo por estar definido en una clase.",
    "- Interpretar la presencia de un test como prueba de un comportamiento diferente del realmente comprobado.","",
    "**Verificación:**",f"Confirmar que el archivo o carpeta {chr(96)}{rel}{chr(96)} existe y que la compilación y las pruebas del punto terminan sin errores. Si falla la comprobación, identificar el nombre del proyecto y la aserción afectada.",""]
   if j in (5,6,7,8,14,15) and target.is_file() and target.suffix==".cs":
    o += ["**Código real de referencia:**","",excerpt(project,rel),"El alumno identifica tipo, parámetros, valor devuelto y caso de error en el archivo anterior.",""]
   if j==1:o+=["**Consola de comprobación:**","",FENCE+"powershell",f"cd M02_APIS_REST_ASPNET_CORE/PROYECTO/{n}","dotnet restore AceriaApp.sln","dotnet build AceriaApp.sln",FENCE,""]
   if "Comparar" in title:
    o += ["**Verificación íntegra en CMD desde la raíz del repositorio:**","",FENCE+"cmd",
     f'for %f in (M02_APIS_REST_ASPNET_CORE\\PROYECTO\\{pre}\\docs\\*.md) do fc /L "%f" "M02_APIS_REST_ASPNET_CORE\\PROYECTO\\{n}\\docs\\%~nxf"' if i else 'fc /L "M01_INTRODUCCION_MICROSERVICIOS\\PROYECTO\\1.5-buenas-practicas\\docs\\ADR-005-buenas-practicas.md" "M02_APIS_REST_ASPNET_CORE\\PROYECTO\\2.1-diseno-apis-rest\\docs\\ADR-005-buenas-practicas.md"',
     FENCE,"Para un archivo .bat debe utilizarse %%f; desde CMD interactivo se usa %f.",""]
  o += ["### Tabla de errores del ejercicio completo","","| Error | Causa | Solución |","|---|---|---|",
        "| No se encuentra la solución | Directorio incorrecto | Cambiar a la carpeta del punto y abrir AceriaApp.sln. |",
        "| No se resuelve un tipo | Proyecto o dependencia ausente | Comprobar csproj y ejecutar dotnet restore. |",
        "| No se publica Swagger | Entorno o middleware incorrecto | Contrastar Development con Production y consultar el JSON real. |",
        "| Fallan tests anteriores | Cambio en el estado heredado | Restaurar el archivo alterado desde la carpeta anterior. |",
        "| La documentación difiere del código | Contrato no actualizado | Comprobar ruta, modelo y respuesta con la API ejecutada. |","",
        "### Reto resuelto paso a paso",""]
  if i in (0,1):
   target="CatalogoUris" if i==0 else "CatalogoCombinaciones"
   source="DisenoRest" if i==0 else "CatalogoRecursos"
   expr="_uris.Count(u => validador.Validar(u).EsValida)" if i==0 else "_combinaciones.Count(c => validador.Validar(c).EsValida)"
   o += [f"**Reto:** ampliar {target} con un resumen de válidas, inválidas y porcentaje.","",
          "**Paso 1:** Crear un record con Validas, Invalidas y PorcentajeValidez.",
          "**Paso 2:** Agregar el método Resumen dentro de la clase indicada.",
          "**Paso 3:** Contar las entradas válidas a través del validador.",
          "**Paso 4:** Calcular las inválidas como total menos válidas.",
          "**Paso 5:** Proteger el denominador cuando el total sea cero.",
          "**Paso 6:** Incorporar un test con tres válidas y dos inválidas.",
          "**Paso 7:** Ejecutar el proyecto de pruebas y comprobar 60%.",
          "**Paso 8:** Conservar la solución previa sin alteraciones.","",
          f"**Referencia de cálculo:** {chr(96)}{expr}{chr(96)}. Esta ampliación está indicada en el código como reto, pero no forma parte del recuento base hasta que se implemente.",""]
  elif i==2:
   o += ["**Reto:** crear ActualizarOrdenRequest y un validador que rechace Guid.Empty.","","**Paso 1:** Crear el record con Guid Id, Cliente, Material y Cantidad.","**Paso 2:** Crear AbstractValidator del nuevo record.","**Paso 3:** Configurar RuleFor(x => x.Id).NotEmpty().","**Paso 4:** Añadir reglas de límites de cantidad.","**Paso 5:** Crear un test con Guid.Empty.","**Paso 6:** Crear un test con Guid.NewGuid().","**Paso 7:** Ejecutar dotnet test y comprobar ocho tests en el proyecto.","**Paso 8:** Verificar que no se modificó 2.2.",""]
  else:
   o += ["**Reto:** añadir EsEntornoDeProduccion a ConfiguracionOpenApi.","","**Paso 1:** Abrir ConfiguracionOpenApi.cs.","**Paso 2:** Implementar string.Equals con Production y OrdinalIgnoreCase.","**Paso 3:** Guardar sin cambiar EsEntornoDeDesarrollo.","**Paso 4:** Incorporar test para Production.","**Paso 5:** Incorporar aserción negativa para Development.","**Paso 6:** Ejecutar los tests de Documentacion.Tests.","**Paso 7:** Volver a comprobar la ausencia de Swagger JSON en Production.","**Paso 8:** Conservar el punto 2.3 sin cambios.",""]
  o += ["### Resultado esperado","",
  f"- Solución independiente con {7+i} proyectos; una API y {6+i} proyectos de tests.",
  f"- Recuento acumulado previsto de pruebas: {[31,36,42,51][i]}.",
  "- Todos los documentos y proyectos de los puntos anteriores permanecen accesibles.","",
  f"### Conclusión y enlace tras el punto 2.{i+1}","",
  f"El punto 2.{i+1} vincula {LABEL[i].lower()} con clases y comprobaciones concretas. El alumnado puede inspeccionar el proyecto y explicar los resultados observados antes de abordar el siguiente punto.","","---"]
 put(BASE/"PRACTICAS/M02_PRACTICAS.md","\n".join(o)+"\n")
def run():
 raise SystemExit("BLOQUEADO: este generador sintético recorta los textos originales del usuario. Sustituir por un procedimiento que use copias literales verificables de los puntos 2.1 a 2.4, aplique exclusivamente correcciones trazadas y produzca prácticas respaldadas por código activable paso a paso. No sobrescribir los Markdown de M02.")
def run_ANTIGUO_DESHABILITADO():
 if not (BASE/"PROYECTO"/NAMES[-1]).exists():raise SystemExit("Falta generar proyectos M02")
 for d in (BASE/"TEORIA",BASE/"PRACTICAS"):
  for i in range(4):make_svg(i,d/"figuras")
 teoria();practice()
 s=(BASE/"TEORIA/M02_TEORIA.md").read_text(encoding="utf-8")
 p=(BASE/"PRACTICAS/M02_PRACTICAS.md").read_text(encoding="utf-8")
 assert len(re.findall(r"^### Bloque [0-9]+",s,re.M))==40
 assert len(re.findall(r"^### PASO 2\.[0-9]+\.[0-9]+",p,re.M))==96
 for i in range(4):
  assert len(STEPS[i])==24 and len(FILES[i])==24 and len(TOPICS[i])==10
 print(json.dumps({"teoria_palabras":len(s.split()),"practicas_palabras":len(p.split()),"bloques":40,"pasos":96},ensure_ascii=False))
if __name__=="__main__":run()
