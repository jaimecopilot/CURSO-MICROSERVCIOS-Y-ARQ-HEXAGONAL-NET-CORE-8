# Punto 8.4 — Balanceo de carga básico

## Objetivo

Distribuir solicitudes entre dos instancias de Inventario, detectar caída y comprobar recuperación.

## Estado del proyecto

Etapa acumulativa con 39 proyectos, 26 proyectos de tests y 50 documentos. El cierre exige 491 pruebas aprobadas sin omisiones; los resultados se registran en los informes del módulo.

## Cómo ejecutarlo

Desde esta carpeta: `dotnet restore AceriaApp.sln`, `dotnet build AceriaApp.sln -c Release` y `dotnet test AceriaApp.sln -c Release`. Configura SQL Server/LocalDB y RabbitMQ según el manual antes de ejecutar la suite completa.

El recorrido funcional inicia Gateway en 5100, Producción en 5105 e Inventario en 5106. La etapa 8.4 añade Inventario en 5107.

## Qué se ha añadido respecto al punto anterior

- Modelo ClusterBalanceo, validador ValidadorBalanceo y catálogo CatalogoClustersBalanceo.
- 10 pruebas de catálogo y 5 pruebas funcionales nuevas.
- Documento temático y ADR-034.
- Reto optativo en copia separada, con una prueba adicional.

## Documentación

- `docs/balanceo-carga.md`.
- `docs/ADR-034-balanceo-carga.md`.
- Las 48 fichas y decisiones anteriores permanecen idénticas.
