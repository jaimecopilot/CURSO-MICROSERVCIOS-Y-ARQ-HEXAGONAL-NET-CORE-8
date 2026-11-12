# Punto 8.3 — Enrutamiento de peticiones

## Objetivo

Aplicar coincidencias de ruta, restricciones de método y transformaciones observables de petición.

## Estado del proyecto

Etapa acumulativa con 38 proyectos, 25 proyectos de tests y 48 documentos. El cierre exige 476 pruebas aprobadas sin omisiones; los resultados se registran en los informes del módulo.

## Cómo ejecutarlo

Desde esta carpeta: `dotnet restore AceriaApp.sln`, `dotnet build AceriaApp.sln -c Release` y `dotnet test AceriaApp.sln -c Release`. Configura SQL Server/LocalDB y RabbitMQ según el manual antes de ejecutar la suite completa.

El recorrido funcional inicia Gateway en 5100, Producción en 5105 e Inventario en 5106. La etapa 8.4 añade Inventario en 5107.

## Qué se ha añadido respecto al punto anterior

- Modelo ReglaEnrutamiento, validador ValidadorEnrutamiento y catálogo CatalogoReglasEnrutamiento.
- 10 pruebas de catálogo y 15 pruebas funcionales nuevas.
- Documento temático y ADR-033.
- Reto optativo en copia separada, con una prueba adicional.

## Documentación

- `docs/enrutamiento-peticiones.md`.
- `docs/ADR-033-enrutamiento-peticiones.md`.
- Las 46 fichas y decisiones anteriores permanecen idénticas.
