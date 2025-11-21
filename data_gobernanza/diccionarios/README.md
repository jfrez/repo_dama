# Diccionarios de datos

Guia para documentar campos y relaciones por capa del modelo (raw/stage/core/dm).

Estructura:
- `raw/`: contrato original, tipos de origen y sensibilidad declarada por la fuente.
- `stage/`: mapeo raw -> stage, normalizaciones y reglas de deduplicacion inicial.
- `core/`: consolidacion de dominios, claves maestras y reglas de negocio aplicadas.
- `dm/`: datamarts o vistas de consumo, definiciones de metricas y layout de salida.

Cada tabla debe registrar campo, tipo, regla de calculo/transformacion, sensibilidad, owner, version y fecha de actualizacion.
Usa la plantilla `../plantillas/diccionario.md` y referencia las fuentes en `metadata/` y las reglas de calidad en `dq_reglas/`.
