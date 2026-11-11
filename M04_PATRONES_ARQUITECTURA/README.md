# Módulo 4 — Patrones de arquitectura con .NET 8

**Curso JAIME GALLO · Código: AceriaApp**

- [Teoría](TEORIA/M04_TEORIA.md) · [PDF](TEORIA/M04_TEORIA.pdf): 50 bloques, diez por punto.
- [Prácticas guiadas](PRACTICAS/M04_PRACTICAS.md) · [PDF](PRACTICAS/M04_PRACTICAS.pdf): 120 pasos y cinco retos resueltos.
- [Proyectos acumulativos](PROYECTO): cinco estados ejecutables que parten de M3, punto 3.4.
- [Evidencia E2E](M04_E2E_RESULTADOS.json): reconstrucción desde el manual, compilaciones, pruebas y retos.
- [Comprobación de los PDF](REPORTE_PDF_M04.json): contenido, explicaciones separadas y geometría de las páginas.

| Punto | Contenido | Proyecto |
|---|---|---|
| 4.1 | Repository | [4.1-repository](PROYECTO/4.1-repository) |
| 4.2 | Unit of Work | [4.2-unit-of-work](PROYECTO/4.2-unit-of-work) |
| 4.3 | Mediator con MediatR | [4.3-mediator](PROYECTO/4.3-mediator) |
| 4.4 | Result Pattern | [4.4-result-pattern](PROYECTO/4.4-result-pattern) |
| 4.5 | Inyección de dependencias | [4.5-inyeccion-dependencias](PROYECTO/4.5-inyeccion-dependencias) |

Cada punto conserva los catálogos de comprobación de las decisiones arquitectónicas y añade pruebas del comportamiento de la aplicación. Las etapas son independientes en disco: avanzar a la siguiente conserva la anterior.

## Ejecución y comprobación

El entorno de trabajo mantiene .NET 8, ASP.NET Core, EF Core 8 y SQL Server Express LocalDB en Windows. Las pruebas del dominio o de coordinación pueden usar dobles; las pruebas de persistencia y transacciones usan **SQL Server real con `UseSqlServer`** y bases aisladas creadas por `BaseSqlServer.Crear()`. La prueba de atomicidad provoca un fallo después de una escritura y verifica el resultado desde otro contexto, incluyendo un control sin transacción que detecta persistencia parcial.

Las pruebas necesitan Docker Desktop con contenedores Linux, o `ACERIA_TEST_SQLSERVER` con una conexión a `master` en un SQL Server disponible, incluyendo LocalDB. Sin esa variable, Testcontainers 3.10.0 inicia la imagen fijada `mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04` con `MSSQL_PID=Express`. Un entorno no disponible produce un fallo; no se sustituye SQL Server por SQLite o InMemory. El [README de M02](../M02_APIS_REST_ASPNET_CORE/README.md#comprobaciones-de-aprendizaje) incluye la configuración de PowerShell.

El estudio integrador 4.2 de la teoría explica preparación de cambios, confirmación y rollback, con un diagrama SVG/PNG y el análisis línea por línea de la comprobación. Distingue lo que demuestra un doble de lo que requiere el proveedor real.

Desde la raíz del repositorio:

```bash
python3 .github/scripts/m04_crear_figuras.py
python3 .github/scripts/figuras_sqlserver.py
python3 .github/scripts/m04_e2e_desde_practicas.py --out M04_PATRONES_ARQUITECTURA/M04_E2E_RESULTADOS.json
python3 .github/scripts/m04_generar_pdf.py
```

El E2E copia el proyecto aprobado de M3 y aplica los bloques de código del manual en orden. Compila estados intermedios, ejecuta todas las pruebas acumuladas de cada etapa y prueba los cinco retos en copias aisladas. Los pasos de interfaz de Visual Studio incluyen un resultado verificable; el informe distingue estas instrucciones de las operaciones ejecutadas automáticamente.

El workflow publica los proyectos, PDF e informes después de superar las comprobaciones. Las referencias de los proyectos generados y los ejemplos del manual pertenecen al mismo proceso de reconstrucción.
