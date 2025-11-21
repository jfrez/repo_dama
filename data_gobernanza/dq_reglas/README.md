# Reglas de calidad de datos

Organiza las reglas DQ por punto de control y dominio, enlazando responsables y umbrales.

Estructura sugerida:
- `ingesta/`: controles en raw (obligatorios, tipos, duplicados basicos).
- `integracion/`: reglas de negocio y consistencia en stage/core.
- `consumo/`: validaciones antes de publicar datamarts/reportes y contratos de salida.

Cada regla debe registrar dominio, dataset, punto de control, umbral, responsable y accion ante brecha. Usa `../plantillas/dq_hallazgos.md` para documentar hallazgos y relacionarlos con el resumen generado en `tmp/dq_resumen.csv`.
