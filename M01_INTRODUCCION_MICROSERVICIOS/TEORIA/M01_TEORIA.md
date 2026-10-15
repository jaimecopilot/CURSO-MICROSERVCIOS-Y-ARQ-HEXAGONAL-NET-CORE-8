Punto 1.1 — Arquitectura monolítica vs. microservicios

Módulo 1: Introducción a los microservicios
Duración: 53 minutos (26 minutos de teoría + 27 minutos de práctica)
Objetivos de aprendizaje:

· Comprender qué es una arquitectura monolítica y qué características la definen.
· Comprender qué es una arquitectura de microservicios y qué características la definen.
· Identificar las ventajas y limitaciones de cada estilo arquitectónico.
· Reconocer los criterios técnicos y organizativos que justifican la adopción de microservicios.
· Crear la estructura inicial del proyecto creciente AceriaApp con una solución, un proyecto de API monolítico de referencia, un proyecto de tests y la documentación de la decisión arquitectónica.


---

PARTE TEÓRICA (26 minutos)

Bloque 1 — Definición de arquitectura monolítica

Una arquitectura monolítica es un estilo de diseño de software en el que todos los componentes funcionales de una aplicación se empaquetan y se despliegan como una única unidad. El término no implica por sí mismo una mala práctica: numerosas aplicaciones empresariales consolidadas se han construido con este enfoque durante décadas. En un monolito, la interfaz de presentación, la lógica de negocio y el acceso a datos residen en el mismo proceso y, con frecuencia, en el mismo artefacto desplegable. La compilación produce un único ensamblado o un conjunto reducido de ensamblados que se ejecutan juntos. Esta concentración simplifica la operación porque existe un único punto de despliegue, un único proceso que arrancar y un único registro donde investigar errores. La comunicación entre componentes se realiza mediante llamadas a métodos en memoria, lo que elimina la latencia de red y reduce la complejidad de la coordinación distribuida. La consecuencia inmediata es que el modelo mental del sistema es sencillo de construir y de explicar.

La estructura interna de un monolito suele organizarse por capas: presentación, aplicación, dominio e infraestructura. Cada capa depende de la inferior y expone una interfaz estable al resto del sistema. Esta organización por capas permite separar responsabilidades dentro del proceso, aunque todas ellas compartan el mismo ciclo de vida de compilación y despliegue. El código fuente completo reside en un único repositorio y, normalmente, en una única solución de Visual Studio. Los equipos trabajan sobre el mismo conjunto de archivos, lo que facilita la reutilización de utilidades comunes y evita duplicaciones accidentales de lógica. La transacción de base de datos se convierte en el mecanismo natural para garantizar la consistencia, porque todas las operaciones ocurren sobre el mismo contexto de persistencia.

AceriaApp.Monolito/
├── AceriaApp.Monolito.Api/          → capa de presentación (endpoints)
├── AceriaApp.Monolito.Aplicacion/   → casos de uso y servicios
├── AceriaApp.Monolito.Dominio/      → entidades y reglas de negocio
└── AceriaApp.Monolito.Infraestructura/ → EF Core, repositorios, migraciones

Línea 1: AceriaApp.Monolito.Api/ → proyecto que expone los endpoints HTTP y arranca el proceso.
Línea 2: AceriaApp.Monolito.Aplicacion/ → proyecto que contiene los casos de uso y orquesta el dominio.
Línea 3: AceriaApp.Monolito.Dominio/ → proyecto que contiene entidades, value objects y reglas invariantes.
Línea 4: AceriaApp.Monolito.Infraestructura/ → proyecto que implementa la persistencia y los servicios externos.

Esta separación lógica de proyectos dentro de un mismo despliegue prepara el terreno para entender por qué los microservicios aplican el mismo principio de separación, pero con un límite físico distinto. La organización por capas dentro de un monolito no impide que el sistema crezca en complejidad interna. Cuando varias funcionalidades comparten el mismo proceso, cualquier cambio en una de ellas obliga a recompilar y redesplegar el conjunto completo. La transacción única garantiza consistencia fuerte, pero también acopla el ciclo de vida de todas las funcionalidades. Este acoplamiento es aceptable en dominios pequeños y estables, y se vuelve problemático cuando el dominio crece y los equipos se multiplican.


---

Bloque 2 — Características operativas del monolito

El despliegue de un monolito consiste en publicar un único artefacto en un servidor o en un contenedor. La configuración se concentra en un archivo appsettings.json y en variables de entorno del proceso. El escalado se realiza replicando el artefacto completo: si una funcionalidad concreta consume más recursos que las demás, se replica todo el proceso, no solo esa funcionalidad. Esta característica se conoce como escalado horizontal homogéneo. Su principal ventaja es la simplicidad: no hay que decidir qué componente escalar ni cómo coordinar réplicas de distintos servicios. Su principal inconveniente es el desperdicio de recursos, porque se replica código que no lo necesita.

{
  "ConnectionStrings": {
    "AceriaDb": "Server=.\\SQLEXPRESS;Database=AceriaDb;Trusted_Connection=True;TrustServerCertificate=True"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}

Línea 1: { → abre el objeto raíz de configuración.
Línea 2: "ConnectionStrings": { → abre la sección donde se declaran las cadenas de conexión.
Línea 3: "AceriaDb": "Server=.\SQLEXPRESS;..." → cadena de conexión a SQL Server Express con autenticación integrada.
Línea 4: }, → cierra la sección de cadenas de conexión.
Línea 5: "Logging": { → abre la sección de configuración de logging.
Línea 6: "LogLevel": { → abre la sección de niveles de log.
Línea 7: "Default": "Information" → nivel por defecto para todos los proveedores.
Línea 8: "Microsoft.AspNetCore": "Warning" → reduce el ruido de los logs del framework.
Línea 9: } → cierra la sección de niveles.
Línea 10: } → cierra la sección de logging.
Línea 11: } → cierra el objeto raíz.

El archivo de configuración único refleja la naturaleza centralizada del monolito: una sola fuente de verdad para todos los componentes. La observabilidad en un monolito se concentra en un único flujo de logs. Cuando ocurre un error, existe un solo archivo o una sola consola donde buscar la traza completa. Esta concentración acelera el diagnóstico inicial, pero también genera ruido: los logs de todas las funcionalidades se mezclan en el mismo flujo. El versionado del artefacto es lineal y cada versión contiene el estado de todas las funcionalidades en ese instante. No es posible desplegar una funcionalidad nueva sin arrastrar los cambios de las demás que se hayan fusionado en la misma rama.


---

Bloque 3 — Ventajas del monolito

La primera ventaja del monolito es la simplicidad operativa. Un único artefacto implica un único pipeline de compilación, un único proceso de despliegue y un único punto de monitorización. Los equipos pequeños pueden operar el sistema sin necesidad de infraestructura de orquestación. Esta simplicidad se traduce en menores costes de arranque y en una curva de aprendizaje más suave para desarrolladores que se incorporan al proyecto. La segunda ventaja es la consistencia transaccional. Al compartir un único contexto de base de datos, las operaciones que afectan a varias tablas pueden ejecutarse dentro de una transacción ACID sin necesidad de patrones de compensación ni de coordinación distribuida.

using var scope = app.Services.CreateScope();
var db = scope.ServiceProvider.GetRequiredService<AceriaDbContext>();
await using var tx = await db.Database.BeginTransactionAsync();
db.Ordenes.Add(new Orden { Id = Guid.NewGuid(), Cliente = "ACX-001" });
db.Inventario.Add(new Movimiento { Id = Guid.NewGuid(), Material = "CHAPA-3MM" });
await db.SaveChangesAsync();
await tx.CommitAsync();

Línea 1: using var scope = app.Services.CreateScope(); → crea un ámbito de servicios para resolver dependencias con ciclo de vida scoped.
Línea 2: var db = scope.ServiceProvider.GetRequiredService<AceriaDbContext>(); → obtiene el contexto de EF Core desde el contenedor de dependencias.
Línea 3: await using var tx = await db.Database.BeginTransactionAsync(); → abre una transacción explícita sobre SQL Server Express.
Línea 4: db.Ordenes.Add(new Orden { ... }); → añade una orden al DbSet de órdenes.
Línea 5: db.Inventario.Add(new Movimiento { ... }); → añade un movimiento al DbSet de inventario dentro de la misma transacción.
Línea 6: await db.SaveChangesAsync(); → persiste los cambios pendientes en la base de datos.
Línea 7: await tx.CommitAsync(); → confirma la transacción y hace visibles los cambios.

Esta transacción única es imposible de replicar de forma directa en microservicios, donde cada servicio posee su propia base de datos y la consistencia se gestiona con patrones como Saga. La tercera ventaja es la facilidad para refactorizar. Cuando todo el código reside en el mismo repositorio y en el mismo proceso, renombrar una clase o mover una responsabilidad entre capas es una operación mecánica que el IDE resuelve sin coordinación entre equipos. La cuarta ventaja es la depuración: se puede ejecutar el sistema completo en la máquina del desarrollador con un único F5 y establecer puntos de interrupción en cualquier capa sin necesidad de levantar varios procesos.


---

Bloque 4 — Limitaciones del monolito

La primera limitación es el acoplamiento del ciclo de vida. Cualquier cambio, por pequeño que sea, obliga a recompilar y redesplegar el artefacto completo. Si el despliegue tarda veinte minutos, cada corrección de una línea cuesta veinte minutos de ventana de mantenimiento. La segunda limitación es el escalado homogéneo. Si un endpoint concreto recibe diez veces más tráfico que el resto, hay que replicar todo el proceso y no solo ese endpoint. El coste de infraestructura crece de forma desproporcionada respecto a la carga real. La tercera limitación es la barrera tecnológica: todos los componentes deben compartir el mismo stack, la misma versión del runtime y las mismas bibliotecas.

Monolito con 4 funcionalidades y escalado homogéneo:

[Instancia 1] Órdenes + Inventario + Clientes + Facturación
[Instancia 2] Órdenes + Inventario + Clientes + Facturación
[Instancia 3] Órdenes + Inventario + Clientes + Facturación

Si solo Órdenes necesita 3 instancias, las otras 3 funcionalidades
también se replican sin necesitarlo.

Línea 1: [Instancia 1] Órdenes + Inventario + Clientes + Facturación → primera réplica del proceso completo.
Línea 2: [Instancia 2] ... → segunda réplica idéntica.
Línea 3: [Instancia 3] ... → tercera réplica idéntica.
Línea 4: Si solo Órdenes necesita 3 instancias, ... → describe el desperdicio de recursos del escalado homogéneo.

La cuarta limitación es la organización de equipos. Cuando varias personas trabajan sobre el mismo artefacto, los conflictos de fusión se multiplican y las decisiones técnicas se centralizan. La quinta limitación es la adopción de nuevas tecnologías: migrar una parte del sistema a una versión superior del framework obliga a migrar todo el conjunto, porque el artefacto es indivisible. Estas limitaciones no invalidan el monolito como opción; simplemente definen el contexto en el que deja de ser la elección óptima.


---

Bloque 5 — Definición de arquitectura de microservicios

Una arquitectura de microservicios es un estilo de diseño en el que la aplicación se descompone en un conjunto de servicios pequeños, autónomos y desplegables de forma independiente. Cada servicio encapsula una capacidad de negocio concreta, posee su propio ciclo de vida y, con frecuencia, su propia base de datos. La comunicación entre servicios se realiza a través de la red mediante protocolos ligeros como HTTP o mensajería asíncrona. El término "micro" hace referencia al alcance funcional del servicio, no al número de líneas de código. Un microservicio puede contener cientos de archivos si su dominio lo justifica; lo relevante es que su límite coincida con una capacidad de negocio claramente identificable.

AceriaApp (microservicios)/
├── AceriaApp.Ordenes.Api/       → servicio de órdenes (puerto 5001)
├── AceriaApp.Inventario.Api/    → servicio de inventario (puerto 5002)
├── AceriaApp.Clientes.Api/      → servicio de clientes (puerto 5003)
└── AceriaApp.Gateway/           → API Gateway con YARP (puerto 5000)

Línea 1: AceriaApp.Ordenes.Api/ → servicio autónomo que gestiona las órdenes de producción.
Línea 2: AceriaApp.Inventario.Api/ → servicio autónomo que gestiona las materias primas.
Línea 3: AceriaApp.Clientes.Api/ → servicio autónomo que gestiona el registro de clientes.
Línea 4: AceriaApp.Gateway/ → punto de entrada único que enruta las peticiones a cada servicio.

Cada servicio de la lista anterior se compila, se despliega y se escala de forma independiente respecto a los demás. La autonomía de cada servicio implica que su equipo puede elegir el stack tecnológico, la versión del runtime y la cadencia de despliegue. Esta libertad acelera la innovación, pero también introduce heterogeneidad operativa. La organización de equipos alrededor de servicios, con equipos pequeños, autónomos y responsables de extremo a extremo, es uno de los principios fundacionales de este estilo arquitectónico. El límite del servicio debe coincidir con una capacidad de negocio, no con una capa técnica.


---

Bloque 6 — Características operativas de los microservicios

El despliegue en microservicios se realiza servicio a servicio. Cada uno tiene su propio pipeline de compilación, su propio artefacto y su propia configuración. El escalado es selectivo: se replica únicamente el servicio que lo necesita. Esta selectividad reduce el coste de infraestructura y permite ajustar los recursos a la carga real de cada capacidad de negocio. La base de datos se descentraliza: cada servicio posee su propio esquema o su propia instancia, y ningún servicio accede directamente a la base de datos de otro. Esta regla se conoce como "database per service" y es la que garantiza el desacoplamiento real entre servicios.

// AceriaApp.Ordenes.Api/Program.cs
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<OrdenesDbContext>(opt =>
    opt.UseSqlServer(builder.Configuration.GetConnectionString("OrdenesDb")));
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
var app = builder.Build();
app.MapGet("/api/v1/ordenes", async (OrdenesDbContext db) =>
    await db.Ordenes.ToListAsync());
app.Run();

Línea 1: var builder = WebApplication.CreateBuilder(args); → crea el constructor de la aplicación Minimal API.
Línea 2: builder.Services.AddDbContext<OrdenesDbContext>(...) → registra el contexto de EF Core específico del servicio de órdenes.
Línea 3: opt.UseSqlServer(...) → configura SQL Server Express como proveedor, leyendo la cadena OrdenesDb.
Línea 4: builder.Services.AddEndpointsApiExplorer(); → habilita la exploración de endpoints para OpenAPI.
Línea 5: builder.Services.AddSwaggerGen(); → registra el generador de Swagger.
Línea 6: var app = builder.Build(); → construye la aplicación.
Línea 7: app.MapGet("/api/v1/ordenes", ...) → define un endpoint GET que devuelve las órdenes del servicio.
Línea 8: await db.Ordenes.ToListAsync()); → consulta la tabla de órdenes del contexto propio.
Línea 9: app.Run(); → arranca el servidor Kestrel.

