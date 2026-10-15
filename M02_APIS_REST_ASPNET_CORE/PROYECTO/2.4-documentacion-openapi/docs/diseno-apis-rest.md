# Diseño de APIs REST — 2.1
## Contrato de recursos
Las rutas identifican colecciones y recursos; no expresan órdenes en forma de verbos. La elección de versión en URI es una convención del curso, no un requisito universal de REST.
## Restricciones
Cliente-servidor, ausencia de estado, cacheabilidad, interfaz uniforme, capas y código bajo demanda (opcional).
## Rutas principales
- GET /api/v1/ordenes
- GET /api/v1/ordenes/{id}
- POST /api/v1/ordenes
- GET /api/v1/ordenes/{id}/lineas (contrato de futuro, todavía no implementado)
## Reglas del validador de ejemplo
El ejemplo valida prefijo api, versión vN y ausencia de segmentos de acción reservados. No constituye un verificador completo de cumplimiento REST ni sustituye una revisión del contrato.
## Representaciones
JSON es la representación implementada. Una cabecera Accept no garantiza automáticamente soporte para XML ni devolución 406.
