# ADR-006 — Convenciones REST

## Estado
Aceptado

## Contexto
AceriaApp necesita ampliar su contrato HTTP sin confundir los recursos de negocio con las entidades de persistencia.

## Decisión
Se adoptan rutas versionadas /api/v1 con nombres de colección, semántica HTTP y un validador básico de nomenclatura.

## Alternativas consideradas
Se descartó la documentación exclusivamente manual por su riesgo de obsolescencia y los nombres de rutas orientados a verbos por su menor consistencia.

## Consecuencias
La evolución queda trazada en cada carpeta autónoma. Los cambios de arranque, cuando son imprescindibles, se hacen únicamente en la copia nueva de Program.cs. Las pruebas deben contrastar el funcionamiento, no solo la existencia de archivos.