Este archivo Program.cs pertenece exclusivamente al servicio de órdenes: el servicio de inventario tendrá su propio Program.cs, su propio DbContext y su propia cadena de conexión. La observabilidad en microservicios requiere correlación de trazas entre servicios, porque una petición puede atravesar varios procesos. El versionado es independiente: cada servicio puede evolucionar a su ritmo siempre que respete los contratos públicos. La consistencia se vuelve eventual y exige patrones como Saga, Outbox o compensación explícita. La comunicación entre servicios debe diseñarse con tolerancia a fallos desde el primer momento.


---

Bloque 7 — Ventajas de los microservicios

La primera ventaja es la independencia de despliegue. Un cambio en el servicio de inventario no obliga a redesplegar el servicio de órdenes. Esta independencia reduce el riesgo de cada despliegue y permite liberar versiones con mayor frecuencia. La segunda ventaja es el escalado selectivo: cada servicio se replica según su propia carga, lo que optimiza el uso de recursos. La tercera ventaja es la autonomía tecnológica: cada equipo puede elegir el stack que mejor se adapte a su dominio, siempre que respete los contratos de comunicación. La cuarta ventaja es el aislamiento de fallos: si un servicio cae, los demás pueden seguir operando, aunque con funcionalidad degradada.

Escalado selectivo:

[Órdenes]    3 instancias  ← recibe el 70% del tráfico
[Inventario] 1 instancia   ← recibe el 20% del tráfico
[Clientes]   1 instancia   ← recibe el 10% del tráfico

Cada servicio se escala según su carga real.

Línea 1: [Órdenes] 3 instancias → el servicio de órdenes se replica tres veces por su alta demanda.
Línea 2: [Inventario] 1 instancia → el servicio de inventario mantiene una sola instancia.
Línea 3: [Clientes] 1 instancia → el servicio de clientes mantiene una sola instancia.
Línea 4: Cada servicio se escala según su carga real. → sintetiza la ventaja del escalado selectivo.

La quinta ventaja es la alineación con equipos autónomos. Cada equipo posee un servicio completo, desde la base de datos hasta el endpoint, y puede tomar decisiones sin coordinación con otros equipos. Esta alineación reduce los cuellos de botella organizativos y acelera la entrega. La sexta ventaja es la posibilidad de adoptar nuevas tecnologías de forma incremental: un servicio puede migrar a una versión superior del runtime sin afectar a los demás. La séptima ventaja es la resiliencia: el aislamiento de fallos permite diseñar degradaciones controladas.


---

Bloque 8 — Desafíos y costes de los microservicios

El primer desafío es la complejidad distribuida. Una llamada que en un monolito era una invocación en memoria se convierte en una llamada de red que puede fallar, tardar o perderse. Hay que gestionar timeouts, reintentos, circuit breakers y compensaciones. El segundo desafío es la consistencia eventual: no existe una transacción ACID que abarque varios servicios, por lo que hay que diseñar patrones como Saga para mantener la coherencia del negocio. El tercer desafío es la observabilidad: sin trazabilidad distribuida, diagnosticar un error que atraviesa cinco servicios es inviable.

var policy = Policy
    .Handle<HttpRequestException>()
    .WaitAndRetryAsync(3, attempt => TimeSpan.FromMilliseconds(200 * attempt));
var response = await policy.ExecuteAsync(() =>
    httpClient.GetAsync("http://acería-inventario/api/v1/materiales"));

Línea 1: var policy = Policy → comienza la definición de una política de Polly.
Línea 2: .Handle<HttpRequestException>() → indica que la política se activa ante errores HTTP.
Línea 3: .WaitAndRetryAsync(3, attempt => ...) → reintenta hasta tres veces con retroceso exponencial.
Línea 4: var response = await policy.ExecuteAsync(...) → ejecuta la llamada HTTP bajo la política.
Línea 5: httpClient.GetAsync("http://acería-inventario/api/v1/materiales") → llamada al servicio de inventario.

La política anterior es necesaria porque en microservicios toda comunicación remota es falible por definición. El cuarto desafío es el coste operativo. Cada servicio requiere su propio pipeline, su propia monitorización y su propia configuración. La infraestructura mínima (contenedores, orquestación, descubrimiento de servicios) añade complejidad que un monolito no necesita. El quinto desafío es la duplicación de código: sin disciplina, cada equipo reimplementa utilidades comunes, lo que fragmenta las convenciones y multiplica los errores. El sexto desafío es la gestión de versiones de los contratos públicos entre servicios.


---

Bloque 9 — Comparativa y criterios de decisión

La elección entre monolito y microservicios no es binaria ni permanente. Un monolito bien modularizado puede evolucionar hacia microservicios extrayendo servicios a medida que aparecen necesidades concretas. Este enfoque se conoce como "monolito modular primero" y es el recomendado por numerosos arquitectos porque evita el coste prematuro de la distribución. La decisión debe basarse en el tamaño del dominio, el número de equipos, la frecuencia de despliegue requerida y la tolerancia al fallo del negocio.

Criterio                  | Monolito            | Microservicios
--------------------------|---------------------|----------------------
Tamaño del dominio        | Pequeño/mediano     | Grande
Número de equipos         | 1-2                 | 3 o más
Frecuencia de despliegue  | Baja/media          | Alta
Consistencia requerida    | Fuerte (ACID)       | Eventual aceptable
Complejidad operativa     | Baja                | Alta
Coste de infraestructura  | Bajo                | Medio/alto

Línea 1: Criterio | Monolito | Microservicios → cabecera de la tabla comparativa.
Línea 2: Tamaño del dominio | Pequeño/mediano | Grande → el tamaño del dominio condiciona la elección.
Línea 3: Número de equipos | 1-2 | 3 o más → los microservicios brillan cuando hay varios equipos.
Línea 4: Frecuencia de despliegue | Baja/media | Alta → la independencia de despliegue importa cuando se libera a menudo.
Línea 5: Consistencia requerida | Fuerte (ACID) | Eventual aceptable → la consistencia fuerte favorece al monolito.
Línea 6: Complejidad operativa | Baja | Alta → los microservicios exigen más inversión operativa.
Línea 7: Coste de infraestructura | Bajo | Medio/alto → el coste crece con la distribución.

La regla práctica es empezar con un monolito modular y extraer microservicios solo cuando un criterio objetivo lo justifique. Los criterios anteriores no son mutuamente excluyentes. Un sistema puede tener un monolito para el dominio administrativo y microservicios para el dominio transaccional. La arquitectura evoluciona con el negocio y con la organización, y la decisión debe revisarse periódicamente. La inversión en microservicios solo se recupera cuando la independencia de despliegue y el escalado selectivo aportan un valor medible.


---

Bloque 10 — Evolución y contexto del proyecto del curso

El proyecto del curso parte de un monolito modular y evoluciona hacia microservicios a lo largo de los ocho módulos. Esta progresión permite entender cada decisión arquitectónica en el momento en que se toma y medir su impacto sobre el código existente. En el módulo 1 se construye la estructura inicial con un monolito de referencia. En el módulo 2 se añade la API REST de órdenes. En el módulo 3 se refactoriza a arquitectura hexagonal. En el módulo 4 se aplican patrones de arquitectura. En el módulo 5 se introduce DDD y CQRS. En el módulo 6 se comunican los servicios. En el módulo 7 se añade observabilidad y resiliencia. En el módulo 8 se publica todo mediante un API Gateway con YARP.

Evolución del proyecto:

M1: Monolito modular de referencia
M2: + API REST de órdenes (Minimal API + OpenAPI)
M3: + Arquitectura hexagonal (puertos y adaptadores)
M4: + Patrones (Repository, UoW, MediatR, Result)
M5: + DDD y CQRS (entidades, VOs, commands, queries)
M6: + Comunicación HTTP y eventos entre servicios
M7: + Observabilidad (Serilog, health checks) y Polly
M8: + API Gateway con YARP (enrutamiento y balanceo)

Línea 1: M1: Monolito modular de referencia → punto de partida del curso.
Línea 2: M2: + API REST de órdenes → primera API REST con Minimal API y OpenAPI.
Línea 3: M3: + Arquitectura hexagonal → refactorización a puertos y adaptadores.
Línea 4: M4: + Patrones → aplicación de Repository, Unit of Work, MediatR y Result Pattern.
Línea 5: M5: + DDD y CQRS → modelado del dominio con entidades, value objects, commands y queries.
Línea 6: M6: + Comunicación entre servicios → HTTP síncrono y eventos asíncronos.
Línea 7: M7: + Observabilidad y resiliencia → Serilog, health checks y Polly.
Línea 8: M8: + API Gateway con YARP → enrutamiento y balanceo de carga.

Cada módulo añade código nuevo sin sustituir el anterior, de modo que la solución final conserva todas las versiones y permite comparar la evolución. El resultado final es una plataforma de microservicios funcional, con persistencia en SQL Server Express, pruebas automatizadas, observabilidad y resiliencia. El alumno puede abrir cualquier carpeta de punto y ejecutarla de forma independiente, y puede comparar dos carpetas consecutivas con diff -r para ver exactamente qué se ha añadido. El proyecto es acumulativo y no opcional: cada punto hace referencia explícita a cómo lo aprendido se integra en el proyecto creciente.


---

Resumen rápido de la teoría

· Un monolito empaqueta todos los componentes en un único artefacto desplegable; su ventaja principal es la simplicidad operativa y transaccional, y su limitación principal es el acoplamiento del ciclo de vida.
· Los microservicios descomponen la aplicación en servicios autónomos con base de datos propia y despliegue independiente; su ventaja principal es la independencia y el escalado selectivo, y su coste principal es la complejidad distribuida.
· La decisión entre ambos estilos depende del tamaño del dominio, el número de equipos, la frecuencia de despliegue y la tolerancia al fallo.
· La estrategia recomendada es empezar con un monolito modular y extraer microservicios cuando un criterio objetivo lo justifique.
· El proyecto del curso evoluciona desde un monolito modular hasta una plataforma de microservicios con arquitectura hexagonal, patrones, DDD, CQRS, comunicación entre servicios, observabilidad, resiliencia y API Gateway.


---


Punto 1.2 — Ventajas e inconvenientes

Módulo 1: Introducción a los microservicios
Duración: 53 minutos (26 minutos de teoría + 27 minutos de práctica)
Objetivos de aprendizaje:

· Identificar las ventajas concretas de una arquitectura monolítica y de una arquitectura de microservicios.
· Identificar los inconvenientes concretos de cada estilo arquitectónico.
· Relacionar cada ventaja y cada inconveniente con criterios técnicos medibles.
· Reconocer los costes ocultos de la distribución y los costes ocultos de la centralización.
· Añadir al proyecto AceriaApp un documento de análisis comparativo en docs/ y una clase de cálculo de métricas de acoplamiento en el proyecto monolítico.


---

PARTE TEÓRICA (26 minutos)

Bloque 1 — Marco de análisis de ventajas e inconvenientes

El análisis de ventajas e inconvenientes de un estilo arquitectónico exige un marco de comparación explícito. Sin ese marco, las decisiones se toman por preferencia técnica o por moda, y no por criterios medibles. Un marco útil organiza los criterios en cuatro dimensiones: despliegue, escalado, organización de equipos y consistencia de datos. Cada dimensión se evalúa con indicadores concretos que permiten comparar monolito y microservicios sin ambigüedad. La dimensión de despliegue mide el tiempo entre la fusión de un cambio y su puesta en producción. La dimensión de escalado mide el coste de infraestructura por unidad de carga. La dimensión de organización mide el número de equipos que pueden trabajar sin coordinación. La dimensión de consistencia mide el nivel de garantía transaccional que el negocio necesita.

Dimensiones del marco de análisis:

1. Despliegue    → tiempo de fusión a producción.
2. Escalado      → coste por unidad de carga.
3. Organización  → equipos que trabajan sin coordinación.
4. Consistencia  → garantía transaccional requerida.

Línea 1: 1. Despliegue → primera dimensión del marco, mide el tiempo de puesta en producción.
Línea 2: 2. Escalado → segunda dimensión, mide el coste de infraestructura por carga.
Línea 3: 3. Organización → tercera dimensión, mide la autonomía de los equipos.
Línea 4: 4. Consistencia → cuarta dimensión, mide la garantía transaccional.

Este marco se aplica a cada decisión arquitectónica del curso y permite justificar por qué el proyecto empieza como monolito modular y evoluciona hacia microservicios. La primera dimensión, el despliegue, es la que más peso tiene en equipos pequeños porque determina la frecuencia con la que se puede entregar valor al negocio. La segunda dimensión, el escalado, es la que más peso tiene en sistemas con cargas muy desiguales entre funcionalidades.

La tercera dimensión, la organización, es la que más peso tiene en empresas con varios equipos trabajando en paralelo sobre el mismo producto. La cuarta dimensión, la consistencia, es la que más peso tiene en dominios financieros o regulados donde la integridad transaccional no es negociable. Ninguna dimensión es universalmente más importante que las demás: el peso relativo depende del contexto del negocio. Lo que sí es universal es la necesidad de medir cada dimensión con indicadores concretos antes de decidir. El marco se completa con una quinta consideración transversal: el coste operativo total, que agrega el esfuerzo de monitorización, configuración y soporte.


