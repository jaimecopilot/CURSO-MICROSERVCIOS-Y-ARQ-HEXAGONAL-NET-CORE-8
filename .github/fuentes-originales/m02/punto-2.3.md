Punto 2.3 — Validación de peticiones

Módulo 2: Desarrollo de APIs REST con ASP.NET Core
Duración: 53 minutos (26 minutos de teoría + 27 minutos de práctica)
Objetivos de aprendizaje:

· Comprender por qué la validación de peticiones es obligatoria en una API REST.
· Identificar los tres niveles de validación: sintáctica, semántica y de negocio.
· Comprender el papel de FluentValidation en ASP.NET Core.
· Comprender la relación entre validación fallida, código 400 y problem details.
· Añadir al proyecto AceriaApp una clase de validación de peticiones con FluentValidation y un test unitario que verifique la validación.


---

PARTE TEÓRICA (26 minutos)

Bloque 1 — La validación como contrato de entrada

La validación de peticiones es el proceso de comprobar que los datos recibidos cumplen las reglas definidas por el servicio. Sin validación, el servicio procesa datos incorrectos y produce resultados incorrectos o falla de forma imprevisible. La validación es un contrato de entrada: define qué datos acepta el servicio y qué datos rechaza. El contrato se documenta y se verifica en cada petición. La validación no es una tarea opcional ni una capa de defensa secundaria: es la primera línea de defensa de la API. Un servicio sin validación es un servicio que delega la responsabilidad de los datos al cliente.

Flujo de la validación:  
  
Cliente → Petición → Validación sintáctica → Validación semántica  
       → Validación de negocio → Procesamiento → Respuesta

Línea 1: Cliente → Petición → el cliente envía la petición al servidor.
Línea 2: → Validación sintáctica → primera comprobación, formato correcto.
Línea 3: → Validación semántica → segunda comprobación, significado correcto.
Línea 4: → Validación de negocio → tercera comprobación, reglas del dominio.
Línea 5: → Procesamiento → se procesa la petición si pasa las tres validaciones.
Línea 6: → Respuesta → se devuelve el resultado al cliente.

La validación se organiza en tres niveles que se aplican de forma secuencial. El primer nivel es la validación sintáctica, que comprueba que el formato de la petición es correcto. El segundo nivel es la validación semántica, que comprueba que los valores tienen sentido en el contexto del recurso. El tercer nivel es la validación de negocio, que comprueba que los datos cumplen las reglas del dominio. Los tres niveles se aplican en orden: si falla el primero, no se aplican los siguientes. La aplicación secuencial evita procesar datos que no pueden ser válidos en ningún caso.

La ausencia de validación produce tres consecuencias medibles. La primera es el incremento de errores en producción, porque los datos incorrectos llegan al procesamiento. La segunda es la dificultad de diagnóstico, porque el error se manifiesta lejos de la causa. La tercera es la pérdida de confianza del consumidor, porque la API no garantiza un contrato estable. Las tres consecuencias se corrigen con la adopción sistemática de la validación en tres niveles. La validación no elimina todos los errores, pero garantiza que los datos procesados cumplen el contrato de entrada.


---

Bloque 2 — Validación sintáctica

La validación sintáctica comprueba que la petición tiene el formato correcto. Se aplica antes de cualquier otra validación. En una API REST, la validación sintáctica incluye la comprobación del tipo de contenido, la comprobación del formato JSON, la comprobación de los tipos de datos de los campos y la comprobación de la presencia de los campos obligatorios. Un JSON mal formado produce un código 400 con un mensaje que indica el error de sintaxis. Un campo con un tipo incorrecto produce un código 400 con un mensaje que indica el campo y el tipo esperado. La validación sintáctica la realiza el framework en la mayoría de los casos.

public record CrearOrdenRequest(  
    string Cliente,  
    string Material,  
    int Cantidad);

Línea 1: public record CrearOrdenRequest( → declara el contrato de entrada.
Línea 2: string Cliente, → campo obligatorio de tipo string.
Línea 3: string Material, → campo obligatorio de tipo string.
Línea 4: int Cantidad); → campo obligatorio de tipo entero.

La validación sintáctica se apoya en el sistema de tipos del lenguaje. Un record con tipos no anulables obliga al framework a rechazar peticiones que no incluyan los campos. Un record con tipos anulables permite que los campos sean opcionales. La elección entre tipos anulables y no anulables es una decisión de diseño que se documenta en el contrato. La validación sintáctica también se apoya en los atributos de enlace de parámetros, que indican de dónde se obtiene cada valor. La combinación de tipos y atributos define la primera línea de defensa de la API.


---

Bloque 3 — Validación semántica

