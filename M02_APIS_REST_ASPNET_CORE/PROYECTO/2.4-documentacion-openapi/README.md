# Punto 2.4 — Documentación mediante OpenAPI (Swagger)

## Objetivo
Construir una evolución verificable del monolito AceriaApp aplicando los conceptos de diseño de APIs REST.

## Estado de la solución
- Solución AceriaApp.sln con 10 proyectos en total (una API y 9 proyectos de pruebas).
- 51 pruebas previstas en la solución completa, pendientes de comprobar mediante CI.
- Documento docs/documentacion-openapi.md y las decisiones arquitectónicas acumuladas.
- El proyecto es independiente: conserva los archivos del punto previo salvo integraciones aditivas documentadas.

## Cómo ejecutarlo
1. Abrir AceriaApp.sln en Visual Studio con SDK .NET 8.
2. Restaurar con dotnet restore AceriaApp.sln.
3. Compilar con dotnet build AceriaApp.sln.
4. Ejecutar dotnet test AceriaApp.sln.
5. Configurar SQL Server Express e iniciar la API con dotnet run --project src/AceriaApp.Monolito.Api.

## Qué incorpora este punto
- SwaggerGen y SwaggerUI configurados desde DocumentacionExtensions; metadatos reales.
- Program.cs de esta copia integra las extensiones y anota los endpoints.
- WebApplicationFactory contrasta la respuesta HTTP real del documento en Development y su ausencia en Production.
- Nueve pruebas nuevas y ADR-009.

## Documentación
- docs/documentacion-openapi.md
- Los ADR previos conservados sin alteración.
