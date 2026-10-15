# Organización de la solución — Punto 1.4

## Tres decisiones de organización

1. Estructura de repositorios.
2. Estructura de carpetas.
3. Convenciones de nombres.

## Estructura de repositorios

Monorepo con una carpeta por módulo y una carpeta por punto.

## Estructura de carpetas

Cada punto contiene `src/`, `tests/` y `docs/`.

## Convenciones de nombres de proyectos

Patrón: `AceriaApp.Componente.Tipo`.

Tipos: `Api`, `Domain`, `Infrastructure`, `Application`, `Tests`.

## Convenciones de espacios de nombres

El espacio de nombres coincide con la estructura de carpetas del proyecto.

## Convenciones de commits

Patrón: `Punto N.M: descripción`.

## Convenciones de ramas

Prefijos: `feature/`, `fix/`, `docs/`, `refactor/`.

## Estructura con varios servicios

Cada servicio tiene su propio conjunto de proyectos y su propio conjunto de tests.

## Aplicación al proyecto del curso

| Decisión | Aplicación |
|----------|------------|
| Monorepo | `AceriaApp/` con módulos y puntos |
| Carpetas | `src/`, `tests/`, `docs/` |
| Nombres | `AceriaApp.Componente.Tipo` |
| Namespaces | Coinciden con la carpeta |
| Commits | `Punto N.M: descripción` |
