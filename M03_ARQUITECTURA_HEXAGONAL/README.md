# Módulo 3 — Arquitectura hexagonal con .NET 8

**Curso JAIME GALLO · Código: AceriaApp**

## Material canónico del módulo

- [Teoría](TEORIA/M03_TEORIA.md) y [PDF](TEORIA/M03_TEORIA.pdf): 40 bloques, los diez de cada punto 3.1–3.4.
- [Prácticas](PRACTICAS/M03_PRACTICAS.md) y [PDF](PRACTICAS/M03_PRACTICAS.pdf): 96 pasos detallados de construcción y pruebas.
- [PROYECTO](PROYECTO): cuatro estados progresivos ejecutables de la API, generados desde los **bloques etiquetados del Markdown**, no de una segunda implementación manual.
- [E2E](M03_E2E_RESULTADOS.json): evidencia de los 96 pasos, compilaciones, proyectos y pruebas acumuladas.

## Requisitos y arquitectura

SDK .NET 8, Visual Studio con ASP.NET/web y SQL Server Express LocalDB para ejecutar las API en Windows. Los tests de integración conservan `UseSqlServer` y ejecutan SQL Server real. `HexagonalFactory` reserva bases independientes para el contexto heredado y el contexto hexagonal mediante `BaseSqlServer.Crear()`. Se conservan los endpoints REST de M02; en 3.4 se añaden endpoints hexagonales con un puerto real, casos de uso y un repositorio EF Core separado en proyectos físicos.

Las pruebas necesitan Docker Desktop con contenedores Linux, o una conexión a `master` en `ACERIA_TEST_SQLSERVER` —por ejemplo, LocalDB en Windows— con permisos para crear y eliminar sus bases aisladas. Sin la variable, Testcontainers 3.10.0 inicia la imagen fijada `mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04` en edición Express. Si el servidor no está disponible, el test falla: no se omite ni cambia a un proveedor en memoria. Consulta el [ejemplo de configuración de M02](../M02_APIS_REST_ASPNET_CORE/README.md#comprobaciones-de-aprendizaje).

La teoría 3.4 amplía la diferencia entre puerto, adaptador, proveedor EF Core y motor SQL Server. Incluye un diagrama SVG/PNG, el registro de los dos contextos explicado por líneas y una tabla que relaciona cada frontera con su prueba.

Los cuatro puntos de M03 usan las carpetas 3.1, 3.2, 3.3 y 3.4 autónomas, manteniendo el anterior como referencia sin sobrescribirlo.

## E2E

```bash
python3 .github/scripts/m03_e2e_desde_practicas.py --out M03_ARQUITECTURA_HEXAGONAL/M03_E2E_RESULTADOS.json
```

Este comprobador copia exclusivamente el **punto 2.4 aprobado de M02**, reconstruye cada etapa de M03 leyendo los 96 pasos del Markdown y ejecuta compilaciones y pruebas. Después aplica y prueba los cuatro retos optativos en copias temporales independientes, conservando intactos los proyectos obligatorios. Los pasos exclusivamente manuales de Visual Studio se documentan con evidencia esperada, pero no se afirma haber ejecutado clics en el IDE. El workflow publica los proyectos y los PDF solo después de que el E2E se complete correctamente.
