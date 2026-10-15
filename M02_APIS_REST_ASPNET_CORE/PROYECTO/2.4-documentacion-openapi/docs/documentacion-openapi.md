# Documentación OpenAPI — 2.4
## Contrato generado
El middleware Swagger expone /swagger/v1/swagger.json exclusivamente en desarrollo. El documento se deriva de los endpoints de Program.cs, no se escribe a mano.
## Metadatos
Se exponen título, versión v1, descripción y contacto técnico ficticio.
## Secciones
info, paths, components y responses documentan lo realmente publicado. Las secciones servers, security o tags solo aparecen cuando corresponda.
## Ejemplos y esquemas
Los DTOs generarán esquemas cuando se usen como parámetros o respuestas declarados. SwaggerGen no infiere automáticamente los mensajes de FluentValidation.
## Verificación de integración
WebApplicationFactory inicia la aplicación, solicita el JSON, comprueba openapi, info.version y paths; también verifica que la ruta no se publique en Production.
## Cierre del módulo
- Cincuenta y una pruebas previstas en nueve proyectos de pruebas; diez proyectos en la solución.
- Nueve puntos acumulados (1.1 a 1.5 y 2.1 a 2.4).
- SQL Server Express sigue siendo el proveedor EF Core del curso.