---

Bloque 2 — Ventajas del monolito en la dimensión de despliegue

En la dimensión de despliegue, el monolito presenta una ventaja clara: un único artefacto implica un único pipeline. El pipeline se configura una vez y se reutiliza para todas las funcionalidades. No hay que coordinar versiones entre servicios ni gestionar contratos públicos entre equipos. La puesta en producción es una operación atómica: o se despliega la versión completa o no se despliega. Esta atomicidad simplifica las reversiones porque basta con volver a la versión anterior del único artefacto. El coste de esta ventaja es que cualquier cambio, por pequeño que sea, arrastra el ciclo de vida completo del artefacto.

# Pipeline único del monolito
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - dotnet build AceriaApp.sln

test:
  stage: test
  script:
    - dotnet test AceriaApp.sln

deploy:
  stage: deploy
  script:
    - dotnet publish src/AceriaApp.Monolito.Api -c Release

Línea 1: stages: → declara las etapas del pipeline en orden.
Línea 2: - build → primera etapa, compilación.
Línea 3: - test → segunda etapa, pruebas.
Línea 4: - deploy → tercera etapa, despliegue.
Línea 5: build: → comienza la definición de la etapa de compilación.
Línea 6: stage: build → asocia el bloque a la etapa build.
Línea 7: script: → declara los comandos a ejecutar.
Línea 8: - dotnet build AceriaApp.sln → compila la solución completa.
Línea 9: test: → comienza la definición de la etapa de pruebas.
Línea 10: stage: test → asocia el bloque a la etapa test.
Línea 11: script: → declara los comandos a ejecutar.
Línea 12: - dotnet test AceriaApp.sln → ejecuta todos los tests.
Línea 13: deploy: → comienza la definición de la etapa de despliegue.
Línea 14: stage: deploy → asocia el bloque a la etapa deploy.
Línea 15: script: → declara los comandos a ejecutar.
Línea 16: - dotnet publish src/AceriaApp.Monolito.Api -c Release → publica el artefacto único en modo Release.

La ventaja del pipeline único se materializa en equipos pequeños, donde una sola persona puede mantener el pipeline sin dedicación exclusiva. La desventaja aparece cuando el pipeline tarda más de lo aceptable: cada corrección de una línea paga el coste completo del pipeline. La dimensión de despliegue, por tanto, no es una ventaja absoluta del monolito sino una ventaja condicionada al tamaño del equipo y a la frecuencia de cambio.


---

Bloque 3 — Ventajas del monolito en la dimensión de consistencia

En la dimensión de consistencia, el monolito ofrece la garantía transaccional más fuerte posible: ACID sobre una única base de datos. Cualquier operación que afecte a varias tablas se ejecuta dentro de una transacción y se confirma o se revierte de forma atómica. No hay que diseñar patrones de compensación, no hay que gestionar estados intermedios y no hay que reconciliar datos entre servicios. La integridad referencial se mantiene con claves foráneas y restricciones declarativas. La consulta de datos relacionados se resuelve con un JOIN en la misma base de datos, sin llamadas de red ni composición de respuestas.

await using var tx = await db.Database.BeginTransactionAsync();
try
{
    var orden = new Orden { Id = Guid.NewGuid(), Cliente = "ACX-001", Cantidad = 10 };
    db.Ordenes.Add(orden);
    var movimiento = new Movimiento { Id = Guid.NewGuid(), OrdenId = orden.Id, Material = "CHAPA-3MM" };
    db.Movimientos.Add(movimiento);
    await db.SaveChangesAsync();
    await tx.CommitAsync();
}
catch
{
    await tx.RollbackAsync();
    throw;
}

Línea 1: await using var tx = await db.Database.BeginTransactionAsync(); → abre una transacción explícita.
Línea 2: try → inicia el bloque protegido.
Línea 3: var orden = new Orden { ... }; → instancia una nueva orden.
Línea 4: db.Ordenes.Add(orden); → añade la orden al contexto.
Línea 5: var movimiento = new Movimiento { ... }; → instancia un movimiento asociado a la orden.
Línea 6: db.Movimientos.Add(movimiento); → añade el movimiento al contexto.
Línea 7: await db.SaveChangesAsync(); → persiste ambos cambios en la misma transacción.
Línea 8: await tx.CommitAsync(); → confirma la transacción.
Línea 9: catch → captura cualquier error.
Línea 10: await tx.RollbackAsync(); → revierte la transacción completa.
Línea 11: throw; → propaga la excepción.

Esta garantía transaccional es el activo más valioso del monolito en dominios regulados. Su coste es el acoplamiento: todas las funcionalidades comparten el mismo esquema y el mismo contexto de persistencia. Un cambio en el esquema afecta a todas las funcionalidades y obliga a coordinarlas en el mismo despliegue.


---

Bloque 4 — Ventajas del monolito en las dimensiones de escalado y organización

En la dimensión de escalado, el monolito ofrece simplicidad: se replica el artefacto completo y ya está. No hay que decidir qué componente escalar ni cómo enrutar el tráfico entre réplicas de distintos servicios. El balanceo se resuelve con un balanceador genérico. La configuración del escalado es idéntica para todas las réplicas. El coste es el desperdicio: se replican funcionalidades que no lo necesitan. En la dimensión de organización, el monolito también ofrece simplicidad: un único repositorio, un único pipeline y un único equipo responsable. Las decisiones técnicas se toman en una sola conversación. El coste es la coordinación: cuando el equipo crece, las decisiones se convierten en cuellos de botella y los conflictos de fusión se multiplican.

Escalado del monolito:

[Balanceador]
      |
      +---> [Instancia 1] (artefacto completo)
      +---> [Instancia 2] (artefacto completo)
      +---> [Instancia 3] (artefacto completo)

Todas las instancias ejecutan el mismo artefacto.

Línea 1: [Balanceador] → punto de entrada único del tráfico.
Línea 2: +---> [Instancia 1] → primera réplica del artefacto completo.
Línea 3: +---> [Instancia 2] → segunda réplica idéntica.
Línea 4: +---> [Instancia 3] → tercera réplica idéntica.
Línea 5: Todas las instancias ejecutan el mismo artefacto. → sintetiza la homogeneidad del escalado.

Las ventajas de simplicidad en escalado y organización son reales y medibles. Su límite aparece cuando el tamaño del equipo supera la capacidad de una única conversación técnica o cuando la carga entre funcionalidades es muy desigual. En ese momento, la simplicidad se convierte en rigidez y el monolito empieza a frenar la evolución del producto.


---

Bloque 5 — Inconvenientes del monolito

El primer inconveniente del monolito es el acoplamiento del ciclo de vida. Cualquier cambio obliga a recompilar y redesplegar todo el artefacto. El tiempo de despliegue se convierte en un coste fijo por cambio. El segundo inconveniente es el escalado homogéneo: se replica el artefacto completo aunque solo una funcionalidad lo necesite. El tercer inconveniente es la barrera tecnológica: todos los componentes comparten el mismo stack y la misma versión del runtime. El cuarto inconveniente es la coordinación de equipos: cuando varias personas trabajan sobre el mismo código, los conflictos de fusión crecen y las decisiones se centralizan.

Coste por cambio en el monolito:

Cambio de 1 línea → recompilar todo → ejecutar todos los tests → desplegar todo

Tiempo total = tiempo del pipeline completo.

Línea 1: Cambio de 1 línea → cualquier modificación, por pequeña que sea.
Línea 2: recompilar todo → se compila el artefacto completo.
Línea 3: ejecutar todos los tests → se ejecuta la suite completa.
Línea 4: desplegar todo → se publica el artefacto completo.
Línea 5: Tiempo total = tiempo del pipeline completo. → el coste por cambio es constante e independiente del tamaño del cambio.

El quinto inconveniente es la adopción de nuevas tecnologías: migrar una parte del sistema obliga a migrar todo el conjunto. El sexto inconveniente es la escalabilidad organizativa: a partir de cierto número de equipos, el monolito se convierte en un cuello de botella de coordinación. Estos inconvenientes no invalidan el monolito en contextos pequeños; simplemente marcan el umbral a partir del cual su coste supera su beneficio.


---

Bloque 6 — Ventajas de los microservicios en la dimensión de despliegue

En la dimensión de despliegue, los microservicios ofrecen independencia: cada servicio tiene su propio pipeline y su propio ciclo de vida. Un cambio en el servicio de inventario no obliga a redesplegar el servicio de órdenes. La frecuencia de despliegue de cada servicio puede ajustarse a su propia cadencia. El riesgo de cada despliegue se limita al servicio afectado. La reversión también se limita al servicio afectado. El coste de esta ventaja es la multiplicación de pipelines: cada servicio requiere su propia configuración, sus propias credenciales y su propia monitorización.

# Pipeline del servicio de órdenes
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - dotnet build src/AceriaApp.Ordenes.Api

test:
  stage: test
  script:
    - dotnet test tests/AceriaApp.Ordenes.Tests

deploy:
  stage: deploy
  script:
    - dotnet publish src/AceriaApp.Ordenes.Api -c Release

Línea 1: stages: → declara las etapas del pipeline del servicio de órdenes.
Línea 2: - build → primera etapa, compilación del servicio.
Línea 3: - test → segunda etapa, pruebas del servicio.
Línea 4: - deploy → tercera etapa, despliegue del servicio.
Línea 5: build: → comienza la definición de la etapa de compilación.
Línea 6: stage: build → asocia el bloque a la etapa build.
Línea 7: script: → declara los comandos a ejecutar.
Línea 8: - dotnet build src/AceriaApp.Ordenes.Api → compila solo el servicio de órdenes.
Línea 9: test: → comienza la definición de la etapa de pruebas.
Línea 10: stage: test → asocia el bloque a la etapa test.
Línea 11: script: → declara los comandos a ejecutar.
Línea 12: - dotnet test tests/AceriaApp.Ordenes.Tests → ejecuta solo los tests del servicio.
Línea 13: deploy: → comienza la definición de la etapa de despliegue.
Línea 14: stage: deploy → asocia el bloque a la etapa deploy.
Línea 15: script: → declara los comandos a ejecutar.
Línea 16: - dotnet publish src/AceriaApp.Ordenes.Api -c Release → publica solo el servicio de órdenes.

La ventaja de la independencia de despliegue se materializa en equipos que necesitan liberar con frecuencia y sin coordinar con otros equipos. Su coste es la duplicación de configuración y la necesidad de gestionar versiones de contratos públicos entre servicios.


---

Bloque 7 — Ventajas de los microservicios en las dimensiones de escalado y organización

En la dimensión de escalado, los microservicios ofrecen selectividad: cada servicio se replica según su propia carga. El coste de infraestructura se ajusta a la demanda real de cada capacidad de negocio. En la dimensión de organización, ofrecen autonomía: cada equipo posee un servicio completo y puede tomar decisiones sin coordinación con otros equipos. Las decisiones técnicas se distribuyen y los conflictos de fusión desaparecen porque cada equipo trabaja en su propio repositorio. El coste es la heterogeneidad: distintos equipos pueden elegir distintos stacks, lo que complica la operación y el soporte.

Escalado selectivo:

[Órdenes]    3 instancias  ← alta demanda
[Inventario] 1 instancia   ← demanda media
[Clientes]   1 instancia   ← demanda baja

Cada servicio se replica según su propia carga.

Línea 1: [Órdenes] 3 instancias → el servicio de órdenes se replica tres veces.
Línea 2: [Inventario] 1 instancia → el servicio de inventario mantiene una sola instancia.
Línea 3: [Clientes] 1 instancia → el servicio de clientes mantiene una sola instancia.
Línea 4: Cada servicio se replica según su propia carga. → sintetiza la selectividad del escalado.

La selectividad y la autonomía son ventajas medibles cuando el número de equipos y la desigualdad de carga lo justifican. Su coste aparece en la operación: cada servicio requiere su propia monitorización, su propia configuración y su propio soporte. El coste operativo agregado puede superar el ahorro de infraestructura si no se invierte en plataformas comunes de observabilidad y despliegue.


---

Bloque 8 — Inconvenientes de los microservicios

El primer inconveniente es la complejidad distribuida. Toda comunicación entre servicios es una llamada de red que puede fallar, tardar o perderse. Hay que gestionar timeouts, reintentos, circuit breakers y compensaciones. El segundo inconveniente es la consistencia eventual: no existe una transacción ACID que abarque varios servicios. Hay que diseñar patrones como Saga, Outbox o compensación explícita. El tercer inconveniente es la observabilidad: sin trazabilidad distribuida, diagnosticar un error que atraviesa varios servicios es inviable.

try
{
    var response = await httpClient.GetAsync("http://acería-inventario/api/v1/materiales");
    response.EnsureSuccessStatusCode();
    var materiales = await response.Content.ReadFromJsonAsync<List<Material>>();
    return materiales;
}
catch (HttpRequestException ex)
{
    logger.LogError(ex, "Fallo al consultar el servicio de inventario");
    throw;
}

Línea 1: try → inicia el bloque protegido.
Línea 2: var response = await httpClient.GetAsync(...); → llama al servicio de inventario.
Línea 3: response.EnsureSuccessStatusCode(); → lanza excepción si el código HTTP no es 2xx.
Línea 4: var materiales = await response.Content.ReadFromJsonAsync<List<Material>>(); → deserializa la respuesta.
Línea 5: return materiales; → devuelve la lista de materiales.
Línea 6: catch (HttpRequestException ex) → captura errores de red o códigos no exitosos.
Línea 7: logger.LogError(ex, "..."); → registra el error con contexto.
Línea 8: throw; → propaga la excepción.

El cuarto inconveniente es el coste operativo: cada servicio requiere su propio pipeline, su propia monitorización y su propia configuración. La infraestructura mínima añade complejidad que un monolito no necesita. El quinto inconveniente es la duplicación de código: sin disciplina, cada equipo reimplementa utilidades comunes. El sexto inconveniente es la gestión de versiones de contratos públicos entre servicios. El séptimo inconveniente es la latencia: una operación que en un monolito era una llamada en memoria se convierte en una cadena de llamadas de red.


