"""Correcciones docentes LOCALIZADAS; nunca modifica fuentes-originales.

El original de cada punto permanece archivado. Los cambios se aplican a
una COPIA generada y se recuentan para que el alumnado vea el itinerario real.
"""
from __future__ import annotations

import re

def step(text: str, point: str, number: int, new: str) -> str:
    start=f"### PASO {point}.{number} —"
    match=re.search(r"(?m)^"+re.escape(start)+r".*$",text)
    if not match:
        raise ValueError(f"No existe {start}")
    next_head=re.search(r"(?m)^### (?:PASO "+re.escape(point)+r"\.\d+ —|Errores comunes del ejercicio completo|Reto resuelto paso a paso|Resultado esperado)",text[match.end():])
    if not next_head:
        raise ValueError(f"No puedo localizar el final de {start}")
    a=match.start()
    b=match.end()+next_head.start()
    return text[:a]+new.strip()+"\n\n"+text[b:]

def replace(text: str, old: str, new: str, *, count=None) -> str:
    seen=text.count(old)
    if count is not None and seen != count:
        raise ValueError(f"Reemplazo esperado {count}, encontrado {seen}: {old[:120]}")
    if not seen:
        raise ValueError(f"Falta texto que debía corregirse: {old[:120]}")
    return text.replace(old,new)

def replace_in_step(text: str, point: str, number: int, old: str, new: str):
    start=text.index(f"### PASO {point}.{number} —")
    m=re.search(r"(?m)^### PASO "+re.escape(point)+r"\.\d+ —",text[start+10:])
    end=start+10+m.start() if m else len(text)
    chunk=replace(text[start:end],old,new)
    return text[:start]+chunk+text[end:]

def comprobacion_docs(point: str, previous: str, actual: str, count: int):
    return (f"- **Acción 6:** Comparar **todos** los {count} documentos Markdown heredados "
            "en lugar de limitarse a los dos ejemplos anteriores. Desde "
            "`C:\\cursos\\AceriaApp`, en la consola **cmd.exe** de Windows, ejecutar:\n\n"
            "```bat\n"
            f"for %f in (modulo-2-apis-rest-aspnet-core\\{previous}\\docs\\*.md) do @fc.exe /L \"%f\" \"modulo-2-apis-rest-aspnet-core\\{actual}\\docs\\%~nxf\"\n"
            "```\n\n"
            f"**Verificación ampliada:** aparecen {count} comparaciones iguales y "
            "no falta ningún documento. En PowerShell se debe usar `fc.exe`, "
            "no el alias `fc`.\n\n").replace("`","`")

def insert_docs(text: str,point: str,number: int,previous: str,actual: str,count: int):
    start=text.index(f"### PASO {point}.{number} —")
    m=re.search(r"(?m)^### PASO "+re.escape(point)+r"\.\d+ —",text[start+10:])
    end=start+10+m.start() if m else len(text)
    chunk=text[start:end]
    target="**Por qué se hace:**"
    if target not in chunk: raise ValueError("Falta 'Por qué se hace' en "+point)
    # Evitar duplicar la acción de 2.2 ya añadida en versión anterior.
    if point=="2.2" and "- **Acción 6:** Comparar también **todos**" in chunk:
        chunk=re.sub(r"- \*\*Acción 6:\*\* Comparar también \*\*todos\*\*.*?(?=\*\*Por qué se hace:\*\*)","",chunk,flags=re.S)
    chunk=chunk.replace(target,comprobacion_docs(point,previous,actual,count)+target,1)
    chunk=chunk.replace("**Verificación:** los dos documentos",f"**Verificación:** los {count} documentos")
    return text[:start]+chunk+text[end:]

