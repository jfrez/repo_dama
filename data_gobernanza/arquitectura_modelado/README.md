# Arquitectura y modelado

Define como se organiza la plataforma de datos (capas raw/stage/core/dm), convenciones de nombres y tratamiento de claves maestras.

Que documentar:
- Convenciones de nombres por capa (prefijos, snake_case, versionado de campos y tablas).
- Modelos logicos y fisicos por dominio; enlaza diagramas detallados en `data_arquitectura/` cuando aplique.
- Gestion de claves maestras y calendarios (vigencia, fechas efectivas, dimension de tiempo).
- Reglas de granularidad, particionado y ventanas de historia/lookback por dominio.
- Planes de versionado de esquemas y compatibilidad hacia consumidores.

Para campos y tablas usa como base `../plantillas/diccionario.md` y el detalle por capa en `diccionarios/`.
