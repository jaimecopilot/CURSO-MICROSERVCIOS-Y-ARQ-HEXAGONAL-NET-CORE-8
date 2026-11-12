# Certificación Windows: broker RabbitMQ NATIVO, no presupone Docker Desktop en runner alojado.
# En el puesto del alumno se utiliza Docker Desktop y Compose según las prácticas.
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
choco install rabbitmq --yes --no-progress --limit-output
if ($LASTEXITCODE -notin @(0,3010)) { throw "Chocolatey no instaló RabbitMQ: $LASTEXITCODE" }
$service = Get-Service -Name RabbitMQ -ErrorAction SilentlyContinue
if (-not $service) { throw 'No se instaló el servicio RabbitMQ en Windows.' }
if ($service.Status -ne 'Running') { Start-Service -Name RabbitMQ }
$tool = Get-ChildItem 'C:\Program Files\RabbitMQ Server' -Filter 'rabbitmqctl.bat' -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $tool) { throw 'No se localizó rabbitmqctl.bat tras la instalación.' }
$cli = $tool.FullName

# Alinear la Erlang cookie del servicio y la sesión CLI, necesario en Windows.
$userCookie = Join-Path $env:USERPROFILE '.erlang.cookie'
if (-not (Test-Path $userCookie)) {
    $sources = @('C:\Windows\System32\config\systemprofile\.erlang.cookie', 'C:\Windows\.erlang.cookie')
    $source = $sources | Where-Object { Test-Path $_ } | Select-Object -First 1
    if ($source) { Copy-Item $source $userCookie -Force }
}

$ready = $false
for ($i=0; $i -lt 60; $i++) {
    & $cli await_startup --timeout 5 *> $null
    if ($LASTEXITCODE -eq 0) { $ready = $true; break }
    Start-Sleep -Seconds 2
}
if (-not $ready) { throw 'RabbitMQ no arrancó o la CLI no autenticó con Erlang cookie.' }
$users = (& $cli list_users --quiet | Out-String)
if ($LASTEXITCODE -ne 0) { throw 'No se pueden listar los usuarios RabbitMQ.' }
if ($users -notmatch '(?m)^curso\s') {
    & $cli add_user curso curso-local
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear el usuario del laboratorio.' }
} else {
    & $cli change_password curso curso-local
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo ajustar la clave del usuario curso.' }
}
& $cli set_permissions -p / curso '.*' '.*' '.*'
if ($LASTEXITCODE -ne 0) { throw 'No se pudieron asignar permisos RabbitMQ.' }
$open = $false
for ($i=0; $i -lt 40; $i++) {
    $tcp = [System.Net.Sockets.TcpClient]::new()
    try {
        $tcp.Connect('127.0.0.1',5672)
        $open = $true
        break
    } catch { Start-Sleep -Seconds 2 }
    finally { $tcp.Dispose() }
}
if (-not $open) { throw 'RabbitMQ no expuso el puerto AMQP 5672.' }
Write-Host 'RabbitMQ nativo Windows listo en 127.0.0.1:5672.'
