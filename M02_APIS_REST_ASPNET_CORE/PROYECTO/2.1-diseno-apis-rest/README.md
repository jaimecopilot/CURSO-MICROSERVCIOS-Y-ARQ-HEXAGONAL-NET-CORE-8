# Punto 2.1 — Diseño de APIs REST

## Objetivo
Construir una evolución verificable del monolito AceriaApp aplicando los conceptos de diseño de APIs REST.

## Estado de la solución
- Solución AceriaApp.sln con 7 proyectos en total (una API y 6 proyectos de pruebas).
- 31 pruebas previstas en la solución completa, pendientes de comprobar mediante CI.
- Documento docs/diseno-apis-rest.md y las decisiones arquitectónicas acumuladas.
- El proyecto es independiente: conserva los archivos del punto previo salvo integraciones aditivas documentadas.

## Cómo ejecutarlo
1. Abrir AceriaApp.sln en Visual Studio con SDK .NET 8.
2. Restaurar con dotnet restore AceriaApp.sln.
3. Compilar con dotnet build AceriaApp.sln.
4. Ejecutar dotnet test AceriaApp.sln.
5. Configurar SQL Server Express e iniciar la API con dotnet run --project src/AceriaApp.Monolito.Api.

## Qué incorpora este punto
- Documento REST y ADR-006.
- Clases de construcción, validación básica de URI y catálogo.
- Ocho pruebas nuevas; no se modifica el código heredado de M01.

## Documentación
- docs/diseno-apis-rest.md
- Los ADR previos conservados sin alteración.
