# Cobertura E2E del módulo 1 · procedimiento interno de validación

El curso presenta cinco soluciones independientes. Las pruebas **nunca alteran** `PROYECTO` directamente: primero copian cada solución, luego activan secuencialmente los bloques `INICIO PASO`/`FIN PASO`, como haría el alumnado. El inventario cubre los 120 pasos, pero no presenta como automatizadas las acciones que dependen del IDE o de hacer un commit manual.

| Etapa | Escenario automático | Condición de éxito |
| --- | --- | --- |
| 1.1 | Compilación inicial, Orden, DbContext, Program, migración | Compila después de activar 11, 12, 13 y 14; 1 test básico |
| 1.1 | SQL, GET, POST, Swagger | Migración aplicada, GET 200 y lista vacía, POST 201 con GUID, GET refleja orden |
| 1.1 · reto | Endpoint GET por id y prueba añadida | 2 tests totales; GET existente 200, inexistente 404 |
| 1.2 | Métricas de acoplamiento y sus pruebas | Compila tras pasos 6, 7, 8, 13, 14, 15; 9 tests básicos acumulados |
| 1.2 · reto | ServicioMenosAcoplado y desempate | 10 tests acumulados al activar el reto |
| 1.3 | Validador de límites y catálogo | 13 tests básicos acumulados |
| 1.3 · reto | Resumen de validez (3 de 4) | 14 tests acumulados, 75 % esperado |
| 1.4 | Convención de nombres y catálogo | 18 tests básicos acumulados |
| 1.4 · reto | Resumen de proyectos (3 de 5) | 19 tests acumulados, 60 % esperado |
| 1.5 | Validador de buenas prácticas y catálogo | 23 tests básicos acumulados |
| 1.5 · reto | Resumen de prácticas (3 de 5) | 24 tests acumulados, 60 % esperado |
| 1.1–1.5 | Herencia documental, 24 pasos/punto, código preparado | 50 bloques teóricos, 120 pasos, 16 documentos idénticos |
| 1.1–1.5 | SQL Server real en contenedor y API por etapa | Cada punto crea su BD nueva, migra, expone OpenAPI y persiste una orden |
| 1.1 y 1.5 | SQL Server **Express LocalDB** en Windows | Prueba SQL y HTTP sin sustituir Express por SQLite o InMemory |

La CI Linux usa **SQL Server 2022 Developer en contenedor**, que prueba el proveedor `UseSqlServer` y el esquema relacional, pero **no sustituye la prueba de Express LocalDB**. Esta última está en un trabajo separado de Windows. Si Express no está instalado, la prueba debe fallar explícitamente, nunca aparecer como superada por una simulación.

Las acciones manuales que no pueden certificarse por CI incluyen abrir Visual Studio 2026, usar `Ctrl+K, Ctrl+U`, observar el explorador de objetos de SQL Server y crear commits personales. Se contrastan sus equivalentes observables (compilación, cambios de código activado y comportamiento de la API), pero siguen marcadas como comprobaciones manuales.

## Invocación

```bash
python .github/scripts/e2e_m01.py --root . --mode static --out resultado-estatico.json
python .github/scripts/e2e_m01.py --root . --mode stage --point 1.3 --reto --out resultado-13.json
# Requiere .NET SDK 8, dotnet-ef 8 y SQL Server accesible:
M01_SQL_CONNECTION_STRING='Server=...;Database=Aceria_E2E;...' python .github/scripts/e2e_m01.py --root . --mode sql --point 1.1 --reto
```

El estado de una prueba solo es `PASS` cuando el comando terminó correctamente y están disponibles las evidencias JSON/TRX. Esta documentación está deliberadamente fuera de `TEORIA`, `PRACTICAS` y los README del alumnado.
