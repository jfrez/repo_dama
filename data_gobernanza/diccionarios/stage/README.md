# Diccionario capa stage

Describe las tablas limpias y deduplicadas tras la ingesta.

Incluye por tabla:
- Mapeo raw -> stage y normalizaciones aplicadas (fechas, codigos, texto).
- PK/BK vigentes, regla de deduplicacion y timestamp de vigencia o corte.
- Campos derivados iniciales y referencias entre tablas.
- Sensibilidad, owner y enlace a las reglas DQ relevantes en `../../dq_reglas/integracion/`.

Usa `../../plantillas/diccionario.md` como formato base.
