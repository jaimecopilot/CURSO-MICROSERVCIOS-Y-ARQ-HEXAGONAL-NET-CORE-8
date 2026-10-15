# Punto 2.2 — Recursos, verbos HTTP y códigos de respuesta

## Objetivo
Construir una evolución verificable del monolito AceriaApp aplicando los conceptos de diseño de APIs REST.

## Estado de la solución
- Solución AceriaApp.sln con 8 proyectos en total (una API y 7 proyectos de pruebas).
- 36 pruebas previstas en la solución completa, pendientes de comprobar mediante CI.
- Documento docs/catalogo-recursos.md y las decisiones arquitectónicas acumuladas.
- El proyecto es independiente: conserva los archivos del punto previo salvo integraciones aditivas documentadas.

## Cómo ejecutarlo
1. Abrir AceriaApp.sln en Visual Studio con SDK .NET 8.
2. Restaurar con dotnet restore AceriaApp.sln.
3. Compilar con dotnet build AceriaApp.sln.
4. Ejecutar dotnet test AceriaApp.sln.
5. Configurar SQL Server Express e iniciar la API con dotnet run --project src/AceriaApp.Monolito.Api.

## Qué incorpora este punto
- Catálogo de recursos y ADR-007.
- Validador de combinaciones verbo-código; cinco nuevos casos xUnit.
- La tabla valida una convención local; no todos los códigos HTTP posibles.

## Documentación
- docs/catalogo-recursos.md
- Los ADR previos conservados sin alteración.
