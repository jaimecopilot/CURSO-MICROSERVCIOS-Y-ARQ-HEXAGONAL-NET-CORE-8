# Módulo 5 — Introducción a DDD y CQRS con .NET 8

**Curso JAIME GALLO · Código: AceriaApp**

- [Teoría](TEORIA/M05_TEORIA.md) · [PDF](TEORIA/M05_TEORIA.pdf): 50 bloques, diez por punto, con ampliaciones y diagramas.
- [Prácticas guiadas](PRACTICAS/M05_PRACTICAS.md) · [PDF](PRACTICAS/M05_PRACTICAS.pdf): 120 pasos y cinco retos resueltos.
- [Proyectos acumulativos](PROYECTO): cinco estados ejecutables que parten de M4, punto 4.5.
- [Evidencia E2E](M05_E2E_RESULTADOS.json): reconstrucción desde el manual, compilaciones, pruebas y retos.
- [Comprobación de los PDF](REPORTE_PDF_M05.json): contenido, explicaciones separadas y geometría de las páginas.

| Punto | Contenido | Proyecto |
|---|---|---|
| 5.1 | Conceptos básicos de DDD | [5.1-conceptos-ddd](PROYECTO/5.1-conceptos-ddd) |
| 5.2 | Entidades y objetos de valor | [5.2-entidades-value-objects](PROYECTO/5.2-entidades-value-objects) |
| 5.3 | Casos de uso | [5.3-casos-de-uso](PROYECTO/5.3-casos-de-uso) |
| 5.4 | Separación de comandos y consultas | [5.4-commands-queries](PROYECTO/5.4-commands-queries) |
| 5.5 | Aplicación al dominio de la acería | [5.5-dominio-aceria](PROYECTO/5.5-dominio-aceria) |

El contexto de Producción incorpora una orden como raíz del agregado, líneas con identidad y objetos de valor para material y cantidad. Los casos de uso permiten crear, consultar, planificar, finalizar y añadir líneas respetando las reglas del agregado. La separación entre comandos y consultas se concreta con MediatR y una proyección de lectura sin seguimiento de cambios.

Cada punto conserva los catálogos de comprobación de decisiones arquitectónicas y añade pruebas del comportamiento de la aplicación. Los ejemplos de otros contextos sirven para razonar sobre los límites del dominio; el contexto implementado en este módulo es Producción. Las etapas son independientes en disco: avanzar a la siguiente conserva la anterior.

## Ejecución y comprobación

El entorno de trabajo mantiene .NET 8, ASP.NET Core, EF Core 8 y SQL Server Express LocalDB en Windows. Producción utiliza su propio contexto de EF y la base de datos `AceriaProduccion`. Las pruebas de integración mantienen **SQL Server real con `UseSqlServer`** y reservan una base única por caso mediante `BaseSqlServer.Crear()`. Comprueban persistencia del agregado y sus líneas, comandos, proyecciones de lectura y contratos HTTP; los tests del dominio conservan su independencia de la infraestructura.

Las pruebas necesitan Docker Desktop con contenedores Linux, o `ACERIA_TEST_SQLSERVER` con una conexión a `master` en un SQL Server disponible, incluyendo LocalDB. Sin esa variable, Testcontainers 3.10.0 inicia la imagen fijada `mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04` con `MSSQL_PID=Express`. La cuenta crea y elimina bases aisladas. Si el entorno falla, la prueba falla: no pasa a SQLite o InMemory. El [README de M02](../M02_APIS_REST_ASPNET_CORE/README.md#comprobaciones-de-aprendizaje) incluye la configuración de PowerShell.

El estudio integrador 5.4 de la teoría incorpora un diagrama SVG/PNG y un recorrido de command a query explicado por líneas. Muestra por qué leer desde un ámbito nuevo verifica la confirmación y por qué esta variante de CQRS comparte una base sin introducir sincronización asíncrona.

Desde la raíz del repositorio:

```bash
python3 .github/scripts/m05_crear_figuras.py
python3 .github/scripts/figuras_sqlserver.py
python3 .github/scripts/m05_e2e_desde_practicas.py --out M05_DDD_CQRS/M05_E2E_RESULTADOS.json
python3 .github/scripts/m05_generar_pdf.py
```

El E2E copia el proyecto aprobado de M4 y aplica los bloques de código del manual en orden. Compila estados intermedios, ejecuta todas las pruebas acumuladas de cada etapa y prueba los cinco retos en copias aisladas. Los pasos de interfaz de Visual Studio incluyen un resultado verificable; el informe distingue estas instrucciones de las operaciones ejecutadas automáticamente.

El workflow publica los proyectos, PDF e informes después de superar las comprobaciones. El informe registra las huellas del manual, de la etapa de partida y de los archivos de cada proyecto reconstruido.
