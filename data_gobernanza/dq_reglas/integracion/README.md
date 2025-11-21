# Reglas DQ en integracion (stage/core)

Controles que aseguran calidad y consistencia al normalizar y consolidar datos.

Incluye:
- Referencial entre tablas (ordenes vs lineas vs pagos; inventario vs catalogo).
- Dedupe y priorizacion por `updated_at` u otros campos de version.
- Balances y conciliaciones de negocio (monto items vs total, stock vs movimientos).
- Umbrales, responsables y accion ante brecha (rechazo, correccion, alerta).

Enlaza ejecuciones de `data_02_integracion/02_procesamiento/revision_calidad.py` y el resumen `tmp/dq_resumen.csv`.