La validación semántica comprueba que los valores de la petición tienen sentido en el contexto del recurso. Se aplica después de la validación sintáctica. En una API REST, la validación semántica incluye la comprobación de rangos, la comprobación de formatos específicos, la comprobación de longitudes máximas y mínimas y la comprobación de coherencia entre campos. Un campo Cantidad con valor negativo falla la validación semántica. Un campo Email con formato incorrecto falla la validación semántica. Un campo FechaFin anterior a FechaInicio falla la validación semántica. La validación semántica se implementa con reglas específicas para cada campo.

public class CrearOrdenRequestValidator : AbstractValidator<CrearOrdenRequest>  
{  
    public CrearOrdenRequestValidator()  
    {  
        RuleFor(x => x.Cliente)  
            .NotEmpty().WithMessage("El cliente es obligatorio.")  
            .MaximumLength(100).WithMessage("El cliente no puede superar 100 caracteres.");  
  
        RuleFor(x => x.Material)  
            .NotEmpty().WithMessage("El material es obligatorio.")  
            .MaximumLength(100).WithMessage("El material no puede superar 100 caracteres.");  
  
        RuleFor(x => x.Cantidad)  
            .GreaterThan(0).WithMessage("La cantidad debe ser mayor que cero.")  
            .LessThanOrEqualTo(10000).WithMessage("La cantidad no puede superar 10000.");  
    }  
}

Línea 1: public class CrearOrdenRequestValidator : AbstractValidator<CrearOrdenRequest> → declara el validador.
Línea 2: { → abre el cuerpo de la clase.
Línea 3: public CrearOrdenRequestValidator() → constructor del validador.
Línea 4: { → abre el cuerpo del constructor.
Línea 5: RuleFor(x => x.Cliente) → comienza la regla para el campo Cliente.
Línea 6: .NotEmpty().WithMessage("El cliente es obligatorio.") → no puede estar vacío.
Línea 7: .MaximumLength(100).WithMessage("El cliente no puede superar 100 caracteres."); → longitud máxima.
Línea 8: RuleFor(x => x.Material) → comienza la regla para el campo Material.
Línea 9: .NotEmpty().WithMessage("El material es obligatorio.") → no puede estar vacío.
Línea 10: .MaximumLength(100).WithMessage("El material no puede superar 100 caracteres."); → longitud máxima.
Línea 11: RuleFor(x => x.Cantidad) → comienza la regla para el campo Cantidad.
Línea 12: .GreaterThan(0).WithMessage("La cantidad debe ser mayor que cero.") → mayor que cero.
Línea 13: .LessThanOrEqualTo(10000).WithMessage("La cantidad no puede superar 10000."); → límite superior.
Línea 14: } → cierra el constructor.
Línea 15: } → cierra la clase.

La validación semántica tiene dos consecuencias prácticas. La primera es que cada campo tiene reglas explícitas y documentadas. La segunda es que los mensajes de error son específicos y útiles para el cliente. La combinación de ambas mejora la experiencia del consumidor y reduce el tiempo de integración. La validación semántica no comprueba reglas de negocio: comprueba que los valores son coherentes en el contexto del recurso. Las reglas de negocio se aplican en el siguiente nivel.


---

Bloque 4 — Validación de negocio

La validación de negocio comprueba que los datos cumplen las reglas del dominio. Se aplica después de la validación semántica. En una API REST, la validación de negocio incluye la comprobación de unicidad, la comprobación de existencia de referencias y la comprobación de reglas específicas del dominio. Un Cliente que no existe falla la validación de negocio. Un Material que está bloqueado falla la validación de negocio. Una Orden con más líneas de las permitidas falla la validación de negocio. La validación de negocio se implementa en la capa de aplicación o en el dominio, no en el validador de la petición.

public class OrdenServicio  
{  
    private readonly AceriaDbContext _db;  
  
    public OrdenServicio(AceriaDbContext db)  
    {  
        _db = db;  
    }  
  
    public async Task<bool> ClienteExisteAsync(string cliente)  
    {  
        return await _db.Clientes.AnyAsync(c => c.Nombre == cliente);  
    }  
  
    public async Task<bool> MaterialDisponibleAsync(string material, int cantidad)  
    {  
        var stock = await _db.Materiales  
            .Where(m => m.Nombre == material)  
            .Select(m => m.Stock)  
            .FirstOrDefaultAsync();  
        return stock >= cantidad;  
    }  
}