P23_STEP_15 = """### PASO 2.3.15 — Crear CrearOrdenRequestTests.cs

**Acción 1:** En el Explorador de soluciones, abrir `tests/AceriaApp.Validacion.Tests`.

**Acción 2:** Agregar una clase llamada `CrearOrdenRequestTests.cs`; no crear `ValidationFilterTests.cs` porque estos dos casos verifican únicamente la asignación de propiedades del `record`.

**Acción 3:** Escribir este código y explicar el constructor y cada aserción:

```csharp
using AceriaApp.Monolito.Api.Validacion;
using FluentAssertions;
using Xunit;

namespace AceriaApp.Validacion.Tests;

public class CrearOrdenRequestTests
{
    [Fact]
    public void CrearOrdenRequest_ConDatosValidos_AsignaValores()
    {
        var peticion = new CrearOrdenRequest("ACX-001", "CHAPA-3MM", 10);

        peticion.Cliente.Should().Be("ACX-001");
        peticion.Material.Should().Be("CHAPA-3MM");
        peticion.Cantidad.Should().Be(10);
    }

    [Fact]
    public void CrearOrdenRequest_ConClienteVacio_AsignaCadenaVacia()
    {
        var peticion = new CrearOrdenRequest(string.Empty, "CHAPA-3MM", 10);

        peticion.Cliente.Should().BeEmpty();
    }
}
```

**Acción 4:** Guardar. Localizar el bloque `INICIO PASO 2.3.15` de la copia de referencia, descomentarlo y compilar.

**Acción 5:** Ejecutar los dos tests de esta clase. En el primero se comprueban `Cliente`, `Material` y `Cantidad`; en el segundo se comprueba que el record conserva la cadena vacía.

**Por qué se hace:** estas pruebas corresponden al contrato de datos, no al comportamiento HTTP de un filtro. El nombre de la clase debe comunicar lo que realmente se verifica.

**Errores comunes:**
- Olvidar el `using` del espacio de nombres de producción.
- Confundir creación de un record con ejecución de FluentValidation.
- Conservar `ValidationFilterTests.cs` sin realizar pruebas reales del filtro.

**Verificación:** el archivo contiene exactamente dos métodos `[Fact]` y no existe `ValidationFilterTests.cs`.
"""

P23_STEP_16 = """### PASO 2.3.16 — Crear ValidacionExtensions y registrar en Program.cs

**Acción 1:** En la carpeta `src/AceriaApp.Monolito.Api/Validacion`, crear `ValidacionExtensions.cs`.

**Acción 2:** Escribir y explicar el método de extensión del contenedor:

```csharp
using FluentValidation;

namespace AceriaApp.Monolito.Api.Validacion;

public static class ValidacionExtensions
{
    public static IServiceCollection AddValidacion(this IServiceCollection services)
    {
        services.AddValidatorsFromAssemblyContaining<CrearOrdenRequestValidator>();
        return services;
    }
}
```

**Acción 3:** Abrir `Program.cs` de **la copia 2.3**, sin tocar el de 2.2.

**Acción 4:** Añadir únicamente esta línea `using`, al principio:

```csharp
using AceriaApp.Monolito.Api.Validacion;
```

**Acción 5:** Después de `builder.Services.AddSwaggerGen();`, añadir esta llamada:

```csharp
builder.Services.AddValidacion();
```

**Acción 6:** Activar progresivamente el bloque marcado `INICIO PASO 2.3.16` en la solución de referencia; comprobar que `Program.cs` solo incorpora esas **dos líneas aditivas**.

**Acción 7:** Compilar y ejecutar los tests del punto. Comprobar que el validador se registra por DI y que el código heredado sigue funcionando.

**Por qué se hace:** el registro del validador se concentra en una extensión nueva. El registro **no ejecuta** la validación automáticamente: para ejecutar el filtro es necesario asociarlo a un endpoint con `AddEndpointFilter`.

**Errores comunes:**
- Registrar de nuevo el validador directamente en `Program.cs`.
- No retornar `services`.
- Omitir el `using` de `Validacion`.
- Confundir registro en DI con la validación efectiva de cada petición.

**Verificación:** `ValidacionExtensions.cs` contiene `AddValidacion`, la copia 2.3 de `Program.cs` utiliza la extensión y la copia 2.2 permanece intacta.
"""