---

Bloque 9 — Costes ocultos de cada estilo

Los costes ocultos del monolito son tres. El primero es el coste de coordinación: a medida que el equipo crece, el tiempo dedicado a reuniones y a resolver conflictos de fusión crece de forma no lineal. El segundo es el coste de oportunidad tecnológica: no poder adoptar una nueva versión del framework en una parte del sistema sin migrar todo el conjunto. El tercero es el coste de escalado: replicar el artefacto completo cuando solo una funcionalidad lo necesita. Los costes ocultos de los microservicios son otros tres. El primero es el coste de la complejidad accidental: timeouts, reintentos, idempotencia y compensaciones que no aportan valor de negocio. El segundo es el coste de la observabilidad: sin trazabilidad distribuida, el tiempo medio de diagnóstico se multiplica. El tercero es el coste de la duplicación: utilidades comunes reimplementadas en cada servicio.

Costes ocultos:

Monolito:
- Coordinación de equipos.
- Oportunidad tecnológica.
- Escalado homogéneo.

Microservicios:
- Complejidad accidental.
- Observabilidad distribuida.
- Duplicación de utilidades.

Línea 1: Costes ocultos: → título del bloque.
Línea 2: Monolito: → comienza la lista de costes ocultos del monolito.
Línea 3: - Coordinación de equipos. → primer coste oculto.
Línea 4: - Oportunidad tecnológica. → segundo coste oculto.
Línea 5: - Escalado homogéneo. → tercer coste oculto.
Línea 6: Microservicios: → comienza la lista de costes ocultos de los microservicios.
Línea 7: - Complejidad accidental. → primer coste oculto.
Línea 8: - Observabilidad distribuida. → segundo coste oculto.
Línea 9: - Duplicación de utilidades. → tercer coste oculto.

La identificación explícita de estos costes ocultos permite comparar los dos estilos con criterios realistas. Sin este ejercicio, la decisión se basa en percepciones y no en datos. El coste oculto más subestimado en equipos pequeños es el de la complejidad accidental de los microservicios. El coste oculto más subestimado en equipos grandes es el de la coordinación del monolito.


---

Bloque 10 — Criterios de decisión y aplicación al proyecto del curso

La decisión entre monolito y microservicios debe tomarse con los seis criterios siguientes: tamaño del dominio, número de equipos, frecuencia de despliegue, tolerancia al fallo, requisitos de consistencia y madurez operativa. Cada criterio se evalúa con un indicador concreto y se pondera según el contexto. En el proyecto del curso, los seis criterios apuntan a empezar con un monolito modular: el dominio es mediano, el equipo es de dos personas, la frecuencia de despliegue es semanal, la tolerancia al fallo es baja, la consistencia requerida es fuerte y la madurez operativa es inicial. El monolito modular permite validar el dominio y las reglas de negocio antes de asumir el coste de la distribución.

Criterios aplicados al proyecto del curso:

Dominio mediano               → monolito modular.
Equipo de 2 personas          → monolito modular.
Despliegue semanal            → monolito modular.
Tolerancia al fallo baja      → monolito modular.
Consistencia fuerte requerida → monolito modular.
Madurez operativa inicial     → monolito modular.

Línea 1: Dominio mediano → el tamaño del dominio no justifica la distribución.
Línea 2: Equipo de 2 personas → el equipo no tiene masa crítica para operar microservicios.
Línea 3: Despliegue semanal → la frecuencia no exige independencia de despliegue.
Línea 4: Tolerancia al fallo baja → el negocio no tolera degradaciones.
Línea 5: Consistencia fuerte requerida → las transacciones ACID son necesarias.
Línea 6: Madurez operativa inicial → no hay plataforma de observabilidad ni de despliegue.

La conclusión es que el monolito modular es la elección correcta para el punto de partida del curso. La evolución hacia microservicios se justificará en módulos posteriores cuando alguno de los seis criterios cambie. El proyecto no adopta microservicios por moda, sino que los adopta cuando un criterio objetivo lo justifique. Este enfoque evita el coste prematuro de la distribución y permite medir el impacto de cada decisión arquitectónica.


---

Resumen rápido de la teoría

· El análisis de ventajas e inconvenientes exige un marco explícito con cuatro dimensiones: despliegue, escalado, organización y consistencia.
· El monolito ofrece ventajas claras en despliegue, consistencia, escalado y organización cuando el dominio es mediano y el equipo es pequeño.
· Los microservicios ofrecen ventajas claras en despliegue independiente, escalado selectivo y autonomía de equipos cuando el dominio es grande y hay varios equipos.
· Los costes ocultos del monolito son coordinación, oportunidad tecnológica y escalado homogéneo.
· Los costes ocultos de los microservicios son complejidad accidental, observabilidad distribuida y duplicación de utilidades.
· Los seis criterios de decisión aplicados al proyecto del curso apuntan a empezar con un monolito modular.


---


Punto 1.3 — Principios de diseño

Módulo 1: Introducción a los microservicios
Duración: 53 minutos (26 minutos de teoría + 27 minutos de práctica)
Objetivos de aprendizaje:

· Comprender los principios de diseño que guían la descomposición de un sistema en servicios autónomos.
· Identificar el principio de responsabilidad única aplicado a servicios.
· Identificar el principio de ocultación de información y su relación con los límites del servicio.
· Identificar el principio de acoplamiento débil y cohesión fuerte.
· Aplicar los principios al dominio de la acería y añadir al proyecto un documento de principios y una clase de validación de límites de servicio.


---

PARTE TEÓRICA (26 minutos)

Bloque 1 — Principios de diseño como criterios de descomposición

Los principios de diseño son reglas generales que guían la toma de decisiones arquitectónicas. En el contexto de los microservicios, su función es determinar dónde trazar la frontera entre un servicio y otro. Sin principios explícitos, la descomposición se convierte en una decisión arbitraria que produce servicios mal delimitados, con dependencias cruzadas y responsabilidades solapadas. Un principio de diseño no es una regla absoluta: es un criterio que se aplica con juicio y que se documenta para que la decisión sea trazable. Los principios se organizan en tres categorías: principios de responsabilidad, principios de ocultación y principios de acoplamiento. Cada categoría responde a una pregunta distinta sobre el límite del servicio.

Categorías de principios de diseño:

1. Responsabilidad  → ¿qué hace el servicio?
2. Ocultación       → ¿qué esconde el servicio?
3. Acoplamiento     → ¿cómo se relaciona con otros?

Línea 1: 1. Responsabilidad → primera categoría, define el alcance funcional del servicio.
Línea 2: 2. Ocultación → segunda categoría, define qué detalles internos no se exponen.
Línea 3: 3. Acoplamiento → tercera categoría, define las dependencias entre servicios.

La primera categoría, la responsabilidad, responde a la pregunta de qué hace el servicio. La segunda, la ocultación, responde a la pregunta de qué esconde. La tercera, el acoplamiento, responde a la pregunta de cómo se relaciona con otros servicios. Las tres categorías se aplican de forma conjunta: un servicio bien diseñado tiene una responsabilidad clara, oculta sus detalles internos y mantiene un acoplamiento débil con el resto. La aplicación conjunta de las tres categorías es lo que distingue un límite de servicio correcto de uno incorrecto.

La ausencia de principios explícitos produce tres síntomas reconocibles. El primero es el servicio "cajón de sastre", que acumula responsabilidades heterogéneas. El segundo es el servicio "transparente", que expone sus tablas y su modelo interno a otros servicios. El tercero es el servicio "acoplado", que necesita coordinarse con otros para cualquier cambio. Los tres síntomas se corrigen aplicando los principios de responsabilidad, ocultación y acoplamiento respectivamente. El curso aplica estos principios al dominio de la acería para que el alumno los vea en un contexto concreto.


---

Bloque 2 — Principio de responsabilidad única aplicado a servicios

El principio de responsabilidad única establece que un servicio debe tener una única razón para cambiar. En el contexto de los microservicios, la "razón para cambiar" se identifica con una capacidad de negocio concreta. Un servicio de órdenes cambia cuando cambian las reglas de las órdenes. Un servicio de inventario cambia cuando cambian las reglas del inventario. Si un servicio cambia por dos motivos distintos, tiene dos responsabilidades y debería dividirse. La identificación de la razón para cambiar se realiza con el lenguaje del negocio, no con el lenguaje técnico. Un servicio no se define por la tecnología que usa, sino por la capacidad de negocio que encapsula.

// Correcto: una responsabilidad por servicio
public class OrdenServicio
{
    public void CrearOrden(CrearOrdenCommand command) { }
    public void CancelarOrden(Guid id) { }
}

// Incorrecto: dos responsabilidades en el mismo servicio
public class OrdenYFacturacionServicio
{
    public void CrearOrden(CrearOrdenCommand command) { }
    public void EmitirFactura(Guid ordenId) { }
}

Línea 1: // Correcto: una responsabilidad por servicio → comentario que indica el caso correcto.
Línea 2: public class OrdenServicio → clase que encapsula solo la capacidad de órdenes.
Línea 3: { → abre el cuerpo de la clase.
Línea 4: public void CrearOrden(...) → método de creación de órdenes.
Línea 5: public void CancelarOrden(...) → método de cancelación de órdenes.
Línea 6: } → cierra el cuerpo de la clase.
Línea 7: // Incorrecto: dos responsabilidades en el mismo servicio → comentario que indica el caso incorrecto.
Línea 8: public class OrdenYFacturacionServicio → clase que mezcla dos capacidades.
Línea 9: { → abre el cuerpo de la clase.
Línea 10: public void CrearOrden(...) → método de órdenes.
Línea 11: public void EmitirFactura(...) → método de facturación.
Línea 12: } → cierra el cuerpo de la clase.

La aplicación del principio tiene una consecuencia práctica: los servicios tienden a ser más pequeños de lo que la intuición sugiere. Un servicio con cinco métodos relacionados con la misma capacidad de negocio es correcto. Un servicio con dos métodos de capacidades distintas es incorrecto aunque tenga pocas líneas de código. El tamaño no es el criterio; la razón para cambiar es el criterio.


---

Bloque 3 — Principio de ocultación de información aplicado a servicios

El principio de ocultación de información establece que un módulo debe exponer solo lo que otros módulos necesitan y ocultar todo lo demás. En microservicios, la ocultación se aplica en tres niveles: el modelo de datos, la lógica interna y la topología de despliegue. El modelo de datos se oculta prohibiendo que un servicio acceda directamente a la base de datos de otro. La lógica interna se oculta exponiendo solo contratos públicos estables. La topología se oculta detrás de un API Gateway que centraliza el enrutamiento. La ocultación no es un fin en sí mismo: su objetivo es permitir que cada servicio evolucione sin romper a los demás.

Ocultación en tres niveles:

1. Modelo de datos   → cada servicio tiene su propia base de datos.
2. Lógica interna    → solo se exponen contratos públicos.
3. Topología         → API Gateway centraliza el enrutamiento.

Línea 1: 1. Modelo de datos → primer nivel, oculta el esquema de persistencia.
Línea 2: 2. Lógica interna → segundo nivel, oculta la implementación.
Línea 3: 3. Topología → tercer nivel, oculta la ubicación de los servicios.

La violación más común del principio es el acceso directo a la base de datos de otro servicio. Cuando dos servicios comparten una base de datos, cualquier cambio en el esquema afecta a ambos y la independencia de despliegue desaparece. La segunda violación es la exposición del modelo interno a través de la API. Cuando un servicio devuelve su entidad de base de datos tal cual, cualquier cambio en la entidad rompe a los consumidores. La tercera violación es la exposición de la topología interna. Cuando los clientes conocen la ubicación de cada servicio, cualquier cambio de infraestructura afecta a los clientes.


---

Bloque 4 — Principio de acoplamiento débil y cohesión fuerte

El principio de acoplamiento débil y cohesión fuerte establece que los elementos de un módulo deben estar fuertemente relacionados entre sí y débilmente relacionados con otros módulos. En microservicios, la cohesión se mide por el número de conceptos distintos que maneja un servicio: a menos conceptos, mayor cohesión. El acoplamiento se mide por el número de servicios con los que un servicio necesita comunicarse para completar una operación: a menos servicios, menor acoplamiento. El equilibrio entre cohesión y acoplamiento determina la calidad del límite del servicio.

Cohesión alta:  un servicio maneja un solo concepto.
Cohesión baja:  un servicio maneja varios conceptos.

Acoplamiento bajo:  un servicio depende de pocos servicios.
Acoplamiento alto:  un servicio depende de muchos servicios.

Línea 1: Cohesión alta: un servicio maneja un solo concepto. → describe el caso deseable.
Línea 2: Cohesión baja: un servicio maneja varios conceptos. → describe el caso no deseable.
Línea 3: Acoplamiento bajo: un servicio depende de pocos servicios. → describe el caso deseable.
Línea 4: Acoplamiento alto: un servicio depende de muchos servicios. → describe el caso no deseable.

La aplicación del principio tiene una consecuencia práctica: los servicios deben agrupar operaciones que cambian juntas y separar operaciones que cambian por motivos distintos. Un servicio que agrupa operaciones que cambian juntas tiene cohesión alta. Un servicio que depende de muchos otros para completar una operación tiene acoplamiento alto. El objetivo es maximizar la cohesión y minimizar el acoplamiento, sin caer en el extremo de crear servicios tan pequeños que cada operación requiera coordinar diez servicios.


---

Bloque 5 — Principio de límite del contexto

El principio de límite del contexto establece que cada servicio debe corresponder a un contexto delimitado del dominio. Un contexto delimitado es una frontera dentro de la cual un término del negocio tiene un significado preciso y consistente. Fuera de esa frontera, el mismo término puede tener otro significado. En el dominio de la acería, el término "orden" puede significar una orden de producción en el contexto de planta y una orden de compra en el contexto de aprovisionamiento. Los dos significados son válidos, pero no deben convivir en el mismo servicio. El límite del contexto define dónde empieza y dónde termina el servicio.

