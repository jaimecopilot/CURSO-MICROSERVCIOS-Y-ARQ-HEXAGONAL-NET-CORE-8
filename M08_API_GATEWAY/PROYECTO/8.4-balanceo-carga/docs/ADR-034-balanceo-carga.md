# ADR-034: Balanceo de carga y cierre del curso

## Estado
Aceptado

## Contexto
El proyecto AceriaApp ha adoptado YARP como gateway. Se quiere comprobar el reparto y la recuperación entre dos instancias de Inventario, manteniendo una instancia de Producción. Este alcance demuestra el mecanismo de balanceo del servicio elegido, sin declarar alta disponibilidad de todos los componentes.

## Decisión
Se fija `LoadBalancingPolicy: RoundRobin` en inventario-cluster, con destinos 5106 y 5107. produccion-cluster conserva el destino 5105 y el gateway escucha en 5100. YARP también ofrece Random, LeastRequests y PowerOfTwoChoices, pero no se dejan implícitos en el ejercicio. No se configura una propiedad nativa Weight ni una política ponderada: los metadatos solo producirían ponderación si una extensión adicional los interpretara. Inventario utiliza sondeos activos a `/health/ready` con intervalo y timeout de un segundo, ConsecutiveFailures y umbral dos. `HealthyAndUnknown` excluye destinos Unhealthy y devuelve 503 si ninguno permanece disponible; permite reincorporar un destino recuperado sin reiniciar el gateway. La validación incluye reparto observable con X-Instancia, caída parcial, caída total y recuperación real. El cierre exige 39 proyectos, 26 proyectos de pruebas, 50 documentos y 491 pruebas esperadas en 8.4 sin omisiones, con evidencia Linux, Windows y PDF de la misma revisión. El recorrido conserva ocho módulos y 34 puntos; esos objetivos no constituyen un PASS antes de ejecutar CI y revisar las evidencias.

## Alternativas consideradas
- Balanceo en el orquestador: descartado por simplicidad del proyecto.
- Balanceo sin health checks: descartado por riesgo de enrutar a instancias no disponibles.
- Política ponderada personalizada: se pospone porque el objetivo es RoundRobin entre dos destinos equivalentes; el indicador TienePesos del catálogo no instala esa política.

## Consecuencias
- Positivas: escalado horizontal, distribución de carga, tolerancia a fallos de instancia.
- Negativas: requiere mantener los dos destinos de Inventario y su política de salud; una petición asignada durante la detección puede fallar. Producción y Gateway siguen siendo instancias únicas en el laboratorio.
- Mitigación: la validación automática y las buenas prácticas documentadas.

## Alcance comprobable de esta etapa

TienePesos expresa una intención de diseño, sin extensión ponderada implementada. Los catálogos no activan el balanceador ni los checks. El estado Aceptado de este ADR expresa la decisión arquitectónica; el resultado de ejecución se registra en los informes y sus hashes.

El directorio anterior se conserva intacto. Las copias del punto actual incluyen los cambios completos indicados en el manual.
