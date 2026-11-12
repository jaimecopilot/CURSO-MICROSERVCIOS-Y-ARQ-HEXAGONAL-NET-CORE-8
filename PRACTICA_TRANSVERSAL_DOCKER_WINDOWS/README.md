# Práctica transversal Docker Desktop para Windows

**Complemento de M01–M08. No es M09.**

Este laboratorio utiliza **Windows, PowerShell 7 y Docker Desktop con WSL 2 (contenedores Linux)**. Distingue el uso de Docker como infraestructura (SQL Server de pruebas o RabbitMQ) del despliegue completo de las APIs .NET 8 y YARP.

## Documentación y recursos

- [Manual guiado en Markdown](PRACTICAS_DOCKER_WINDOWS.md) · [PDF](PRACTICAS_DOCKER_WINDOWS.pdf): instalación, imágenes, redes, volúmenes, bases de datos, mensajería, APIs, pruebas y recuperación.
- [Dockerfile para aplicaciones .NET 8](docker/Dockerfile.Servicio).
- [Compose del sistema completo](docker/compose.fullstack.yml): SQL Server Express, RabbitMQ, Producción, Inventario 1 y 2, YARP.
- [Script PowerShell de despliegue y comprobación](EJECUTAR_DOCKER_WINDOWS.ps1).
- [Ejemplo de variables del laboratorio](.env.example). Copia como `.env` y cambia su contraseña; el archivo real **no debe subirse al repositorio**.

## Comenzar

Desde la raíz del repositorio abre PowerShell 7:

```powershell
Set-Location .\PRACTICA_TRANSVERSAL_DOCKER_WINDOWS
Copy-Item .\.env.example .\.env
notepad .\.env
.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion preparar
.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion levantar
```

El script comprueba servicios reales, HTTP, RabbitMQ, SQL Server Express, YARP y persistencia. Los ejercicios de parada y recuperación se describen en el manual. Detener servicios no requiere borrar volúmenes.

**Importante:** la certificación completa de Docker Desktop requiere ejecutar el laboratorio en un ordenador Windows real; una ejecución correcta del mismo Compose sobre Linux no demuestra que Docker Desktop funcione en tu PC. Las contraseñas y opciones de confianza de certificados del ejemplo son únicamente para formación local.
