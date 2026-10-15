# Principios de diseño — Punto 1.3

## Categorías de principios

Tres categorías: responsabilidad, ocultación y acoplamiento.

## Principio de responsabilidad única

Un servicio debe tener una sola razón para cambiar, identificada con una capacidad de negocio.

## Principio de ocultación de información

Un servicio debe exponer solo lo necesario y ocultar el modelo de datos, la lógica interna y la topología.

## Principio de acoplamiento débil y cohesión fuerte

Los elementos de un servicio deben estar fuertemente relacionados entre sí y débilmente con otros.

## Principio de límite del contexto

Cada servicio debe corresponder a un contexto delimitado del dominio.

## Principio de autonomía del servicio

Un servicio debe poder operar de forma independiente en despliegue, datos y fallo.

## Principio de contrato explícito

La comunicación entre servicios se realiza a través de contratos públicos, versionados y documentados.

## Principio de tolerancia al fallo

Un servicio debe seguir operando cuando una dependencia falla, aunque sea con funcionalidad degradada.

## Principio de evolución independiente

Un servicio debe poder evolucionar sin obligar a los demás a cambiar al mismo ritmo.

## Aplicación al proyecto del curso

| Principio | Aplicación |
|-----------|------------|
| Responsabilidad única | Módulos por capacidad de negocio |
| Ocultación | Cada módulo con su propia carpeta |
| Acoplamiento débil | Interfaces entre módulos |
| Límite del contexto | Contextos delimitados |
| Autonomía | Evolución hacia microservicios |
| Contrato explícito | DTOs públicos |
| Tolerancia al fallo | Polly |
| Evolución independiente | Versionado de contratos |
