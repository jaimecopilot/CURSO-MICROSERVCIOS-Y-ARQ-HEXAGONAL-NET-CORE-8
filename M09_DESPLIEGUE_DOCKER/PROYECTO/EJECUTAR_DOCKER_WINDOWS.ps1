<#
M09 - Despliegue Docker Windows (.NET 8): prepara, levanta, verifica, detiene o limpia.
Ejecución real exige Docker Desktop con Linux containers sobre WSL 2.
No es un certificado hasta que todas las llamadas devuelvan PASS.
#>
[CmdletBinding()]
param(
    [ValidateSet('preparar','levantar','verificar','detener','bajar','limpiar')]
    [string]$Accion = 'preparar',
    [switch]$ConfirmarBorradoDatos,
    [switch]$PermitirLinuxEnCI
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $IsWindows -and -not $PermitirLinuxEnCI) {
    throw 'Esta práctica certifica Docker Desktop en Windows. -PermitirLinuxEnCI solo es para la prueba técnica Linux (no certifica Windows).'
}
$lab = $PSScriptRoot
$compose = Join-Path $lab 'docker/compose.fullstack.yml'
$envfile = Join-Path $lab '.env'
if (-not (Test-Path -LiteralPath $envfile)) {
    throw "Falta $envfile; copie .env.example, cambie su clave y no publique .env."
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'No se encuentra docker; instale/abra Docker Desktop en Windows.'
}
$platform = (& docker info --format '{{.OSType}}' 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $platform -ne 'linux') {
    throw 'Docker Desktop no expone un motor de contenedores Linux.'
}
$dockerOS = (& docker info --format '{{.OperatingSystem}}' 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0) { throw 'No se pudo comprobar el sistema del motor Docker.' }
if ($IsWindows -and $dockerOS -notmatch 'Docker Desktop') {
    throw "El motor Linux responde en Windows, pero no se ha acreditado Docker Desktop: $dockerOS"
}