def p23_practicas(text: str):
    text=step(text,"2.3",15,P23_STEP_15.replace("`","`"))  # delimitadores resueltos por apply()
    text=step(text,"2.3",16,P23_STEP_16.replace("`","`"))
    text=replace_in_step(text,"2.3",5,"FluentValidation.AspNetCore","FluentValidation.DependencyInjectionExtensions")
    text=replace(text,"Falta el paquete FluentValidation.AspNetCore","Falta el paquete FluentValidation.DependencyInjectionExtensions")
    text=replace(text,"dotnet add package FluentValidation.AspNetCore","dotnet add package FluentValidation.DependencyInjectionExtensions")
    text=replace(text,"con diez proyectos","con nueve proyectos")
    text=replace(text,"El punto 2.3 parte del contenido del punto 2.2 sin modificar ningún archivo existente: solo añade archivos nuevos.",
                 "El punto 2.3 parte de una copia completa del punto 2.2, añade archivos y modifica únicamente Program.cs de la copia 2.3 con dos líneas nuevas para registrar los validadores; la solución independiente 2.2 permanece intacta.")
    text=replace(text,"once documentos","trece documentos")
    text=insert_docs(text,"2.3",22,"2.2-recursos-verbos-codigos","2.3-validacion-peticiones",13)
    text=replace(text,"- Registro de validadores en `Program.cs` con `AddValidatorsFromAssemblyContaining`.",
                     "- Archivo nuevo `Validacion/ValidacionExtensions.cs` con el registro de validadores.\n- El `Program.cs` de la copia 2.3 incorpora solo dos líneas aditivas: `using AceriaApp.Monolito.Api.Validacion;` y `builder.Services.AddValidacion();`.")
    text=replace(text,"- No se ha modificado ningún archivo del punto 2.2 excepto `Program.cs`, que añade líneas nuevas sin eliminar las existentes.",
                     "- La solución independiente del punto 2.2 no se modifica; solo cambia `Program.cs` de la copia 2.3.")
    text=replace(text,"con tres clases nuevas","con cuatro clases nuevas")
    text=text.replace("tres clases nuevas","cuatro clases nuevas")
    text=replace(text,"Program.cs modificado solo con líneas añadidas: using FluentValidation;, using AceriaApp.Monolito.Api.Validacion; y builder.Services.AddValidatorsFromAssemblyContaining<CrearOrdenRequestValidator>();.",
                     "Program.cs de la copia 2.3 modificado solo con dos líneas aditivas: using AceriaApp.Monolito.Api.Validacion; y builder.Services.AddValidacion();.")
    return text


P24_STEP_9 = """### PASO 2.4.9 — Crear DocumentacionExtensions e integrar Swagger real

**Acción 1:** Crear `src/AceriaApp.Monolito.Api/Documentacion/DocumentacionExtensions.cs` en la copia 2.4. No crear `ConstructorDocumentoOpenApi`: fabricar una cadena YAML no es generar el contrato real.

**Acción 2:** Escribir y explicar este código:

```csharp
using Microsoft.OpenApi.Models;

namespace AceriaApp.Monolito.Api.Documentacion;

public static class DocumentacionExtensions
{
    public static IServiceCollection AddDocumentacionOpenApi(
        this IServiceCollection services, MetadatosApi metadatos)
    {
        services.AddEndpointsApiExplorer();
        services.AddSwaggerGen(options =>
        {
            options.SwaggerDoc(metadatos.Version, new OpenApiInfo
            {
                Title = metadatos.Titulo,
                Version = metadatos.Version,
                Description = metadatos.Descripcion,
                Contact = new OpenApiContact
                {
                    Name = metadatos.ContactoNombre,
                    Email = metadatos.ContactoEmail
                }
            });
        });
        return services;
    }

    public static WebApplication UseDocumentacionOpenApi(
        this WebApplication app, ConfiguracionOpenApi configuracion)
    {
        if (configuracion.EsEntornoDeDesarrollo(app.Environment.EnvironmentName))
        {
            app.UseSwagger();
            if (configuracion.PublicarSwaggerUI)
            {
                app.UseSwaggerUI(options =>
                {
                    options.SwaggerEndpoint(
                        configuracion.RutaDocumento,
                        configuracion.NombreDocumento);
                });
            }
        }
        return app;
    }
}
```

**Acción 3:** Comprobar que la API tiene una referencia al paquete `Swashbuckle.AspNetCore`. En la solución de referencia, descomentar el bloque `INICIO PASO 2.4.9`.

**Acción 4:** En el `Program.cs` de **la copia 2.4**, añadir `using AceriaApp.Monolito.Api.Documentacion;`.

**Acción 5:** Sustituir las dos llamadas heredadas:

```csharp
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
```

por la única llamada real:

```csharp
builder.Services.AddDocumentacionOpenApi(new MetadatosApi());
```

**Acción 6:** Sustituir el bloque heredado que publica Swagger por:

```csharp
app.UseDocumentacionOpenApi(new ConfiguracionOpenApi());
```

**Acción 7:** Guardar, compilar e iniciar la aplicación en entorno `Development`.

**Acción 8:** Solicitar `/swagger/v1/swagger.json` y comprobar que es JSON OpenAPI con `info.title`, `info.version` y `paths["/api/v1/ordenes"]`. En `Production`, verificar que ese endpoint no se sirve.

**Por qué se hace:** estas extensiones registran y publican el documento **real** generado a partir de la API. No sirve crear código sin invocarlo en `Program.cs`. La solución 2.3 anterior no se modifica.

**Errores comunes:**
- Duplicar `AddSwaggerGen` en `Program.cs`.
- Crear la extensión pero no llamarla.
- Omitir `using Microsoft.OpenApi.Models;`.
- No activar el bloque del paso antes de compilar.
- Publicar el documento OpenAPI en producción.

**Verificación:** un GET real al documento Swagger en `Development` devuelve estado 200 y las rutas de la API; en `Production` devuelve 404.
"""

