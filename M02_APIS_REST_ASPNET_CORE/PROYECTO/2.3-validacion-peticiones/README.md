# Punto 2.3 — Validación de peticiones

## Objetivo
Construir una evolución verificable del monolito AceriaApp aplicando los conceptos de diseño de APIs REST.

## Estado de la solución
- Solución AceriaApp.sln con 9 proyectos en total (una API y 8 proyectos de pruebas).
- 42 pruebas previstas en la solución completa, pendientes de comprobar mediante CI.
- Documento docs/validacion-peticiones.md y las decisiones arquitectónicas acumuladas.
- El proyecto es independiente: conserva los archivos del punto previo salvo integraciones aditivas documentadas.

## Cómo ejecutarlo
1. Abrir AceriaApp.sln en Visual Studio con SDK .NET 8.
2. Restaurar con dotnet restore AceriaApp.sln.
3. Compilar con dotnet build AceriaApp.sln.
4. Ejecutar dotnet test AceriaApp.sln.
5. Configurar SQL Server Express e iniciar la API con dotnet run --project src/AceriaApp.Monolito.Api.

## Qué incorpora este punto
- Contrato y validador de creación, filtro reutilizable y ADR-008.
- Program.cs incorpora únicamente dos líneas aditivas: using AceriaApp.Monolito.Api.Validacion; y builder.Services.AddValidacion();.
- ValidacionExtensions contiene el registro y las seis pruebas nuevas no se atribuyen indebidamente al filtro.

## Documentación
- docs/validacion-peticiones.md
- Los ADR previos conservados sin alteración.
