# Health Checks — Punto 7.2

## Definición

Punto de entrada que expone el estado del servicio.

## Tipos

- Liveness: el proceso puede atender. Una plataforma configurada puede reiniciarlo tras sus umbrales; este endpoint no consulta SQL ni RabbitMQ.
- Readiness: el servicio puede atender con sus dependencias críticas. Un balanceador configurado deja de enviar tráfico a una instancia que falla.
- Startup: comprueba el arranque con un presupuesto propio. Una plataforma puede reiniciar el contenedor si agota el umbral; no espera indefinidamente.

## Disponibilidad

- 200 OK: las comprobaciones seleccionadas devuelven el estado admitido por el endpoint.
- 503 Service Unavailable: una comprobación seleccionada impide readiness.
- Sin respuesta: no se ha obtenido evidencia a tiempo; puede ser proceso, red o timeout. No prueba por sí solo que el proceso haya terminado.

## Integración con ASP.NET Core

    builder.Services.AddHealthChecks()
        .AddCheck("self", () => HealthCheckResult.Healthy(), tags: new[] { "live" })
        .AddCheck<SqlServicioHealthCheck>("sql", tags: new[] { "ready" });

    app.MapHealthChecks("/health/live", new HealthCheckOptions
    {
        Predicate = check => check.Tags.Contains("live")
    });
    app.MapHealthChecks("/health/ready", new HealthCheckOptions
    {
        Predicate = check => check.Tags.Contains("ready")
    });

## Health checks personalizados

Implementan `IHealthCheck`. El método `CheckHealthAsync` devuelve un `HealthCheckResult` con estado `Healthy`, `Degraded` o `Unhealthy`.

## Formato de la respuesta

Por defecto: texto plano. Configurable: JSON.

## Health checks en contenedores

- Docker: `HEALTHCHECK`.
- Kubernetes: `livenessProbe`, `readinessProbe`, `startupProbe`.

## Health checks en balanceadores

El balanceador consulta el endpoint de readiness y retira las instancias no disponibles.

## Buenas prácticas

1. Endpoints separados para liveness y readiness.
2. Solo recursos críticos en readiness.
3. Startup check para arranques lentos.
4. Sin información sensible.
5. Tiempos e intervalos configurados.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Endpoint liveness | /health/live |
| Endpoint readiness | /health/ready |
| Comprobaciones | Base de datos, broker |
| Formato | JSON |
| Validación | Test de coherencia |
## Contrato del ejercicio

El fragmento muestra la selección por tags; el archivo completo de registro añade RabbitMQ solo cuando los workers están habilitados, configura límites de espera y serializa una respuesta pública sin excepciones ni cadenas de conexión. Dos rutas sin `Predicate` ejecutarían todas las comprobaciones en ambas y no separarían liveness de readiness.

El catálogo declara recursos, tipo, timeout y protección de información. Su bandera `ConsultaDependenciaExterna` permite detectar un liveness acoplado a una dependencia. No conecta a ningún recurso; los checks funcionales ejecutan SQL y AMQP de verdad. Readiness acredita acceso, no el vaciado del outbox ni la finalización de los consumidores.
