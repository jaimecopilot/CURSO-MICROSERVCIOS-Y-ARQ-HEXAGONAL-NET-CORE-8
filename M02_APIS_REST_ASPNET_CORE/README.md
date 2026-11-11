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

Las cuatro soluciones usan .NET 8 y se pueden compilar y probar de forma independiente. La aplicación local utiliza **SQL Server Express LocalDB** en Windows. Las pruebas de integración mantienen **EF Core SQL Server y un motor SQL Server real**: cada caso obtiene una base aislada mediante `BaseSqlServer.Crear()` y la elimina al terminar.

Para ejecutar las pruebas, elige uno de estos entornos:

- **Docker Desktop con contenedores Linux**, sin definir `ACERIA_TEST_SQLSERVER`: `Testcontainers.MsSql` 3.10.0 inicia SQL Server con la imagen `mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04` y `MSSQL_PID=Express`.
- **SQL Server disponible**, incluyendo LocalDB en Windows: define `ACERIA_TEST_SQLSERVER` con una conexión a `master` y una cuenta que pueda crear y eliminar bases de pruebas. El helper genera nombres únicos; no reutiliza la base cotidiana de la API.

Ejemplo en PowerShell, desde la carpeta de una solución:

```powershell
$env:ACERIA_TEST_SQLSERVER = 'Server=(localdb)\MSSQLLocalDB;Database=master;Trusted_Connection=True;TrustServerCertificate=True'
dotnet test
Remove-Item Env:ACERIA_TEST_SQLSERVER
```

Un Docker inaccesible o un SQL Server no disponible hace fallar las pruebas que lo necesitan. No hay sustitución automática por InMemory o SQLite ni omisión silenciosa. La [teoría, estudio integrador 2.1](TEORIA/M02_TEORIA.md#estudio-integrador-21--probar-http-y-persistencia-con-sql-server-real) explica imagen, contenedor, puertos, cadenas de conexión y el recorrido completo del test, con diagramas SVG/PNG y explicaciones separadas de cada línea.

El laboratorio se comprueba también con un **E2E de reconstrucción**: una copia temporal de las cuatro etapas se genera a partir de fragmentos C# del Markdown y se compila repetidamente hasta superar sus pruebas. Esta comprobación no automatiza las acciones exclusivamente manuales del IDE.

Los PDFs se obtienen desde los Markdown mediante el flujo de generación del repositorio. El archivo MD es la fuente; el PDF es el material distribuible.