P24_STEP_15 = """### PASO 2.4.15 — Crear DocumentacionExtensionsTests y probar el contrato HTTP

**Acción 1:** Añadir al proyecto `AceriaApp.Documentacion.Tests` el paquete de integración compatible con .NET 8:

```powershell
dotnet add tests\\AceriaApp.Documentacion.Tests\\AceriaApp.Documentacion.Tests.csproj package Microsoft.AspNetCore.Mvc.Testing --version 8.0.0
```

**Acción 2:** Crear `src/AceriaApp.Monolito.Api/Program.Public.cs` dentro del proyecto de API para que las pruebas puedan arrancar la aplicación con `WebApplicationFactory<Program>`:

```csharp
public partial class Program { }
```

**Acción 3:** Crear el archivo `tests/AceriaApp.Documentacion.Tests/DocumentacionExtensionsTests.cs` y escribir estos tres tests de integración:

```csharp
using System.Net;
using System.Text.Json;
using FluentAssertions;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace AceriaApp.Documentacion.Tests;

public class DocumentacionExtensionsTests
{
    [Fact]
    public async Task SwaggerJson_EnDevelopment_ContieneMetadatosV1()
    {
        using var factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(b => b.UseEnvironment("Development"));
        using var client = factory.CreateClient();
        using var response = await client.GetAsync("/swagger/v1/swagger.json");

        response.StatusCode.Should().Be(HttpStatusCode.OK);
        using var json = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        var info = json.RootElement.GetProperty("info");
        info.GetProperty("title").GetString().Should().Be("AceriaApp.Monolito.Api");
        info.GetProperty("version").GetString().Should().Be("v1");
    }

    [Fact]
    public async Task SwaggerJson_EnDevelopment_DescribeLosEndpointsReales()
    {
        using var factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(b => b.UseEnvironment("Development"));
        using var client = factory.CreateClient();
        using var response = await client.GetAsync("/swagger/v1/swagger.json");

        response.StatusCode.Should().Be(HttpStatusCode.OK);
        using var json = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        var ordenes = json.RootElement.GetProperty("paths")
            .GetProperty("/api/v1/ordenes");
        ordenes.TryGetProperty("get", out _).Should().BeTrue();
        ordenes.TryGetProperty("post", out _).Should().BeTrue();
    }

    [Fact]
    public async Task SwaggerJson_EnProduction_NoEstaPublicado()
    {
        using var factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(b => b.UseEnvironment("Production"));
        using var client = factory.CreateClient();
        using var response = await client.GetAsync("/swagger/v1/swagger.json");

        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
}
```

**Acción 4:** Guardar los archivos y descomentar los bloques `INICIO PASO 2.4.15` en la copia de referencia.

**Acción 5:** Compilar y ejecutar los tres tests de integración, junto con los dos de `MetadatosApiTests` y los cuatro de `ConfiguracionOpenApiTests`.

**Por qué se hace:** un test que compara dos cadenas YAML no demuestra que la API sirva un documento OpenAPI. Estas pruebas arrancan la aplicación real en memoria, descargan JSON y contrastan rutas y entorno.

**Errores comunes:**
- Olvidar `Microsoft.AspNetCore.Mvc.Testing` o `Program.Public.cs`.
- No haber conectado las extensiones en `Program.cs`.
- Comprobar solo valores del contenedor de DI, sin realizar una petición HTTP.
- Olvidar configurar `Development` y `Production` en los tests.

**Verificación:** pasan **tres** pruebas HTTP reales. El proyecto tiene **nueve** tests base en total; la solución acumula **51** tests base.
"""

