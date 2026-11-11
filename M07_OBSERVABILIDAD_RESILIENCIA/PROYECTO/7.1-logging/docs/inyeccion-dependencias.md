# Inyección de dependencias — Punto 4.5

## Principio de inversión de dependencias

Los módulos de alto nivel y de bajo nivel dependen de abstracciones. Las abstracciones no dependen de los detalles.

## Inyección de dependencias

Un objeto no crea sus dependencias: las recibe desde el exterior, normalmente por constructor.

## Contenedor de ASP.NET Core

Registra y resuelve las dependencias. Gestiona el ciclo de vida de las instancias.

## Ciclos de vida

- Transient: nueva instancia en cada resolución.
- Scoped: una instancia por ámbito de petición.
- Singleton: una instancia por aplicación.

## Registro por convención

Agrupar registros por capa es una convención de organización. `AddPatronesOrdenes` contiene registros explícitos de cada puerto, adaptador y caso de uso; no adivina implementaciones por su nombre.

## Registro por ensamblado

`RegisterServicesFromAssemblyContaining<CrearOrdenCommand>()` descubre los manejadores de MediatR por los contratos que implementan en ese ensamblado. Los demás servicios se registran explícitamente; no se utiliza el nombre del tipo como regla de descubrimiento.

## Reglas de registro

1. En este flujo se elige una implementación por puerto; el contenedor permite varias cuando se solicita una colección de servicios.
2. Ciclo adecuado al estado.
3. Inyección por constructor.
4. Sin resolución manual.
5. Sin capturar el contenedor.

## Prohibiciones

1. No convertir los casos de uso en Service Locator; la raíz de composición y los tests sí pueden resolver servicios para construir o verificar el flujo.
2. No capturar el contenedor.
3. No registrar en tiempo de ejecución.
4. No depender de ciclos más cortos.

## Inyección de dependencias y tests

Las dependencias se sustituyen por dobles en los tests.

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Registro de puertos | Interfaces con adaptadores |
| Ciclo de vida | Scoped para la mayoría |
| Configuración | Métodos de extensión |
| Prohibiciones | Respetadas |
| Validación | Test de coherencia |

## Cierre del módulo 4

El proyecto AceriaApp dispone de:

- Patrón Repository con repositorios específicos.
- Patrón Unit of Work con coordinación de repositorios.
- Patrón Mediator con MediatR.
- Patrón Result para errores esperados.
- Inyección de dependencias con métodos de extensión.
- 118 pruebas acumuladas en 10 proyectos de tests.
- Dieciocho puntos completados (1.1 a 1.5, 2.1 a 2.4, 3.1 a 3.4 y 4.1 a 4.5).

## Correspondencia con el código ejecutable

El catálogo de este punto describe reglas de diseño y contiene ejemplos de contratos. Sus nombres no implican servicios registrados. La implementación utiliza los proyectos `AceriaApp.Hexagonal.Aplicacion`, `AceriaApp.Hexagonal.Dominio` y `AceriaApp.Hexagonal.Infraestructura`, compuestos desde `AceriaApp.Api`. Comprueba los archivos y los tests funcionales que incorpora el paso de compilación de este punto.
