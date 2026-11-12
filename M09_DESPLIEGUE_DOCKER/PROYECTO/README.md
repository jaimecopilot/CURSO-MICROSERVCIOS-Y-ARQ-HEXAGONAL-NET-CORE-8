# Proyecto M09 — Despliegue Docker de AceriaApp

El código C# no se duplica. Las imágenes se compilan **directamente** desde `../../M08_API_GATEWAY/PROYECTO/8.4-balanceo-carga` mediante `docker/Dockerfile.Servicio`. La carpeta contiene infraestructura y automatización:

- `docker/Dockerfile.Servicio`: imagen multietapa .NET 8.
- `docker/compose.fullstack.yml`: SQL Server, RabbitMQ, Producción, Inventario x2 y YARP.
- `.env.example`: copia a `.env` y cambia la contraseña; no publiques credenciales.
- `EJECUTAR_DOCKER_WINDOWS.ps1`: preparar, levantar, verificar, detener, bajar y limpiar.

En PowerShell 7, dentro de `PROYECTO`:

```powershell
Copy-Item .\.env.example .\.env
notepad .\.env
.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion preparar
.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion levantar
```

Consulta [los 16 pasos de M09](../PRACTICAS/M09_PRACTICAS.md). El motor debe ser Docker Desktop con contenedores Linux sobre Windows y WSL2. No se debe ejecutar `limpiar` si se pretende demostrar persistencia.
