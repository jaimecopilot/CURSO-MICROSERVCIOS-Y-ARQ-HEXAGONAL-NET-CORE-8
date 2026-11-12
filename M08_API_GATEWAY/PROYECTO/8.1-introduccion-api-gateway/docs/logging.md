# Logging — Punto 7.1

## Definición

Registro de eventos que ocurren durante la ejecución del sistema.

## Niveles de log

- Trace: información muy detallada.
- Debug: información de depuración.
- Information: operación normal.
- Warning: situación anómala.
- Error: error que impide una operación.
- Critical: error que afecta a todo el sistema.

## Logging estructurado

Registra una plantilla de mensaje y propiedades nombradas y tipadas. El mensaje sigue siendo texto; las propiedades permiten buscar y agregar sin analizarlo con expresiones regulares.

## Serilog

Biblioteca de logging estructurado para .NET.

## Integración con ASP.NET Core

    builder.Host.UseSerilog((context, config) =>
    {
        config
            .MinimumLevel.Information()
            .Enrich.FromLogContext()
            .WriteTo.Console(new JsonFormatter());
    });

## Correlación

Identificador común que se propaga entre servicios con la cabecera `X-Correlation-Id`.

## Logging de errores

Registra el tipo de fallo y los identificadores aprobados. No vuelques mensajes libres, cuerpos, query strings, cabeceras Authorization ni excepciones completas que puedan contener secretos. La respuesta pública tampoco expone detalles internos.

## Buenas prácticas

1. Logging estructurado.
2. Plantillas con propiedades.
3. Sin información sensible.
4. Nivel mínimo por entorno.
5. Correlación con identificador.

## Configuración por entorno

El nivel mínimo se ajusta por entorno en `appsettings.json`.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Biblioteca | Serilog |
| Sinks | Consola JSON en el ejercicio; un archivo requeriría retención, permisos y rotación |
| Enrichers | LogContext |
| Correlación | X-Correlation-Id |
| Nivel | Configurado por entorno |
| Validación | Test de coherencia |
## Contrato del ejercicio

Los seis niveles Trace, Debug, Information, Warning, Error y Critical corresponden a `Microsoft.Extensions.Logging`. Serilog los representa mediante Verbose, Debug, Information, Warning, Error y Fatal; `None` desactiva el registro y no es un nivel de evento. El catálogo exige logging estructurado, correlación, protección de datos y configuración por entorno como política del curso, sin imponer que todas las aplicaciones deban aceptar un header del cliente.

El middleware valida `X-Correlation-ID`: entre 1 y 64 caracteres ASCII alfanuméricos, guion o subrayado. Sustituye valores inválidos, conserva un identificador por petición y lo devuelve y propaga al cliente HTTP. Un identificador de correlación no demuestra por sí solo un sistema de trazas distribuido.
