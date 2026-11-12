using System.Security.Cryptography;
using System.Text.Json;
using Microsoft.Data.SqlClient;
using Testcontainers.MsSql;

namespace AceriaApp.PruebasSqlServer;

// Una instancia de contenedor por proceso; cada prueba conserva su propia base.
public sealed class BaseSqlServer : IDisposable, IAsyncDisposable
{
    private static readonly Lazy<MsSqlContainer> Servidor = new(() =>
    {
        var contenedor = new MsSqlBuilder()
            .WithImage("mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04")
            .WithEnvironment("MSSQL_PID", "Express")
            .WithPassword("Axia!" + Convert.ToHexString(RandomNumberGenerator.GetBytes(24)))
            .Build();
        contenedor.StartAsync().GetAwaiter().GetResult();
        // Ryuk retira el contenedor al finalizar el proceso de pruebas.
        return contenedor;
    });

    private readonly string _master;
    private readonly string _nombre = "AceriaTest_" + Guid.NewGuid().ToString("N");
    private int _eliminada;
    private bool _creada;
    public string ConnectionString { get; }

    private BaseSqlServer(string servidor)
    {
        var cadena = new SqlConnectionStringBuilder(servidor) { InitialCatalog = "master" };
        _master = cadena.ConnectionString;
        cadena.InitialCatalog = _nombre;
        ConnectionString = cadena.ConnectionString;
    }

    public static BaseSqlServer Crear()
    {
        var externa = Environment.GetEnvironmentVariable("ACERIA_TEST_SQLSERVER");
        var modo = string.IsNullOrWhiteSpace(externa) ? "testcontainers" : "conexion_externa";
        var bd = new BaseSqlServer(modo == "testcontainers" ? Servidor.Value.GetConnectionString() : externa!);
        try
        {
            using var conexion = new SqlConnection(bd._master);
            conexion.Open();
            using var crear = conexion.CreateCommand();
            // El identificador procede únicamente de Guid, nunca de la conexión externa.
            crear.CommandText = $"CREATE DATABASE [{bd._nombre}]";
            crear.ExecuteNonQuery();
            bd._creada = true;
            bd.GuardarEvidencia(conexion, modo);
            return bd;
        }
        catch
        {
            bd.Dispose();
            throw;
        }
    }

    private void GuardarEvidencia(SqlConnection conexion, string modo)
    {
        var carpeta = Environment.GetEnvironmentVariable("ACERIA_SQL_EVIDENCE_DIR");
        if (string.IsNullOrWhiteSpace(carpeta)) return;
        using var consulta = conexion.CreateCommand();
        consulta.CommandText = "SELECT CONVERT(int, SERVERPROPERTY('EngineEdition')), " +
            "CONVERT(nvarchar(128), SERVERPROPERTY('ProductVersion'))";
        using var lector = consulta.ExecuteReader();
        lector.Read();
        var evidencia = new
        {
            provider = "Microsoft.EntityFrameworkCore.SqlServer",
            engineEdition = lector.GetInt32(0),
            version = lector.GetString(1),
            database = _nombre,
            modo,
            origen = Environment.GetEnvironmentVariable("ACERIA_SQL_ORIGIN")
                ?? (modo == "testcontainers" ? "Testcontainers" : "SQLServer")
        };
        Directory.CreateDirectory(carpeta);
        // Solo se guardan datos de motor y de base: nunca credenciales ni cadenas.
        File.WriteAllText(Path.Combine(carpeta, _nombre + ".json"),
            JsonSerializer.Serialize(evidencia, new JsonSerializerOptions { WriteIndented = true }));
    }

    public void Dispose()
    {
        if (Interlocked.Exchange(ref _eliminada, 1) != 0 || !_creada) return;
        // Vacía solo el pool de esta base; las demás factorías siguen funcionando.
        using var propia = new SqlConnection(ConnectionString);
        SqlConnection.ClearPool(propia);
        using var conexion = new SqlConnection(_master);
        conexion.Open();
        using var borrar = conexion.CreateCommand();
        borrar.CommandText = $"IF DB_ID(N'{_nombre}') IS NOT NULL BEGIN " +
            $"ALTER DATABASE [{_nombre}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE; " +
            $"DROP DATABASE [{_nombre}]; END";
        borrar.ExecuteNonQuery();
    }

    public ValueTask DisposeAsync()
    {
        Dispose();
        return ValueTask.CompletedTask;
    }
}
