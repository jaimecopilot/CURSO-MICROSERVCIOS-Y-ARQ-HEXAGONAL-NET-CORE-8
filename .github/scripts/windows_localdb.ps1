# Inicializa SQL Server LocalDB en el ejecutor Windows de GitHub Actions.
# Instancia EXPLÍCITA: evita la creación implícita e intermitente de MSSQLLocalDB.
# No valida Docker Desktop; eso requiere un equipo Windows con Docker Desktop/WSL2.
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$instance = 'AxiaCI'
$cmd = Get-Command sqllocaldb.exe -ErrorAction SilentlyContinue
if ($cmd) {
  $exe = $cmd.Source
} else {
  $found = Get-ChildItem 'C:\Program Files\Microsoft SQL Server' -Recurse -Filter sqllocaldb.exe -ErrorAction SilentlyContinue | Select-Object -First 1
  if (-not $found) { throw 'No se ha encontrado SQL Server LocalDB en el runner Windows.' }
  $exe = $found.FullName
}
Write-Host "sqllocaldb: $exe"
$lastMessage = ''
for ($attempt = 1; $attempt -le 3; $attempt++) {
  Write-Host "Intento $attempt/3: preparar LocalDB $instance"
  $available = @(& $exe info 2>&1)
  if ($LASTEXITCODE -ne 0) {
    $lastMessage = "sqllocaldb info falló: $($available -join ' ')"
    Start-Sleep -Seconds 3
    continue
  }
  if (@($available | ForEach-Object { "$_".Trim() }) -notcontains $instance) {
    $created = @(& $exe create $instance 2>&1)
    if ($LASTEXITCODE -ne 0) {
      $lastMessage = "No se pudo crear ${instance}: $($created -join ' ')"
      Write-Warning $lastMessage
      Start-Sleep -Seconds 3
      continue
    }
  }
  $started = @(& $exe start $instance 2>&1)
  $startCode = $LASTEXITCODE
  $detail = @(& $exe info $instance 2>&1)
  $infoCode = $LASTEXITCODE
  Write-Host ($detail -join [Environment]::NewLine)
  if ($startCode -eq 0 -and $infoCode -eq 0 -and (($detail -join "`n") -match '(?m)^\s*State:\s*Running\s*$')) {
    Write-Host "LocalDB $instance operativo, instancia explícita."
    exit 0
  }
  $lastMessage = "No arrancó $instance (start=$startCode, info=$infoCode). $($started -join ' '); $($detail -join ' ')"
  Write-Warning $lastMessage
  # Solo se toca la instancia de CI creada en este job efímero.
  & $exe stop $instance -k 2>&1 | Out-Null
  & $exe delete $instance 2>&1 | Out-Null
  Start-Sleep -Seconds 4
}
throw "No se ha certificado el arranque real de SQL Server LocalDB: $lastMessage"
