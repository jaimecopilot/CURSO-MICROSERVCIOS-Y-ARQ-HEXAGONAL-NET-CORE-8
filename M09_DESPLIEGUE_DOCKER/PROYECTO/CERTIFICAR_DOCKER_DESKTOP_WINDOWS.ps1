<#
M09: certificación real en Windows 10/11 con Docker Desktop/WSL2.
NO admite Linux CI ni Windows Server. Requiere PowerShell 7.
Genera evidencias JSON; nunca borra los volúmenes de SQL y RabbitMQ.
#>
[CmdletBinding()]
param([switch]$ConservarContenedores,[switch]$NoCrearEnv)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$root=$PSScriptRoot
$folder=Join-Path $root '.qa'
New-Item -ItemType Directory -Path $folder -Force | Out-Null
$out=Join-Path $folder 'certificacion-windows-docker-desktop.json'
$compose=Join-Path $root 'docker/compose.fullstack.yml'
$envFile=Join-Path $root '.env'
$oldProject=$env:COMPOSE_PROJECT_NAME
$env:COMPOSE_PROJECT_NAME='aceria-win-'+[guid]::NewGuid().ToString('N').Substring(0,8)
$report=[ordered]@{
  fecha_utc=[DateTime]::UtcNow.ToString('o')
  tipo='Windows Docker Desktop WSL 2'
  resultado='FAIL'
  comprobaciones=[ordered]@{}
}
$started=$false
try {
  if (-not $IsWindows) { throw 'La certificación se exige en Windows 10/11.' }
  if ($PSVersionTable.PSVersion.Major -lt 7) {
    throw 'Ejecute desde PowerShell 7 o superior.'
  }
  $report.comprobaciones.powershell='PASS'
  $os=Get-CimInstance Win32_OperatingSystem
  $build=[int]$os.BuildNumber
  if ($os.ProductType -ne 1) { throw 'Docker Desktop no está soportado en Windows Server.' }
  if ($build -lt 19045 -or ($build -ge 22000 -and $build -lt 22631)) {
    throw "Versión de Windows no compatible: build $build."
  }
  $report.windows=$os.Caption
  $report.build=$build
  $report.comprobaciones.windows_compatible='PASS'
  if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
    throw 'WSL no está disponible.'
  }
  $status=(& wsl.exe --status 2>&1 | Out-String).Replace([char]0,'')
  if ($LASTEXITCODE -ne 0) { throw 'WSL informa un error.' }
  $distros=(& wsl.exe --list --verbose 2>&1 | Out-String).Replace([char]0,'')
  if ($LASTEXITCODE -ne 0 -or $distros -notmatch '(?im)^\s*\*?\s*docker-desktop\b.*\s2\s*$') {
    throw 'Docker Desktop no aparece configurado sobre WSL2.'
  }
  $report.comprobaciones.wsl2='PASS'
  if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'No se encuentra docker CLI.'
  }
  $type=(& docker info --format '{{.OSType}}' | Out-String).Trim()
  $desktop=(& docker info --format '{{.OperatingSystem}}' | Out-String).Trim()
  if ($LASTEXITCODE -ne 0 -or $type -ne 'linux' -or $desktop -notmatch 'Docker Desktop') {
    throw "No se identifica Docker Desktop con motor Linux: $type / $desktop"
  }
  $report.motor=$desktop
  $report.comprobaciones.docker_desktop='PASS'
  & docker compose version | Out-Null
  if ($LASTEXITCODE -ne 0) { throw 'Docker Compose no responde.' }
  $report.comprobaciones.compose='PASS'
  $sdks=& dotnet --list-sdks
  if ($LASTEXITCODE -ne 0 -or (($sdks | Out-String) -notmatch '(?m)^8\.')) {
    throw 'Falta SDK .NET 8.'
  }
  $report.comprobaciones.sdk_net8='PASS'
  if (-not (Test-Path $envFile)) {
    if ($NoCrearEnv) { throw 'Cree .env con una contraseña segura para SQL.' }
    $bytes=[System.Security.Cryptography.RandomNumberGenerator]::GetBytes(24)
    $pw=[Convert]::ToHexString($bytes)+'aA1!'
    $line='ACERIA_SA_PASSWORD='+$pw+[Environment]::NewLine
    [System.IO.File]::WriteAllText($envFile,$line,
      [System.Text.UTF8Encoding]::new($false))
    Write-Host 'Archivo .env privado generado con contraseña aleatoria.'
  }
  $configured=(Get-Content $envFile | Where-Object {
    $_ -match '^ACERIA_SA_PASSWORD=' } | Select-Object -First 1)
  if (-not $configured -or $configured -eq 'ACERIA_SA_PASSWORD=AxiaDocker_2026!Local9') {
    throw 'Configure una contraseña SQL no predeterminada en .env.'
  }
  & docker compose --env-file $envFile -f $compose config --quiet
  if ($LASTEXITCODE -ne 0) { throw 'El Compose no es válido.' }
  $names=@(& docker compose --env-file $envFile -f $compose config --services)
  $expected=@('sqlserver','rabbitmq','produccion','inventario-1',
              'inventario-2','gateway')
  if (@(Compare-Object ($names | Sort-Object) ($expected | Sort-Object)).Count -gt 0) {
    throw 'El Compose no define los seis servicios previstos.'
  }
  $report.comprobaciones.seis_servicios='PASS'
  & (Join-Path $root 'EJECUTAR_DOCKER_WINDOWS.ps1') -Accion preparar
  if ($LASTEXITCODE -ne 0) { throw 'Fallo en preparar.' }
  $report.comprobaciones.preparar='PASS'
  $started=$true
  & (Join-Path $root 'EJECUTAR_DOCKER_WINDOWS.ps1') -Accion levantar
  if ($LASTEXITCODE -ne 0) { throw 'Fallo en levantar.' }
  $report.comprobaciones.levantar='PASS'
  & (Join-Path $root 'EJECUTAR_DOCKER_WINDOWS.ps1') -Accion verificar
  if ($LASTEXITCODE -ne 0) { throw 'Fallo en verificar.' }
  $report.comprobaciones.verificacion='PASS'
  & (Join-Path $root 'VALIDAR_FALLOS_DOCKER_WINDOWS.ps1')
  if ($LASTEXITCODE -ne 0) { throw 'Fallo en caídas y recuperación.' }
  $report.comprobaciones.recuperacion='PASS'
  & (Join-Path $root 'EJECUTAR_DOCKER_WINDOWS.ps1') -Accion verificar
  if ($LASTEXITCODE -ne 0) { throw 'Fallo tras recuperación.' }
  $report.comprobaciones.verificacion_final='PASS'
  foreach ($name in @('docker-windows-e2e.json','docker-fallos-e2e.json')) {
    $file=Join-Path $folder $name
    if (-not (Test-Path $file)) { throw "Evidencia ausente: $name" }
    $evidence=Get-Content -Raw $file | ConvertFrom-Json
    if ($evidence.resultado -ne 'PASS') { throw "Evidencia sin PASS: $name" }
  }
  $report.comprobaciones.evidencias='PASS'
  $report.resultado='PASS'
} catch {
  $report.error=$_.Exception.Message
  Write-Host "CERTIFICACIÓN NO SUPERADA: $($report.error)"
} finally {
  $report | ConvertTo-Json -Depth 8 | Set-Content $out -Encoding utf8
  if ($started -and -not $ConservarContenedores) {
    try { & docker compose --env-file $envFile -f $compose down --remove-orphans }
    catch { Write-Host 'ADVERTENCIA al detener contenedores.' }
  }
  $env:COMPOSE_PROJECT_NAME=$oldProject
  Write-Host "Informe Windows: $out. Resultado: $($report.resultado)."
}
if ($report.resultado -ne 'PASS') { exit 1 }
Write-Host 'PASS: M09 certificado en Windows con Docker Desktop WSL2.'
) {
    throw 'Docker Desktop no aparece configurado sobre WSL2.'
  }
  $report.comprobaciones.wsl2='PASS'
  if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'No se encuentra docker CLI.'
  }
  $type=(& docker info --format '{{.OSType}}' | Out-String).Trim()
  $desktop=(& docker info --format '{{.OperatingSystem}}' | Out-String).Trim()
  if ($LASTEXITCODE -ne 0 -or $type -ne 'linux' -or $desktop -notmatch 'Docker Desktop') {
    throw "No se identifica Docker Desktop con motor Linux: $type / $desktop"
  }
  $report.motor=$desktop
  $report.comprobaciones.docker_desktop='PASS'
  & docker compose version | Out-Null
  if ($LASTEXITCODE -ne 0) { throw 'Docker Compose no responde.' }
  $report.comprobaciones.compose='PASS'
  $sdks=& dotnet --list-sdks
  if ($LASTEXITCODE -ne 0 -or (($sdks | Out-String) -notmatch '(?m)^8\.')) {
    throw 'Falta SDK .NET 8.'
  }
  $report.comprobaciones.sdk_net8='PASS'
  if (-not (Test-Path $envFile)) {
    if ($NoCrearEnv) { throw 'Cree .env con una contraseña segura para SQL.' }
    $bytes=[System.Security.Cryptography.RandomNumberGenerator]::GetBytes(24)
    $pw=[Convert]::ToHexString($bytes)+'aA1!'
    $line='ACERIA_SA_PASSWORD='+$pw+[Environment]::NewLine
    [System.IO.File]::WriteAllText($envFile,$line,
      [System.Text.UTF8Encoding]::new($false))
    Write-Host 'Archivo .env privado generado con contraseña aleatoria.'
  }
  $configured=(Get-Content $envFile | Where-Object {
    $_ -match '^ACERIA_SA_PASSWORD=' } | Select-Object -First 1)
  if (-not $configured -or $configured -eq 'ACERIA_SA_PASSWORD=AxiaDocker_2026!Local9') {
    throw 'Configure una contraseña SQL no predeterminada en .env.'
  }
  & docker compose --env-file $envFile -f $compose config --quiet
  if ($LASTEXITCODE -ne 0) { throw 'El Compose no es válido.' }
  $names=@(& docker compose --env-file $envFile -f $compose config --services)
  $expected=@('sqlserver','rabbitmq','produccion','inventario-1',
              'inventario-2','gateway')
  if (@(Compare-Object ($names | Sort-Object) ($expected | Sort-Object)).Count -gt 0) {
    throw 'El Compose no define los seis servicios previstos.'
  }
  $report.comprobaciones.seis_servicios='PASS'
  & (Join-Path $root 'EJECUTAR_DOCKER_WINDOWS.ps1') -Accion preparar
  if ($LASTEXITCODE -ne 0) { throw 'Fallo en preparar.' }
  $report.comprobaciones.preparar='PASS'
  $started=$true
  & (Join-Path $root 'EJECUTAR_DOCKER_WINDOWS.ps1') -Accion levantar
  if ($LASTEXITCODE -ne 0) { throw 'Fallo en levantar.' }
  $report.comprobaciones.levantar='PASS'
  & (Join-Path $root 'EJECUTAR_DOCKER_WINDOWS.ps1') -Accion verificar
  if ($LASTEXITCODE -ne 0) { throw 'Fallo en verificar.' }
  $report.comprobaciones.verificacion='PASS'
  & (Join-Path $root 'VALIDAR_FALLOS_DOCKER_WINDOWS.ps1')
  if ($LASTEXITCODE -ne 0) { throw 'Fallo en caídas y recuperación.' }
  $report.comprobaciones.recuperacion='PASS'
  & (Join-Path $root 'EJECUTAR_DOCKER_WINDOWS.ps1') -Accion verificar
  if ($LASTEXITCODE -ne 0) { throw 'Fallo tras recuperación.' }
  $report.comprobaciones.verificacion_final='PASS'
  foreach ($name in @('docker-windows-e2e.json','docker-fallos-e2e.json')) {
    $file=Join-Path $folder $name
    if (-not (Test-Path $file)) { throw "Evidencia ausente: $name" }
    $evidence=Get-Content -Raw $file | ConvertFrom-Json
    if ($evidence.resultado -ne 'PASS') { throw "Evidencia sin PASS: $name" }
  }
  $report.comprobaciones.evidencias='PASS'
  $report.resultado='PASS'
} catch {
  $report.error=$_.Exception.Message
  Write-Host "CERTIFICACIÓN NO SUPERADA: $($report.error)"
} finally {
  $report | ConvertTo-Json -Depth 8 | Set-Content $out -Encoding utf8
  if ($started -and -not $ConservarContenedores) {
    try { & docker compose --env-file $envFile -f $compose down --remove-orphans }
    catch { Write-Host 'ADVERTENCIA al detener contenedores.' }
  }
  $env:COMPOSE_PROJECT_NAME=$oldProject
  Write-Host "Informe Windows: $out. Resultado: $($report.resultado)."
}
if ($report.resultado -ne 'PASS') { exit 1 }
Write-Host 'PASS: M09 certificado en Windows con Docker Desktop WSL2.'
