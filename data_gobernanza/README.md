# Gobernanza de datos (demo educacional)

Directorio central para evidencias de gobierno y linaje alineadas a DAMA-DMBOK:

- `gobierno_politicas/`: roles, criterios de acceso, excepciones y retencion.
- `arquitectura_modelado/`: convenciones de capas raw/stage/core/dm y claves maestras.
- `diccionarios/`: definiciones de tablas y campos por capa (subcarpetas raw/stage/core/dm) usando `plantillas/diccionario.md`.
- `dq_reglas/`: reglas de calidad por punto de control (ingesta, integracion, consumo) con responsables y umbrales.
- `metadata/`: fichas de fuentes y productos (periodicidad, SLA, contacto, criticidad, retencion).
- `linaje/`: trazabilidad de origen a destino y transformaciones clave.
- `seguridad_privacidad/`: clasificacion de datos, mascaras, controles de uso y politicas de retencion.
- `operacion_continuidad/`: calendario de ejecuciones, observabilidad y planes de reproceso/recuperacion.
- `agentes_ia/`: prompts de apoyo para mantener la documentacion y revisar cumplimiento.
- `plantillas/`: formatos sugeridos para diccionario, hallazgos DQ, catalogo y linaje.

Cada vez que se cambie un proceso en `data_0X_*`, actualiza la documentacion correspondiente y registra supuestos o decisiones.
