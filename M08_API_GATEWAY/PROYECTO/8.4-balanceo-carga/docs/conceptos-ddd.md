# Conceptos básicos de Domain-Driven Design — Punto 5.1

## Definición

Enfoque que sitúa el dominio del negocio en el centro del proceso de desarrollo.

## Dominio y subdominios

- Núcleo: aporta valor diferencial.
- Soporte: apoya al núcleo.
- Genérico: se resuelve con soluciones existentes.

## Contexto delimitado

Frontera dentro de la cual un modelo es consistente y un término tiene un significado preciso.

## Lenguaje ubicuo

Vocabulario común entre negocio y desarrollo. Se refleja en el código.

## Modelo del dominio

- Entidades: objetos con identidad propia.
- Value objects: objetos sin identidad propia.
- Agregados: grupos de objetos con una raíz.
- Servicios de dominio: operaciones sin estado.

## DDD estratégico y táctico

- Estratégico: contextos delimitados y lenguaje ubicuo.
- Táctico: entidades, value objects, agregados, repositorios.

## DDD y microservicios

Un contexto delimita un modelo y un lenguaje. Puede implementarse como módulo del mismo proceso o evolucionar hacia un servicio autónomo; DDD no exige desplegar un microservicio por contexto.

## Beneficios

Comunicación, alineación, mantenibilidad y evolución.

## Costes

Inversión inicial, colaboración continua, complejidad adicional y dificultad en dominios poco comprendidos.

## Contextos delimitados del proyecto

| Contexto | Descripción |
|----------|-------------|
| Producción | Órdenes de fabricación |
| Aprovisionamiento | Órdenes de compra |
| Clientes | Registro de clientes |
| Identidad | Usuarios, roles y permisos |

## Aplicación al proyecto del curso

| Elemento | Aplicación |
|----------|------------|
| Contextos de análisis | Producción, aprovisionamiento, clientes e identidad |
| Lenguaje ubicuo | Términos del negocio |
| Implementación ejecutable | Contexto Producción en un ensamblado de dominio independiente |
| Validación | Test de coherencia |

## Correspondencia ejecutable

`ContextoDelimitado`, `CatalogoContextos` y `ValidadorContextos` representan datos del ejercicio. Sus indicadores no prueban la arquitectura por sí solos. El contexto implementado es Producción, con `OrdenProduccion` en un proyecto independiente y transiciones controladas. Las pruebas funcionales comprueban construcción, reglas y frontera de dependencias. La relación entre contextos no requiere compartir las entidades del modelo.