Contextos delimitados en la acería:

Contexto de producción  → "orden" = orden de fabricación.
Contexto de aprovisionamiento → "orden" = orden de compra.
Contexto de clientes    → "cliente" = empresa compradora.

Línea 1: Contexto de producción → primer contexto delimitado, con su propio significado de "orden".
Línea 2: Contexto de aprovisionamiento → segundo contexto, con otro significado de "orden".
Línea 3: Contexto de clientes → tercer contexto, con su propio significado de "cliente".

La aplicación del principio tiene una consecuencia práctica: los servicios deben corresponder a contextos delimitados, no a entidades de la base de datos ni a capas técnicas. Un servicio que corresponde a una tabla de la base de datos no es un servicio, es un envoltorio de tabla. Un servicio que corresponde a un contexto delimitado encapsula un significado de negocio completo. El límite del contexto es el criterio más importante para decidir dónde trazar la frontera entre servicios.


---

Bloque 6 — Principio de autonomía del servicio

El principio de autonomía establece que un servicio debe poder operar de forma independiente respecto a los demás. La autonomía se manifiesta en tres dimensiones: autonomía de despliegue, autonomía de datos y autonomía de fallo. La autonomía de despliegue permite que un servicio se actualice sin coordinar con los demás. La autonomía de datos permite que un servicio gestione su propia persistencia sin depender de otros. La autonomía de fallo permite que un servicio siga operando cuando otro falla, aunque con funcionalidad degradada. La autonomía no es absoluta: ningún servicio es completamente autónomo en un sistema distribuido.

// Autonomía de datos: cada servicio tiene su propio DbContext
public class OrdenesDbContext : DbContext
{
    public DbSet<Orden> Ordenes => Set<Orden>();
}

public class InventarioDbContext : DbContext
{
    public DbSet<Material> Materiales => Set<Material>();
}

Línea 1: // Autonomía de datos: cada servicio tiene su propio DbContext → comentario que indica el principio.
Línea 2: public class OrdenesDbContext : DbContext → contexto propio del servicio de órdenes.
Línea 3: { → abre el cuerpo de la clase.
Línea 4: public DbSet<Orden> Ordenes => Set<Orden>(); → solo expone las órdenes.
Línea 5: } → cierra el cuerpo de la clase.
Línea 6: public class InventarioDbContext : DbContext → contexto propio del servicio de inventario.
Línea 7: { → abre el cuerpo de la clase.
Línea 8: public DbSet<Material> Materiales => Set<Material>(); → solo expone los materiales.
Línea 9: } → cierra el cuerpo de la clase.

La aplicación del principio tiene una consecuencia práctica: los servicios no comparten contexto de persistencia. Cada servicio tiene su propio DbContext y su propia base de datos. La comunicación entre servicios se realiza a través de la red, no a través de la base de datos. Esta separación garantiza que un cambio en el esquema de un servicio no afecte a los demás.


---

Bloque 7 — Principio de contrato explícito

El principio de contrato explícito establece que la comunicación entre servicios debe realizarse a través de contratos públicos, versionados y documentados. Un contrato explícito define qué datos se intercambian, en qué formato y con qué garantías. El contrato no expone la implementación interna del servicio, solo su interfaz pública. Los contratos se versionan para permitir la evolución independiente de los servicios. La versión del contrato se negocia entre el servicio productor y el servicio consumidor. La violación del principio produce acoplamiento por implementación, donde un cambio interno rompe a los consumidores.

public record OrdenDto(
    Guid Id,
    string Cliente,
    string Material,
    int Cantidad,
    DateTime FechaCreacion);

Línea 1: public record OrdenDto( → declara un contrato inmutable con la palabra clave record.
Línea 2: Guid Id, → identificador de la orden.
Línea 3: string Cliente, → nombre del cliente.
Línea 4: string Material, → material solicitado.
Línea 5: int Cantidad, → cantidad solicitada.
Línea 6: DateTime FechaCreacion); → fecha de creación de la orden.

La aplicación del principio tiene una consecuencia práctica: los servicios no exponen sus entidades de dominio a través de la API. Exponen DTOs específicos que representan el contrato público. La entidad Orden puede cambiar sin romper el contrato OrdenDto. La separación entre entidad y DTO es la garantía de que el contrato público se mantiene estable aunque la implementación evolucione.


---

Bloque 8 — Principio de tolerancia al fallo

El principio de tolerancia al fallo establece que un servicio debe seguir operando cuando una dependencia falla, aunque sea con funcionalidad degradada. La tolerancia se implementa con timeouts, reintentos, circuit breakers y respuestas de reserva. El timeout evita que una llamada bloquee el servicio indefinidamente. El reintento recupera errores transitorios. El circuit breaker evita que un servicio saturado reciba más carga. La respuesta de reserva devuelve un valor por defecto cuando la dependencia no está disponible. La tolerancia no elimina el fallo: lo contiene y evita que se propague.

var policy = Policy
    .Handle<HttpRequestException>()
    .CircuitBreakerAsync(
        exceptionsAllowedBeforeBreaking: 3,
        durationOfBreak: TimeSpan.FromSeconds(30));

Línea 1: var policy = Policy → comienza la definición de la política.
Línea 2: .Handle<HttpRequestException>() → se activa ante errores HTTP.
Línea 3: .CircuitBreakerAsync( → configura un circuit breaker.
Línea 4: exceptionsAllowedBeforeBreaking: 3, → tres errores antes de abrir el circuito.
Línea 5: durationOfBreak: TimeSpan.FromSeconds(30)); → el circuito permanece abierto 30 segundos.

La aplicación del principio tiene una consecuencia práctica: cada llamada a otro servicio se envuelve en una política de tolerancia. Sin esta política, un fallo en un servicio se propaga en cascada y bloquea todo el sistema. Con la política, el fallo se contiene y el sistema sigue operando con funcionalidad degradada.


---

Bloque 9 — Principio de evolución independiente

El principio de evolución independiente establece que un servicio debe poder evolucionar sin obligar a los demás a cambiar al mismo ritmo. La evolución se manifiesta en tres dimensiones: evolución del modelo de datos, evolución de la lógica interna y evolución del contrato público. La evolución del modelo de datos es libre porque cada servicio tiene su propia base de datos. La evolución de la lógica interna es libre porque la implementación está oculta. La evolución del contrato público se gestiona con versionado. La violación del principio produce acoplamiento temporal, donde todos los servicios deben desplegarse a la vez.

Versionado de contratos:

/api/v1/ordenes  → contrato estable, sin cambios.
/api/v2/ordenes  → contrato nuevo, con campos adicionales.

Línea 1: /api/v1/ordenes → primera versión del contrato, permanece activa.
Línea 2: /api/v2/ordenes → segunda versión del contrato, con campos nuevos.

La aplicación del principio tiene una consecuencia práctica: los contratos públicos se versionan en la URL y las versiones antiguas se mantienen durante un periodo de transición. Los consumidores migran a la nueva versión cuando pueden. El productor retira la versión antigua cuando ningún consumidor la usa. Este ciclo permite la evolución independiente sin romper a los consumidores.


---

Bloque 10 — Aplicación de los principios al proyecto del curso

El proyecto del curso aplica los principios de diseño en cada decisión arquitectónica. El principio de responsabilidad única justifica que el monolito modular se organice por capacidades de negocio. El principio de ocultación justifica que cada módulo tenga su propia carpeta y su propia interfaz. El principio de acoplamiento débil justifica que las dependencias entre módulos se gestionen con interfaces. El principio de límite del contexto justifica que el monolito se organice en torno a contextos delimitados. El principio de autonomía justifica la evolución hacia microservicios cuando el contexto lo permite. El principio de contrato explícito justifica la creación de DTOs. El principio de tolerancia al fallo justifica la introducción de Polly. El principio de evolución independiente justifica el versionado de contratos.

Aplicación de los principios al proyecto:

Responsabilidad única       → módulos por capacidad de negocio.
Ocultación                  → cada módulo con su propia carpeta.
Acoplamiento débil          → interfaces entre módulos.
Límite del contexto         → contextos delimitados.
Autonomía                   → evolución hacia microservicios.
Contrato explícito          → DTOs públicos.
Tolerancia al fallo         → Polly.
Evolución independiente     → versionado de contratos.

Línea 1: Responsabilidad única → módulos por capacidad de negocio.
Línea 2: Ocultación → cada módulo con su propia carpeta.
Línea 3: Acoplamiento débil → interfaces entre módulos.
Línea 4: Límite del contexto → contextos delimitados.
Línea 5: Autonomía → evolución hacia microservicios.
Línea 6: Contrato explícito → DTOs públicos.
Línea 7: Tolerancia al fallo → Polly.
Línea 8: Evolución independiente → versionado de contratos.

La aplicación de los principios no es un ejercicio teórico: cada principio se materializa en una decisión concreta del proyecto. El alumno puede rastrear cada decisión hasta el principio que la justifica. Esta trazabilidad es lo que distingue una arquitectura razonada de una arquitectura por acumulación. El punto 1.3 cierra el bloque de fundamentos y prepara el terreno para el punto 1.4, donde se estudiará la organización concreta de una solución basada en microservicios.


---

Resumen rápido de la teoría

· Los principios de diseño se organizan en tres categorías: responsabilidad, ocultación y acoplamiento.
· El principio de responsabilidad única establece que un servicio debe tener una sola razón para cambiar, identificada con una capacidad de negocio.
· El principio de ocultación establece que un servicio debe exponer solo lo necesario y ocultar el modelo de datos, la lógica interna y la topología.
· El principio de acoplamiento débil y cohesión fuerte establece que los elementos de un servicio deben estar fuertemente relacionados entre sí y débilmente con otros.
· El principio de límite del contexto establece que cada servicio debe corresponder a un contexto delimitado del dominio.
· Los principios de autonomía, contrato explícito, tolerancia al fallo y evolución independiente completan el marco de diseño.


---


Punto 1.4 — Organización de una solución basada en microservicios

Módulo 1: Introducción a los microservicios
Duración: 53 minutos (26 minutos de teoría + 27 minutos de práctica)
Objetivos de aprendizaje:

· Comprender cómo se organiza una solución basada en microservicios.
· Diferenciar entre repositorio único (monorepo) y repositorio por servicio (polyrepo).
· Identificar las convenciones de nombres de proyectos, carpetas y ensamblados.
· Comprender la separación entre código de producción, tests y documentación.
· Añadir al proyecto AceriaApp un documento de organización de solución y una clase de verificación de convenciones de nombres.


---

PARTE TEÓRICA (26 minutos)

Bloque 1 — Organización de soluciones y su impacto en la evolución

La organización de una solución basada en microservicios determina la facilidad con la que el equipo puede añadir servicios, extraerlos o reemplazarlos. Una organización deficiente produce dependencias ocultas, duplicación de convenciones y dificultad para localizar el código. Una organización correcta produce límites visibles, convenciones uniformes y navegación predecible. La organización se materializa en tres decisiones: la estructura de repositorios, la estructura de carpetas dentro de cada repositorio y las convenciones de nombres. Las tres decisiones son independientes entre sí, pero se refuerzan mutuamente. Una decisión coherente en las tres produce una solución que cualquier desarrollador puede entender en pocos minutos.

Tres decisiones de organización:

1. Estructura de repositorios  → monorepo o polyrepo.
2. Estructura de carpetas      → src, tests, docs.
3. Convenciones de nombres     → proyectos, ensamblados, espacios de nombres.

Línea 1: 1. Estructura de repositorios → primera decisión, define dónde vive el código.
Línea 2: 2. Estructura de carpetas → segunda decisión, define cómo se organiza dentro del repositorio.
Línea 3: 3. Convenciones de nombres → tercera decisión, define cómo se identifican los artefactos.

La organización no es una cuestión estética: tiene consecuencias medibles sobre el tiempo de incorporación de nuevos desarrolladores, sobre la facilidad para extraer servicios y sobre la capacidad de automatizar tareas. Un proyecto mal organizado tarda semanas en incorporar a un nuevo desarrollador. Un proyecto bien organizado tarda días. La diferencia no está en la complejidad técnica del código, sino en la previsibilidad de su estructura. El curso aplica estas tres decisiones al proyecto AceriaApp de forma explícita y trazable.


---

Bloque 2 — Monorepo frente a polyrepo

Un monorepo es un único repositorio que contiene todos los servicios, sus tests y su documentación. Un polyrepo es un conjunto de repositorios, uno por servicio, con su propio ciclo de vida. La elección entre ambos depende del tamaño del equipo, de la madurez de las herramientas de construcción y de la frecuencia con la que los servicios cambian juntos. El monorepo facilita la búsqueda global, la refactorización entre servicios y la coherencia de convenciones. El polyrepo facilita la autonomía total de cada equipo y la independencia de permisos. Ninguno de los dos es universalmente mejor: cada uno tiene ventajas e inconvenientes concretos.

Monorepo:

AceriaApp/
├── modulo-1/
│   ├── 1.1-monolito-vs-microservicios/
│   ├── 1.2-ventajas-inconvenientes/
│   └── ...

Polyrepo:

AceriaApp.Ordenes/     → repositorio independiente.
AceriaApp.Inventario/  → repositorio independiente.
AceriaApp.Clientes/    → repositorio independiente.

Línea 1: Monorepo: → título del ejemplo de monorepo.
Línea 2: AceriaApp/ → raíz única del repositorio.
Línea 3: ├── modulo-1/ → carpeta por módulo.
Línea 4: │   ├── 1.1-monolito-vs-microservicios/ → punto 1.1 dentro del módulo.
Línea 5: │   ├── 1.2-ventajas-inconvenientes/ → punto 1.2 dentro del módulo.
Línea 6: Polyrepo: → título del ejemplo de polyrepo.
Línea 7: AceriaApp.Ordenes/ → repositorio independiente del servicio de órdenes.
Línea 8: AceriaApp.Inventario/ → repositorio independiente del servicio de inventario.
Línea 9: AceriaApp.Clientes/ → repositorio independiente del servicio de clientes.

