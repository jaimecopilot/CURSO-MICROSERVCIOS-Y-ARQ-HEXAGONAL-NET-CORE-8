# Validación de los puntos del módulo 3

He revisado los cuatro puntos del módulo 3 (3.1, 3.2, 3.3, 3.4) contra las reglas fijadas. Este es el resultado.

## Lo que está correcto en los cuatro puntos

| Regla | 3.1 | 3.2 | 3.3 | 3.4 |
|-------|-----|-----|-----|-----|
| 10 bloques × 3 párrafos = 30 párrafos | Sí | Sí | Sí | Sí |
| Párrafos de 150-180 palabras | Sí | Sí | Sí | Sí |
| Tono expositivo, sin preguntas | Sí | Sí | Sí | Sí |
| Sin analogías | Sí | Sí | Sí | Sí |
| 24 pasos numerados | Sí | Sí | Sí | Sí |
| Acción 1, Acción 2, Acción 3... en negrita | Sí | Sí | Sí | Sí |
| Verbos concretos al inicio | Sí | Sí | Sí | Sí |
| Ubicación exacta, elemento, valor | Sí | Sí | Sí | Sí |
| Por qué se hace / Errores comunes / Verificación | Sí | Sí | Sí | Sí |
| Entre 3 y 8 acciones por paso | Sí | Sí | Sí | Sí |
| Explicación línea por línea del código | Sí | Sí | Sí | Sí |
| Tabla de errores del ejercicio | Sí | Sí | Sí | Sí |
| Reto resuelto paso a paso | Sí | Sí | Sí | Sí |
| Resultado esperado | Sí | Sí | Sí | Sí |
| Conclusión y enlace | Sí | Sí | Sí | Sí |
| Estructura del módulo/punto | Sí | Sí | Sí | Sí |
| Sin labs, metaprompt, verificacion, Claude | Sí | Sí | Sí | Sí |
| Stack fijo (.NET 8, EF Core 8.0.0, SQL Server Express) | Sí | Sí | Sí | Sí |
| Prácticas crecientes (no modificar anteriores) | Sí | Sí | Sí | Sí |
| Un commit por punto | Sí | Sí | Sí | Sí |

## Recuento de tests verificados

| Punto | Tests nuevos | Acumulado declarado | Acumulado real |
|-------|--------------|---------------------|----------------|
| 3.1 | 7 | 58 | 58 |
| 3.2 | 8 | 66 | 66 |
| 3.3 | 7 | 73 | 73 |
| 3.4 | 8 | 81 | 81 |

Recuento real acumulado:
- Módulo 1: 1 + 8 + 4 + 5 + 5 = 23 tests.
- Módulo 2: 8 + 5 + 6 + 9 = 28 tests.
- Módulo 3: 7 + 8 + 7 + 8 = 30 tests.
- Total: 23 + 28 + 30 = 81 tests.

Los recuentos declarados en cada punto coinciden con el acumulado real. **Correcto.**

## Errores y problemas detectados

### 1. Punto 3.4: recuento de proyectos en el README

El README del punto 3.4 dice: "Solución `AceriaApp.sln` con quince proyectos". Recuento real:
- Punto 3.3 termina con 14 proyectos (heredados de 3.2: 12 + `AceriaApp.Capas.Tests` + `AceriaApp.PuertosAdaptadores.Tests` + `AceriaApp.SeparacionCapas.Tests` = 14).

Espera, revisemos con cuidado. Al abrir la solución del punto 3.4:
- Del punto 3.3 hereda: `AceriaApp.Monolito.Api`, `AceriaApp.Monolito.Tests`, `AceriaApp.Metricas.Tests`, `AceriaApp.Diseno.Tests`, `AceriaApp.Organizacion.Tests`, `AceriaApp.BuenasPracticas.Tests`, `AceriaApp.DisenoRest.Tests`, `AceriaApp.CatalogoRecursos.Tests`, `AceriaApp.Validacion.Tests`, `AceriaApp.Documentacion.Tests`, `AceriaApp.Capas.Tests`, `AceriaApp.PuertosAdaptadores.Tests`, `AceriaApp.SeparacionCapas.Tests` = **13 proyectos**.

El punto 3.4 añade `AceriaApp.Implementacion.Tests` = **14 proyectos** al terminar.

El README dice "quince proyectos". **Incorrecto**. Debería decir catorce.

### 2. Punto 3.4: paso 2 del ejercicio menciona trece proyectos heredados

El paso 2 del punto 3.4 verifica "los trece proyectos heredados del punto 3.3". Recuento real al abrir la solución del punto 3.4: **13 proyectos** (12 del punto 3.2 + `AceriaApp.SeparacionCapas.Tests` creado en el punto 3.3). El paso 2 es **correcto**.

Pero el paso 19 (README) y la sección "Resultado esperado" dicen "quince proyectos" en el README y "quince" en la conclusión. Inconsistencia.

### 3. Punto 3.4: el documento `implementacion-aspnet-core.md` dice "Setenta y cuatro pruebas"

El documento `docs/implementacion-aspnet-core.md` del punto 3.4 dice: "Setenta y cuatro pruebas unitarias acumuladas en catorce proyectos de tests."

Recuento real:
- Acumulado hasta 3.3: 73 tests.
- Punto 3.4: 8 tests nuevos.
- Total: **81 tests**.

El documento dice "Setenta y cuatro pruebas" cuando deberían ser 81. **Incorrecto.** Y dice "catorce proyectos de tests" cuando el recuento real es **catorce proyectos totales** (no catorce proyectos de tests). Doble error.