P24_RETO = """### Reto resuelto paso a paso

**Reto:** distinguir explícitamente producción de desarrollo con el método `ConfiguracionOpenApi.EsEntornoDeProduccion` y comprobar ambas opciones en una prueba.

**Paso 1:** Abrir `ConfiguracionOpenApi.cs` de la copia 2.4 y localizar la clase.

**Paso 2:** Añadir el método siguiente conservando los métodos anteriores:

```csharp
public bool EsEntornoDeProduccion(string entorno)
{
    return string.Equals(entorno, "Production", StringComparison.OrdinalIgnoreCase);
}
```

**Paso 3:** Comprobar que `EsEntornoDeDesarrollo` no ha cambiado.

**Paso 4:** Abrir `ConfiguracionOpenApiTests.cs` y añadir:

```csharp
[Fact]
public void EsEntornoDeProduccion_DistingueProductionDeDevelopment()
{
    _configuracion.EsEntornoDeProduccion("Production").Should().BeTrue();
    _configuracion.EsEntornoDeProduccion("Development").Should().BeFalse();
}
```

**Paso 5:** Guardar y descomentar los bloques correspondientes al reto en la solución de referencia.

**Paso 6:** Ejecutar `dotnet test tests\\AceriaApp.Documentacion.Tests\\AceriaApp.Documentacion.Tests.csproj`.

**Paso 7:** Comprobar **10 tests** en el punto 2.4 tras realizar el reto, y **52** en total si no se han incorporado acumulativamente otros retos opcionales.

**Paso 8:** Registrar el cambio cuando realmente se haya completado.

**Por qué se hace:** distingue explícitamente los dos entornos sin recurrir a una clase que fabrique documentos ficticios.

**Errores comunes:** no conservar el método de desarrollo, comparar con igualdad sensible a mayúsculas o no activar el nuevo test.

**Verificación:** Production devuelve verdadero; Development devuelve falso, y el test lo demuestra.
"""

