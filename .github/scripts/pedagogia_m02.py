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
    return (f"**Acción adicional:** Comparar **todos** los {count} documentos Markdown heredados "
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
    text=replace(text,"once documentos","trece documentos")
    text=insert_docs(text,"2.3",22,"2.2-recursos-verbos-codigos","2.3-validacion-peticiones",13)
    text=replace(text,"- Registro de validadores en `Program.cs` con `AddValidatorsFromAssemblyContaining`.",
                     "- Archivo nuevo `Validacion/ValidacionExtensions.cs` con el registro de validadores.\n- El `Program.cs` de la copia 2.3 incorpora solo dos líneas aditivas: `using AceriaApp.Monolito.Api.Validacion;` y `builder.Services.AddValidacion();`.")
    text=replace(text,"- No se ha modificado ningún archivo del punto 2.2 excepto `Program.cs`, que añade líneas nuevas sin eliminar las existentes.",
                     "- La solución independiente del punto 2.2 no se modifica; solo cambia `Program.cs` de la copia 2.3.")
    text=replace(text,"con tres clases nuevas","con cuatro clases nuevas")
    text=replace(text,"tres clases nuevas","cuatro clases nuevas")
    text=replace(text,"Program.cs modificado solo con líneas añadidas: using FluentValidation;, using AceriaApp.Monolito.Api.Validacion; y builder.Services.AddValidatorsFromAssemblyContaining<CrearOrdenRequestValidator>();.",
                     "Program.cs de la copia 2.3 modificado solo con dos líneas aditivas: using AceriaApp.Monolito.Api.Validacion; y builder.Services.AddValidacion();.")
    return text