El monorepo es la elección del curso porque el equipo es pequeño y los servicios cambian juntos durante la fase de aprendizaje. Un equipo de dos personas que trabaja sobre tres servicios no se beneficia de la independencia de permisos del polyrepo, pero sí se beneficia de la búsqueda global y de la refactorización entre servicios del monorepo. La decisión se documenta en un ADR y se revisa cuando el equipo crece.


---

Bloque 3 — Estructura de carpetas dentro de un repositorio

Dentro de un repositorio, la estructura de carpetas debe separar claramente el código de producción, los tests y la documentación. La separación se materializa en tres carpetas de primer nivel: src/, tests/ y docs/. La carpeta src/ contiene los proyectos ejecutables y las bibliotecas compartidas. La carpeta tests/ contiene los proyectos de pruebas. La carpeta docs/ contiene la documentación, los ADRs y los diagramas. Esta separación es una convención ampliamente adoptada en el ecosistema .NET y facilita la configuración de pipelines de compilación y de pruebas.

Estructura de un punto del curso:

1.1-monolito-vs-microservicios/
├── README.md
├── AceriaApp.sln
├── src/
│   └── AceriaApp.Monolito.Api/
├── tests/
│   ├── AceriaApp.Monolito.Tests/
│   ├── AceriaApp.Metricas.Tests/
│   └── AceriaApp.Diseno.Tests/
└── docs/
    ├── ADR-001-monolito-vs-microservicios.md
    ├── ADR-002-metricas-acoplamiento.md
    └── ADR-003-principios-diseno.md

Línea 1: 1.1-monolito-vs-microservicios/ → carpeta del punto.
Línea 2: ├── README.md → documento de descripción del punto.
Línea 3: ├── AceriaApp.sln → solución que agrupa los proyectos.
Línea 4: ├── src/ → carpeta de código de producción.
Línea 5: │   └── AceriaApp.Monolito.Api/ → proyecto de API dentro de src.
Línea 6: ├── tests/ → carpeta de proyectos de pruebas.
Línea 7: │   ├── AceriaApp.Monolito.Tests/ → proyecto de tests del monolito.
Línea 8: │   ├── AceriaApp.Metricas.Tests/ → proyecto de tests de métricas.
Línea 9: │   └── AceriaApp.Diseno.Tests/ → proyecto de tests de diseño.
Línea 10: └── docs/ → carpeta de documentación.
Línea 11: ├── ADR-001-monolito-vs-microservicios.md → primer ADR.
Línea 12: ├── ADR-002-metricas-acoplamiento.md → segundo ADR.
Línea 13: └── ADR-003-principios-diseno.md → tercer ADR.

La separación en tres carpetas de primer nivel es una convención, no una obligación técnica. Su valor está en la previsibilidad: cualquier desarrollador que abra el repositorio sabe dónde buscar el código, dónde buscar los tests y dónde buscar la documentación. Esta previsibilidad reduce el tiempo de incorporación y facilita la automatización de tareas de compilación y despliegue.


---

Bloque 4 — Convenciones de nombres de proyectos

Las convenciones de nombres de proyectos en .NET siguen el patrón Empresa.Producto.Componente.Tipo. El prefijo de empresa o producto agrupa todos los proyectos relacionados. El componente identifica la capacidad de negocio o el módulo. El tipo identifica la naturaleza del proyecto: Api, Tests, Domain, Infrastructure, Application. Esta estructura jerárquica permite agrupar y filtrar proyectos por convención. En el proyecto AceriaApp, el prefijo es AceriaApp, el componente es el nombre del servicio o módulo, y el tipo identifica la función del proyecto.

Convención de nombres:

AceriaApp.Ordenes.Api        → API del servicio de órdenes.
AceriaApp.Ordenes.Domain     → dominio del servicio de órdenes.
AceriaApp.Ordenes.Tests      → tests del servicio de órdenes.
AceriaApp.Inventario.Api     → API del servicio de inventario.
AceriaApp.Monolito.Api       → API del monolito de referencia.

Línea 1: AceriaApp.Ordenes.Api → prefijo AceriaApp, componente Ordenes, tipo Api.
Línea 2: AceriaApp.Ordenes.Domain → tipo Domain para el dominio.
Línea 3: AceriaApp.Ordenes.Tests → tipo Tests para las pruebas.
Línea 4: AceriaApp.Inventario.Api → componente Inventario, tipo Api.
Línea 5: AceriaApp.Monolito.Api → componente Monolito, tipo Api.

La convención facilita la búsqueda por nombre, la configuración de pipelines y la organización de la solución en el panel Solution Explorer. Un proyecto mal nombrado rompe la uniformidad y obliga a los desarrolladores a recordar excepciones. La convención se aplica también a los espacios de nombres: el espacio de nombres raíz de cada proyecto coincide con el nombre del proyecto. Esta coherencia entre nombre de proyecto y espacio de nombres facilita la resolución de tipos y la lectura del código.


---

Bloque 5 — Convenciones de nombres de espacios de nombres

Los espacios de nombres en .NET siguen el patrón Empresa.Producto.Componente.Tipo.Capa. El prefijo coincide con el nombre del proyecto. Las capas dentro del proyecto se organizan en subespacios: Dominio, Infraestructura, Metricas, Diseno, Aplicacion. Esta estructura permite organizar el código por responsabilidad y facilita la navegación. En el proyecto monolítico de referencia, los espacios de nombres son AceriaApp.Monolito.Api.Dominio, AceriaApp.Monolito.Api.Infraestructura, AceriaApp.Monolito.Api.Metricas y AceriaApp.Monolito.Api.Diseno.

namespace AceriaApp.Monolito.Api.Dominio;

public class Orden
{
    public Guid Id { get; set; }
}

Línea 1: namespace AceriaApp.Monolito.Api.Dominio; → espacio de nombres del dominio.
Línea 2: public class Orden → clase del dominio.
Línea 3: { → abre el cuerpo de la clase.
Línea 4: public Guid Id { get; set; } → propiedad del dominio.
Línea 5: } → cierra el cuerpo de la clase.

La convención de espacios de nombres debe ser consistente con la estructura de carpetas del proyecto. Un archivo en la carpeta Dominio debe declarar el espacio de nombres ...Dominio. Un archivo en la carpeta Infraestructura debe declarar el espacio de nombres ...Infraestructura. Esta correspondencia facilita la navegación y evita conflictos de nombres. La convención se aplica también a los tests: cada proyecto de tests declara un espacio de nombres que termina en Tests.


---

Bloque 6 — Separación entre código de producción y tests

La separación entre código de producción y tests se materializa en dos carpetas de primer nivel: src/ y tests/. Cada proyecto de producción tiene su proyecto de tests correspondiente. La correspondencia se establece por convención de nombres: AceriaApp.Monolito.Api tiene su proyecto AceriaApp.Monolito.Tests. Esta correspondencia permite ejecutar los tests de un proyecto concreto sin ejecutar los de los demás. La separación también facilita la configuración de pipelines que compilan y publican solo el código de producción. Los tests no se publican en producción.

Correspondencia entre producción y tests:

AceriaApp.Monolito.Api     → AceriaApp.Monolito.Tests
AceriaApp.Metricas         → AceriaApp.Metricas.Tests
AceriaApp.Diseno           → AceriaApp.Diseno.Tests

Línea 1: AceriaApp.Monolito.Api → proyecto de producción.
Línea 2: AceriaApp.Metricas → módulo de producción.
Línea 3: AceriaApp.Diseno → módulo de producción.
Línea 4: AceriaApp.Monolito.Tests → proyecto de tests correspondiente.
Línea 5: AceriaApp.Metricas.Tests → proyecto de tests correspondiente.
Línea 6: AceriaApp.Diseno.Tests → proyecto de tests correspondiente.

La correspondencia uno a uno entre producción y tests no es obligatoria pero sí recomendable. Un proyecto de producción sin proyecto de tests correspondiente es una señal de deuda técnica. Un proyecto de tests sin proyecto de producción correspondiente es una señal de código obsoleto. La convención facilita la detección de ambas señales. La separación entre src/ y tests/ también facilita la configuración de la solución para que los proyectos de tests no se incluyan en el artefacto publicado.


---

Bloque 7 — Documentación como parte del repositorio

La documentación es parte del repositorio, no un artefacto externo. Se organiza en la carpeta docs/ y contiene los ADRs, los diagramas y las guías. Los ADRs documentan las decisiones arquitectónicas con su contexto, alternativas y consecuencias. Los diagramas documentan la estructura del sistema. Las guías documentan los procedimientos operativos. La documentación se versiona junto con el código y se revisa en las mismas pull requests. Esta práctica garantiza que la documentación evoluciona con el código y no queda obsoleta.

Contenido de docs/:

docs/
├── ADR-001-monolito-vs-microservicios.md
├── ADR-002-metricas-acoplamiento.md
├── ADR-003-principios-diseno.md
├── analisis-ventajas-inconvenientes.md
└── principios-diseno.md

Línea 1: docs/ → carpeta de documentación.
Línea 2: ADR-001-monolito-vs-microservicios.md → primer ADR.
Línea 3: ADR-002-metricas-acoplamiento.md → segundo ADR.
Línea 4: ADR-003-principios-diseno.md → tercer ADR.
Línea 5: analisis-ventajas-inconvenientes.md → documento de análisis.
Línea 6: principios-diseno.md → documento de principios.

La documentación se organiza por tipo: los ADRs con prefijo ADR-NNN-, los análisis con nombre descriptivo, las guías con prefijo guia-. Esta organización permite localizar rápidamente el documento relevante. La documentación no duplica el código: describe las decisiones y las razones, no la implementación. Un documento que describe línea por línea lo que hace el código es un documento que queda obsoleto en el primer cambio. Un documento que describe por qué se tomó una decisión es un documento que permanece válido aunque el código cambie.


---

Bloque 8 — Convenciones de ramas y commits

Las convenciones de ramas y commits determinan la trazabilidad del trabajo. Las ramas se nombran con el prefijo del tipo de cambio: feature/, fix/, docs/, refactor/. Los commits se nombran con el prefijo del punto del curso: Punto N.M: descripción. Esta convención permite filtrar commits por punto y comparar el estado del proyecto entre puntos consecutivos. La trazabilidad entre commits, puntos y módulos facilita la auditoría del progreso del alumno.

Convenciones de ramas:

feature/nueva-funcionalidad
fix/correccion-error
docs/actualizacion-adr
refactor/extraccion-servicio

Convenciones de commits:

Punto 1.1: estructura inicial del proyecto AceriaApp
Punto 1.2: análisis de ventajas e inconvenientes y métricas de acoplamiento
Punto 1.3: principios de diseño y validación de límites de servicio
Punto 1.4: organización de la solución y convenciones de nombres

Línea 1: feature/nueva-funcionalidad → rama para una nueva funcionalidad.
Línea 2: fix/correccion-error → rama para una corrección.
Línea 3: docs/actualizacion-adr → rama para documentación.
Línea 4: refactor/extraccion-servicio → rama para refactorización.
Línea 5: Punto 1.1: estructura inicial del proyecto AceriaApp → primer commit.
Línea 6: Punto 1.2: análisis de ventajas e inconvenientes y métricas de acoplamiento → segundo commit.
Línea 7: Punto 1.3: principios de diseño y validación de límites de servicio → tercer commit.
Línea 8: Punto 1.4: organización de la solución y convenciones de nombres → cuarto commit.

La convención de commits permite comparar el estado del proyecto entre dos puntos consecutivos con git diff Punto1.1 Punto1.2. Esta capacidad es útil para el alumno que quiere ver exactamente qué se añadió en cada punto. La convención de ramas permite aislar el trabajo en curso sin afectar a la rama principal. Ambas convenciones son recomendaciones, no obligaciones: su valor está en la trazabilidad que proporcionan.


---

Bloque 9 — Estructura de una solución con varios servicios

Cuando el proyecto evolucione hacia microservicios, la estructura de la solución reflejará la separación entre servicios. Cada servicio tendrá su propio proyecto de API, su propio proyecto de dominio, su propio proyecto de infraestructura y su propio proyecto de tests. La solución agrupará todos los proyectos y permitirá compilarlos y ejecutarlos conjuntamente. La estructura de carpetas será la misma que en el monolito modular: src/ con los proyectos de producción y tests/ con los proyectos de tests.

Estructura con varios servicios:

src/
├── AceriaApp.Ordenes.Api/
├── AceriaApp.Ordenes.Domain/
├── AceriaApp.Ordenes.Infrastructure/
├── AceriaApp.Inventario.Api/
├── AceriaApp.Inventario.Domain/
└── AceriaApp.Inventario.Infrastructure/

tests/
├── AceriaApp.Ordenes.Tests/
└── AceriaApp.Inventario.Tests/

Línea 1: src/ → carpeta de producción.
Línea 2: AceriaApp.Ordenes.Api/ → API del servicio de órdenes.
Línea 3: AceriaApp.Ordenes.Domain/ → dominio del servicio de órdenes.
Línea 4: AceriaApp.Ordenes.Infrastructure/ → infraestructura del servicio de órdenes.
Línea 5: AceriaApp.Inventario.Api/ → API del servicio de inventario.
Línea 6: AceriaApp.Inventario.Domain/ → dominio del servicio de inventario.
Línea 7: AceriaApp.Inventario.Infrastructure/ → infraestructura del servicio de inventario.
Línea 8: tests/ → carpeta de tests.
Línea 9: AceriaApp.Ordenes.Tests/ → tests del servicio de órdenes.
Línea 10: AceriaApp.Inventario.Tests/ → tests del servicio de inventario.

La estructura con varios servicios mantiene la separación entre src/ y tests/ y añade la separación entre servicios. Cada servicio tiene su propio conjunto de proyectos y su propio conjunto de tests. Esta estructura permite compilar y desplegar un servicio de forma independiente aunque todos los servicios vivan en el mismo repositorio. La solución se convierte en el punto de entrada común para compilar y probar todos los servicios.