Línea 1: public class OrdenServicio → declara el servicio de aplicación.
Línea 2: { → abre el cuerpo de la clase.
Línea 3: private readonly AceriaDbContext _db; → campo para el contexto de base de datos.
Línea 4: public OrdenServicio(AceriaDbContext db) → constructor.
Línea 5: { → abre el cuerpo del constructor.
Línea 6: _db = db; → asigna el contexto al campo.
Línea 7: } → cierra el constructor.
Línea 8: public async Task<bool> ClienteExisteAsync(string cliente) → método de comprobación de cliente.
Línea 9: { → abre el cuerpo del método.
Línea 10: return await _db.Clientes.AnyAsync(c => c.Nombre == cliente); → comprueba existencia.
Línea 11: } → cierra el método.
Línea 12: public async Task<bool> MaterialDisponibleAsync(string material, int cantidad) → método de comprobación de stock.
Línea 13: { → abre el cuerpo del método.
Línea 14: var stock = await _db.Materiales → consulta el stock.
Línea 15: .Where(m => m.Nombre == material) → filtra por nombre.
Línea 16: .Select(m => m.Stock) → proyecta el stock.
Línea 17: .FirstOrDefaultAsync(); → obtiene el primer resultado.
Línea 18: return stock >= cantidad; → comprueba disponibilidad.
Línea 19: } → cierra el método.
Línea 20: } → cierra la clase.

La validación de negocio tiene dos consecuencias prácticas. La primera es que se separa de la validación sintáctica y semántica. La segunda es que requiere acceso a datos externos al propio validador. La separación permite que la validación de negocio se implemente en la capa de aplicación o en el dominio, donde tiene acceso a los repositorios y a los servicios necesarios. La validación de negocio no se realiza en el validador de la petición porque el validador no tiene acceso a la base de datos. La separación por niveles es la clave para mantener la validación como un contrato claro y mantenible.


---

Bloque 5 — FluentValidation en ASP.NET Core

FluentValidation es una biblioteca para definir reglas de validación de forma fluida y testeable. Se integra con ASP.NET Core mediante la clase AbstractValidator<T> y el método RuleFor. Cada regla se compone de una expresión lambda que selecciona el campo, un método de validación y un mensaje de error. La biblioteca ofrece más de treinta métodos de validación entre los que se incluyen NotEmpty, MaximumLength, GreaterThan, EmailAddress, RegularExpression, Must y Custom. La combinación de métodos permite expresar reglas complejas de forma legible.

builder.Services.AddValidatorsFromAssemblyContaining<CrearOrdenRequestValidator>();

Línea 1: builder.Services.AddValidatorsFromAssemblyContaining<CrearOrdenRequestValidator>(); → registra todos los validadores del ensamblado.

La integración con ASP.NET Core se realiza en el contenedor de dependencias. El método AddValidatorsFromAssemblyContaining registra todos los validadores del ensamblado que contiene el tipo especificado. Los validadores se inyectan en los endpoints o en los manejadores de MediatR. La validación se ejecuta antes de la lógica de negocio y devuelve una lista de errores si falla. La lista se transforma en una respuesta problem details con código 400. La integración con el contenedor y con el formato de error es la que permite que la validación sea transparente para la lógica de negocio.


---

Bloque 6 — Integración de la validación con Minimal API

En Minimal API, la validación se integra con un filtro de endpoint o con un manejador de excepciones. El filtro se ejecuta antes del manejador del endpoint y devuelve una respuesta problem details si la validación falla. El manejador se ejecuta solo si la validación pasa. La integración con Minimal API requiere registrar el filtro o el manejador en el contenedor y aplicarlo a los endpoints que lo necesitan. La aplicación selectiva del filtro permite que solo los endpoints con validación lo usen.

public class ValidationFilter<T> : IEndpointFilter where T : class  
{  
    private readonly IValidator<T> _validator;  
  
    public ValidationFilter(IValidator<T> validator)  
    {  
        _validator = validator;  
    }  
  
    public async ValueTask<object?> InvokeAsync(  
        EndpointFilterInvocationContext context,  
        EndpointFilterDelegate next)  
    {  
        var request = context.Arguments.OfType<T>().FirstOrDefault();  
        if (request is null)  
        {  
            return Results.BadRequest();  
        }  
  
        var result = await _validator.ValidateAsync(request);  
        if (!result.IsValid)  
        {  
            var errores = result.Errors  
                .GroupBy(e => e.PropertyName)  
                .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray());  
  
            return Results.ValidationProblem(errores);  
        }  
  
        return await next(context);  
    }  
}

