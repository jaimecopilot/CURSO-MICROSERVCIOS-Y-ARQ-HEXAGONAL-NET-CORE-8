# Proyecto M09 — Despliegue Docker de AceriaApp

El código C# no se duplica. Las imágenes se compilan **directamente** desde `../../M08_API_GATEWAY/PROYECTO/8.4-balanceo-carga` mediante `docker/Dockerfile.Servicio`. La carpeta contiene infraestructura y automatización:

- `docker/Dockerfile.Servicio`: imagen multietapa .NET 8.
- `docker/compose.fullstack.yml`: SQL Server, RabbitMQ, Producción, Inventario x2 y YARP.
- `.env.example`: copia a `.env` y cambia la contraseña; no publiques credenciales.
- `EJECUTAR_DOCKER_WINDOWS.ps1`: preparar, levantar, verificar, detener, bajar y limpiar.
- `VALIDAR_FALLOS_DOCKER_WINDOWS.ps1`: tras levantar, detener y recuperar Inventario 2 y RabbitMQ, sin borrar sus volúmenes.
- `CERTIFICAR_DOCKER_DESKTOP_WINDOWS.ps1`: prueba de cierre desde un **Windows 10/11 real** con Docker Desktop sobre WSL 2; verifica el sistema anfitrión, ejecuta las pruebas anteriores y guarda un certificado JSON.

En PowerShell 7, dentro de `PROYECTO`:

```powershell
Copy-Item .\.env.example .\.env
notepad .\.env
.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion preparar
.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion levantar
.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion verificar
.\VALIDAR_FALLOS_DOCKER_WINDOWS.ps1
.\EJECUTAR_DOCKER_WINDOWS.ps1 -Accion verificar
```

Consulta [los 16 pasos de M09](../PRACTICAS/M09_PRACTICAS.md). El motor debe ser Docker Desktop con contenedores Linux sobre Windows y WSL2. No se debe ejecutar `limpiar` si se pretende demostrar persistencia.

La prueba de fallos exige que los seis contenedores ya estén operativos y guarda `.qa/docker-fallos-e2e.json`. GitHub Actions también la ejecuta sobre Linux con `-PermitirLinuxEnCI`, pero solo una ejecución real en Docker Desktop para Windows certifica el entorno práctico del alumno.


## Certificación final sobre Windows

Además del recorrido didáctico anterior, en un equipo Windows 10/11 compatible, con Docker Desktop iniciado en modo Linux/WSL 2 y PowerShell 7, se puede ejecutar directamente desde `PROYECTO`:

```powershell
.\CERTIFICAR_DOCKER_DESKTOP_WINDOWS.ps1
```

El comando no utiliza el modo Linux de CI, no acepta Windows Server, revisa la presencia de WSL 2 y del motor Docker Desktop, y ejecuta una prueba integral seguida de los dos fallos controlados y de una nueva prueba funcional. Escribe **tres informes** en `.qa/`: `docker-windows-e2e.json`, `docker-fallos-e2e.json` y `certificacion-windows-docker-desktop.json`. El último solo contiene `resultado=PASS` cuando todas las operaciones terminan correctamente. No se destruyen volúmenes. La contraseña SQL se toma de `.env`; si falta, se crea una de laboratorio aleatoria sin mostrarla en pantalla.

Para ejecutar este mismo comprobador desde GitHub Actions, se ha añadido `.github/workflows/m09-certificacion-windows-desktop.yml`. Exige un runner **self-hosted** con las etiquetas `Windows`, `X64` y `docker-desktop-wsl2`, instalado en un Windows 10/11 compatible dentro de una sesión que tenga Docker Desktop abierto. Se ejecuta exclusivamente de forma manual. No debe utilizarse en un runner estándar `windows-2022`, ya que Docker Desktop no está admitido en Windows Server. Una ejecución pendiente por falta de runner **no** se considera aprobada.

La prueba Linux existente continúa siendo evidencia independiente; no se transforma en una certificación Windows por ejecutar el mismo PowerShell en Linux.