def p24_practicas(text: str):
    text=step(text,"2.4",9,P24_STEP_9)
    text=step(text,"2.4",15,P24_STEP_15)
    # Sustituir el reto entero, nunca concatenar dos retos incompatibles.
    a=text.index("### Reto resuelto paso a paso")
    b=text.index("### Resultado esperado",a)
    text=text[:a]+P24_RETO.strip()+"\n\n"+text[b:]

    # El literal ORIGINAL permanece en la fuente; solo el DOCENTE cambia.
    text=replace(text,"equipo@acería.local","equipo@acerialocal")
    text=replace(text,"Cuarenta y cuatro pruebas unitarias acumuladas en diez proyectos de tests.",
                 "Cincuenta y una pruebas unitarias acumuladas en nueve proyectos de pruebas; diez proyectos en la solución.")
    text=replace(text,"con once proyectos","con diez proyectos")
    text=replace(text,"El punto 2.4 parte del contenido del punto 2.3 sin modificar ningún archivo existente: solo añade archivos nuevos.",
                 "El punto 2.4 copia íntegramente el estado 2.3 y añade archivos nuevos; como integración necesaria, modifica solo Program.cs de la copia 2.4 para invocar las extensiones OpenAPI. La solución 2.3 permanece intacta.")
    text=replace(text,"doce documentos","quince documentos")
    text=insert_docs(text,"2.4",21,"2.3-validacion-peticiones","2.4-documentacion-openapi",15)

    # README y resultado esperado: las extensiones sí están conectadas.
    text=replace(text,"`MetadatosApi`, `ConfiguracionOpenApi` y `ConstructorDocumentoOpenApi`",
                 "`MetadatosApi`, `ConfiguracionOpenApi` y `DocumentacionExtensions`")
    text=replace(text,"Las clases MetadatosApi, ConfiguracionOpenApi y ConstructorDocumentoOpenApi",
                 "Las clases MetadatosApi, ConfiguracionOpenApi y DocumentacionExtensions")
    text=replace(text,"Nueve tests nuevos en `tests/AceriaApp.Documentacion.Tests`.",
                 "Nueve tests nuevos en `tests/AceriaApp.Documentacion.Tests`, incluidos tres tests HTTP del documento real.")
    text=replace(text,"- No se ha modificado ningún archivo del punto 2.3.",
                 "- La solución independiente 2.3 no se modifica; `Program.cs` de la copia 2.4 se adapta para conectar las extensiones OpenAPI.")
    text=replace(text,"- Registro de validadores en `Program.cs` con `AddValidatorsFromAssemblyContaining`.",
                 "- Registro de validadores en una extensión de servicios.") if "- Registro de validadores en `Program.cs` con `AddValidatorsFromAssemblyContaining`." in text else text
    text=replace(text,"Se implementan clases de configuración y de construcción de la cabecera del documento para verificar la coherencia.",
                 "Se implementa la extensión de Swagger real y se comprueba el contrato generado mediante peticiones HTTP.")
    text=replace(text,"la clase ConstructorDocumentoOpenApi","la extensión DocumentacionExtensions") if "la clase ConstructorDocumentoOpenApi" in text else text
    text=replace(text,"NullReferenceException en ConfiguracionOpenApi No se inicializa Metadatos con new() Inicializar con new()",
                 "NullReferenceException en ConfiguracionOpenApi No se inicializa Metadatos con new() Inicializar con new()")
    text=replace(text,"La cabecera no incluye la versión El método ConstruirCabecera no la incluye Revisar la interpolación de la cadena",
                 "El JSON Swagger no incluye la versión No se registró SwaggerDoc con los metadatos Revisar DocumentacionExtensions")
    text=replace(text,"La ruta no incluye la versión El método ConstruirRuta no la incluye Revisar la interpolación de la cadena",
                 "El endpoint Swagger no aparece Falta la integración en Program.cs Comprobar AddDocumentacionOpenApi y UseDocumentacionOpenApi")
    text=replace(text,"El proyecto tests/AceriaApp.Documentacion.Tests con nueve tests (diez tras el reto).",
                 "El proyecto tests/AceriaApp.Documentacion.Tests con nueve tests, tres de integración HTTP (diez tras el reto).")
    return text

def aplicar(text: str, point: str, tipo: str) -> tuple[str,list[str]]:
    """Corrige solamente la copia docente. Si cambia la fuente, FALLA."""
    cambios=[]
    if tipo!="PRACTICAS":
        return text,cambios
    if point=="2.2":
        text=insert_docs(text,"2.2",21,"2.1-diseno-apis-rest","2.2-recursos-verbos-codigos",11)
        cambios=["2.2.21 comparar 11 documentos heredados"]
    elif point=="2.3":
        text=p23_practicas(text)
        cambios=["2.3.5 DI moderno", "2.3.15 test record",
                 "2.3.16 extensión", "2.3.22 comparación completa",
                 "recuentos y README"]
    elif point=="2.4":
        text=p24_practicas(text)
        cambios=["2.4.4 51 tests", "2.4.6 y 13 correo",
                 "2.4.9 Swagger real", "2.4.15 HTTP",
                 "2.4.21 comparación completa", "reto Production",
                 "recuentos y README"]
    return text,cambios