Línea 1: public class ValidationFilter<T> : IEndpointFilter where T : class → declara el filtro genérico.
Línea 2: { → abre el cuerpo de la clase.
Línea 3: private readonly IValidator<T> _validator; → campo para el validador.
Línea 4: public ValidationFilter(IValidator<T> validator) → constructor.
Línea 5: { → abre el cuerpo del constructor.
Línea 6: _validator = validator; → asigna el validador.
Línea 7: } → cierra el constructor.
Línea 8: public async ValueTask<object?> InvokeAsync( → método de invocación del filtro.
Línea 9: EndpointFilterInvocationContext context, → contexto de la petición.
Línea 10: EndpointFilterDelegate next) → siguiente paso en la cadena.
Línea 11: { → abre el cuerpo del método.
Línea 12: var request = context.Arguments.OfType<T>().FirstOrDefault(); → obtiene la petición.
Línea 13: if (request is null) → comprueba si la petición es nula.
Línea 14: { → abre el bloque de error.
Línea 15: return Results.BadRequest(); → devuelve 400.
Línea 16: } → cierra el bloque de error.
Línea 17: var result = await _validator.ValidateAsync(request); → ejecuta la validación.
Línea 18: if (!result.IsValid) → comprueba si hay errores.
Línea 19: { → abre el bloque de error.
Línea 20: var errores = result.Errors → comienza la agrupación de errores.
Línea 21: .GroupBy(e => e.PropertyName) → agrupa por nombre de propiedad.
Línea 22: .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray()); → construye el diccionario.
Línea 23: return Results.ValidationProblem(errores); → devuelve 400 con problem details.
Línea 24: } → cierra el bloque de error.
Línea 25: return await next(context); → continúa la cadena.
Línea 26: } → cierra el método.
Línea 27: } → cierra la clase.

El filtro genérico se aplica a los endpoints que lo necesitan. La aplicación se realiza con la extensión AddEndpointFilter. El filtro obtiene el validador del contenedor de dependencias y ejecuta la validación. Si la validación falla, devuelve una respuesta problem details con código 400 y los errores agrupados por propiedad. Si la validación pasa, continúa la cadena y ejecuta el manejador del endpoint. La integración con Minimal API es transparente para la lógica de negocio.


---

Bloque 7 — Mensajes de error y localización

Los mensajes de error de la validación deben ser claros y útiles para el cliente. Un mensaje como "Valor inválido" no aporta información. Un mensaje como "La cantidad debe ser mayor que cero" aporta información concreta. Los mensajes se definen en el validador con el método WithMessage. La localización de los mensajes permite que la API devuelva mensajes en el idioma del cliente. La localización se implementa con recursos o con un proveedor de mensajes. La adopción de mensajes específicos y localizados mejora la experiencia del consumidor y reduce el tiempo de integración.

RuleFor(x => x.Cantidad)  
    .GreaterThan(0).WithMessage("La cantidad debe ser mayor que cero.")  
    .LessThanOrEqualTo(10000).WithMessage("La cantidad no puede superar 10000.");

Línea 1: RuleFor(x => x.Cantidad) → comienza la regla para el campo Cantidad.
Línea 2: .GreaterThan(0).WithMessage("La cantidad debe ser mayor que cero.") → regla y mensaje.
Línea 3: .LessThanOrEqualTo(10000).WithMessage("La cantidad no puede superar 10000."); → regla y mensaje.

La adopción de mensajes específicos tiene dos consecuencias prácticas. La primera es que el cliente sabe exactamente qué ha fallado. La segunda es que el soporte puede reproducir el error con el mensaje. La localización se aplica de forma opcional según los requisitos del proyecto. El curso usa mensajes en español sin localización porque el alcance no lo requiere. La adopción de mensajes específicos es independiente de la localización y se aplica en todos los casos.


---

Bloque 8 — Validación y códigos de respuesta

La validación fallida produce un código de respuesta específico. El código 400 Bad Request se usa cuando la petición no cumple el contrato de entrada. El código 422 Unprocessable Entity se usa cuando la petición es sintácticamente correcta pero semánticamente inválida. La elección entre 400 y 422 depende del nivel de validación que haya fallado. Si falla la validación sintáctica o semántica, se devuelve 400. Si falla la validación de negocio, se devuelve 422. La distinción permite al cliente distinguir entre un error de datos y un error de negocio.

Códigos de respuesta según el nivel de validación:  
  
Sintáctica fallida   → 400 Bad Request.  
Semántica fallida    → 400 Bad Request.  
Negocio fallida      → 422 Unprocessable Entity.

Línea 1: Sintáctica fallida → error de formato, código 400.
Línea 2: Semántica fallida → error de valores, código 400.
Línea 3: Negocio fallida → error de reglas, código 422.

La distinción entre 400 y 422 tiene dos consecuencias prácticas. La primera es que el cliente puede reaccionar de forma distinta a cada código. La segunda es que las herramientas de monitorización pueden separar los errores de datos de los errores de negocio. La separación permite generar alertas específicas para cada tipo de error. El curso usa 400 para errores sintácticos y semánticos y 422 para errores de negocio.


---

Bloque 9 — Validación y problem details

La respuesta de validación fallida usa el formato problem details con el campo errors que contiene el diccionario de errores por propiedad. El campo errors no forma parte del estándar original de la RFC 7807, pero se ha convertido en una extensión ampliamente adoptada. La estructura del campo errors es un diccionario donde la clave es el nombre de la propiedad y el valor es una lista de mensajes de error. La estructura permite al cliente procesar los errores de forma uniforme.

{  
  "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",  
  "title": "One or more validation errors occurred.",  
  "status": 400,  
  "errors": {  
    "Cliente": ["El cliente es obligatorio."],  
    "Cantidad": ["La cantidad debe ser mayor que cero."]  
  }  
}