### 4. Punto 3.4: la sección "Cierre del módulo 3" del documento

El documento dice:
```text
- Setenta y cuatro pruebas unitarias acumuladas en catorce proyectos de tests.
- Doce puntos completados (1.1 a 1.5, 2.1 a 2.4 y 3.1 a 3.4).
```

Los puntos completados son **13**: 5 del módulo 1 + 4 del módulo 2 + 4 del módulo 3 = 13. El documento dice "Doce". **Incorrecto.**

Y "setenta y cuatro pruebas" debería ser 81. **Incorrecto.**

### 5. Punto 3.4: la tabla de errores del ejercicio menciona un error incorrecto

La tabla de errores del ejercicio incluye: "El validador no detecta adaptadores Transient". El validador sí detecta adaptadores Transient porque tiene la comprobación `registro.EsAdaptadorDeSalida && registro.Ciclo == "Transient"`. La redacción del error es correcta como error común del alumno (por si olvida la comprobación), pero el mensaje podría ser más claro.

**Gravedad:** baja.

### 6. Punto 3.3: recuento de proyectos en el README

El README del punto 3.3 dice "Solución `AceriaApp.sln` con catorce proyectos". Recuento real:
- Punto 3.2 termina con 13 proyectos.
- Punto 3.3 añade `AceriaApp.SeparacionCapas.Tests` = 14 proyectos.

El README dice "catorce proyectos". **Correcto.**

### 7. Punto 3.2: recuento de proyectos en el README

El README del punto 3.2 dice "Solución `AceriaApp.sln` con trece proyectos". Recuento real:
- Punto 3.1 termina con 12 proyectos.
- Punto 3.2 añade `AceriaApp.PuertosAdaptadores.Tests` = 13 proyectos.

El README dice "trece proyectos". **Correcto.**

### 8. Punto 3.1: recuento de proyectos en el README

El README del punto 3.1 dice "Solución `AceriaApp.sln` con doce proyectos". Recuento real:
- Punto 2.4 termina con 11 proyectos.
- Punto 3.1 añade `AceriaApp.Capas.Tests` = 12 proyectos.

El README dice "doce proyectos". **Correcto.**

### 9. Punto 3.4: paso 2 describe 13 proyectos heredados pero la lista no los enumera

El paso 2 del punto 3.4 enumera 13 proyectos en la lista. Recuento de la lista:
1. `AceriaApp.Monolito.Api`
2. `AceriaApp.Monolito.Tests`
3. `AceriaApp.Metricas.Tests`
4. `AceriaApp.Diseno.Tests`
5. `AceriaApp.Organizacion.Tests`
6. `AceriaApp.BuenasPracticas.Tests`
7. `AceriaApp.DisenoRest.Tests`
8. `AceriaApp.CatalogoRecursos.Tests`
9. `AceriaApp.Validacion.Tests`
10. `AceriaApp.Documentacion.Tests`
11. `AceriaApp.Capas.Tests`
12. `AceriaApp.PuertosAdaptadores.Tests`
13. `AceriaApp.SeparacionCapas.Tests`

El paso 2 enumera correctamente los 13 proyectos heredados. **Correcto.**

### 10. Punto 3.4: falta verificación de recuento acumulado en paso 18

El paso 18 del punto 3.4 dice `Passed: 81`. Recuento real: 73 (acumulado hasta 3.3) + 8 (punto 3.4) = **81**. **Correcto.**

## Resumen de errores reales

| # | Error | Punto | Gravedad | Corrección |
|---|-------|-------|----------|------------|
| 1 | README dice "quince proyectos" cuando son 14 | 3.4 | Media | Cambiar a "catorce proyectos" |
| 2 | Documento dice "Setenta y cuatro pruebas" cuando son 81 | 3.4 | Media | Cambiar a "Ochenta y una pruebas" |
| 3 | Documento dice "catorce proyectos de tests" cuando son 14 proyectos totales | 3.4 | Media | Cambiar a "catorce proyectos" |
| 4 | Documento dice "Doce puntos completados" cuando son 13 | 3.4 | Media | Cambiar a "Trece puntos completados" |
| 5 | Resultado esperado y conclusión dicen "quince proyectos" | 3.4 | Media | Cambiar a "catorce proyectos" |
| 6 | Tabla de errores del ejercicio: redacción mejorable | 3.4 | Baja | Aceptar |
| 7 | Recuentos de puntos 3.1, 3.2, 3.3 verificados | — | — | Sin corrección |
| 8 | Recuento de tests verificados | — | — | Sin corrección |

## Propuesta de corrección

Los errores 1, 2, 3, 4 y 5 se corrigen con sustituciones de texto puntuales en el punto 3.4:

- README: "quince proyectos" → "catorce proyectos".
- Documento `implementacion-aspnet-core.md`: "Setenta y cuatro pruebas unitarias acumuladas en catorce proyectos de tests" → "Ochenta y una pruebas unitarias acumuladas en catorce proyectos".
- Documento `implementacion-aspnet-core.md`: "Doce puntos completados" → "Trece puntos completados".
- Resultado esperado del punto 3.4: "quince proyectos" → "catorce proyectos".
- Conclusión del punto 3.4: "quince proyectos" → "catorce proyectos".

Ninguna corrección requiere reescribir el punto. Son cinco sustituciones puntuales.

¿Aplico estas correcciones antes de continuar con el módulo 4?

