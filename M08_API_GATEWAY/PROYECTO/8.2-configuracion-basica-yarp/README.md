# Punto 8.2 — Configuración básica de YARP

## Objetivo

Configurar y ejecutar un gateway YARP independiente hacia Producción e Inventario.

## Estado del proyecto

Etapa acumulativa con 37 proyectos, 24 proyectos de tests y 46 documentos. El cierre exige 451 pruebas aprobadas sin omisiones; los resultados se registran en los informes del módulo.

## Cómo ejecutarlo

Desde esta carpeta: `dotnet restore AceriaApp.sln`, `dotnet build AceriaApp.sln -c Release` y `dotnet test AceriaApp.sln -c Release`. Configura SQL Server/LocalDB y RabbitMQ según el manual antes de ejecutar la suite completa.

El recorrido funcional inicia Gateway en 5100, Producción en 5105 e Inventario en 5106. La etapa 8.4 añade Inventario en 5107.

## Qué se ha añadido respecto al punto anterior

- Modelo ClusterYarp, validador ValidadorConfiguracionYarp y catálogo CatalogoClusters.
- 10 pruebas de catálogo y 26 pruebas funcionales nuevas.
- Documento temático y ADR-032.
- Reto optativo en copia separada, con una prueba adicional.

## Documentación

- `docs/configuracion-basica-yarp.md`.
- `docs/ADR-032-configuracion-basica-yarp.md`.
- Las 44 fichas y decisiones anteriores permanecen idénticas.
