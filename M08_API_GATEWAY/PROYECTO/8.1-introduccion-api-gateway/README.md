# Punto 8.1 — Introducción al patrón API Gateway

## Objetivo

Modelar rutas y responsabilidades del gateway, conservando las decisiones anteriores de AceriaApp.

## Estado del proyecto

Etapa acumulativa con 35 proyectos, 23 proyectos de tests y 44 documentos. El cierre exige 415 pruebas aprobadas sin omisiones; los resultados se registran en los informes del módulo.

## Cómo ejecutarlo

Desde esta carpeta: `dotnet restore AceriaApp.sln`, `dotnet build AceriaApp.sln -c Release` y `dotnet test AceriaApp.sln -c Release`. Configura SQL Server/LocalDB y RabbitMQ según el manual antes de ejecutar la suite completa.

## Qué se ha añadido respecto al punto anterior

- Modelo RutaGateway, validador ValidadorApiGateway y catálogo CatalogoRutas.
- 12 pruebas de catálogo y 0 pruebas funcionales nuevas.
- Documento temático y ADR-031.
- Reto optativo en copia separada, con una prueba adicional.

## Documentación

- `docs/introduccion-api-gateway.md`.
- `docs/ADR-031-introduccion-api-gateway.md`.
- Las 42 fichas y decisiones anteriores permanecen idénticas.
