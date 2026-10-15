# ADR-009 — Documentación ejecutable

## Estado
Aceptado

## Contexto
AceriaApp necesita ampliar su contrato HTTP sin confundir los recursos de negocio con las entidades de persistencia.

## Decisión
Se emplea SwaggerGen real, encapsulado en extensiones, y WebApplicationFactory para comprobar la respuesta HTTP.

## Alternativas consideradas
Se descartó la documentación exclusivamente manual por su riesgo de obsolescencia y los nombres de rutas orientados a verbos por su menor consistencia.

## Consecuencias
La evolución queda trazada en cada carpeta autónoma. Los cambios de arranque, cuando son imprescindibles, se hacen únicamente en la copia nueva de Program.cs. Las pruebas deben contrastar el funcionamiento, no solo la existencia de archivos.
