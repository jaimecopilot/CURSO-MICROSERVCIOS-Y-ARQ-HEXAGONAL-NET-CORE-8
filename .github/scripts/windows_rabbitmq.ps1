# RabbitMQ real en Windows nativo, no presupone Docker Desktop en runner alojado.
# Chocolatey instala Erlang y RabbitMQ; crea el usuario didáctico vía API Management.
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
choco install rabbitmq --yes --no-progress --limit-output
if ($LASTEXITCODE -notin @(0,3010)) { throw "Chocolatey no pudo instalar RabbitMQ: $LASTEXITCODE" }

$machineErlang = [Environment]::GetEnvironmentVariable('ERLANG_HOME','Machine')
if ($machineErlang) { $env:ERLANG_HOME = $machineErlang }
$service = Get-Service -Name RabbitMQ -ErrorAction SilentlyContinue
if (-not $service) { throw 'No existe el servicio RabbitMQ en Windows.' }
# Chocolatey habilita rabbitmq_management offline: reiniciar aplica el plugin.
if ($service.Status -eq 'Running') { Restart-Service RabbitMQ -Force }
else { Start-Service RabbitMQ }

$broker = $false
$management = $false
$basicGuest = 'Basic ' + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('guest:guest'))
$admin = @{ Authorization = $basicGuest }
for ($i = 0; $i -lt 80; $i++) {
    $tcp = [System.Net.Sockets.TcpClient]::new()
    try {
        $tcp.Connect('127.0.0.1', 5672)
        $broker = $true
    } catch {} finally { $tcp.Dispose() }
    if ($broker) {
        try {
            $response = Invoke-WebRequest -Uri 'http://127.0.0.1:15672/api/overview' -Headers $admin -TimeoutSec 5
            if ($response.StatusCode -eq 200) { $management = $true; break }
        } catch {}
    }
    Start-Sleep -Seconds 2
}
if (-not $broker) { throw 'RabbitMQ no expuso el puerto AMQP 5672.' }
if (-not $management) { throw 'RabbitMQ Management en localhost:15672 no está listo para guest.' }

# guest solo puede autenticarse localmente, aquí se usa desde 127.0.0.1.
# La API evita depender de la cookie Erlang de rabbitmqctl del servicio Windows.
$user = @{ password = 'curso-local'; tags = 'management' } | ConvertTo-Json -Compress
Invoke-RestMethod -Uri 'http://127.0.0.1:15672/api/users/curso' -Method Put -Headers $admin -Body $user -ContentType 'application/json' -TimeoutSec 15
$perm = @{ configure = '.*'; write = '.*'; read = '.*' } | ConvertTo-Json -Compress
Invoke-RestMethod -Uri 'http://127.0.0.1:15672/api/permissions/%2F/curso' -Method Put -Headers $admin -Body $perm -ContentType 'application/json' -TimeoutSec 15
$courseAuth = 'Basic ' + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes('curso:curso-local'))
$overview = Invoke-RestMethod -Uri 'http://127.0.0.1:15672/api/overview' -Headers @{ Authorization = $courseAuth } -TimeoutSec 15
if (-not $overview.rabbitmq_version) { throw 'RabbitMQ no devuelve una versión real.' }
Write-Host "RabbitMQ $($overview.rabbitmq_version) operativo en Windows, puertos 5672 y 15672."
