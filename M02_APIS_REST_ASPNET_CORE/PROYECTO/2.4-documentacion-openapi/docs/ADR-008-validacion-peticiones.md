# ADR-008 — FluentValidation y filtros

## Estado
Aceptado

## Contexto
AceriaApp necesita ampliar su contrato HTTP sin confundir los recursos de negocio con las entidades de persistencia.

## Decisión
Se encapsula el registro de validadores en ValidacionExtensions y se reserva la ejecución del filtro para endpoints que acepten el DTO validado.

## Alternativas consideradas
Se descartó la documentación exclusivamente manual por su riesgo de obsolescencia y los nombres de rutas orientados a verbos por su menor consistencia.

## Consecuencias
La evolución queda trazada en cada carpeta autónoma. Los cambios de arranque, cuando son imprescindibles, se hacen únicamente en la copia nueva de Program.cs. Las pruebas deben contrastar el funcionamiento, no solo la existencia de archivos.
