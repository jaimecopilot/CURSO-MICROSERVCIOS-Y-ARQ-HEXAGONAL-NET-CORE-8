# Punto 1.5 — Buenas prácticas

## Objetivo
Comprender las buenas prácticas aplicables al desarrollo de microservicios y añadir al proyecto las clases de validación de buenas prácticas. Cerrar el módulo 1 con el resumen del estado del proyecto.

## Estado del proyecto
- Solución `AceriaApp.sln` con seis proyectos: `AceriaApp.Monolito.Api`, `AceriaApp.Monolito.Tests`, `AceriaApp.Metricas.Tests`, `AceriaApp.Diseno.Tests`, `AceriaApp.Organizacion.Tests` y `AceriaApp.BuenasPracticas.Tests`.
- Documento `docs/buenas-practicas.md` con las cuatro categorías y el cierre del módulo 1.
- Clases `Practica`, `ValidadorBuenasPracticas` y `CatalogoPracticas` en `src/AceriaApp.Monolito.Api/BuenasPracticas/`.
- Cinco tests nuevos en `tests/AceriaApp.BuenasPracticas.Tests`.

## Cómo ejecutarlo
1. Abrir `AceriaApp.sln` en Visual Studio 2026.
2. Verificar que SQL Server Express está arrancado.
3. Ejecutar `dotnet ef database update` en `src\AceriaApp.Monolito.Api`.
4. Ejecutar `dotnet run` en `src\AceriaApp.Monolito.Api`.
5. Navegar a `/swagger` en el puerto indicado por la API.
6. Ejecutar `dotnet test AceriaApp.sln`.

## Qué se ha añadido respecto al punto anterior
- Documento `docs/buenas-practicas.md`.
- Carpeta `BuenasPracticas` en el proyecto monolítico con tres clases nuevas.
- Proyecto `tests/AceriaApp.BuenasPracticas.Tests` con cinco tests nuevos.
- Cierre del módulo 1 con el resumen del estado del proyecto.
- No se ha modificado ningún archivo de código heredado del punto 1.4.

## Documentación
- [ADR-001](docs/ADR-001-monolito-vs-microservicios.md)
- [ADR-002](docs/ADR-002-metricas-acoplamiento.md)
- [ADR-003](docs/ADR-003-principios-diseno.md)
- [ADR-004](docs/ADR-004-organizacion-solucion.md)
- [Análisis de ventajas e inconvenientes](docs/analisis-ventajas-inconvenientes.md)
- [Principios de diseño](docs/principios-diseno.md)
- [Organización de la solución](docs/organizacion-solucion.md)
- [Buenas prácticas](docs/buenas-practicas.md)

## Código progresivo del punto 1.5

Esta solución contiene **activo** el código del punto anterior. Los archivos nuevos del punto 1.5 están comentados inicialmente para que los actives según los pasos de las prácticas. No se altera el código heredado.

- **Paso 1.5.9:** `src/AceriaApp.Monolito.Api/BuenasPracticas/CatalogoPracticas.cs`
- **Paso 1.5.6:** `src/AceriaApp.Monolito.Api/BuenasPracticas/Practica.cs`
- **Paso 1.5.7:** `src/AceriaApp.Monolito.Api/BuenasPracticas/ValidadorBuenasPracticas.cs`
- **Paso 1.5.15:** `tests/AceriaApp.BuenasPracticas.Tests/CatalogoPracticasTests.cs`
- **Paso 1.5.14:** `tests/AceriaApp.BuenasPracticas.Tests/ValidadorBuenasPracticasTests.cs`

En Visual Studio, abre cada archivo cuando lo indique la práctica, selecciona **exclusivamente las líneas del bloque comentado** entre `INICIO PASO` y `FIN PASO`, y pulsa `Ctrl+K, Ctrl+U`. Primero se activan las clases de producción y después sus pruebas. Después de activar un paso, guarda el archivo y compila cuando lo indique la práctica. Evita descomentar bloques posteriores antes de llegar a ellos.

## Alcance de las buenas prácticas

Los objetos `Practica`, `ValidadorBuenasPracticas` y `CatalogoPracticas` permiten registrar y revisar **declaraciones** de aplicación de prácticas. No inspeccionan automáticamente los endpoints ni demuestran por sí solos que existan idempotencia HTTP, DTOs, Polly o respuestas Problem Details. Estas capacidades se desarrollan en puntos y módulos posteriores.
