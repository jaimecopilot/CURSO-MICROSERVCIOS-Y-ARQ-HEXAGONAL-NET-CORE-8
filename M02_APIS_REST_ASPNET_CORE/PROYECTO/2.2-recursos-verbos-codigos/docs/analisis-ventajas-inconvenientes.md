# Análisis de ventajas e inconvenientes — Punto 1.2

## Marco de análisis

Cuatro dimensiones: despliegue, escalado, organización y consistencia.
Consideración transversal: coste operativo total.

## Ventajas del monolito

### Despliegue
- Pipeline único.
- Despliegue atómico.
- Reversión atómica.

### Consistencia
- Transacciones ACID sobre una única base de datos.
- Integridad referencial declarativa.
- Consultas con JOIN sin llamadas de red.

### Escalado
- Réplica del artefacto completo.
- Configuración idéntica para todas las réplicas.

### Organización
- Un único repositorio.
- Un único equipo responsable.
- Decisiones técnicas en una sola conversación.

## Inconvenientes del monolito

- Acoplamiento del ciclo de vida.
- Escalado homogéneo.
- Barrera tecnológica.
- Coordinación de equipos creciente.
- Adopción de nuevas tecnologías bloqueada por el conjunto.
- Cuello de botella organizativo a partir de cierto tamaño.

## Ventajas de los microservicios

### Despliegue
- Pipeline independiente por servicio.
- Frecuencia de despliegue ajustada a cada servicio.
- Riesgo y reversión limitados al servicio afectado.

### Escalado
- Selectividad: cada servicio se replica según su carga.
- Coste de infraestructura ajustado a la demanda real.

### Organización
- Autonomía de equipos.
- Decisiones técnicas distribuidas.
- Sin conflictos de fusión entre equipos.

## Inconvenientes de los microservicios

- Complejidad distribuida.
- Consistencia eventual.
- Observabilidad distribuida.
- Coste operativo por servicio.
- Duplicación de utilidades comunes.
- Gestión de versiones de contratos públicos.
- Latencia de red en cada llamada.

## Costes ocultos

### Monolito
- Coordinación de equipos.
- Oportunidad tecnológica.
- Escalado homogéneo.

### Microservicios
- Complejidad accidental.
- Observabilidad distribuida.
- Duplicación de utilidades.

## Criterios de decisión aplicados al proyecto del curso

| Criterio | Valor | Decisión |
|----------|-------|----------|
| Tamaño del dominio | Mediano | Monolito modular |
| Número de equipos | 2 | Monolito modular |
| Frecuencia de despliegue | Semanal | Monolito modular |
| Tolerancia al fallo | Baja | Monolito modular |
| Consistencia requerida | Fuerte | Monolito modular |
| Madurez operativa | Inicial | Monolito modular |

## Conclusión

El proyecto empieza como monolito modular. La evolución hacia microservicios se justificará cuando alguno de los seis criterios cambie.