Línea 1: { → abre el objeto de error.
Línea 2: "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1", → tipo del error.
Línea 3: "title": "One or more validation errors occurred.", → resumen.
Línea 4: "status": 400, → código HTTP.
Línea 5: "errors": { → abre el diccionario de errores.
Línea 6: "Cliente": ["El cliente es obligatorio."], → error del campo Cliente.
Línea 7: "Cantidad": ["La cantidad debe ser mayor que cero."] → error del campo Cantidad.
Línea 8: } → cierra el diccionario de errores.
Línea 9: } → cierra el objeto de error.

La estructura del campo errors tiene dos consecuencias prácticas. La primera es que el cliente puede mostrar los errores junto a los campos correspondientes. La segunda es que el cliente puede procesar los errores de forma uniforme sin analizar el mensaje. La adopción del formato problem details con el campo errors es la práctica más común en las APIs REST modernas. El curso usa este formato en todos los endpoints que devuelven errores de validación.


---

Bloque 10 — Aplicación al proyecto del curso

El proyecto del curso aplica la validación de peticiones en tres niveles. La validación sintáctica se aplica con tipos no anulables en los record de petición. La validación semántica se aplica con FluentValidation. La validación de negocio se aplica en la capa de aplicación con acceso a la base de datos. La integración con Minimal API se realiza con un filtro genérico. La respuesta de validación fallida usa problem details con código 400. La respuesta de validación de negocio fallida usa problem details con código 422.

Aplicación al proyecto del curso:  
  
Sintáctica    → records con tipos no anulables.  
Semántica     → FluentValidation.  
Negocio       → capa de aplicación.  
Integración   → filtro genérico.  
Respuesta     → problem details 400 o 422.

Línea 1: Sintáctica → tipos no anulables en los records.
Línea 2: Semántica → reglas con FluentValidation.
Línea 3: Negocio → comprobaciones en la capa de aplicación.
Línea 4: Integración → filtro genérico en Minimal API.
Línea 5: Respuesta → problem details con 400 o 422.

La aplicación de la validación prepara el proyecto para el punto 2.4, donde se estudiará la documentación OpenAPI de los endpoints validados. La documentación OpenAPI incluye los esquemas de petición y de respuesta, y los códigos de error. El punto 2.4 usará los validadores definidos en el punto 2.3 para generar la documentación automática. El punto 2.3 establece la base que se aplicará en el punto 2.4.


---

Resumen rápido de la teoría

· La validación es el contrato de entrada de la API y se aplica en tres niveles: sintáctica, semántica y de negocio.
· La validación sintáctica comprueba el formato y los tipos.
· La validación semántica comprueba los valores y las longitudes.
· La validación de negocio comprueba las reglas del dominio con acceso a datos.
· FluentValidation permite definir reglas de validación de forma fluida y testeable.
· La integración con Minimal API se realiza con un filtro genérico.
· La validación fallida produce problem details con código 400 o 422 según el nivel.
· El campo errors de problem details contiene el diccionario de errores por propiedad.


---

PARTE PRÁCTICA (27 minutos)

Ejercicio: Añadir al punto 2.2 un documento de validación de peticiones en docs/, una clase de validación con FluentValidation en el proyecto monolítico, un filtro genérico de validación para Minimal API y un test unitario que verifique la validación. El punto 2.3 parte del contenido del punto 2.2 sin modificar ningún archivo existente: solo añade archivos nuevos.

Ubicación de trabajo: C:\cursos\AceriaApp\modulo-2-apis-rest-aspnet-core\


---

Paso 1 — Crear la carpeta del punto 2.3 a partir del punto 2.2

Acción 1: Abrir la terminal integrada de Visual Studio 2026 con Ctrl+ñ (o Ctrl+``  en teclados no españoles).
Acción 2: Escribir cd C:\cursos\AceriaApp\modulo-2-apis-rest-aspnet-core y pulsar Enter.
Acción 3: Escribir mkdir 2.3-validacion-peticiones y pulsar Enter.
Acción 4: Escribir xcopy 2.2-recursos-verbos-codigos 2.3-validacion-peticiones /E /I /H /Y y pulsar Enter.
Acción 5: Escribir dir 2.3-validacion-peticiones y pulsar Enter para verificar que se ha copiado el contenido.

Por qué se hace: cada punto del curso parte del contenido del punto anterior. El punto 2.3 se construye sobre el punto 2.2 copiando su contenido y añadiendo archivos nuevos sin modificar los existentes.

Errores comunes:

· Usar copy en lugar de xcopy: copy no copia carpetas de forma recursiva.
· Olvidar el flag /E: no se copian las subcarpetas vacías.
· Olvidar el flag /I: xcopy pregunta si el destino es un directorio cuando no existe.
· Olvidar el flag /Y: xcopy pide confirmación para sobrescribir.

