using System.Diagnostics;
using System.Text.Json;
using Microsoft.Data.SqlClient;
using Testcontainers.MsSql;
using Testcontainers.RabbitMq;

var local = args.Length > 0 && args[0] == "--localdb";
if (local) args = args.Skip(1).ToArray();
if (args.Length == 0) return 2;
MsSqlContainer? sql = null;
RabbitMqContainer? rabbit = null;
var prefix = "AceriaM06Http_" + Guid.NewGuid().ToString("N");
string connection = @"Server=(localdb)\MSSQLLocalDB;Database=master;Trusted_Connection=True;TrustServerCertificate=True";
try
{
    if (!local)
    {
        sql = new MsSqlBuilder().WithImage("mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04")
            .WithEnvironment("MSSQL_PID", "Express").WithPassword("Ax!" + Guid.NewGuid().ToString("N") + "9z").Build();
        await sql.StartAsync();
        connection = sql.GetConnectionString();
        rabbit = new RabbitMqBuilder().WithImage("rabbitmq:4.1.5-management")
            .WithUsername("curso").WithPassword("curso-local").Build();
        await rabbit.StartAsync();
    }
    var start = new ProcessStartInfo(args[0]) { UseShellExecute = false };
    foreach (var argument in args.Skip(1)) start.ArgumentList.Add(argument);
    start.Environment["ACERIA_TEST_SQLSERVER"] = connection;
    start.Environment["ACERIA_SQL_ORIGIN"] = local ? "LocalDB" : "Testcontainers";
    start.Environment["ACERIA_HTTP_SQL_PREFIX"] = prefix;
    if (rabbit is not null) start.Environment["ACERIA_TEST_RABBITMQ"] = rabbit.GetConnectionString();
    Console.WriteLine(local ? "LocalDB real preparado para recorrido HTTP." : "SQL Server Express y RabbitMQ reales preparados con Testcontainers.");
    using var child = Process.Start(start) ?? throw new InvalidOperationException("No se inició el proceso de comprobación.");
    await child.WaitForExitAsync();
    return child.ExitCode;
}
finally
{
    try
    {
        await using var master = new SqlConnection(new SqlConnectionStringBuilder(connection) { InitialCatalog = "master" }.ConnectionString);
        await master.OpenAsync();
        var names = new List<string>();
        await using (var list = master.CreateCommand())
        {
            list.CommandText = "SELECT name FROM sys.databases WHERE name LIKE @prefix";
            list.Parameters.AddWithValue("@prefix", prefix + "%");
            await using var reader = await list.ExecuteReaderAsync();
            while (await reader.ReadAsync()) names.Add(reader.GetString(0));
        }
        foreach (var name in names)
        {
            if (!name.StartsWith(prefix, StringComparison.Ordinal) || name.Any(c => !char.IsAsciiLetterOrDigit(c) && c != '_'))
                throw new InvalidOperationException("Nombre de limpieza fuera del alcance de la ejecución.");
            await using var drop = master.CreateCommand();
            drop.CommandText = $"ALTER DATABASE [{name}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE; DROP DATABASE [{name}]";
            await drop.ExecuteNonQueryAsync();
        }
        Console.WriteLine("Bases HTTP temporales eliminadas: " + names.Count);
    }
    finally
    {
        if (rabbit is not null) await rabbit.DisposeAsync();
        if (sql is not null) await sql.DisposeAsync();
    }
}