---

Bloque 10 — Aplicación de la organización al proyecto del curso

El proyecto del curso aplica las tres decisiones de organización de forma explícita. La estructura de repositorios es un monorepo con una carpeta por módulo y una carpeta por punto. La estructura de carpetas dentro de cada punto es src/, tests/ y docs/. Las convenciones de nombres de proyectos siguen el patrón AceriaApp.Componente.Tipo. Las convenciones de espacios de nombres coinciden con la estructura de carpetas. Las convenciones de commits siguen el patrón Punto N.M: descripción. Todas estas decisiones se documentan en un ADR y se verifican con una clase de validación de convenciones.

Aplicación al proyecto:

Monorepo                  → AceriaApp/ con módulos y puntos.
src/, tests/, docs/       → separación dentro de cada punto.
AceriaApp.Componente.Tipo → convención de nombres.
Namespace = carpeta       → convención de espacios de nombres.
Punto N.M: descripción    → convención de commits.

Línea 1: Monorepo → el proyecto usa un único repositorio.
Línea 2: src/, tests/, docs/ → separación de carpetas dentro de cada punto.
Línea 3: AceriaApp.Componente.Tipo → convención de nombres de proyectos.
Línea 4: Namespace = carpeta → convención de espacios de nombres.
Línea 5: Punto N.M: descripción → convención de mensajes de commit.

La aplicación de estas convenciones prepara el proyecto para la extracción de microservicios en módulos posteriores. Cuando un módulo se extraiga como servicio, mantendrá la misma estructura de carpetas y las mismas convenciones de nombres. La coherencia entre el monolito modular y los microservicios facilita la transición y reduce el coste de la migración. El punto 1.4 cierra el bloque de fundamentos del módulo 1 y prepara el terreno para el punto 1.5, donde se estudiarán las buenas prácticas de desarrollo de microservicios.


---

Resumen rápido de la teoría

· La organización de una solución se materializa en tres decisiones: estructura de repositorios, estructura de carpetas y convenciones de nombres.
· El monorepo facilita la búsqueda global y la coherencia de convenciones; el polyrepo facilita la autonomía total de cada equipo.
· La separación en src/, tests/ y docs/ es una convención ampliamente adoptada en el ecosistema .NET.
· Las convenciones de nombres de proyectos siguen el patrón Empresa.Producto.Componente.Tipo.
· Los espacios de nombres coinciden con la estructura de carpetas del proyecto.
· Las convenciones de commits siguen el patrón Punto N.M: descripción y permiten comparar el estado del proyecto entre puntos consecutivos.


---


Punto 1.5 — Buenas prácticas

Módulo 1: Introducción a los microservicios
Duración: 53 minutos (26 minutos de teoría + 27 minutos de práctica)
Objetivos de aprendizaje:

· Identificar las buenas prácticas aplicables al desarrollo de microservicios.
· Comprender la idempotencia como requisito de las operaciones expuestas.
· Comprender el versionado de contratos públicos y su relación con la evolución independiente.
· Comprender la gestión explícita de errores mediante códigos de respuesta y problem details.
· Añadir al proyecto AceriaApp un documento de buenas prácticas, una clase de validación de buenas prácticas y un cierre del módulo 1 con el resumen del estado del proyecto.


---

PARTE TEÓRICA (26 minutos)

Bloque 1 — Buenas prácticas como marco de calidad

Las buenas prácticas son reglas de actuación que se aplican de forma sistemática en el desarrollo de un sistema. No son principios de diseño, que definen la estructura, ni patrones, que resuelven problemas recurrentes. Son hábitos de trabajo que reducen el coste de mantenimiento y aumentan la previsibilidad del resultado. En microservicios, las buenas prácticas se organizan en cuatro categorías: prácticas de contrato, prácticas de operación, prácticas de comunicación y prácticas de evolución. Cada categoría responde a un riesgo concreto del desarrollo distribuido. La aplicación sistemática de las cuatro categorías reduce los fallos más comunes en producción.

Categorías de buenas prácticas:

1. Contrato     → qué se expone y cómo.
2. Operación    → cómo se ejecuta y se recupera.
3. Comunicación → cómo se habla con otros servicios.
4. Evolución    → cómo se cambia sin romper.

Línea 1: 1. Contrato → primera categoría, define el contrato público del servicio.
Línea 2: 2. Operación → segunda categoría, define cómo se ejecuta y se recupera.
Línea 3: 3. Comunicación → tercera categoría, define cómo se habla con otros.
Línea 4: 4. Evolución → cuarta categoría, define cómo se cambia sin romper.

La primera categoría, contrato, agrupa las prácticas relacionadas con lo que el servicio expone. La segunda, operación, agrupa las prácticas relacionadas con la ejecución. La tercera, comunicación, agrupa las prácticas relacionadas con las llamadas a otros servicios. La cuarta, evolución, agrupa las prácticas relacionadas con el cambio. Las cuatro categorías se aplican de forma conjunta: un servicio con buen contrato pero mala operación falla en producción. Un servicio con buena operación pero mal contrato rompe a los consumidores. La aplicación conjunta es lo que produce un servicio de calidad.

La ausencia de buenas prácticas produce cuatro síntomas reconocibles. El primero es el contrato inestable, que cambia sin versionado y rompe a los consumidores. El segundo es la operación frágil, que no tolera fallos ni recupera el estado. El tercero es la comunicación caótica, sin timeouts ni reintentos controlados. El cuarto es la evolución bloqueada, donde ningún servicio puede cambiar sin coordinación global. Los cuatro síntomas se corrigen aplicando las buenas prácticas de contrato, operación, comunicación y evolución respectivamente. El curso aplica estas buenas prácticas al dominio de la acería de forma explícita y trazable.


---

Bloque 2 — Buena práctica de contrato: exposición de DTOs

La primera buena práctica de contrato es exponer DTOs específicos en lugar de entidades de dominio. Una entidad de dominio contiene la lógica y la estructura interna del servicio. Exponerla equivale a publicar la implementación interna como contrato público. Cualquier cambio en la entidad rompe a los consumidores. Un DTO, en cambio, es una proyección estable diseñada específicamente para el consumo externo. No contiene lógica ni referencias internas. Su única función es transportar datos. La separación entre entidad y DTO es la garantía de que el contrato público se mantiene estable aunque la implementación evolucione.

// Entidad de dominio: no se expone.
public class Orden
{
    public Guid Id { get; set; }
    public string Cliente { get; set; } = string.Empty;
    public string Material { get; set; } = string.Empty;
    public int Cantidad { get; set; }
    public DateTime FechaCreacion { get; set; }
    public EstadoOrden Estado { get; set; }
}

// DTO público: se expone.
public record OrdenDto(
    Guid Id,
    string Cliente,
    string Material,
    int Cantidad,
    DateTime FechaCreacion);

Línea 1: // Entidad de dominio: no se expone. → comentario que indica que la entidad no se expone.
Línea 2: public class Orden → entidad de dominio.
Línea 3: { → abre el cuerpo de la clase.
Línea 4: public Guid Id { get; set; } → identificador de la orden.
Línea 5: public string Cliente { get; set; } = string.Empty; → nombre del cliente.
Línea 6: public string Material { get; set; } = string.Empty; → material solicitado.
Línea 7: public int Cantidad { get; set; } → cantidad solicitada.
Línea 8: public DateTime FechaCreacion { get; set; } → fecha de creación.
Línea 9: public EstadoOrden Estado { get; set; } → estado de la orden.
Línea 10: } → cierra el cuerpo de la clase.
Línea 11: // DTO público: se expone. → comentario que indica que el DTO se expone.
Línea 12: public record OrdenDto( → declara el contrato público inmutable.
Línea 13: Guid Id, → identificador de la orden.
Línea 14: string Cliente, → nombre del cliente.
Línea 15: string Material, → material solicitado.
Línea 16: int Cantidad, → cantidad solicitada.
Línea 17: DateTime FechaCreacion); → fecha de creación.

La diferencia entre la entidad y el DTO no es solo de forma: la entidad puede cambiar sin romper el contrato, mientras que el DTO es el contrato. Si mañana la entidad Orden añade un campo Prioridad, el DTO sigue igual y los consumidores no se ven afectados. Si el DTO necesita el campo Prioridad, se crea un DTO nuevo o se versiona el contrato. La separación entre entidad y DTO es una inversión inicial que se recupera en el primer cambio de la entidad.


---

Bloque 3 — Buena práctica de contrato: versionado en la URL

La segunda buena práctica de contrato es versionar el contrato público en la URL. El versionado permite que varias versiones del mismo contrato convivan durante un periodo de transición. Los consumidores migran a la nueva versión cuando pueden. El productor retira la versión antigua cuando ningún consumidor la usa. El versionado en la URL es más explícito y visible que el versionado por cabecera. La versión forma parte de la ruta y se identifica a simple vista. En el proyecto AceriaApp, los endpoints se versionan con el prefijo /api/v1/ para la primera versión estable.

Endpoints versionados:

GET  /api/v1/ordenes
GET  /api/v1/ordenes/{id}
POST /api/v1/ordenes
GET  /api/v2/ordenes   ← versión futura, convive con v1

Línea 1: GET /api/v1/ordenes → primera versión del endpoint de lista.
Línea 2: GET /api/v1/ordenes/{id} → primera versión del endpoint de detalle.
Línea 3: POST /api/v1/ordenes → primera versión del endpoint de creación.
Línea 4: GET /api/v2/ordenes → versión futura que convive con la v1.

El versionado en la URL tiene dos consecuencias prácticas. La primera es que el enrutamiento se resuelve con un prefijo explícito, sin lógica condicional. La segunda es que el consumidor declara explícitamente qué versión usa. La combinación de las dos consecuencias facilita la detección de consumidores obsoletos: el productor puede contar cuántas peticiones recibe cada versión y decidir cuándo retirar la antigua. El versionado en la URL es la práctica más adoptada en el ecosistema .NET y la que el curso aplica.


---

Bloque 4 — Buena práctica de operación: idempotencia

La primera buena práctica de operación es la idempotencia. Una operación es idempotente cuando ejecutarla varias veces produce el mismo resultado que ejecutarla una vez. La idempotencia es esencial en sistemas distribuidos porque las llamadas de red pueden duplicarse por reintentos. Sin idempotencia, un reintento puede crear dos órdenes en lugar de una. La idempotencia se implementa con un identificador de operación único que el servicio comprueba antes de ejecutar. Si el identificador ya existe, el servicio devuelve el resultado anterior sin ejecutar la operación de nuevo.

app.MapPost("/api/v1/ordenes", async (
    AceriaDbContext db,
    Orden orden,
    [FromHeader(Name = "Idempotency-Key")] string? idempotencyKey) =>
{
    if (!string.IsNullOrWhiteSpace(idempotencyKey))
    {
        var existente = await db.Ordenes
            .FirstOrDefaultAsync(o => o.IdempotencyKey == idempotencyKey);
        if (existente is not null)
        {
            return Results.Ok(existente);
        }
    }

    orden.Id = Guid.NewGuid();
    orden.IdempotencyKey = idempotencyKey;
    orden.FechaCreacion = DateTime.UtcNow;
    db.Ordenes.Add(orden);
    await db.SaveChangesAsync();
    return Results.Created($"/api/v1/ordenes/{orden.Id}", orden);
});

Línea 1: app.MapPost("/api/v1/ordenes", async ( → declara el endpoint POST.
Línea 2: AceriaDbContext db, → inyecta el contexto de base de datos.
Línea 3: Orden orden, → recibe la orden del cuerpo.
Línea 4: [FromHeader(Name = "Idempotency-Key")] string? idempotencyKey) => → lee la cabecera de idempotencia.
Línea 5: { → abre el cuerpo del lambda.
Línea 6: if (!string.IsNullOrWhiteSpace(idempotencyKey)) → comprueba si hay clave.
Línea 7: { → abre el bloque de comprobación.
Línea 8: var existente = await db.Ordenes → consulta la orden existente.
Línea 9: .FirstOrDefaultAsync(o => o.IdempotencyKey == idempotencyKey); → filtra por clave.
Línea 10: if (existente is not null) → si ya existe.
Línea 11: { → abre el bloque de retorno.
Línea 12: return Results.Ok(existente); → devuelve la orden existente con 200.
Línea 13: } → cierra el bloque de retorno.
Línea 14: } → cierra el bloque de comprobación.
Línea 15: orden.Id = Guid.NewGuid(); → asigna un identificador nuevo.
Línea 16: orden.IdempotencyKey = idempotencyKey; → guarda la clave de idempotencia.
Línea 17: orden.FechaCreacion = DateTime.UtcNow; → asigna la fecha de creación.
Línea 18: db.Ordenes.Add(orden); → añade la orden al contexto.
Línea 19: await db.SaveChangesAsync(); → persiste los cambios.
Línea 20: return Results.Created($"/api/v1/ordenes/{orden.Id}", orden); → devuelve 201 con la ubicación.
Línea 21: }); → cierra el lambda.

La idempotencia no se aplica a todas las operaciones: solo a las que crean o modifican estado. Las operaciones de lectura son idempotentes por definición. Las operaciones de borrado pueden ser idempotentes si el resultado es el mismo cuando el recurso ya no existe. La idempotencia de las operaciones de creación es la más crítica porque un duplicado produce un recurso duplicado. La clave de idempotencia se genera en el cliente y se envía en la cabecera. El servidor la comprueba y decide si ejecuta o devuelve el resultado anterior.


---

Bloque 5 — Buena práctica de operación: gestión explícita de errores

La segunda buena práctica de operación es la gestión explícita de errores mediante códigos de respuesta HTTP y problem details. La gestión implícita devuelve siempre 200 o 500 sin información útil. La gestión explícita devuelve el código adecuado a cada situación: 400 para errores de validación, 404 para recursos no encontrados, 409 para conflictos, 422 para entidades no procesables, 500 para errores internos. El cuerpo del error sigue el formato problem details definido en la RFC 7807. Este formato incluye el tipo del error, el título, el código de estado y el detalle. La adopción del formato facilita el consumo uniforme por parte de los clientes.