function Compose([string[]]$argsList) {
    & docker compose --env-file $envfile -f $compose @argsList
    if ($LASTEXITCODE -ne 0) { throw "docker compose falló: $($argsList -join ' ')" }
}
Compose @('config','--quiet')
if ($Accion -eq 'preparar') {
    Write-Host 'PASS: Docker Desktop Linux y sintaxis Compose preparados (sin contenedores).'
    exit 0
}
if ($Accion -eq 'detener') {
    Compose @('stop')
    Write-Host 'Se han detenido los servicios conservando SQL y colas.'
    exit 0
}
if ($Accion -eq 'bajar') {
    Compose @('down')
    Write-Host 'Se han retirado los contenedores y red, conservando volúmenes.'
    exit 0
}
if ($Accion -eq 'limpiar') {
    if (-not $ConfirmarBorradoDatos) {
        throw 'Para destruir datos del laboratorio incluya -ConfirmarBorradoDatos.'
    }
    Compose @('down','-v')
    Write-Host 'Datos didácticos destruidos por solicitud explícita.'
    exit 0
}
function Esperar-Http([string]$uri, [int]$repeticiones = 90) {
    for ($k = 0; $k -lt $repeticiones; $k++) {
        try {
            $respuesta = Invoke-WebRequest -Uri $uri -TimeoutSec 5 -SkipHttpErrorCheck
            if ($respuesta.StatusCode -eq 200) { return }
        } catch {}
        Start-Sleep -Seconds 2
    }
    throw "No se obtuvo HTTP 200 de $uri."
}
function Esperar-Sql {
    for ($k = 0; $k -lt 120; $k++) {
        $id = (& docker compose --env-file $envfile -f $compose ps -q sqlserver 2>$null | Select-Object -First 1)
        if ($id) {
            $estado = (& docker inspect --format '{{.State.Health.Status}}' $id 2>$null | Out-String).Trim()
            if ($estado -eq 'healthy') { return }
        }
        Start-Sleep -Seconds 2
    }
    throw 'SQL Server Express no ha alcanzado healthy; consulte logs sqlserver.'
}
function Comprobar-Salud {
    $live = Invoke-RestMethod 'http://localhost:5100/health/live' -TimeoutSec 10
    if ($live.servicio -ne 'Gateway' -or $live.estado -ne 'vivo') {
        throw 'Gateway no expuso liveness real.'
    }
    foreach ($puerto in @(5105,5106,5107)) {
        $salud = Invoke-RestMethod "http://localhost:$puerto/health/ready" -TimeoutSec 10
        if ($salud.estado -ne 'Healthy') {
            throw "Readiness no está Healthy en puerto $puerto."
        }
    }
}
if ($Accion -eq 'levantar') {
    Compose @('up','-d','sqlserver','rabbitmq')
    Esperar-Sql
    foreach ($servicio in @(
        @{ nombre='inventario-1'; url='http://localhost:5106/health/ready' },
        @{ nombre='inventario-2'; url='http://localhost:5107/health/ready' },
        @{ nombre='produccion'; url='http://localhost:5105/health/ready' },
        @{ nombre='gateway'; url='http://localhost:5100/health/live' }
    )) {
        Compose @('up','-d','--build','--no-deps', $servicio.nombre)
        Esperar-Http $servicio.url
        Write-Host "PASS: $($servicio.nombre) está listo."
    }
}
if ($Accion -eq 'verificar') {
    Esperar-Http 'http://localhost:5100/health/live'
    foreach ($puerto in @(5105,5106,5107)) { Esperar-Http "http://localhost:$puerto/health/ready" }
}
$reporte = [ordered]@{
    fecha_utc = [DateTime]::UtcNow.ToString('o')
    anfitrion = $(if ($IsWindows) { 'Windows + Docker Desktop (contenedores Linux)' } else { 'Linux GitHub Actions; NO certifica Docker Desktop Windows' })
    sistema_operativo_motor_docker = $dockerOS
    accion = $Accion
    resultado = 'FAIL'
    pruebas = [ordered]@{}
}
try {
    Comprobar-Salud
    $reporte.pruebas.salud = 'PASS'
    $base = 'http://localhost:5100'
    $stock = Invoke-RestMethod "$base/api/v1/materiales/Acero" -TimeoutSec 10
    if ($stock.stock -ne 300) { throw "Stock inicial inesperado: $($stock.stock)" }
    $reporte.pruebas.yarp_stock = 'PASS'
    $instancias = @{}
    for ($i=0; $i -lt 12; $i++) {
        $r = Invoke-WebRequest "$base/api/v1/materiales/Acero" -TimeoutSec 10
        if ($r.StatusCode -ne 200) { throw 'Balanceo: HTTP != 200.' }
        $n = [string]$r.Headers['X-Instancia']
        if ($n) { $instancias[$n] = $true }
    }
    if (-not $instancias.ContainsKey('inventario-1') -or -not $instancias.ContainsKey('inventario-2')) {
        throw "YARP no recorrió ambas instancias: $($instancias.Keys -join ', ')"
    }
    $reporte.pruebas.balanceo = 'PASS'
    $cuerpo = @{ cliente='Axia Docker E2E'; material='Acero'; cantidad=20 } | ConvertTo-Json
    $creada = Invoke-WebRequest -Uri "$base/api/v1/produccion/ordenes" -Method Post -ContentType 'application/json' -Body $cuerpo -SkipHttpErrorCheck -TimeoutSec 30
    if ($creada.StatusCode -ne 201) { throw "POST producción no dio 201: $($creada.Content)" }
    $id = [string](($creada.Content | ConvertFrom-Json).id)
    if ([guid]$id -eq [guid]::Empty) { throw 'Orden sin GUID.' }
    $uri = "$base/api/v1/produccion/ordenes/$id"
    $linea = @{ material='Inoxidable'; cantidad=10 } | ConvertTo-Json
    $agregada = Invoke-WebRequest -Uri "$uri/lineas" -Method Post -ContentType 'application/json' -Body $linea -SkipHttpErrorCheck -TimeoutSec 30
    if ($agregada.StatusCode -ne 200) { throw "POST segunda línea no devolvió 200: $($agregada.Content)" }
    $borrador = Invoke-RestMethod $uri -TimeoutSec 10
    if ($borrador.estado -ne 'Borrador' -or $borrador.cantidadTotal -ne 30 -or @($borrador.lineas).Count -ne 2) {
        throw 'El agregado creado no conserva dos líneas y cantidad 30.'
    }
    $plan = "$base/api/v1/comunicacion/ordenes/$id/planificar"
    $aceptada = Invoke-WebRequest -Uri $plan -Method Post -ContentType 'application/json' -Body '{}' -SkipHttpErrorCheck -TimeoutSec 30
    if ($aceptada.StatusCode -ne 202) { throw "Planificar no devolvió 202: $($aceptada.Content)" }
    $duplicada = Invoke-WebRequest -Uri $plan -Method Post -ContentType 'application/json' -Body '{}' -SkipHttpErrorCheck -TimeoutSec 30
    if ($duplicada.StatusCode -ne 409) { throw 'Repetir planificación no devolvió 409.' }
    $reporte.pruebas.produccion_http = 'PASS'
    $proyeccion = "$base/api/v1/planificaciones/$id"
    $recibida = $null
    for ($i=0; $i -lt 90; $i++) {
        $r = Invoke-WebRequest $proyeccion -SkipHttpErrorCheck -TimeoutSec 10
        if ($r.StatusCode -eq 200) {
            $recibida = $r.Content | ConvertFrom-Json
            break
        }
        if ($r.StatusCode -ne 404) { throw "Error inesperado de proyección: HTTP $($r.StatusCode)" }
        Start-Sleep -Seconds 2
    }
    if ($null -eq $recibida -or [string]$recibida.ordenId -ne $id -or $recibida.cantidadTotal -ne 30) {
        throw 'No se pudo comprobar la entrega real outbox/inbox.'
    }
    $reporte.pruebas.evento_outbox_inbox = 'PASS'
    Compose @('restart','inventario-1','inventario-2','produccion','gateway')
    Esperar-Http 'http://localhost:5100/health/live'
    foreach ($puerto in @(5105,5106,5107)) { Esperar-Http "http://localhost:$puerto/health/ready" }
    Comprobar-Salud
    $ordenPostReinicio = Invoke-RestMethod $uri -TimeoutSec 20
    $eventoPostReinicio = Invoke-RestMethod $proyeccion -TimeoutSec 20
    if ($ordenPostReinicio.estado -ne 'Planificada' -or $ordenPostReinicio.cantidadTotal -ne 30 -or
        [string]$eventoPostReinicio.eventoId -ne [string]$recibida.eventoId) {
        throw 'El reinicio alteró datos o identidad del evento.'
    }
    $reporte.pruebas.persistencia_despues_reinicio = 'PASS'
    $reporte.orden_id = $id
    $reporte.evento_id = [string]$recibida.eventoId
    $reporte.resultado = 'PASS'
} catch {
    $reporte.error = $_.Exception.Message
    Write-Host "FAIL: $($reporte.error)"
} finally {
    $destino = Join-Path $lab '.qa'
    New-Item -ItemType Directory -Path $destino -Force | Out-Null
    $file = Join-Path $destino 'docker-windows-e2e.json'
    $reporte | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $file -Encoding utf8
    Write-Host "Evidencia: $file | resultado: $($reporte.resultado)"
}
if ($reporte.resultado -ne 'PASS') { exit 1 }
Write-Host 'PASS integral: SQL Server Express + RabbitMQ + API + dos inventarios + YARP + evento + persistencia.'
