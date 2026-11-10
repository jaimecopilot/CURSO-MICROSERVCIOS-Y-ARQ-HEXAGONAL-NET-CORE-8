# Módulo 3 — Arquitectura hexagonal con .NET 8

**Curso JAIME GALLO · Código: AceriaApp**

## Material canónico del módulo

- [Teoría](TEORIA/M03_TEORIA.md) y [PDF](TEORIA/M03_TEORIA.pdf): 40 bloques, los diez de cada punto 3.1–3.4.
- [Prácticas](PRACTICAS/M03_PRACTICAS.md) y [PDF](PRACTICAS/M03_PRACTICAS.pdf): 96 pasos detallados de construcción y pruebas.
- [PROYECTO](PROYECTO): cuatro estados progresivos ejecutables de la API, generados desde los **bloques etiquetados del Markdown**, no de una segunda implementación manual.
- [E2E](M03_E2E_RESULTADOS.json): evidencia de los 96 pasos, compilaciones, proyectos y pruebas acumuladas.

## Requisitos y arquitectura

SDK .NET 8, Visual Studio con ASP.NET/web, SQL Server Express LocalDB para ejecutar las API en Windows. Los tests de integración usan EF Core InMemory, sin exigir SQL Server en CI. Se conservan los endpoints REST de M02; en 3.4 se añaden endpoints hexagonales con un puerto real, casos de uso y un repositorio EF Core separado en proyectos físicos.

Los cuatro puntos de M03 usan las carpetas 3.1, 3.2, 3.3 y 3.4 autónomas, manteniendo el anterior como referencia sin sobrescribirlo.

## E2E

```bash
python3 .github/scripts/m03_e2e_desde_practicas.py --out M03_ARQUITECTURA_HEXAGONAL/M03_E2E_RESULTADOS.json
```

Este comprobador copia exclusivamente el **punto 2.4 aprobado de M02**, reconstruye cada etapa de M03 leyendo los 96 pasos del Markdown y ejecuta compilaciones y pruebas. Los pasos exclusivamente manuales de Visual Studio se documentan con evidencia esperada, pero no se afirma haber ejecutado clics en el IDE. El workflow publica los proyectos y los PDF solo después de que el E2E se complete correctamente.