app.MapPost("/api/v1/ordenes", async (AceriaDbContext db, Orden orden) =>
{
    if (string.IsNullOrWhiteSpace(orden.Cliente))
    {
        return Results.Problem(
            title: "Cliente requerido",
            detail: "El campo Cliente no puede estar vacío.",
            statusCode: StatusCodes.Status400BadRequest);
    }

    orden.Id = Guid.NewGuid();
    orden.FechaCreacion = DateTime.UtcNow;
    db.Ordenes.Add(orden);
    await db.SaveChangesAsync();
    return Results.Created($"/api/v1/ordenes/{orden.Id}", orden);
});

Línea 1: app.MapPost("/api/v1/ordenes", async (AceriaDbContext db, Orden orden) => → declara el endpoint POST.
Línea 2: { → abre el cuerpo del lambda.
Línea 3: if (string.IsNullOrWhiteSpace(orden.Cliente)) → valida el campo Cliente.
Línea 4: { → abre el bloque de error.
Línea 5: return Results.Problem( → devuelve un problem details.
Línea 6: title: "Cliente requerido", → título del error.
Línea 7: detail: "El campo Cliente no puede estar vacío.", → detalle del error.
Línea 8: statusCode: StatusCodes.Status400BadRequest); → código 400.
Línea 9: } → cierra el bloque de error.
Línea 10: orden.Id = Guid.NewGuid(); → asigna el identificador.
Línea 11: orden.FechaCreacion = DateTime.UtcNow; → asigna la fecha.
Línea 12: db.Ordenes.Add(orden); → añade al contexto.
Línea 13: await db.SaveChangesAsync(); → persiste.
Línea 14: return Results.Created($"/api/v1/ordenes/{orden.Id}", orden); → devuelve 201.
Línea 15: }); → cierra el lambda.

La gestión explícita de errores tiene dos consecuencias prácticas. La primera es que el cliente sabe exactamente qué ha fallado. La segunda es que el soporte puede reproducir el error con el código y el detalle. La adopción del formato problem details evita la duplicación de estructuras de error y facilita la integración con herramientas de monitorización. El curso aplica este formato en todos los endpoints que devuelven errores.


---

Bloque 6 — Buena práctica de comunicación: timeouts y reintentos

La primera buena práctica de comunicación es configurar timeouts y reintentos controlados en todas las llamadas a otros servicios. Un timeout evita que una llamada bloquee el servicio indefinidamente. Un reintento recupera errores transitorios. La combinación de ambos reduce la tasa de fallo observada sin añadir complejidad al código. Los timeouts se configuran con valores inferiores al tiempo máximo que el cliente está dispuesto a esperar. Los reintentos se configuran con retroceso exponencial para no saturar al servicio destino. La política se aplica de forma uniforme a todas las llamadas externas.

var policy = Policy
    .Handle<HttpRequestException>()
    .WaitAndRetryAsync(
        retryCount: 3,
        sleepDurationProvider: attempt => TimeSpan.FromMilliseconds(200 * Math.Pow(2, attempt)),
        onRetry: (exception, delay, attempt, _) =>
        {
            Console.WriteLine($"Reintento {attempt} tras {delay.TotalMilliseconds} ms");
        });

var httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(5) };
var response = await policy.ExecuteAsync(() =>
    httpClient.GetAsync("http://acería-inventario/api/v1/materiales"));

Línea 1: var policy = Policy → comienza la definición de la política.
Línea 2: .Handle<HttpRequestException>() → se activa ante errores HTTP.
Línea 3: .WaitAndRetryAsync( → configura reintentos con espera.
Línea 4: retryCount: 3, → hasta tres reintentos.
Línea 5: sleepDurationProvider: attempt => TimeSpan.FromMilliseconds(200 * Math.Pow(2, attempt)), → retroceso exponencial.
Línea 6: onRetry: (exception, delay, attempt, _) => → acción en cada reintento.
Línea 7: { → abre el bloque de la acción.
Línea 8: Console.WriteLine($"Reintento {attempt} tras {delay.TotalMilliseconds} ms"); → registra el reintento.
Línea 9: }); → cierra la política.
Línea 10: var httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(5) }; → crea el cliente con timeout.
Línea 11: var response = await policy.ExecuteAsync(() => → ejecuta bajo la política.
Línea 12: httpClient.GetAsync("http://acería-inventario/api/v1/materiales")); → llamada al servicio de inventario.

La configuración de timeouts y reintentos no es opcional en sistemas distribuidos. La latencia de red es variable y los errores transitorios son frecuentes. Un servicio sin timeouts puede bloquearse indefinidamente. Un servicio sin reintentos propaga errores transitorios como fallos definitivos. La combinación de ambos reduce la tasa de fallo observada sin añadir complejidad al código. La política se aplica en un solo lugar y se reutiliza en todas las llamadas externas del servicio.


---

Bloque 7 — Buena práctica de comunicación: circuit breaker

La segunda buena práctica de comunicación es el circuit breaker. Un circuit breaker es un mecanismo que abre el circuito cuando el servicio destino falla de forma repetida y lo cierra cuando se recupera. Mientras el circuito está abierto, las llamadas fallan inmediatamente sin intentar contactar con el destino. Esta falla rápida evita que el servicio origen se sature esperando respuestas que no van a llegar. El circuit breaker se configura con dos parámetros: el número de fallos que abren el circuito y el tiempo que permanece abierto. La combinación de ambos parámetros determina la sensibilidad del mecanismo.

var circuitBreaker = Policy
    .Handle<HttpRequestException>()
    .CircuitBreakerAsync(
        exceptionsAllowedBeforeBreaking: 3,
        durationOfBreak: TimeSpan.FromSeconds(30),
        onBreak: (exception, timespan) =>
        {
            Console.WriteLine($"Circuito abierto durante {timespan.TotalSeconds} s");
        },
        onReset: () =>
        {
            Console.WriteLine("Circuito cerrado de nuevo");
        });

Línea 1: var circuitBreaker = Policy → comienza la definición de la política.
Línea 2: .Handle<HttpRequestException>() → se activa ante errores HTTP.
Línea 3: .CircuitBreakerAsync( → configura el circuit breaker.
Línea 4: exceptionsAllowedBeforeBreaking: 3, → tres errores antes de abrir.
Línea 5: durationOfBreak: TimeSpan.FromSeconds(30), → permanece abierto 30 segundos.
Línea 6: onBreak: (exception, timespan) => → acción al abrir el circuito.
Línea 7: { → abre el bloque de la acción.
Línea 8: Console.WriteLine($"Circuito abierto durante {timespan.TotalSeconds} s"); → registra la apertura.
Línea 9: }, → cierra el bloque.
Línea 10: onReset: () => → acción al cerrar el circuito.
Línea 11: { → abre el bloque de la acción.
Línea 12: Console.WriteLine("Circuito cerrado de nuevo"); → registra el cierre.
Línea 13: }); → cierra la política.

El circuit breaker se combina con el reintento y con el timeout para formar una política completa de resiliencia. El reintento recupera errores transitorios. El timeout evita bloqueos indefinidos. El circuit breaker evita la saturación cuando el destino falla de forma sostenida. Las tres políticas se aplican en capas: primero el timeout, después el reintento, después el circuit breaker. El orden de aplicación determina el comportamiento observado. El curso introduce el circuit breaker en el módulo 7 con detalle; en el módulo 1 se presenta como buena práctica.


---

Bloque 8 — Buena práctica de evolución: contratos compatibles

La primera buena práctica de evolución es mantener la compatibilidad de los contratos públicos. Un contrato es compatible hacia atrás cuando los consumidores antiguos siguen funcionando con la nueva versión del productor. La compatibilidad se mantiene añadiendo campos opcionales en lugar de obligatorios, evitando eliminar campos existentes y evitando cambiar el tipo de los campos. Un cambio incompatible requiere una nueva versión del contrato. La compatibilidad hacia atrás es la garantía de que el productor puede evolucionar sin romper a los consumidores.

Cambios compatibles:

+ Añadir campo opcional al DTO.
+ Añadir nuevo endpoint.
+ Añadir nuevo valor a un enum existente.

Cambios incompatibles:

- Eliminar campo del DTO.
- Cambiar tipo de campo del DTO.
- Cambiar el significado de un campo existente.
- Eliminar un endpoint.

Línea 1: + Añadir campo opcional al DTO. → cambio compatible.
Línea 2: + Añadir nuevo endpoint. → cambio compatible.
Línea 3: + Añadir nuevo valor a un enum existente. → cambio compatible.
Línea 4: - Eliminar campo del DTO. → cambio incompatible.
Línea 5: - Cambiar tipo de campo del DTO. → cambio incompatible.
Línea 6: - Cambiar el significado de un campo existente. → cambio incompatible.
Línea 7: - Eliminar un endpoint. → cambio incompatible.

La compatibilidad de contratos se verifica con tests que consumen la versión antigua y comprueban que siguen funcionando. Estos tests se ejecutan en el pipeline antes de publicar una nueva versión. Si un test falla, el cambio es incompatible y requiere una nueva versión del contrato. La verificación automática evita que un cambio incompatible llegue a producción. El curso introduce los tests de compatibilidad en el módulo 2 con detalle; en el módulo 1 se presenta como buena práctica.


---

Bloque 9 — Buena práctica de evolución: documentación viva

La segunda buena práctica de evolución es mantener la documentación viva. La documentación viva se genera a partir del código y se actualiza automáticamente. OpenAPI es el estándar para documentar APIs REST. La documentación se publica junto con el servicio y se mantiene sincronizada con el código. Los consumidores consultan la documentación para conocer los contratos y los endpoints disponibles. La documentación viva evita la documentación obsoleta que describe APIs que ya no existen.

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "AceriaApp.Ordenes.Api",
        Version = "v1",
        Description = "API de gestión de órdenes de producción."
    });
});

app.UseSwagger();
app.UseSwaggerUI(options =>
{
    options.SwaggerEndpoint("/swagger/v1/swagger.json", "AceriaApp.Ordenes.Api v1");
});

Línea 1: builder.Services.AddEndpointsApiExplorer(); → habilita la exploración de endpoints.
Línea 2: builder.Services.AddSwaggerGen(options => → registra el generador de Swagger.
Línea 3: { → abre el bloque de configuración.
Línea 4: options.SwaggerDoc("v1", new OpenApiInfo → declara el documento de la versión 1.
Línea 5: { → abre el bloque de información.
Línea 6: Title = "AceriaApp.Ordenes.Api", → título de la API.
Línea 7: Version = "v1", → versión del contrato.
Línea 8: Description = "API de gestión de órdenes de producción." → descripción.
Línea 9: }); → cierra el bloque.
Línea 10: }); → cierra la configuración.
Línea 11: app.UseSwagger(); → habilita el endpoint de Swagger.
Línea 12: app.UseSwaggerUI(options => → habilita la interfaz gráfica.
Línea 13: { → abre el bloque de configuración.
Línea 14: options.SwaggerEndpoint("/swagger/v1/swagger.json", "AceriaApp.Ordenes.Api v1"); → declara el endpoint del JSON.
Línea 15: }); → cierra el bloque.

La documentación viva tiene dos consecuencias prácticas. La primera es que el contrato público está siempre actualizado porque se genera a partir del código. La segunda es que los consumidores pueden probar los endpoints directamente desde la interfaz gráfica. La combinación de ambas reduce el tiempo de integración entre servicios. La documentación se versiona con el código y se publica con el servicio. El curso usa OpenAPI con Swagger en todos los servicios.


---

Bloque 10 — Aplicación de las buenas prácticas al proyecto del curso

El proyecto del curso aplica las buenas prácticas de forma explícita en cada punto. La exposición de DTOs se aplica creando contratos separados de las entidades. El versionado en la URL se aplica con el prefijo /api/v1/. La idempotencia se aplica con la cabecera Idempotency-Key. La gestión explícita de errores se aplica con problem details. Los timeouts y reintentos se aplican con Polly. El circuit breaker se aplica con Polly. La compatibilidad de contratos se verifica con tests. La documentación viva se aplica con OpenAPI.

Aplicación al proyecto del curso:

DTOs separados          → OrdenDto en lugar de Orden.
Versionado en URL       → /api/v1/ordenes.
Idempotencia            → cabecera Idempotency-Key.
Errores explícitos      → problem details.
Timeouts y reintentos   → Polly.
Circuit breaker         → Polly.
Contratos compatibles   → tests de compatibilidad.
Documentación viva      → OpenAPI.

Línea 1: DTOs separados → contratos separados de las entidades.
Línea 2: Versionado en URL → prefijo /api/v1/.
Línea 3: Idempotencia → cabecera Idempotency-Key.
Línea 4: Errores explícitos → problem details.
Línea 5: Timeouts y reintentos → Polly.
Línea 6: Circuit breaker → Polly.
Línea 7: Contratos compatibles → tests de compatibilidad.
Línea 8: Documentación viva → OpenAPI.

La aplicación de las buenas prácticas prepara el proyecto para la evolución hacia microservicios. Cuando un módulo se extraiga como servicio, mantendrá las mismas buenas prácticas. La coherencia entre el monolito modular y los microservicios facilita la transición. El punto 1.5 cierra el módulo 1 y prepara el terreno para el módulo 2, donde se estudiará el desarrollo de APIs REST con ASP.NET Core.


---

Resumen rápido de la teoría

· Las buenas prácticas se organizan en cuatro categorías: contrato, operación, comunicación y evolución.
· La exposición de DTOs separa el contrato público de la entidad de dominio.
· El versionado en la URL permite que varias versiones del contrato convivan durante la transición.
· La idempotencia evita duplicados cuando las llamadas se reintentan.
· La gestión explícita de errores usa códigos HTTP y problem details.
· Los timeouts, reintentos y circuit breaker protegen al servicio de fallos en las dependencias.
· La compatibilidad de contratos y la documentación viva permiten la evolución sin romper a los consumidores.


---
