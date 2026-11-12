using System.Collections.Generic;

namespace AceriaApp.Api.HealthChecks;

public class CatalogoHealthChecks
{
    public static List<HealthCheck> HealthChecksPorDefecto()
    {
        return new List<HealthCheck>
        {
            new() { Nombre = "Self", Tipo = "Liveness", Recurso = "Aplicación", TieneTimeout = true, ExponeInformacionSensible = false },
            new() { Nombre = "Database", Tipo = "Readiness", ConsultaDependenciaExterna = true, Recurso = "SQL Server Express", TieneTimeout = true, ExponeInformacionSensible = false },
            new() { Nombre = "RabbitMQ", Tipo = "Readiness", ConsultaDependenciaExterna = true, Recurso = "Broker de mensajería", TieneTimeout = true, ExponeInformacionSensible = false }
        };
    }
}