Verificación: al ejecutar dir 2.3-validacion-peticiones, deben aparecer AceriaApp.sln, README.md, src, tests y docs.


---

Paso 2 — Abrir la solución copiada en Visual Studio 2026

Acción 1: Escribir cd 2.3-validacion-peticiones y pulsar Enter.
Acción 2: Escribir start AceriaApp.sln y pulsar Enter.
Acción 3: Verificar que Visual Studio 2026 abre la solución y muestra los proyectos heredados del punto 2.2: AceriaApp.Monolito.Api, AceriaApp.Monolito.Tests, AceriaApp.Metricas.Tests, AceriaApp.Diseno.Tests, AceriaApp.Organizacion.Tests, AceriaApp.BuenasPracticas.Tests, AceriaApp.DisenoRest.Tests y AceriaApp.CatalogoRecursos.Tests.
Acción 4: Verificar que la solución compila con Ctrl+Shift+B y que la salida muestra Build succeeded..

Por qué se hace: abrir la solución copiada permite trabajar en el punto 2.3 sobre la base del punto 2.2. La compilación verifica que la copia es correcta.

Errores comunes:

· Abrir la solución del punto 2.2 en lugar de la del punto 2.3: los cambios se aplican al punto equivocado.
· No compilar antes de empezar: si la copia tiene errores, los cambios posteriores fallan.
· Tener la API del punto 2.2 en ejecución: el puerto queda ocupado y la compilación falla.

Verificación: Visual Studio 2026 muestra la solución AceriaApp con los ocho proyectos heredados del punto 2.2 y la compilación es correcta.


---

Paso 3 — Verificar que la carpeta docs contiene los documentos del punto 2.2

Acción 1: En el panel Solution Explorer, expandir la carpeta docs del punto 2.3.
Acción 2: Verificar que contiene ADR-001 a ADR-007, analisis-ventajas-inconvenientes.md, principios-diseno.md, organizacion-solucion.md, buenas-practicas.md, diseno-apis-rest.md y catalogo-recursos.md.
Acción 3: Verificar que ninguno de los once documentos se ha modificado.
Acción 4: Verificar que la carpeta docs no contiene ningún archivo nuevo del punto 2.3 todavía.

Por qué se hace: el punto 2.3 parte del contenido del punto 2.2, que ya incluye la carpeta docs con once documentos. No se modifica ningún documento existente.

Errores comunes:

· Modificar alguno de los ADR o documentos existentes: viola la regla de no modificar archivos del punto anterior.
· Eliminar algún documento existente: pierde la trazabilidad del punto 2.2.
· Crear la carpeta docs si ya existe: mkdir falla.

Verificación: la carpeta docs contiene los once documentos del punto 2.2 sin modificaciones.


---

Paso 4 — Crear el documento de validación de peticiones en docs

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta docs.
Acción 2: Seleccionar Add → New Item → Text File y nombrar el archivo validacion-peticiones.md.
Acción 3: Escribir exactamente el siguiente contenido:

# Validación de peticiones — Punto 2.3  
  
## Niveles de validación  
  
1. Sintáctica.  
2. Semántica.  
3. De negocio.  
  
## Validación sintáctica  
  
Comprueba el formato y los tipos de datos. Se implementa con tipos no anulables en los `record` de petición.  
  
## Validación semántica  
  
Comprueba los valores y las longitudes. Se implementa con FluentValidation.  
  
## Validación de negocio  
  
Comprueba las reglas del dominio. Se implementa en la capa de aplicación con acceso a la base de datos.  
  
## Códigos de respuesta  
  
| Nivel fallido | Código |  
|---------------|--------|  
| Sintáctica | 400 Bad Request |  
| Semántica | 400 Bad Request |  
| Negocio | 422 Unprocessable Entity |  
  
## Formato de error  
  
Problem details con campo `errors`.  
  
## Aplicación al proyecto del curso  
  
| Elemento | Aplicación |  
|----------|------------|  
| Sintáctica | Records con tipos no anulables |  
| Semántica | FluentValidation |  
| Negocio | Capa de aplicación |  
| Integración | Filtro genérico |  
| Respuesta | Problem details 400 o 422 |

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que el archivo aparece en la carpeta docs sin subrayados rojos.

Por qué se hace: el documento de validación de peticiones es el artefacto de docs específico del punto 2.3. No modifica los once documentos existentes del punto 2.2.

Errores comunes:

· Nombrar el archivo con otro nombre: rompe la trazabilidad del punto.
· Modificar los ADR existentes: viola la regla de no modificar archivos del punto anterior.
· Guardar el archivo en la raíz del punto en lugar de docs: rompe la estructura del repositorio.

Verificación: el archivo docs\validacion-peticiones.md existe con las siete secciones.


---

