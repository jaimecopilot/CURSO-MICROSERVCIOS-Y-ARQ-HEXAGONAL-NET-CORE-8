# Práctica transversal — Docker Desktop para Windows y microservicios .NET 8

**No es M09.** Es un laboratorio práctico independiente de los ocho módulos que amplía los comandos Docker usados en M02–M08. No reemplaza ni altera las prácticas existentes ni el código de referencia de AceriaApp.

- `PRACTICAS_DOCKER_WINDOWS.md`: itinerario completo con qué, cómo, para qué, pruebas y fallos habituales.
- `docker/Dockerfile.Servicio`: compilación multietapa de .NET 8, parametrizada por proyecto.
- `docker/compose.fullstack.yml`: SQL Server Express, RabbitMQ, Producción, Inventario x2 y YARP.
- `.env.example`: credencial local de ejemplo; copiar como `.env` y no subir credenciales reales.
- `EJECUTAR_DOCKER_WINDOWS.ps1`: verificación Windows, despliegue secuencial, flujo HTTP/outbox/inbox y persistencia.

**Estado de la certificación:** los workflows Linux del curso ya verificaron E2E con SQL Server real y RabbitMQ. La rama de cierre añade pruebas Windows independientes; esta práctica integral Docker Desktop requiere además ejecutarse en un equipo Windows con WSL2/Docker Desktop, porque los runners Windows alojados de GitHub Actions no acreditan esa ejecución. No confundir evidencia estática o Linux con una certificación física de Docker Desktop en Windows.

La integración en `main` y el inicio de M09 quedan sujetos a cierre técnico, entrega editorial y revisión del usuario.
