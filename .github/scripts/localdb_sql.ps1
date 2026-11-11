param([ValidateSet('info','drop')][string]$Action, [string]$Databases = '')
$ErrorActionPreference = 'Stop'
$cn = New-Object System.Data.SqlClient.SqlConnection 'Server=(localdb)\MSSQLLocalDB;Database=master;Integrated Security=True;TrustServerCertificate=True'
try {
    $cn.Open()
    if ($Action -eq 'info') {
        $cmd = $cn.CreateCommand()
        $cmd.CommandText = "SELECT CAST(SERVERPROPERTY('EngineEdition') AS int), CAST(SERVERPROPERTY('ProductVersion') AS nvarchar(128))"
        $reader = $cmd.ExecuteReader()
        if (-not $reader.Read()) { throw 'SQL Server no devolvio metadatos' }
        $edition = $reader.GetInt32(0)
        $version = $reader.GetString(1)
        $reader.Close()
        if ($edition -ne 4) { throw 'Se requiere SQL Server Express LocalDB real' }
        @{engineEdition=$edition; version=$version; modo='LocalDB'} | ConvertTo-Json -Compress
    } else {
        foreach ($name in $Databases.Split(',')) {
            if ($name -notmatch '^AceriaTest_[a-f0-9]{32}_(AceriaApp|AceriaHexagonal|AceriaProduccion)$') { throw 'Nombre ajeno a esta comprobacion' }
            $cmd = $cn.CreateCommand()
            $cmd.CommandText = "IF DB_ID(N'$name') IS NOT NULL BEGIN ALTER DATABASE [$name] SET SINGLE_USER WITH ROLLBACK IMMEDIATE; DROP DATABASE [$name]; END"
            [void]$cmd.ExecuteNonQuery()
        }
    }
} finally { $cn.Dispose() }