Paso 5 — Añadir el paquete FluentValidation.AspNetCore al proyecto monolítico

Acción 1: En la terminal, escribir dotnet add src\AceriaApp.Monolito.Api\AceriaApp.Monolito.Api.csproj package FluentValidation.AspNetCore y pulsar Enter.
Acción 2: Escribir dotnet list src\AceriaApp.Monolito.Api\AceriaApp.Monolito.Api.csproj package y pulsar Enter.
Acción 3: Verificar que la salida muestra FluentValidation.AspNetCore con su versión.

Por qué se hace: FluentValidation.AspNetCore proporciona la integración de FluentValidation con el contenedor de dependencias de ASP.NET Core. Es necesario para registrar los validadores y para inyectarlos en los endpoints.

Errores comunes:

· Instalar FluentValidation sin AspNetCore: falta la integración con el contenedor.
· Instalar una versión preliminar: el curso usa la última estable.
· Añadir el paquete al proyecto de tests: los validadores no se resuelven en producción.

Verificación: la salida de dotnet list package muestra FluentValidation.AspNetCore con una versión estable.


---

Paso 6 — Crear la carpeta Validacion en el proyecto monolítico

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre el proyecto AceriaApp.Monolito.Api.
Acción 2: Seleccionar Add → New Folder y nombrar la carpeta Validacion.
Acción 3: Verificar que la carpeta Validacion aparece dentro de AceriaApp.Monolito.Api sin afectar a las carpetas existentes.
Acción 4: Verificar que no se ha modificado ningún archivo existente del punto 2.2.

Por qué se hace: la carpeta Validacion albergará los validadores y el filtro genérico. Se crea como carpeta nueva sin tocar las carpetas existentes.

Errores comunes:

· Crear la carpeta dentro de alguna de las carpetas existentes: rompe la separación de responsabilidades.
· Modificar las carpetas existentes: viola la regla de no modificar archivos del punto anterior.
· Crear la carpeta con otro nombre: rompe la convención del curso.

Verificación: la carpeta Validacion existe dentro de AceriaApp.Monolito.Api y las carpetas existentes permanecen intactas.


---

Paso 7 — Crear el record CrearOrdenRequest

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta Validacion.
Acción 2: Seleccionar Add → Class y nombrar la clase CrearOrdenRequest.cs.
Acción 3: Escribir exactamente el siguiente código:

namespace AceriaApp.Monolito.Api.Validacion;  
  
public record CrearOrdenRequest(  
    string Cliente,  
    string Material,  
    int Cantidad);

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: el record CrearOrdenRequest modela el contrato de entrada del endpoint de creación de órdenes. Los tipos no anulables aplican la validación sintáctica.

Errores comunes:

· Olvidar el namespace: la clase no se resuelve desde otros archivos.
· Usar string? en lugar de string: los campos serían opcionales y la validación sintáctica no se aplicaría.
· Usar int? en lugar de int: la cantidad sería opcional.

Verificación: el record CrearOrdenRequest compila sin errores y expone tres propiedades.


---

Paso 8 — Crear el validador CrearOrdenRequestValidator

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta Validacion.
Acción 2: Seleccionar Add → Class y nombrar la clase CrearOrdenRequestValidator.cs.
Acción 3: Escribir exactamente el siguiente código:

using FluentValidation;  
  
namespace AceriaApp.Monolito.Api.Validacion;  
  
public class CrearOrdenRequestValidator : AbstractValidator<CrearOrdenRequest>  
{  
    public CrearOrdenRequestValidator()  
    {  
        RuleFor(x => x.Cliente)  
            .NotEmpty().WithMessage("El cliente es obligatorio.")  
            .MaximumLength(100).WithMessage("El cliente no puede superar 100 caracteres.");  
  
        RuleFor(x => x.Material)  
            .NotEmpty().WithMessage("El material es obligatorio.")  
            .MaximumLength(100).WithMessage("El material no puede superar 100 caracteres.");  
  
        RuleFor(x => x.Cantidad)  
            .GreaterThan(0).WithMessage("La cantidad debe ser mayor que cero.")  
            .LessThanOrEqualTo(10000).WithMessage("La cantidad no puede superar 10000.");  
    }  
}

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: el validador CrearOrdenRequestValidator define las reglas semánticas del contrato de entrada. Cada regla tiene un mensaje de error específico.

Errores comunes:

· Olvidar el using FluentValidation;: AbstractValidator no se resuelve.
· Usar RuleFor con una expresión incorrecta: el validador no se ejecuta.
· No usar WithMessage: los mensajes de error son genéricos.

Verificación: el validador CrearOrdenRequestValidator compila sin errores y expone tres reglas.


---

Paso 9 — Crear el filtro genérico ValidationFilter

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta Validacion.
Acción 2: Seleccionar Add → Class y nombrar la clase ValidationFilter.cs.
Acción 3: Escribir exactamente el siguiente código:

