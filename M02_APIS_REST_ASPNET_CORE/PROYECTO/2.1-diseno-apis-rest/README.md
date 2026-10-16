# M02 — Etapa 1/4 · API REST en ASP.NET Core 8

Este proyecto funciona independientemente del resto. El alumnado lo construye
de forma progresiva siguiendo M02_PRACTICAS.md, con Visual Studio y SQL Server
Express LocalDB (Windows). NO requiere comandos Git.

## Ejecución
1. Abrir src/AceriaApp.Api/AceriaApp.Api.csproj en Visual Studio.
2. Comprobar que está instalado .NET 8 y SQL Server Express LocalDB.
3. Ejecutar `dotnet restore` y `dotnet run --project src/AceriaApp.Api`.
4. Probar las peticiones HTTP del archivo AceriaApp.http.
5. Ejecutar `dotnet test tests/AceriaApp.Api.Tests`.

En Development, EnsureCreated crea la base de aprendizaje sin migraciones.
No debe usarse como estrategia de despliegue productivo.
La API emplea SQL Server Express LocalDB; EF Core InMemory está solo en tests.
Etapa: GET de colección y detalle.
