using System.Diagnostics;
using Testcontainers.MsSql;

if (args.Length == 0)
{
    Console.Error.WriteLine("Indica el ejecutable y sus argumentos; SQL Server se elimina al finalizar.");
    return 2;
}
await using var sql = new MsSqlBuilder()
    .WithImage("mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04")
    .WithEnvironment("MSSQL_PID", "Express")
    .WithPassword("Ax!" + Guid.NewGuid().ToString("N") + "9z")
    .Build();
await sql.StartAsync();
Console.WriteLine("SQL Server Express iniciado mediante Testcontainers; conexión reservada al proceso hijo.");
var start = new ProcessStartInfo(args[0]) { UseShellExecute = false };
foreach (var argument in args.Skip(1)) start.ArgumentList.Add(argument);
start.Environment["ACERIA_TEST_SQLSERVER"] = sql.GetConnectionString();
start.Environment["ACERIA_SQL_ORIGIN"] = "Testcontainers";
using var child = Process.Start(start) ?? throw new InvalidOperationException("No se pudo iniciar la validación.");
await child.WaitForExitAsync();
return child.ExitCode;