using FluentValidation;  
  
namespace AceriaApp.Monolito.Api.Validacion;  
  
public class ValidationFilter<T> : IEndpointFilter where T : class  
{  
    private readonly IValidator<T> _validator;  
  
    public ValidationFilter(IValidator<T> validator)  
    {  
        _validator = validator;  
    }  
  
    public async ValueTask<object?> InvokeAsync(  
        EndpointFilterInvocationContext context,  
        EndpointFilterDelegate next)  
    {  
        var request = context.Arguments.OfType<T>().FirstOrDefault();  
        if (request is null)  
        {  
            return Results.BadRequest();  
        }  
  
        var result = await _validator.ValidateAsync(request);  
        if (!result.IsValid)  
        {  
            var errores = result.Errors  
                .GroupBy(e => e.PropertyName)  
                .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray());  
  
            return Results.ValidationProblem(errores);  
        }  
  
        return await next(context);  
    }  
}

Acción 4: Pulsar Ctrl+S para guardar el archivo.
Acción 5: Verificar que la clase compila sin errores.

Por qué se hace: el filtro genérico ValidationFilter<T> integra FluentValidation con Minimal API. Obtiene el validador del contenedor de dependencias, ejecuta la validación y devuelve problem details si falla.

Errores comunes:

· Olvidar el using FluentValidation;: IValidator no se resuelve.
· Olvidar el using System.Linq;: OfType, FirstOrDefault, GroupBy, ToDictionary y Select no se resuelven.
· No comprobar si la petición es nula: el filtro lanza NullReferenceException.

Verificación: el filtro ValidationFilter<T> compila sin errores y expone un constructor y un método.


---

Paso 10 — Añadir los using necesarios en ValidationFilter

Acción 1: En el panel Solution Explorer, hacer doble clic en ValidationFilter.cs.
Acción 2: Añadir la línea using System.Linq; al principio del archivo si no está presente.
Acción 3: Verificar que no hay subrayados rojos en OfType, FirstOrDefault, GroupBy, ToDictionary ni Select.
Acción 4: Pulsar Ctrl+S para guardar el archivo.

Por qué se hace: los métodos OfType, FirstOrDefault, GroupBy, ToDictionary y Select pertenecen a System.Linq. En proyectos con ImplicitUsings desactivado, hay que añadir el using explícito.

Errores comunes:

· Añadir using System.Collections.Generic; en lugar de System.Linq: no resuelve los métodos.
· Añadir el using después del namespace: el compilador no lo reconoce.
· Olvidar el using y confiar en ImplicitUsings: el proyecto puede tenerlo desactivado.

Verificación: ValidationFilter.cs compila sin errores y no muestra subrayados rojos.


---

Paso 11 — Crear el proyecto de tests del punto 2.3

Acción 1: En el panel Solution Explorer, hacer clic derecho sobre la carpeta tests.
Acción 2: Seleccionar Add → New Project.
Acción 3: Seleccionar la plantilla xUnit Test Project, nombrar el proyecto AceriaApp.Validacion.Tests y pulsar Create.
Acción 4: Verificar que el proyecto aparece en la solución y que se ha creado la carpeta tests\AceriaApp.Validacion.Tests.

Por qué se hace: el punto 2.3 añade un proyecto de tests específico para los validadores. Se crea como proyecto nuevo sin modificar los proyectos de tests existentes.

Errores comunes:

· Crear el proyecto dentro de src en lugar de tests: rompe la estructura.
· Modificar los proyectos de tests del punto 2.2: viola la regla de no modificar archivos del punto anterior.
· Usar dotnet new mstest: el curso usa xUnit.

Verificación: el proyecto AceriaApp.Validacion.Tests aparece en la solución y su carpeta existe en tests\AceriaApp.Validacion.Tests.


---

Paso 12 — Añadir la referencia del proyecto de tests a la API monolítica

Acción 1: En la terminal, escribir dotnet add tests\AceriaApp.Validacion.Tests\AceriaApp.Validacion.Tests.csproj reference src\AceriaApp.Monolito.Api\AceriaApp.Monolito.Api.csproj y pulsar Enter.
Acción 2: Verificar que la salida muestra Reference added successfully.
Acción 3: Verificar que el archivo AceriaApp.Validacion.Tests.csproj contiene la referencia.

Por qué se hace: la referencia permite que el proyecto de tests acceda a los validadores del proyecto monolítico.

Errores comunes:

· Añadir la referencia en dirección inversa: crea una dependencia circular.
· Olvidar el nombre completo del archivo .csproj: el comando falla.
· Ejecutar el comando desde la carpeta equivocada: la ruta relativa no se resuelve.

Verificación: el archivo AceriaApp.Validacion.Tests.csproj contiene un ProjectReference al proyecto monolítico.


---

