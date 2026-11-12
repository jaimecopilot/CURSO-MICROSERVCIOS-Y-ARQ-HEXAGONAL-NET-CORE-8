# M09 — Despliegue integral de AceriaApp con Docker Desktop para Windows

**Módulo exclusivamente práctico · Proyecto AceriaApp (.NET 8)**

El objetivo es **desplegar en Docker todos los componentes ejecutables** sin reprogramar M08. Se reutiliza el código de `M08_API_GATEWAY/PROYECTO/8.4-balanceo-carga`.

## Material didáctico

- [Prácticas guiadas M09 en Markdown](PRACTICAS/M09_PRACTICAS.md) · [PDF](PRACTICAS/M09_PRACTICAS.pdf).
- [Proyecto de despliegue](PROYECTO/README.md): Dockerfile multietapa, Compose, variables y script de PowerShell 7.

## Seis contenedores

| Contenedor | Función |
|---|---|
| `sqlserver` | SQL Server Express: persistencia de Producción e Inventario |
| `rabbitmq` | Mensajería AMQP, publicación y recepción de eventos |
| `produccion` | API de Producción y outbox |
| `inventario-1` | API y consumidor de eventos |
| `inventario-2` | Segunda instancia para balanceo |
| `gateway` | API Gateway YARP |

La solución utiliza una red Compose privada, dos volúmenes persistentes y puertos locales. Windows ejecuta Docker Desktop y PowerShell; las imágenes utilizan Linux dentro de WSL2. LocalDB **no funciona dentro de estos contenedores**, por eso se usa SQL Server Express.

## Comenzar en Windows (PowerShell 7)

Desde la raíz del repositorio:

```powershell
Set-Location .\M09_DESPLIEGUE_DOCKER\PROYECTO
Copy-Item .\.env.example .\.env
notepad .\.env     # Cambiar contraseña didáctica
.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion preparar
.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion levantar
.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion verificar
```

Se comprueban SQL Server, RabbitMQ, tres APIs, Gateway YARP, balanceo, eventos outbox/inbox, peticiones HTTP y persistencia tras reiniciar. Para detener conservando datos: `.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion detener`.

**Certificación:** una ejecución correcta del sistema en Linux no acredita Docker Desktop sobre un Windows real; esa validación es independiente.
