# Integración (data_02_integracion)

Demuestra la ruta staging → validación → consolidación para ecommerce.

- `01_construccion/stage_comercio.py`: normaliza y deduplica clientes, catálogo, órdenes, líneas, pagos e inventario.
- `02_procesamiento/revision_calidad.py`: genera `tmp/dq_resumen.csv` con hallazgos (nulos, negativos) sobre las tablas stage.
- `03_consolidacion/consolidar_modelo.py`: construye `core_ordenes/core_order_items` y los datamarts `dm_sales_diarias`, `dm_pagos_diarios`, `dm_inventario_snapshot`.

Corre estos scripts después de las ingestas de `data_01_adquisicion`. Cada uno registra su ejecución en `control_ejecuciones`.
