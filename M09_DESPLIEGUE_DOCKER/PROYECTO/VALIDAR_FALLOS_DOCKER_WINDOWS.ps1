<#
M09 - Ensayo adicional de tolerancia a fallo de una instancia y de RabbitMQ.
Ejecutar con el laboratorio M09 ya levantado.
Linux CI: -PermitirLinuxEnCI sólo para validación técnica, NO certifica Docker Desktop Windows.
No borra datos ni volúmenes; intenta restaurar servicios en finally.
#>
[CmdletBinding()]
param([switch]$PermitirLinuxEnCI)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $IsWindows -and -not $PermitirLinuxEnCI) {
    throw 'Esta práctica se desarrolla en Windows + Docker Desktop. Solo Linux CI puede omitir el control con -PermitirLinuxEnCI.'
}
$lab = $PSScriptRoot
$compose = Join-Path $lab 'docker/compose.fullstack.yml'
$envfile = Join-Path $lab '.env'
if (-not (Test-Path $envfile)) { throw 'Falta .env de laboratorio.' }
$platform = (& docker info --format '{{.OSType}}' 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $platform -ne 'linux') {
    throw 'Se requiere motor Docker con contenedores Linux.'
}

function Compose([string[]] $arguments) {
    & docker compose --env-file $envfile -f $compose @arguments
    if ($LASTEXITCODE -ne 0) { throw "Compose falló: $($arguments -join ' ')" }
}
function Http([string]$uri) {
    try {
        return Invoke-WebRequest -Uri $uri -TimeoutSec 6 -SkipHttpErrorCheck
    } catch { return $null }
}
function Ready([int]$port) {
    $response = Http "http://localhost:$port/health/ready"
    return ($null -ne $response -and $response.StatusCode -eq 200)
}
function Wait-Ready([int]$port, [int]$attempts=90) {
    for ($i=0; $i -lt $attempts; $i++) {
        if (Ready $port) { return }
        Start-Sleep -Seconds 2
    }
    throw "Puerto $port no recuperó readiness."
}
function Get-Instancia {
    $r = Http 'http://localhost:5100/api/v1/materiales/Acero'
    if ($null -eq $r -or $r.StatusCode -ne 200) { return '' }
    return [string]$r.Headers['X-Instancia']
}
function Wait-Balanceo([int]$attempts=90) {
    $observed = @{}
    for ($i=0; $i -lt $attempts; $i++) {
        $n = Get-Instancia
        if ($n) { $observed[$n] = $true }
        if ($observed.ContainsKey('inventario-1') -and
            $observed.ContainsKey('inventario-2')) { return }
        Start-Sleep -Seconds 2
    }
    throw "No se observaron ambas instancias: $($observed.Keys -join ', ')"
}

$reporte=[ordered]@{
    fecha_utc=[DateTime]::UtcNow.ToString('o')
    anfitrion=$(if ($IsWindows) {'Windows + Docker Desktop'} else {'Linux CI: NO certifica Windows'})
    resultado='FAIL'
    pruebas=[ordered]@{}
}
$inv2Stopped=$false
$rabbitStopped=$false
try {
    Wait-Ready 5105
    Wait-Ready 5106
    Wait-Ready 5107
    Wait-Balanceo
    $reporte.pruebas.balanceo_inicial='PASS'

    # PASO 9.13: el destino restante debe sostener las lecturas.
    Compose @('stop','inventario-2')
    $inv2Stopped=$true
    $convergencia=$false
    for ($i=0; $i -lt 75; $i++) {
        $n=Get-Instancia
        if ($n -eq 'inventario-1') { $convergencia=$true; break }
        Start-Sleep -Seconds 2
    }
    if (-not $convergencia) {
        throw 'YARP no alcanzó a Inventario 1 tras detener Inventario 2.'
    }
    for ($i=0; $i -lt 10; $i++) {
        $n=Get-Instancia
        if ($n -ne 'inventario-1') {
            throw "Inventario 1 no atendió una de las diez consultas ($n)."
        }
    }
    $reporte.pruebas.fallo_inventario_2='PASS'
    Compose @('start','inventario-2')
    $inv2Stopped=$false
    Wait-Ready 5107
    Wait-Balanceo
    $reporte.pruebas.recuperacion_inventario_2='PASS'

    # PASO 9.14: readiness debe degradarse cuando el broker se detiene.
    Compose @('stop','rabbitmq')
    $rabbitStopped=$true
    $degradado=$false
    for ($i=0; $i -lt 75; $i++) {
        $r=Http 'http://localhost:5106/health/ready'
        if ($null -eq $r -or $r.StatusCode -ne 200) {
            $degradado=$true
            break
        }
        Start-Sleep -Seconds 2
    }
    if (-not $degradado) {
        throw 'Readiness de Inventario no detectó la caída de RabbitMQ.'
    }
    $reporte.pruebas.readiness_sin_rabbitmq='PASS'
    Compose @('start','rabbitmq')
    $rabbitStopped=$false
    $ping=$false
    for ($i=0; $i -lt 75; $i++) {
        & docker compose --env-file $envfile -f $compose exec -T rabbitmq rabbitmq-diagnostics -q ping 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) { $ping=$true; break }
        Start-Sleep -Seconds 2
    }
    if (-not $ping) { throw 'RabbitMQ no respondió a ping tras recuperarse.' }
    foreach ($port in @(5105,5106,5107)) { Wait-Ready $port }
    $reporte.pruebas.recuperacion_rabbitmq='PASS'
    $reporte.resultado='PASS'
} catch {
    $reporte.error=$_.Exception.Message
    Write-Host "FAIL en prueba de resiliencia: $($reporte.error)"
} finally {
    # Restauración de infraestructura en cualquier caso, sin borrar volúmenes.
    if ($rabbitStopped) {
        try { Compose @('start','rabbitmq') } catch {
            Write-Host "ADVERTENCIA: no pudo restaurarse RabbitMQ: $($_.Exception.Message)"
        }
    }
    if ($inv2Stopped) {
        try { Compose @('start','inventario-2') } catch {
            Write-Host "ADVERTENCIA: no pudo restaurarse Inventario 2: $($_.Exception.Message)"
        }
    }
    $dir=Join-Path $lab '.qa'
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    $file=Join-Path $dir 'docker-fallos-e2e.json'
    $reporte | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $file -Encoding utf8
    Write-Host "Evidencia resiliencia: $file; resultado: $($reporte.resultado)"
}
if ($reporte.resultado -ne 'PASS') { exit 1 }
Write-Host 'PASS resiliencia M09: balanceo, caída/recuperación Inventario 2 y RabbitMQ.'
