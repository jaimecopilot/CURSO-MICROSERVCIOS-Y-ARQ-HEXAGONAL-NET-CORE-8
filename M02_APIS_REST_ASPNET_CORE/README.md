# Módulo 2 — APIs REST con ASP.NET Core 8

**Autor: JAIME GALLO**

## Material canónico de aprendizaje

- [Teoría de M02](TEORIA/M02_TEORIA.md).
- [Prácticas de M02](PRACTICAS/M02_PRACTICAS.md): **guion único del alumno**, con 96 pasos numerados de 2.1.1 a 2.4.24.
- [Prácticas de M02 en PDF](PRACTICAS/M02_PRACTICAS.pdf): generado directamente desde el mismo Markdown, con la plantilla tipográfica del módulo 1.

## Cómo utilizar las prácticas

El alumno trabaja sobre su propia solución y sigue el **orden de los pasos**. El código fuente que aparece en el laboratorio debe escribirse en el archivo indicado. Cuando el ejercicio dice *ampliar*, debe modificar el archivo ya creado, no volver a copiar una versión completa ni declarar un segundo endpoint con la misma ruta.

Cada carpeta de PROYECTO contiene el **estado final de referencia de su etapa**, no una aplicación que deba copiarse al principio:

| Etapa | Carpeta | Resultado |
| --- | --- | --- |
| 2.1 | `PROYECTO/2.1-diseno-apis-rest` | GET, OrdenDto, EF Core 8, LocalDB y pruebas HTTP |
| 2.2 | `PROYECTO/2.2-recursos-verbos-codigos` | POST, PUT, PATCH, DELETE y reglas de estado |
| 2.3 | `PROYECTO/2.3-validacion-peticiones` | FluentValidation y filtros conectados a endpoints |
| 2.4 | `PROYECTO/2.4-documentacion-openapi` | Documento Swagger/OpenAPI y pruebas de contrato |

## Comprobaciones de aprendizaje

Las cuatro soluciones usan .NET 8 y se pueden compilar y probar de forma independiente. La aplicación local requiere **SQL Server Express LocalDB**; las pruebas usan **EF Core InMemory** para ejecutarse sin una base externa.

El laboratorio se comprueba también con un **E2E de reconstrucción**: una copia temporal de las cuatro etapas se genera a partir de fragmentos C# del Markdown y se compila repetidamente hasta superar sus pruebas. Esta comprobación no automatiza las acciones exclusivamente manuales del IDE.

Los PDFs se obtienen desde los Markdown mediante el flujo de generación del repositorio. El archivo MD es la fuente; el PDF es el material distribuible.
